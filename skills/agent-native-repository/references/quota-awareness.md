# Quota awareness

## Enable or disable

Off unless the repository's `AGENTS.md` contains the line
`Quota awareness: on`. `Quota awareness: off`, or no line, means do not read
usage, run the calculator or warn about quota. Re-check the line when starting
work; the user may flip it at any time. This switch does not affect context
awareness in the `token-efficiency` skill, which is always on.

Before substantial work, when usage readings are available, estimate whether
either account quota will run out before its reset. Warn the user early if so,
and leave a resumable handoff at meaningful checkpoints when quota is low.
Forecasts are advisory, not an instruction to stop authorized work.

Use the provider's verified usage interface to obtain remaining percentages and
next reset timestamps. Verify access methods and window lengths for the current
account; do not assume a provider-specific duration. If readings are unavailable,
say so rather than inventing them. Collection is outside this calculator.

## Run anywhere

The standalone `scripts/quota_forecast.py` needs only Python 3.7+; no packages,
configuration, credentials, history files, or network access. It also ships with
the normal skill installation. From a repository with the skill installed:

```sh
python3 .agents/skills/agent-native-repository/scripts/quota_forecast.py \
  --weekly-reset '2026-10-23T15:00:00+03:00' \
  --weekly-remaining 60 \
  --short-hours 5 \
  --short-reset '2026-10-19T18:00:00+03:00' \
  --short-remaining 40
```

Replace all five example values with current readings. Times must include a
timezone offset (`Z` for UTC is also accepted). Percentages mean **remaining**,
not used. The shorter window length must be a positive integer number of hours.

## Interpretation

Weekly start is next reset minus 168 hours; shorter start is next reset minus
the supplied hours. For each quota, the calculator uses the current time and:

```text
elapsed = now - window start
consumption rate = (100 - remaining percentage) / elapsed
projected exhaustion = now + remaining percentage / consumption rate
```

Output gives each projected exhaustion timestamp in UTC and its relationship
to reset. A projection after reset is hypothetical: the quota resets first.
At 0% it reports already exhausted; at 100% or zero elapsed time it reports
insufficient consumption history. Expired resets and future window starts are
rejected.

This assumes full replenishment at the start of fixed windows. It does not model
rolling replenishment, extra credits, or changing limits. Idle time counts toward
the average; a burst of work may exhaust quota sooner. Account-wide activity
is included in the supplied readings. These estimates cannot guarantee that a
particular task will finish.
