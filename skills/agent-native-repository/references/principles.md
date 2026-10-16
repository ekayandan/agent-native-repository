# Principles

Each practice is a contract: **Goal**, **Contract** (what must be true),
**Verify** (how to check it mechanically), **Why** and **Adapt** (what varies by
stack). The contract is the requirement; any implementation that satisfies it is
fine.

---

## 1. Codebase map in the agent file, enforced

**Goal.** A fresh agent session goes straight to the right file instead of
searching the tree.

**Contract.** The agent file (`AGENTS.md`) has a `## Codebase map` section of
fenced `text` blocks. Each line is `<path> <whitespace> <one-line purpose>`.
A path ending in `/` covers everything beneath it; name files individually where
a directory mixes concerns. Grouped under short subheadings (Backend, Frontend,
Data, Tests, Config/Docs). Every tracked file falls under an entry, and every
entry exists. A change that adds, moves or deletes a file updates the map in the
same change.

**Verify.** A check fails when (a) a map path does not exist, (b) a tracked
file is not covered, (c) a doc names a repository path that no longer exists.
Reference: [`scripts/docs_map_check.py`](../scripts/docs_map_check.py). Run it
in the quality command and in CI.

**Why.** Unenforced docs drift and then mislead; a drifted map is worse than
none. The test turns documentation upkeep into a failing build.

**Adapt.** Express it as a native test where one exists. Mark generated or
vendored directories as one entry each (`dist/`, `vendor/`), or exclude them via
`.gitignore`. In a large monorepo keep one map per package and a short root map
that links to them (see the checker's `--agents-file` option).

---

## 2. "Finding your way" routing table

**Goal.** Keep context small as the repository grows.

**Contract.** The agent file contains a table: *doc → what to read it for*, and
the instruction "read only the docs the task touches". Long docs are split into
`##` sections by topic so one section can be read at a time (tell agents to use
`grep -n '^##' <doc>`). Task-specific rules are not pasted into the agent file;
the agent file links to them with a trigger ("before changing crawlable routes,
read X").

**Verify.** Every doc under `docs/` appears in the table or is reachable from
one that does. No doc is so large that a section cannot be read alone (rule of
thumb: split above ~400 lines).

**Why.** Always-loaded text is paid for on every task. Depth behind a pointer is
paid for only when needed.

---

## 3. Spec / decisions / backlog split

**Goal.** Separate what is true now, what was tried and rejected, and what is
open, so none rots the others.

**Contract.**
- `spec` (technical spec): **current behavior only**. No history.
- `decisions`: features removed or parked and approaches rejected, each with the
  reason, the date and who decided. It opens with "read the relevant entry
  before reviving or redesigning any of these".
- `backlog`: **open work only**. Each entry says what it is, why it was set
  aside and what was already checked by hand. When done, delete the entry and
  record the outcome in spec or decisions.
- Anything worth keeping from a deleted experiment (measurements, limits,
  rejected approaches) goes in these docs, never in dead code.

**Verify.** Review: no "we used to" prose in the spec; no finished items in the
backlog; no stale TODOs in code (they belong in the backlog).

**Why.** Agents re-propose rejected ideas and resurrect removed code when the
rejection is not written down where they will read it.

---

## 4. One quality command

**Goal.** A single, documented command an agent runs before handing back.

**Contract.** One entry point (`make check`, `npm run quality`, `just check`,
`./gradlew check`, `tox`, `task quality` ...) runs type check, lint, tests and
the structural checks. A cheaper variant may exist for CI; a heavier variant
(coverage, dependency audit) is optional. Documented in the agent file
Conventions section with the exact command.

**Verify.** The command exists, passes on a clean checkout, and CI runs the same
thing (CI should call the entry point, not re-list the steps).

---

## 5. Mechanical size and dead-code limits

**Goal.** Files stay small enough to read whole; no inactive code.

**Contract.**
- A per-file line cap enforced by the linter or a script (suggested 300 for
  application code; exempt generated files, lockfiles, data, fixtures; do not
  count comment lines). Message: "split along responsibilities".
- An unused-code scanner in CI (Knip for JS/TS, `vulture` for Python,
  `deadcode`/`staticcheck` for Go, `cargo udeps`/`warnings` for Rust, IDE
  inspections or `unused` plugins for JVM/.NET).
- Rule in the agent file: do not leave inactive code behind flags, comments or
  TODOs. If it may be useful later, save it in a `git stash` with a message that
  says what it does, why it was set aside and where the reasoning is written;
  move lasting knowledge to `docs/decisions`. Removing a feature removes every
  trace of it (types, enum members, helpers, styles).
- Open each module with a short comment saying what it owns and why.

**Verify.** The limit rule fails on a deliberately long file. For existing
offenders use a baseline ratchet (see
[migrating-legacy-repos.md](migrating-legacy-repos.md)).

---

## 6. Structural tests

**Goal.** Catch drift that unit tests miss.

**Contract.** Tests that pin relationships rather than behavior, as the stack
allows:
- generated files equal what their generator produces now (run generator, diff);
- every advertised route/page/endpoint answers and unknown ones return 404;
- docs and the codebase map reference real paths (principle 1);
- configuration that must change in two places (for example a CI job name and a
  ruleset's required checks) is compared by a test or flagged in a comment at
  both sites.

**Verify.** Break one relationship on purpose and confirm the test fails.

---

## 7. Workflow rules

Written in the agent file, stated as imperatives with the reason in the linked
delivery doc.

- **Scope discipline.** "Only implement changes asked by the user. Do not assume
  implementation details; ask if anything is ambiguous."
- **Issue-linked branches.** Every piece of work has an issue; branches are
  `<type>/<issue>-<slug>` (types: feature, fix, chore, docs, refactor, test).
  One line of work keeps one branch and one PR until it merges.
- **History safety.** Never amend, rebase or force-push a pushed branch; catch up
  with `git merge origin/<default>`. Squash-merge PRs so the branch's WIP
  commits collapse to one revertable commit.
- **Commit and push at the end of every turn** that changed something, so the
  remote always holds the latest state and another machine or agent can resume.
  (Enforce neutrally: principle 8.)
- **Humans merge.** Agents never merge, never enable auto-merge, never push to
  the default branch. A green CI run is not approval.
- **User concludes manual tests.** The agent prepares the environment (dev
  server reachable from the user's device, exact steps) and reports
  *automated* results and *left-for-user* items separately. An automated
  browser is not a user.
- **PR description is the handoff**: goal, state, next steps, checks run, what
  the user must test. Keep it current.
- **Parallel agents** (optional): one worktree per session with claimed ports;
  see the worktree notes in [agent-compatibility.md](agent-compatibility.md).

**Adapt.** Replace "issue" with the team's tracker key. Drop what the team does
not use (worktrees, squash). Keep scope discipline and "humans merge"
everywhere.

---

## 8. Neutral enforcement

**Goal.** A rule that exists only in prose is a suggestion. Enforce it so every
agent, not just one vendor's, is held to it.

**Contract.** Enforce each rule at the lowest layer that can see it:

| Rule | Layer |
| --- | --- |
| No direct push to default; branch up to date | repository ruleset + `pre-push` hook ([`scripts/pre-push-sync.sh`](../scripts/pre-push-sync.sh)) |
| Docs map true, size cap, dead code | quality command + CI |
| Required checks, linear history, no force-push, squash-only | repository ruleset / settings |
| Commit and push before ending a turn | agent hook (adapter), backed by the written rule |

Agent-specific hooks live in `adapters/<agent>/` and are optional. They never
carry the only copy of a rule.

**Verify.** Each rule has a failing demonstration: try the forbidden action and
see it refused.

---

## 9. CI hygiene

- Run on `push` to the default branch and on PRs; optionally gate PR runs behind
  a `ready-to-merge` label so draft and in-review work does not burn CI.
- `concurrency` cancels superseded PR runs; default-branch runs are keyed by
  commit and never cancelled.
- `timeout-minutes` on every job; `permissions: contents: read` by default.
- Pin third-party actions to a commit SHA with a version comment; install with a
  lockfile-respecting, script-less command (`npm ci --ignore-scripts`,
  `pip install --require-hashes`, `cargo --locked`).
- CI calls the quality entry point (principle 4).
- Dependency updates grouped weekly (minor+patch in one PR, majors alone,
  security grouped); a weekly workflow for slow checks (audit, coverage).
- PR template with issue link, what/why, **Handoff**, local checks, manual-test
  URL/steps/verdict (verdict filled from the user, never by the agent), and a
  docs/map checklist.

Templates: [`assets/templates/`](../assets/templates/).

---

## 10. Progressive-disclosure skills

**Goal.** Domain depth without loading it every session.

**Contract.** For a recurring domain (UI, SEO, database migrations, API design,
copywriting), create `.agents/skills/<name>/SKILL.md`: a short router that
names the compact core, topic guides and a bounded lookup, and says what *not*
to load. Companions where they fit: a **component/primitive inventory** ("read
before writing a new one; add yours in the same change") and an **accepted
decisions log** that records only actual user decisions and concluded tests,
never agent preferences. Reference large source corpora by ID and page, with a
lookup script that returns a bounded passage.

**Verify.** `SKILL.md` stays under ~100 lines and links to its depth; the
description says when to use it.
