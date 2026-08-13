---
name: feedback_comment_style
description: "Write minimal, short code comments — only genuinely necessary ones; never comment everywhere"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

When writing code, keep comments minimal and short. Only comment genuinely non-obvious things (a surprising design decision, a non-trivial invariant, a "why"). Do NOT add per-field / per-line comments that restate what the code already says, and don't write verbose doc-block headers on every file/entity.

**Why:** Yuvraj finds heavy commenting noisy and wants code that reads clean.
**How to apply:** At most one short purpose line per file/entity where it helps; explain *why*, not *what*; skip the obvious. Applies across all repos (Axis etc.). Even when surrounding/template code is comment-heavy, prefer the lean style.
