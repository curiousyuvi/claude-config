---
name: feedback_minimal_comments
description: "Use minimal, necessary comments only — don't comment what doesn't need it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1985cacb-734e-4712-95fa-d406d20ebc72
---

Hard rule for this project: write minimal and necessary comments only. If a piece of code doesn't need a comment, don't add one. Don't restate what the code already says; reserve comments for non-obvious "why" (gotchas, invariants, surprising constraints), and keep those terse — a line or two, not paragraphs.

**Why:** The user finds verbose/explanatory comment blocks noisy and asked to strip them repeatedly. Self-evident code should stand on its own.

**How to apply:** When writing or editing code, default to no comment. Add one only when the reasoning isn't clear from the code itself, and compact it. Avoid multi-paragraph doc blocks, comments that narrate obvious steps, and redundant inline notes. Leave genuinely load-bearing pre-existing comments alone, but don't add new ceremony.
