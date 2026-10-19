#!/usr/bin/env python3
"""Forecast quota exhaustion from average consumption since each window began."""

import argparse
import math
from datetime import datetime, timedelta, timezone


def timestamp(value):
    """Require an explicit UTC offset so results do not depend on host timezone."""
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("use an ISO timestamp with timezone offset") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise argparse.ArgumentTypeError("timestamp must include a timezone offset")
    return result.astimezone(timezone.utc)


def percentage(value):
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("remaining quota must be a percentage") from exc
    if not math.isfinite(result) or not 0 <= result <= 100:
        raise argparse.ArgumentTypeError("remaining quota must be between 0 and 100")
    return result


def positive_hours(value):
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("short hours must be a positive integer") from exc
    if result <= 0:
        raise argparse.ArgumentTypeError("short hours must be a positive integer")
    return result


def forecast(reset, remaining, hours, now):
    """Return a linear projection; a reset must end the currently active window."""
    try:
        start = reset - timedelta(hours=hours)
    except OverflowError as exc:
        raise ValueError("window duration is too large") from exc
    if not start <= now < reset:
        raise ValueError("reset must be in the future and window start must not be in the future")
    if remaining == 0:
        return "already exhausted"
    elapsed = (now - start).total_seconds()
    if remaining == 100 or elapsed == 0:
        return "insufficient consumption history to estimate exhaustion"
    seconds_left = elapsed * remaining / (100 - remaining)
    try:
        exhaustion = now + timedelta(seconds=seconds_left)
    except OverflowError:
        return "quota resets before projected exhaustion (date exceeds supported range)"
    date = exhaustion.isoformat(timespec="seconds")
    if exhaustion < reset:
        gap_hours = (reset - exhaustion).total_seconds() / 3600
        return "{} — {:.2f} hours before reset".format(date, gap_hours)
    if exhaustion == reset:
        return "{} — projected exhaustion coincides with reset".format(date)
    return "{} — quota resets before projected exhaustion".format(date)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weekly-reset", required=True, type=timestamp)
    parser.add_argument("--weekly-remaining", required=True, type=percentage)
    parser.add_argument("--short-hours", required=True, type=positive_hours)
    parser.add_argument("--short-reset", required=True, type=timestamp)
    parser.add_argument("--short-remaining", required=True, type=percentage)
    args = parser.parse_args(argv)
    now = datetime.now(timezone.utc)
    try:
        weekly = forecast(args.weekly_reset, args.weekly_remaining, 7 * 24, now)
        short = forecast(args.short_reset, args.short_remaining, args.short_hours, now)
    except ValueError as exc:
        parser.error(str(exc))
    print("As of: {} (all output times UTC)".format(now.isoformat(timespec="seconds")))
    print("Weekly: " + weekly)
    print("Short ({} hours): {}".format(args.short_hours, short))
    print("Assumes 100% at window start and continued average consumption since then.")


if __name__ == "__main__":
    main()
