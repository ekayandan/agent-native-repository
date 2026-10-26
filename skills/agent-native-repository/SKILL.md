---
name: agent-native-repository
description: Audit a repository for agent-readiness and bootstrap or migrate it toward the practices that make AI coding agents effective - AGENTS.md with an enforced codebase map, task-routed docs, spec/decisions/backlog split, size and dead-code gates, one quality command, branch and PR conventions, and neutral enforcement hooks. Stack-agnostic - discover the repo's own language and tooling first. Use when asked to make a repo agent-friendly, set up AGENTS.md, improve docs for agents, or fix a repo that agents struggle with as it grows.
---

# Agent-native repository

Agents work well in a repository when three things are true: they can find the
right file without searching the whole tree, the docs they read are known to be
true, and the rules they must follow are enforced by tooling rather than only
written down. This skill brings a repository to that state.

It is **stack-agnostic by design**. Everything here is described as a *contract*
(what must be true, and how to check it) plus optional reference
implementations. You, the consumer agent, adapt each contract to the repository
in front of you. Never copy a template blindly, and never impose a tool the
repository does not already have a native equivalent for.

## Before anything else: discover the repository

Do this first and write down the answers. Every later step depends on them.

1. **Stack**: languages, package manager, build tool, monorepo layout. Look for
   manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
   `pom.xml`/`build.gradle*`, `*.csproj`, `Gemfile`, `composer.json`,
   `Package.swift`, `Makefile`).
2. **Existing gates**: test runner, linter, formatter, type checker, CI
   provider and workflows, git hooks (`.githooks/`, `.husky/`, `lefthook`,
   `pre-commit`).
3. **Existing agent files**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
   `.cursor/rules`, `.github/copilot-instructions.md`, `.agents/`, `.claude/`.
   Extend and consolidate these; do not duplicate them.
4. **Size and age**: file count (`git ls-files | wc -l`), largest files, how
   stale the docs are (`git log -1 --format=%cd -- docs/`).
5. **Who merges and how**: default branch, PR flow, merge strategy, issue
   tracker. Ask the user if this is unclear.

Then ask the user only what you cannot determine: which practices they want,
and anything in [adaptation-guide.md](references/adaptation-guide.md) marked
"ask".

## Modes

Pick one with the user. Default to **audit**.

- **Audit**: score the repository against
  [audit-checklist.md](references/audit-checklist.md) and report gaps ranked by
  value. Change nothing.
- **Bootstrap**: a new or small repository. Create the missing pieces from
  [assets/templates/](assets/templates/), adapted to the discovered stack.
- **Migrate**: an existing repository that has outgrown its structure. Follow
  [migrating-legacy-repos.md](references/migrating-legacy-repos.md); it is
  incremental and ratchet-based so the repo never has to be fixed in one go.

## The practices (read the contract before applying one)

Full contracts, reasons and verification are in
[principles.md](references/principles.md). In value order:

1. **Codebase map in the agent file, enforced by a check.** Highest value.
2. **"Finding your way" routing table**, so agents read only the docs a task needs.
3. **Spec / decisions / backlog split**: current state, rejected history, open work.
4. **One quality command** that runs every gate; agents run it before handing back.
5. **Mechanical size and dead-code limits.**
6. **Structural tests**: generated files not drifted, advertised routes answer,
   docs reference real paths.
7. **Workflow rules**: scope discipline, issue-linked branches, never amend or
   force-push, humans merge, user concludes manual testing.
8. **Neutral enforcement**: git hooks, CI and repository rulesets; agent-specific
   hooks only as optional adapters.
9. **CI hygiene**: gated runs, concurrency cancel, timeouts, least privilege,
   pinned actions, grouped dependency updates.
10. **Progressive-disclosure skills** for recurring domains.

Optional: **Quota awareness**, only when the repository's `AGENTS.md` says
`Quota awareness: on`; then, before substantial work when usage readings are
available, follow [quota-awareness.md](references/quota-awareness.md) and use its
standalone calculator to project weekly and shorter-window exhaustion.

## Adaptation rules

- **Contracts over code.** Reference scripts in [scripts/](scripts/) and
  [adapters/](adapters/) are examples that run with only Python 3 or POSIX `sh`.
  Where the repository has a native test runner, express the same check as a
  native test so it runs with everything else. See
  [adaptation-guide.md](references/adaptation-guide.md).
- **Prefer existing tooling.** If the repo has a linter that can cap file
  length, use it; if it has none, use the reference script rather than adding a
  dependency the maintainers did not choose.
- **Ratchet, never big-bang.** Where a rule would fail on existing code
  (file-size cap, unused code), record a baseline of current offenders and fail
  only on new or worsened ones.
- **Verify every claim you write down.** Each statement placed in the agent
  file (commands, paths, ports, conventions) must be checked against the repo
  before you commit it. Run the quality command you document.
- **Keep the always-loaded text small.** The agent file is read on every
  session. Route to depth; do not paste depth into it.
- **Agent compatibility.** Put rules in `AGENTS.md`; make other agents' files
  import it. Details and the points that must be re-verified against current
  tool docs are in [agent-compatibility.md](references/agent-compatibility.md).
- **Do not overreach.** Do not edit CI, rulesets or repository settings, install
  hooks, or push without the user's explicit go-ahead; propose them and show
  the diff. Hooks and CI changes affect everyone who uses the repo.

## Finishing

Report separately: what you changed, what you verified by running it (with the
command and result), what you only wrote down and did not run, and what needs a
human decision. Leave a short note in the agent file's maintenance section on
how the map check is run.
