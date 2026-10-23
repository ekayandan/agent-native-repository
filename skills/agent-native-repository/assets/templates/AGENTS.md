<!--
Template. Replace every <placeholder>, delete sections that do not apply, and
verify each command by running it. Keep this file short: route to docs for depth.
-->
# <Project> agent guide

## Agent Behavior

Only implement changes asked by the user. Do not assume implementation details
and ask the user if anything is ambiguous.

Keep token use low without being asked: one task per session, delegate wide
reads and searches to a cheap subagent, prefer text over screenshots, bound
file and command output. See the `token-efficiency` skill.

## Finding your way

Start from the codebase map below; search the tree only when it does not answer
the question. Then read only the docs the task touches, not all of them:

| Doc | Read it for |
| --- | --- |
| `docs/technical-spec.md` | Current product and technical behavior. Source of truth. |
| `docs/decisions.md` | Features removed or parked and approaches rejected, with reasons. Read before reviving or redesigning one. |
| `docs/backlog.md` | Open work only. |
| `docs/delivery.md` | Branch, PR, CI and deployment conventions and their reasons. |
| `docs/<topic>.md` | <what it covers> |

Docs are split into `##` sections; `grep -n '^##' docs/<name>.md` lists them
with line numbers so a long doc can be read one section at a time.

## Codebase map

Every tracked file must fall under an entry here and every entry must exist;
`<command that runs docs_map_check>` fails otherwise. An entry ending in `/`
covers everything beneath it; name files individually where a directory mixes
concerns. When you add, move or delete a file, update this map in the same
change.

### <Area, e.g. Backend>

```text
<path/>                 <one-line purpose>
<path/file.ext>         <one-line purpose>
```

### <Area, e.g. Tests>

```text
<tests/>                <what lives here and how it is run>
```

### Docs and configuration

```text
AGENTS.md               This guide
docs/                   See "Finding your way" above
<manifest>              <dependencies and scripts>
<ci config>             <what CI runs>
```

## Conventions

- Before substantial work, when usage readings are available, follow
  `.agents/skills/agent-native-repository/references/quota-awareness.md` to
  forecast quota exhaustion and warn early. Keep this rule only if the skill
  is installed, or adapt the path to where you copied the guide and calculator.

- `<quality command>` runs <type check, lint, tests, map check>. Run it before
  handing back.
- Source files stay under <300> lines (enforced by <rule>). Comment lines do not
  count. Split a growing file along its responsibilities instead of appending.
- Open each module with a short comment saying what it owns and why.
- Deferred work goes in `docs/backlog.md`. A removed feature, a parked
  implementation or a rejected approach goes in `docs/decisions.md`.

## Unused code

Do not leave inactive code in the codebase: delete it rather than disabling it
behind a flag, a commented-out block or a `TODO`. When it might be useful later,
put it in a `git stash` entry whose message says what it does, why it was set
aside and where the reasoning is written down. A stash is local and never
pushed, so anything worth keeping (measurements, limits, rejected approaches)
belongs in `docs/`. Removing a feature removes every trace of it.

## Branch workflow

Every piece of work has an issue in <tracker>. Branches are named
`<type>/<issue>-<slug>` with types `feature`, `fix`, `chore`, `docs`,
`refactor`, `test`. One line of work keeps one branch and one pull request until
it merges; follow-up work starts from a fresh `<default branch>`.

**Commit and push at the end of every turn** that left changes, so the remote
always holds the latest state. Never commit to or push `<default branch>`, and
never amend, rebase or force-push a pushed branch; catch up with
`git merge origin/<default branch>`. Do not commit secrets or anything
gitignored. Keep the PR description current with goal, state, next steps and
what the user must test.

Pull requests are squash-merged, and only by the user. Agents never merge and
never enable auto-merge. Run `<quality command>` before marking a PR ready.

**The user runs and concludes manual tests, not the agent.** Prepare what they
need (a reachable dev server, exact steps), hand it over and wait for their
verdict. Report what you verified automatically and what is left for the user
to confirm, and keep those two separate. An automated browser is not a user.

## Architecture and localization

<Boundaries that must not be crossed, e.g. "only the adapter talks to the
provider API"; where locale-specific text lives; which rules stay locale-neutral.
Delete this section if nothing applies.>
