# Migrating a repository that has outgrown its structure

Large, old repositories fail agents in predictable ways: too many files to
search, docs that lie, giant files, history nobody wrote down. Fix them in
small steps that each leave the repo better and never block the team. One PR per
step.

## Step 0: baseline

Record numbers before changing anything, so progress is visible:

- tracked file count; the 20 largest source files by line count
- number of docs, last commit date of each
- does the quality command exist; does CI pass on the default branch
- existing agent files

Put the baseline in the PR description of step 1.

## Step 1: codebase map (biggest win)

1. Generate a draft listing: `git ls-files`, collapse directories where every
   file shares a purpose (one `dir/` entry), keep files individual where a
   directory mixes concerns.
2. Write a one-line purpose per entry **from reading the code**, not from file
   names. For hundreds of files, sample the module header or exports. Mark
   uncertain ones `(unverified)` and fix them later.
3. Put it in `AGENTS.md` under `## Codebase map`, grouped by area.
4. Add the map check. Initially list generated or vendored directories as single
   entries so the check passes. Merge only when it is green.

For a monorepo, give each package its own `AGENTS.md` map and a root map that
lists the packages; run the check once per package with `--agents-file`.

## Step 2: routing table and doc triage

1. List every doc with last-modified date and size.
2. Classify each as *spec* (current), *decision/history*, *backlog*, *reference*
   or *stale*. Stale docs get deleted or corrected, not kept "just in case"
   (git has them).
3. Split any doc over ~400 lines by `##` topic.
4. Create `decisions` and `backlog` files if missing and move history and open
   work into them (principle 3).
5. Add the routing table to `AGENTS.md`.

## Step 3: one quality command

Wire together whatever already runs (tests, lint, type check), then add the map
check. Make CI call it. Do not add new tools in this step.

## Step 4: ratchets

For each rule the code currently violates:

- **File-size cap.** Compute offenders with the chosen cap, write a baseline
  file of `path lines`. The check fails if a file is new and over the cap, or an
  offender grew. When a baseline file shrinks below the cap, remove it from the
  baseline (the check should demand this so the baseline only shrinks).
- **Unused code.** Run the scanner, record current findings as the allowed set
  (or fix the cheap ones), fail on new findings.
- **Lint.** Same: baseline suppressions, fail on new violations.

List the biggest offenders in the backlog with a suggested split along
responsibilities; do not split them all in one PR.

## Step 5: workflow rules and enforcement

Add the workflow section to `AGENTS.md`, the PR template, and propose (do not
silently apply) rulesets, `pre-push` hook and CI gating. See
[principles.md](principles.md) 7-9.

## Step 6: recurring domains

When agents repeatedly stumble in one area (UI, migrations, API contracts), write
a router skill for it. Prefer a short skill that links to existing docs over
new prose.

## Order of operations and stopping points

Steps 1-3 alone remove most of the pain and are safe to ship in a day. Stop
after any step; each is independently valuable. Re-run the audit checklist at the
end and put the before/after score in the final report.

## Pitfalls

- Writing the map without reading the code produces confident wrong docs. Mark
  uncertainty.
- Moving files while writing the map invalidates it; map first, restructure in
  later PRs (the check will keep the map honest through the moves).
- A baseline that is never lowered becomes permanent. Make the check fail when an
  entry can be removed.
- Do not rewrite history or reformat the whole repo as part of this; that buries
  the change and conflicts with every open branch.
