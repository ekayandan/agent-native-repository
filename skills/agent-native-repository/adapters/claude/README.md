# Claude Code adapter

Optional. Backs the "commit and push at the end of every turn" rule with a
`Stop` hook. The rule must also exist in `AGENTS.md` and, where possible, be
enforced neutrally (`scripts/pre-push-sync.sh`, CI); this hook only helps one
agent follow it and cannot see changes made purely through shell commands in
another worktree.

Install (ask the user first; hooks affect everyone using the repo):

1. Copy `commit-push-gate.mjs` to `.claude/hooks/` in the target repository.
2. Merge `settings.snippet.json` into `.claude/settings.json`.
3. Needs Node 18+ on the developer machine. If Node is not part of the
   repository's stack, port the script to the stack's scripting language or
   skip this adapter.
4. Verify: edit a file on a feature branch, try to end the turn, and confirm
   the hook blocks until the work is committed and pushed.
