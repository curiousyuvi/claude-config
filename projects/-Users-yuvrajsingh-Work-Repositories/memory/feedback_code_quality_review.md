---
name: feedback_code_quality_review
description: "Periodically run the /thermo-nuclear-code-quality-review skill while writing code, for responsible high quality"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

Yuvraj wants the `/thermo-nuclear-code-quality-review` skill run **every now and then** while writing code — at sensible checkpoints (after a substantive slice, around commits / before pushing) — to keep code genuinely high-quality and responsible, beyond just passing typecheck + biome.

**Why:** he wants deliberate quality gates on written code, not just "it compiles."
**How to apply:** invoke the skill at meaningful checkpoints (a completed service/feature slice, non-trivial pre-commit changes). NOTE: confirm the exact skill name/availability in-session before claiming to run it — it was NOT in the available-skills list when this was written; never fake-invoke it. If unavailable, fall back to the repo's `/code-review` (and `/security-review`) and flag that the named skill wasn't found.
