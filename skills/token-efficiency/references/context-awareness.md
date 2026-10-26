# Context awareness

Always on; no setting turns it off. Cache re-reads dominate cost, so every turn
should justify the context it drags along. These are soft guards: advise, never
block or act without the user.

## Why

Each turn re-reads the whole context. Cost is about `context size x turns`, so a
thread that doubles in size costs more than twice as much to finish. Long
replies and pasted output are paid for again on every later turn.

## Work in documents, not chat

- Put anything longer than ~30 lines (plans, findings, audits, drafts, specs,
  handoffs) in a file, and reply with the path plus a summary of a few lines.
  Prefer an existing home (`docs/`, the backlog, the PR description) over a new
  file; use the scratchpad for throwaway notes.
- Update the file instead of restating it. Re-read only the range you need.
- Keep decisions and next steps in the file, so a fresh thread can resume from
  it without this conversation.

## Judge the thread at breakpoints

Check when a subtask finishes, before a long pause, or after a large output
lands. Use the provider's context or usage reading if available; otherwise
estimate (turns so far, big reads, screenshots, pasted logs). Say it is an
estimate. Cache TTLs and prices vary - verify for your provider.

| Signal | Suggest |
| --- | --- |
| Same task, context ~100-150K+, much of it resolved detail (old reads, dead ends) | **Compact**, keeping goal, decisions, open items |
| Task done and the next one is unrelated | **Clear**, after state is saved to files |
| Context ~150K+ or 50+ turns on one thread and work continues | **New thread**: write a handoff file (goal, state, next step, files touched), then start fresh pointing at it |
| Idle gap longer than the cache TTL ahead | Compact or hand off first; resuming re-writes the whole context at the higher cache-write price |
| Large images or logs in context that are no longer needed | Compact or new thread; they are re-read every turn |

## Soft-guard rules

- Suggest once per breakpoint, in one line with the reason ("~180K context, next
  step is unrelated: clear after saving the handoff?"). Do not repeat after the
  user declines; ask again only at the next breakpoint where the numbers grew
  materially.
- Do the preparation yourself (write the handoff or save state) before the user
  clears or compacts, so nothing is lost.
- The user's call wins. Never clear, compact or restart on your own.
- Prefer avoiding growth over trimming it: delegate wide reads, bound output,
  use text over screenshots (see the main skill).
