# Audit checklist

Score each line 0 (absent), 1 (partial), 2 (present and enforced). Report the
total, then the gaps ranked by value (the order below is value order). Cite the
evidence (path, command output) for every score. Do not change anything in audit
mode.

## Discoverability

- [ ] Agent file exists (`AGENTS.md`), is under ~500 lines, and other agents'
      files import it rather than copy it.
- [ ] Codebase map exists and covers every tracked file. **Enforced** by a check
      that runs in the quality command and CI (2 only if enforced).
- [ ] Routing table says which doc to read for which task.
- [ ] Docs are split into `##` sections; none is too large to read by section.
- [ ] Modules open with a comment saying what they own.

## Truthfulness

- [ ] Spec describes current behavior only.
- [ ] Decisions doc records rejected/removed approaches with reasons.
- [ ] Backlog lists open work only; no stale TODOs in code.
- [ ] Docs reference only existing paths (checked).
- [ ] README setup instructions work on a clean checkout (try them).

## Gates

- [ ] One documented quality command; passes on a clean checkout.
- [ ] CI runs that command; jobs have timeouts, least-privilege permissions,
      concurrency cancel, pinned third-party actions.
- [ ] File-size cap enforced (or ratchet baseline).
- [ ] Unused-code scan runs in CI.
- [ ] Structural tests exist for generated files / routes / two-place config.
- [ ] Dependency updates grouped and automated; security alerts on.

## Workflow

- [ ] Scope-discipline rule present.
- [ ] Branch naming tied to issues; one branch and PR per line of work.
- [ ] Never amend/rebase/force-push pushed branches; squash-merge.
- [ ] Humans merge; agents do not merge or push to the default branch;
      enforced by ruleset or hook, not only prose.
- [ ] Manual testing is concluded by the user; agent hands over environment,
      steps, and separates automated from left-for-user results.
- [ ] PR template includes a Handoff section.
- [ ] Commit-and-push-per-turn rule present with a neutral backstop
      (`pre-push` or CI) and, optionally, an agent adapter.

## Depth on demand

- [ ] Recurring domains have a short skill that routes to depth.
- [ ] Reusable-component inventory exists where the repo has a UI.
- [ ] Accepted-decisions log exists and holds only real user decisions.

## Reporting format

```text
Score: NN / MM
Top gaps (highest value first):
1. <gap> - evidence - suggested fix - effort (S/M/L)
Verified by running: <commands and results>
Written but not run: <items>
Needs a human decision: <items>
```
