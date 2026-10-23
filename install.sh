#!/bin/sh
# Install the agent-native-repository and token-efficiency skills into a target repository.
#   ./install.sh <target-repo> [--link]
# Copies the skill to <target>/.agents/skills/<skill> (portable,
# committable). With --link it symlinks to this clone instead (local only; do
# not commit a link that points outside the repository). Also makes
# <target>/.claude/skills point at .agents/skills when .claude/skills is absent.
# Never overwrites anything that already exists.
set -eu

target="${1:-}"
mode="copy"
[ "${2:-}" = "--link" ] && mode="link"
if [ -z "$target" ] || [ ! -d "$target/.git" ]; then
  echo "usage: $0 <path to a git repository> [--link]" >&2
  exit 2
fi

here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$target/.agents/skills"
for name in agent-native-repository token-efficiency; do
  src="$here/skills/$name"
  dest="$target/.agents/skills/$name"
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    echo "left alone: $dest already exists; remove it first to reinstall." >&2
    continue
  fi
  if [ "$mode" = "link" ]; then
    ln -s "$src" "$dest"
  else
    cp -R "$src" "$dest"
  fi
  echo "installed: $dest ($mode)"
done

if [ ! -e "$target/.claude/skills" ] && [ ! -L "$target/.claude/skills" ]; then
  mkdir -p "$target/.claude"
  ln -s ../.agents/skills "$target/.claude/skills"
  echo "linked:    $target/.claude/skills -> ../.agents/skills"
else
  echo "left alone: $target/.claude/skills already exists (make sure it reaches .agents/skills)"
fi

echo
echo "Next: start an agent in $target and ask it to run the agent-native-repository skill in audit mode."
echo "Gemini CLI and Codex: see skills/agent-native-repository/references/agent-compatibility.md."
