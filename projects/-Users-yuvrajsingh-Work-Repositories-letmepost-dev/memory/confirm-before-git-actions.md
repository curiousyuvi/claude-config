---
name: confirm-before-git-actions
description: Always ask for explicit confirmation before any git commit/push/merge/etc.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8a26c084-ea6a-4c39-9a35-4d08d4a7463c
---

Always ask for explicit confirmation before running any git action that changes state — commit, push, merge, rebase, branch deletion, tag, etc. Creating a working branch is fine, but do not commit/push/merge without the user saying yes first.

**Why:** The user wants to review what will be committed and stay in control of git history.

**How to apply:** When work is ready, summarize what would be committed and ask before running the command. Relates to [[no-ai-attribution]].
