#!/usr/bin/env bash
# agent/undo_day.sh <commit> — put the site back to how it was before one
# day's agent run, keeping the agent's own records (log, roadmap ticks,
# inbox) as they are now, so it doesn't redo the same work tomorrow.
#
# Exit codes: 0 = undone (not yet committed), 3 = later changes overlap
# with that day, so it can't be undone mechanically.
set -u
SHA="$1"
BASE="$(git rev-parse HEAD)"

if ! git revert --no-commit "$SHA" >/dev/null 2>&1; then
  git revert --abort >/dev/null 2>&1 || git reset --hard -q "$BASE"
  exit 3
fi

# Keep the records as they are now.
for path in inbox agent/LOG.md agent/NEEDS_FROM_LERET.md agent/STYLE.md agent/SOURCES.md agent/FEEDBACK.md; do
  if git cat-file -e "HEAD:$path" 2>/dev/null; then
    git restore --source=HEAD --staged --worktree -- "$path"
  fi
done

python3 agent/guard.py "$BASE" "$SHA"
