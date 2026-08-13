---
name: feedback-no-claude-author
description: "Never attribute any AI tool (Claude, Copilot, Cursor, Codex, etc.) as author/co-author in commits, PR descriptions, or any authored artifact in axis"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6c827962-d2a7-4b55-9d3f-d69ead777bdf
---

Never attribute ANY AI tool or app as author/co-author anywhere. No `Co-Authored-By: Claude <...>`, no "Generated with Claude Code", and likewise nothing referencing Copilot, Cursor, Codex, ChatGPT, or any other AI assistant — in git commits, PR titles/descriptions/bodies, issue comments, code comments, changelogs, or any other authored artifact. The user authors the work; AI involvement must be invisible.

**Why:** User explicit instruction — they want the commit log, PR metadata, and all artifacts to read as their own work, with no trace of an AI tool.

**How to apply:** When running `git commit`, omit any `Co-Authored-By:` trailer and any "Generated with …" footer. When using `gh pr create` / `gh pr edit`, write the body with no AI-attribution lines or mentions. Don't drop AI-tool names into code comments either. Applies retroactively — if asked to amend a message or body, strip such lines. Pairs with [[feedback_no_git_writes_without_permission]] (don't commit/push/merge without explicit permission).
