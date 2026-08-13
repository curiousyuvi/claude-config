---
name: Don't pause between phases for confirmation
description: When working through a sequence of phases/PRs, keep going through all of them without stopping for approval at each boundary. Only stop on real breakage or genuine need for input.
type: feedback
originSessionId: 79e97dfd-6c88-43e4-a2d4-0f0def85294f
---
When working through a multi-phase build (e.g., Phase 3a → 3b → 3c → ...), do not stop and ask "want me to continue to the next phase?" between each one. Just keep going.

**Why:** The user wants forward progress — pausing for permission at each phase boundary slows them down without adding value. They've already approved the overall direction; the per-phase confirmation is friction.

**How to apply:**
- Merge PR → sync main → start the next branch → build → commit → open PR → merge → repeat. Continue until either (a) the natural sequence completes, (b) something breaks, or (c) you genuinely need user input on a non-obvious decision.
- "Want me to continue?" / "Should I move on?" / "Ready for the next chunk?" — never. Just continue.
- Reasonable judgment calls (which phase is next, scope of each phase, deferred items) are yours to make. The user will redirect if needed.
- Still pause for: build failures, type errors I can't resolve, schema/architecture decisions with real tradeoffs, anything destructive.
