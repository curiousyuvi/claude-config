#!/bin/sh
# Commits and pushes ~/.claude config to curiousyuvi/claude-config. Registered as a Stop hook.
set -u
cd "$HOME/.claude" || exit 0

git add -A >/dev/null 2>&1
git diff --cached --quiet && exit 0

if git diff --cached | grep -qEi 'sk-[a-zA-Z0-9]{20}|ghp_[a-zA-Z0-9]{20}|github_pat_|ops_[a-zA-Z0-9]{40}|AKIA[0-9A-Z]{16}|xoxb-|BEGIN [A-Z ]*PRIVATE KEY'; then
  git reset -q
  echo "claude-config sync aborted: staged diff looks like it contains a secret. Fix it, then commit by hand." >&2
  exit 0
fi

git commit -q -m "Sync Claude Code config $(date '+%Y-%m-%d %H:%M')" >/dev/null 2>&1
git push -q origin main >/dev/null 2>&1 || echo "claude-config sync: commit made, push failed." >&2
exit 0
