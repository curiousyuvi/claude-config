---
name: feedback-no-git-writes-without-permission
description: "Never commit, push, or merge in axis without the user's explicit permission"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c827962-d2a7-4b55-9d3f-d69ead777bdf
---

In the axis project, NEVER run `git commit`, `git push`, `git merge`, or merge/close a PR (or any branch-state-changing write) without the user's explicit permission for that specific action. Finish the work — including resolving conflicts and running all checks — then stop and report, leaving changes staged/uncommitted until the user says to proceed.

**Why:** The user wants to review and control exactly what lands on their branches and PRs; surprise commits/pushes/merges are unwelcome even when CI is green.

**How to apply:** Do all the edits, conflict resolution, and verification (typecheck, `pnpm check`, tests, build). Then present a summary and wait. Only commit/push/merge when the user explicitly asks in that turn. Resolving a merge locally is fine; committing the merge or pushing it is not, absent permission. Relates to [[feedback_no_claude_author]] (commit/PR authoring rules).
