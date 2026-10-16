# Agent compatibility

Goal: one source of truth that Claude Code, Codex, Gemini CLI and other agents
all read. Tool behavior changes quickly. **Everything in the "Expected" column is
a starting point; verify against the tool's current documentation or by testing
before relying on it**, and say in your report which you verified.

## Rules file

| Agent | Expected behavior | Action |
| --- | --- | --- |
| Codex and many others | Reads `AGENTS.md` | Put the rules in `AGENTS.md` |
| Claude Code | Reads `CLAUDE.md`; supports `@path` imports | `CLAUDE.md` containing `@AGENTS.md` |
| Gemini CLI | Reads `GEMINI.md` by default; the file name(s) can be configured | Either a one-line `GEMINI.md` that imports/points at `AGENTS.md`, or configure the context file name to include `AGENTS.md` |
| Cursor, Copilot, others | Their own rule files | Optional thin files that point at `AGENTS.md`; do not duplicate rules |

If a tool cannot import another file, keep a short pointer file ("Read
AGENTS.md before doing anything") rather than a copy that will drift.

## Skills

Skills follow the Agent Skills layout: a folder with `SKILL.md` (frontmatter
`name`, `description`) and optional `references/`, `scripts/`, `assets/`.

Canonical location: `.agents/skills/<name>/`. Expected discovery:

- Codex and other `.agents`-aware tools: `.agents/skills/` (verify per tool).
- Claude Code: `.claude/skills/` - create a symlink to `.agents/skills`
  (`ln -s ../.agents/skills .claude/skills`) or per-skill symlinks.
- Gemini CLI: has its own skills directory convention - verify whether it also
  scans `.agents/skills`; if not, symlink.

Where symlinks are unavailable (Windows without developer mode), copy and add a
check that the copies match.

## Hooks

Hooks are vendor-specific and must not carry the only copy of a rule.

- Neutral layer: git hooks (`pre-push`, `pre-commit`), CI, repository rulesets.
- Optional adapter: [`adapters/claude/`](../adapters/claude/) holds a Claude Code
  `Stop` hook that blocks ending a turn while feature-branch work is
  uncommitted or unpushed. Equivalent adapters for other agents are welcome once
  their hook mechanism is verified; keep them under `adapters/<agent>/`.

Installing hooks changes the behavior of everyone who uses the repo. Propose,
show the diff, and wait for approval.

## Parallel sessions (optional)

If several agents work at once, give each its own git worktree and a claimed dev
port so they do not collide, and make "claim / park / resume" explicit. Only add
this if the user actually runs parallel agents; it is heavy machinery. A
lighter alternative is a convention: one branch per agent, branch name includes
the issue, PR is the claim.

## Verifying you wired it up

For each agent the user cares about, start a fresh session and ask: "What does
this repository's AGENTS.md say about merging?" If it cannot answer, the file is
not being read. Do this check before telling the user it works.
