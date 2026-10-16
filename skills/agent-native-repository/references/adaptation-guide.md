# Adaptation guide

The reference scripts need only Python 3 (standard library) or POSIX `sh`, so
they run anywhere. They are examples of a contract, not the way the contract
must be met. Adapt each practice to what the repository already uses.

## Method

For each practice in [principles.md](principles.md):

1. Find the repository's native mechanism (table below).
2. If one exists, use it. If the practice can be a native test, write it as one
   so it runs with the rest of the suite.
3. If none exists, use the reference script, run from the quality command.
4. Write the exact command into the agent file and run it once to prove it works.
5. If two reasonable options remain and the choice is lasting (new dependency,
   new CI job, hook installation), **ask the user**.

## Native equivalents by stack

| Concern | JS/TS | Python | Go | Rust | JVM | .NET | Ruby | PHP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Quality entry point | `npm run quality` | `make check` / `tox` / `nox` | `make check` | `cargo xtask check` / `just` | `./gradlew check` | `dotnet test` + build props | `rake check` | `composer check` |
| File-length cap | Biome `noExcessiveLinesPerFile`, ESLint `max-lines` | Ruff `PLR0915`-style rules + script, `pylint max-module-lines` | script / `revive file-length-limit` | clippy `too_many_lines` (fn) + script | Checkstyle `FileLength` | Analyzer rule + script | RuboCop `Metrics/ModuleLength` | PHPMD / script |
| Unused code | Knip | vulture | `deadcode`, staticcheck U1000 | rustc warnings as errors, `cargo udeps` | Detekt / IDE inspections | analyzers IDE0051/IDE0052 | `debride` | `phpstan` |
| Dep updates | Dependabot npm | Dependabot pip | gomod | cargo | gradle/maven | nuget | bundler | composer |
| Lockfile-safe install in CI | `npm ci --ignore-scripts` | `pip install -r ... --require-hashes` / `uv sync --frozen` | `go mod download` + `-mod=readonly` | `--locked` | wrapper + dependency locking | `--locked-mode` | `bundle install --deployment` | `composer install --no-scripts` |
| Native test to host the map check | Vitest/Jest | pytest | `go test` | `cargo test` | JUnit | xUnit | RSpec/Minitest | PHPUnit |

(Treat the table as a starting point. Confirm the current tool names and flags
in the repository's own docs or by running `--help` before relying on them.)

## Hosting the docs-map check

`scripts/docs_map_check.py` exits non-zero with a listing of offenders and takes
`--agents-file`, `--docs-dir`, `--ignore GLOB`. Options:

- **Native test (preferred).** Reimplement the three checks in the repo's test
  language (about 60 lines: read `git ls-files`, parse fenced `text` blocks
  under `## Codebase map`, check path existence). Keep the same failure messages.
- **Wrapper test.** A test that shells out to the script and asserts exit 0.
- **Make/CI step.** Add `python3 scripts/docs_map_check.py` to the quality
  command. Fine when Python 3 is present on every developer machine and CI
  image; if not, port it.

## Hosting the size cap

1. If the linter supports it, enable the rule and list exemptions in config.
2. Otherwise add a small script that counts non-comment, non-blank lines for
   files matching the source globs, and fails above the cap.
3. If existing files already exceed the cap, create a baseline file
   (`path  current_line_count`), fail only on files that are new or got longer.
   Lower the baseline whenever a file shrinks. This is the **ratchet**; see
   [migrating-legacy-repos.md](migrating-legacy-repos.md).

## Hosting structural tests

Pick tests that match what the repo generates or advertises:

- **Generators.** Run the generator into a temp dir and diff against the
  committed output. Fails when someone edited generated output or forgot to
  regenerate.
- **Routes/endpoints.** Enumerate the advertised list (sitemap, router table,
  OpenAPI) and request each against the app in-process; also request an unknown
  path and expect 404.
- **Two-place config.** If a name must match across files (CI job vs ruleset),
  add a test or a comment at both locations.

## No test runner, no CI, no linter

Do not build everything. Order of value for a bare repository:

1. Agent file with the codebase map and the map check as a Make target or shell
   script. 
2. The routing table and spec/decisions/backlog stubs.
3. A one-command quality entry point that runs whatever exists.
4. Ask the user before introducing a linter, test framework or CI provider.

## Things to ask the user

- Preferred default branch, merge strategy, issue tracker and branch naming.
- Whether agents may commit/push (and to which branches), and whether PRs are
  drafts until the agent is done.
- Whether to add hooks, rulesets or CI changes (these are shared state).
- Size cap value and which directories are exempt.
- Whether parallel agent sessions are used (worktrees, port claims).
- Language of user-facing copy, if the repo has localized text (set locale rules
  in the agent file).

## Things never to assume

- That Node, Python or any particular runtime is installed on CI or developer
  machines.
- Ports, hostnames, secret names or file paths copied from another repository.
- That `main` is the default branch.
- That a rule from the source project ("Tailscale host binding", "Doppler
  secrets") applies. Those are project-local; the principles are not.
