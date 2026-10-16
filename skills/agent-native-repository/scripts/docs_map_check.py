#!/usr/bin/env python3
"""Keep the AGENTS.md codebase map and the docs' path references true.

Reference implementation of principle 1 (see references/principles.md). Standard
library only. Port it to the repository's own test language when there is one.

Checks, run from the repository root (or with --root):
  1. every path named in the "## Codebase map" section exists;
  2. every tracked file is covered by a map entry (an entry ending in "/" covers
     everything beneath it);
  3. every repository path a doc names (backticked spans containing a slash that
     start with a top-level entry, plus relative markdown links) exists.

Exit status 0 when everything holds, 1 otherwise, 2 on a usage problem.
"""
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path


def tracked_files(root: Path) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, check=True
    ).stdout.decode()
    # A file deleted in the working tree but not yet staged is still listed.
    return [f for f in out.split("\0") if f and (root / f).exists()]


def map_entries(agents_file: Path, heading: str) -> list[str]:
    text = agents_file.read_text(encoding="utf8").replace("\r", "")
    sections = re.split(r"^## ", text, flags=re.M)
    section = next((s for s in sections if s.startswith(heading)), None)
    if section is None:
        raise SystemExit(f'{agents_file} has no "## {heading}" section')
    entries: list[str] = []
    for block in re.finditer(r"^```text\n(.*?)^```", section, flags=re.M | re.S):
        for line in block.group(1).split("\n"):
            parts = line.strip().split()
            if parts:
                entries.append(parts[0])
    if not entries:
        raise SystemExit(f"{agents_file}: the map section has no ```text blocks")
    return entries


def referenced_paths(root: Path, doc: Path, top_level: set[str]) -> list[str]:
    text = doc.read_text(encoding="utf8")
    spans = [
        re.sub(r":\d+(-\d+)?$", "", m.group(1))
        for m in re.finditer(r"`([^`\s]+)`", text)
    ]
    spans = [
        s for s in spans
        if "/" in s and s.split("/")[0] in top_level and not re.search(r"[*?<>{}]", s)
    ]
    links = [
        m.group(1)
        for m in re.finditer(r"\]\(([^)\s]+)\)", text)
        if not re.match(r"^([a-z]+:|#)", m.group(1)) and not re.search(r"[*?<>{}]", m.group(1))
    ]
    resolved = [
        os.path.normpath(os.path.join(os.path.dirname(doc.relative_to(root)), t.split("#")[0]))
        for t in links
        if t.split("#")[0]
    ]
    return spans + resolved


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    ap.add_argument("--agents-file", default="AGENTS.md")
    ap.add_argument("--heading", default="Codebase map")
    ap.add_argument("--docs-dir", default="docs", help="markdown here is checked too")
    ap.add_argument(
        "--ignore",
        action="append",
        default=[],
        metavar="GLOB",
        help="tracked files not required in the map (repeatable)",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    agents_file = root / args.agents_file
    if not agents_file.is_file():
        print(f"{agents_file} not found", file=sys.stderr)
        return 2

    entries = map_entries(agents_file, args.heading)
    files = [
        f for f in tracked_files(root)
        if not any(fnmatch.fnmatch(f, pat) for pat in args.ignore)
    ]
    problems: list[str] = []

    for e in entries:
        if not (root / e).exists():
            problems.append(f"map names a path that does not exist: {e}")

    def covered(f: str) -> bool:
        return any(f.startswith(e) if e.endswith("/") else e == f for e in entries)

    for f in files:
        if not covered(f):
            problems.append(f"tracked file not in the codebase map: {f}")

    top_level = {p.name for p in root.iterdir()}
    docs = [agents_file, *(root / "README.md",)] if (root / "README.md").exists() else [agents_file]
    docs_dir = root / args.docs_dir
    if docs_dir.is_dir():
        docs += sorted(docs_dir.rglob("*.md"))
    for doc in docs:
        for ref in referenced_paths(root, doc, top_level):
            if not (root / ref).exists():
                problems.append(f"{doc.relative_to(root)} names a missing path: {ref}")

    if problems:
        print("\n".join(sorted(set(problems))))
        print(f"\n{len(set(problems))} problem(s). Update {args.agents_file} or the docs.")
        return 1
    print(f"codebase map OK ({len(entries)} entries, {len(files)} tracked files, {len(docs)} docs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
