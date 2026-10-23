# agent-native-repository agent guide

This repository is an Agent Skill, and it follows its own advice.

## Agent Behavior

Only implement changes asked by the user. Do not assume implementation details
and ask the user if anything is ambiguous.

Keep token use low without being asked: one task per session, delegate wide
reads and searches to a cheap subagent, prefer text over screenshots, bound
file and command output. See the `token-efficiency` skill.

## Finding your way

| Doc | Read it for |
| --- | --- |
| `README.md` | What the skill is, install and use |
| `skills/agent-native-repository/SKILL.md` | The skill's entry point; start here when changing behavior |
| `skills/agent-native-repository/references/principles.md` | The contract for each practice |
| `skills/token-efficiency/SKILL.md` | The token-efficiency skill: change it when updating cost-saving habits |
| `skills/agent-native-repository/references/quota-awareness.md` | Before substantial work when quota readings are available: project exhaustion and warn early |

## Codebase map

Checked by `python3 skills/agent-native-repository/scripts/docs_map_check.py`.
Update this map in the same change that adds, moves or deletes a file.

```text
skills/agent-native-repository/SKILL.md                         Skill entry point: discovery, modes, adaptation rules
skills/agent-native-repository/references/                      Principles, adaptation, audit, migration, compatibility, quota awareness
skills/agent-native-repository/scripts/                         Stdlib-only checks and quota calculator with tests
skills/agent-native-repository/adapters/                        Optional vendor-specific hooks, one directory per agent
skills/agent-native-repository/assets/templates/                Templates the consumer agent adapts: AGENTS.md, docs, PR template, CI
skills/token-efficiency/                                        Token-efficiency skill: cheap habits for agents, plus measuring reference
.agents/skills/agent-native-repository                          Symlink to the skill so agents working here can use it
.agents/skills/token-efficiency                                 Symlink to the token-efficiency skill
.claude/skills                                                  Symlink to .agents/skills for Claude Code
install.sh                                                      Installs the skill into another repository
README.md                                                       Overview, install, use
AGENTS.md                                                       This guide
CLAUDE.md                                                       Imports this guide for Claude Code
GEMINI.md                                                       Points Gemini CLI at this guide
.github/workflows/ci.yml                                        Runs the map check and the script tests
.gitignore                                                     Excludes local and generated files
```

## Conventions

- Keep the skill stack-agnostic: describe contracts, ship only reference
  implementations that need Python 3 or POSIX sh, and never hardcode a project's
  paths, ports or tool choices.
- Mark any claim about a third-party tool's behavior "verify" until checked.
- The scripts must keep passing against a real repository before changing them.
- Branches: `<type>/<slug>`; one PR per line of work; humans merge.
