---
name: feedback_confirm_before_commit
description: Always confirm with the user before any git commit or push
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1985cacb-734e-4712-95fa-d406d20ebc72
---

Always confirm with the user before running `git commit` or `git push`. Stage and prepare the change, show what will be committed, but wait for explicit go-ahead before committing/pushing.

**Why:** The user wants to review changes before they land in git history / on the remote.

**How to apply:** When work is ready to commit, summarize what would be committed (and the proposed message) and ask. Don't auto-commit even after finishing a task or fixing review feedback. Relates to [[feedback_ask_before_deciding]].
