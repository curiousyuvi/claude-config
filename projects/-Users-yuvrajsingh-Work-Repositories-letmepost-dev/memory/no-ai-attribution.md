---
name: no-ai-attribution
description: Never attribute commits/PRs to AI; write all prose to read as human-authored
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8a26c084-ea6a-4c39-9a35-4d08d4a7463c
---

Never mention Claude, AI, or any assistant as an author or co-author in commit messages or PR descriptions. Omit the `Co-Authored-By: Claude` trailer and any "Generated with Claude Code" line. Every commit message, PR body, code comment, and text description must read as if a human wrote it — no AI-tells.

**Why:** The user is making open-source contributions under their own name and wants the work to appear entirely human-authored.

**How to apply:** Skip the standard AI co-author/generated-by trailers entirely. Match the surrounding repo's tone and comment density so prose blends in.
