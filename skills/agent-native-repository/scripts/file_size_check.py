#!/usr/bin/env python3
"""File-length cap with a ratchet baseline (principle 5).

Reference implementation for repositories whose linter cannot cap file length.
Standard library only. Prefer the linter's own rule when it has one.

Counts non-blank, non-comment-only lines of tracked files that match --include
(and not --exclude). A file passes when it is within --max, or when it is listed
in the baseline file and has not grown. The check also fails when a baselined
file is now within the cap or has shrunk, so the baseline can only get smaller
(use --update-baseline to rewrite it after splitting files).

Baseline format, one per line: "<path> <line count>" (lines starting with # are
comments). Exit status 0 ok, 1 violations, 2 usage.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
from pathlib import Path

COMMENT = re.compile(r"^\s*(//|#|--|;|\*|/\*|\*/|<!--)")


def tracked(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True
    ).stdout.decode()
    return [f for f in out.split("\0") if f and (root / f).is_file()]


def count(path: Path) -> int:
    try:
        lines = path.read_text(encoding="utf8").splitlines()
    except (UnicodeDecodeError, OSError):
        return 0  # binary or unreadable: not source
    return sum(1 for ln in lines if ln.strip() and not COMMENT.match(ln))


def read_baseline(path: Path) -> dict[str, int]:
    base: dict[str, int] = {}
    if path.exists():
        for ln in path.read_text(encoding="utf8").splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                name, _, n = ln.rpartition(" ")
                base[name] = int(n)
    return base


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("--include", action="append", default=[], metavar="GLOB",
                    help="source globs, e.g. '*.py' (repeatable; required)")
    ap.add_argument("--exclude", action="append", default=[], metavar="GLOB",
                    help="e.g. 'generated/*' 'data/*' (repeatable)")
    ap.add_argument("--baseline", default=".file-size-baseline")
    ap.add_argument("--update-baseline", action="store_true")
    args = ap.parse_args()
    if not args.include:
        print("pass at least one --include glob", file=sys.stderr)
        return 2

    root = Path(args.root).resolve()
    sizes = {
        f: count(root / f)
        for f in tracked(root)
        if any(fnmatch.fnmatch(f, g) for g in args.include)
        and not any(fnmatch.fnmatch(f, g) for g in args.exclude)
    }
    over = {f: n for f, n in sizes.items() if n > args.max}
    baseline_path = root / args.baseline

    if args.update_baseline:
        body = "# Files over the cap; this list may only shrink.\n" + "".join(
            f"{f} {n}\n" for f, n in sorted(over.items())
        )
        baseline_path.write_text(body, encoding="utf8")
        print(f"baseline written: {len(over)} file(s) over {args.max}")
        return 0

    baseline = read_baseline(baseline_path)
    problems: list[str] = []
    for f, n in sorted(over.items()):
        if f not in baseline:
            problems.append(f"{f}: {n} lines, cap {args.max}; split along responsibilities")
        elif n > baseline[f]:
            problems.append(f"{f}: grew to {n} lines (baseline {baseline[f]})")
    for f, b in sorted(baseline.items()):
        n = sizes.get(f)
        if n is None:
            problems.append(f"{f}: in baseline but gone; run --update-baseline")
        elif n <= args.max:
            problems.append(f"{f}: now {n} lines, within cap; run --update-baseline")
        elif n < b:
            problems.append(f"{f}: shrank to {n} (baseline {b}); run --update-baseline")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"file sizes OK ({len(sizes)} files, {len(baseline)} baselined over {args.max})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
