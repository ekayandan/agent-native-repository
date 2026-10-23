# Measuring token usage

Verify each command against the installed tool versions before relying on it.

## Totals by token type and day

CodexBar (macOS menu bar app; CLI at `codexbar`) reads local Claude and Codex
logs and estimates cost at API list prices:

```sh
codexbar cost --provider claude --days 60 --breakdown --no-color
codexbar cost --provider claude --days 60 --json
```

The JSON `daily[]` entries carry `cacheReadTokens`, `cacheCreationTokens`,
`inputTokens`, `outputTokens`, `totalCost` and per-model breakdowns. Cache reads
dominating tokens is normal; look at how the total moves between days and
models. Cost shares by token type are not reported, so estimate them from the
provider's price ratios (verify; at the time of writing cache read is about
0.1x input, cache write 1.25x, output 5x).

## Finding runaway sessions

Claude Code writes one JSONL log per session under
`~/.claude/projects/<project>/<session>.jsonl`. Each assistant record has
`message.usage` with `cache_read_input_tokens` and
`cache_creation_input_tokens`. Group by `message.id` (a message can be written
more than once) and compute per session: turns, total cache read, and the
largest per-turn cache read (the context size). Sessions with many hundreds of
turns or a context beyond a few hundred K are the ones to split.

To see what filled a session's context, sum the size of `tool_result` content
by the originating tool name. Screenshot and browser tools are the usual
offender.

## Targets

These are starting points, not laws:

- Context per turn under ~150K typically; handoff before ~200K.
- Sessions under ~150 turns.
- Re-run the 60-day report monthly and compare cache-read tokens per output
  token (a falling ratio means shorter contexts).
