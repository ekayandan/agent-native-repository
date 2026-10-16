#!/bin/sh
# Git pre-push hook (principle 8): refuse pushes to the default branch and
# refuse feature branches that are behind the default branch on the remote.
# POSIX sh, no dependencies. Install by copying or symlinking to
# .git/hooks/pre-push, or point core.hooksPath at a tracked directory:
#   git config core.hooksPath .githooks
# Bypass in an emergency with: git push --no-verify
#
# Configure with environment variables:
#   DEFAULT_BRANCH  (default: detected from origin/HEAD, else main)

remote="$1"
zero=0000000000000000000000000000000000000000

default="${DEFAULT_BRANCH:-}"
if [ -z "$default" ]; then
  default=$(git symbolic-ref --quiet --short "refs/remotes/$remote/HEAD" 2>/dev/null | sed "s|^$remote/||")
  default="${default:-main}"
fi

status=0
while read -r local_ref local_sha remote_ref remote_sha; do
  [ -z "$local_ref" ] && continue
  case "$local_ref" in refs/tags/*) continue ;; esac
  [ "$local_sha" = "$zero" ] && continue # branch deletion
  if [ "$remote_ref" = "refs/heads/$default" ]; then
    echo "Never push directly to $default. Open a pull request from a branch." >&2
    status=1
    continue
  fi
  git fetch "$remote" "$default" --quiet 2>/dev/null || true # offline: use cached ref
  if git rev-parse --verify --quiet "refs/remotes/$remote/$default" >/dev/null; then
    if ! git merge-base --is-ancestor "refs/remotes/$remote/$default" "$local_sha"; then
      behind=$(git rev-list --count "$local_sha..refs/remotes/$remote/$default")
      echo "Push rejected: ${local_ref#refs/heads/} is $behind commit(s) behind $remote/$default." >&2
      echo "  git merge $remote/$default   (never rebase a pushed branch)" >&2
      status=1
    fi
  fi
done
exit $status
