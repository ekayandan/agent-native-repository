# agent-native-repository

A portable [Agent Skill](https://agentskills.io) that brings any repository to
the state where AI coding agents (Claude Code, Codex, Gemini CLI, ...) work
well in it: they find the right file fast, the docs they read are known to be
true, and the rules they must follow are enforced by tooling.

Distilled from a repository that agents work in unusually well. The practices
are generalized into *contracts* plus small reference implementations, so the
consuming agent adapts them to the repository's own language and tooling instead
of copying a stack-specific setup.

## What it teaches an agent

1. A codebase map in `AGENTS.md`, **enforced by a check**
2. A routing table so agents read only the docs a task needs
3. Spec / decisions / backlog docs, each with one job
4. One quality command that every gate hangs off
5. File-size and dead-code limits (with a ratchet for legacy code)
6. Structural tests (generated files, routes, docs-reference-real-paths)
7. Workflow rules: scope discipline, issue-linked branches, humans merge,
   the user concludes manual testing
8. Enforcement in neutral tooling (git hooks, CI, rulesets); vendor hooks only
   as optional adapters
9. CI and dependency hygiene
10. Progressive-disclosure skills for recurring domains

## Install

```sh
git clone https://github.com/ekayandan/agent-native-repository.git
./agent-native-repository/install.sh /path/to/your/repo          # copies the skill
./agent-native-repository/install.sh /path/to/your/repo --link   # local symlink
```

This places the skill at `.agents/skills/agent-native-repository/` and points
`.claude/skills` at `.agents/skills`. For Gemini CLI and Codex discovery, see
[agent-compatibility.md](skills/agent-native-repository/references/agent-compatibility.md).

## Use

Start an agent in the target repository and ask, for example:

- "Run the agent-native-repository skill in **audit** mode." (read-only report)
- "**Migrate** this repo using agent-native-repository, starting with steps 1-3."
- "**Bootstrap** AGENTS.md and docs for this new project."

The skill first discovers the stack and existing gates, asks only what it cannot
determine, and never changes CI, rulesets, hooks or pushes without approval.

## Layout

```text
skills/agent-native-repository/
  SKILL.md                      entry point: discovery, modes, adaptation rules
  references/                   principles, adaptation guide, audit checklist,
                                legacy migration, agent compatibility
  scripts/                      stdlib-only reference checks (Python 3 / POSIX sh)
  adapters/claude/              optional Claude Code Stop hook
  assets/templates/             AGENTS.md, decisions, backlog, PR template, CI
```

## Quota calculator

Estimate weekly and shorter-window quota exhaustion with the standalone
[`quota_forecast.py`](skills/agent-native-repository/scripts/quota_forecast.py).
It runs anywhere with Python 3.7+ and needs no installation or dependencies.
Supply five values: weekly reset and remaining percentage, shorter-window hours,
reset and remaining percentage. See the [usage guide](skills/agent-native-repository/references/quota-awareness.md)
for the command and assumptions. Agents obtain usage readings separately.

## Status

The reference scripts are tested against the repository this was distilled from.
Agent-discovery claims for Codex and Gemini CLI are marked "verify" in the
compatibility notes; confirm them against current tool docs when you install.
