---
name: token-efficiency
description: Cheapest habits for keeping agent token and quota usage low - short sessions, delegating reads and searches to a cheap model or subagent, text instead of screenshots, bounded file and command output, model routing, batched turns. Apply on your own at the start of any non-trivial task and whenever the conversation grows long; no user request needed. Also use when asked why usage is high or how to work more cheaply.
---

# Token efficiency

Most agent cost is **re-reading the conversation**, not new work. Every turn
re-sends the whole context (served from cache, so cheap per token, but billed on
every turn). Cost is roughly `context size x number of turns`. Measured on a
real account over 60 days: cache reads were 96% of tokens and ~60% of cost;
the heaviest session ran 644 turns with context growing from 45K to 650K tokens
and was never cleared, and most of that growth was browser screenshots.

So the wins are about **keeping context small and turns few**. Apply these
without being asked. They are defaults, not restrictions: if the user asks for
something different, do that.

## The wins, in value order

1. **Keep sessions short; one task per session.** Past roughly 150K tokens of
   context, or when the task changes, write a short handoff (goal, state, next
   step, files touched) and continue in a fresh or compacted session. Tell the
   user you are doing so. A 650K-context session costs far more per turn than
   five 130K ones doing the same work. Do not carry finished work forward.
2. **Delegate wide reads and searches to a cheap model or subagent.** Anything
   that means reading many files, sweeping the tree, or digesting long logs or
   docs goes to a read-only subagent on the cheapest capable model (Haiku-class,
   or an Explore agent), which returns only the conclusion with `path:line`
   pointers. The main context should hold answers, not the files read to find
   them. Ask for a bounded report ("under 200 words").
3. **Verify UIs with text, not screenshots.** Images stay in context for every
   later turn. Prefer, in order: DOM or accessibility reads, page text,
   console and network output, then a screenshot only to judge visuals. When
   you must screenshot: scale down, crop with zoom, and take few. Run long
   browser verification in a subagent or a fresh session and bring back a
   verdict, not the transcript.
4. **Bound every read and command.** Search first (`grep`, glob), then read the
   range you need (offset and limit) instead of the whole file. Cap command
   output (`| head`, `| tail`, `--quiet`, summary flags). Never print lockfiles,
   build output, or whole logs into the conversation; write them to a file and
   search it.
5. **Route the model by task.** Mechanical work (renames, formatting, lookups,
   summaries, test runs) on the cheap model; implementation on the mid model;
   the expensive model only for architecture, hard debugging and planning that
   needs it. Switch down for the grind after a plan is settled. Model names
   and prices change - check the provider's current list.
6. **Fewer, fuller turns.** Issue independent tool calls in parallel in one
   message. Combine edits to one file. Batch browser actions. Do not narrate
   plans at length or re-explain; each extra turn re-reads everything.
7. **Do not re-derive.** Do not re-read a file you just edited, re-run a passing
   check, or repeat a search whose result is already in context.
8. **Keep always-loaded text small.** Agent files, memory indexes, skills and
   MCP servers are paid for on every turn of every session. Route to depth
   (see agent-native-repository); disable plugins and servers the project does
   not use.
9. **Mind idle gaps.** The prompt cache expires after a short idle (minutes -
   verify the current TTL for your provider). Resuming a huge session after a
   break re-writes the whole context at the higher cache-write price. Compact
   or restart before a long pause.

## Context awareness (always on)

Write long output to files instead of chat, and at breakpoints suggest
compact, clear or a new thread when re-read cost is climbing. Soft guards only:
the user decides. Thresholds and rules in
[context-awareness.md](references/context-awareness.md).

## Self-check at natural breakpoints

When a subtask finishes, ask: is the context over ~150K or are the next steps
unrelated to what is loaded? Did I read whole files where a range would do? Did
I take screenshots where text would answer? If yes, hand off and restart
instead of continuing.

## Measure

Evidence beats guessing. See [measuring.md](references/measuring.md) for the
commands to see where usage goes and to find runaway sessions.
