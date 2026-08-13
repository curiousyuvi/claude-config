---
name: project_salience_layer
description: "Salience-layer redesign status — significance model, fast-path disambiguation, validator loop shipped; cascade gated off pending eval calibration."
metadata: 
  node_type: memory
  type: project
  originSessionId: 79e97dfd-6c88-43e4-a2d4-0f0def85294f
---

The salience layer (fix for "costs too much" + "junk accumulates, no importance discrimination") **merged to main 2026-06-01**: loreengine-agents PR #24 (squash `2d0dea0`), loreengine-web PR #68 (`054d8eb`). Full design: `docs/architecture-plan-salience.md`.

**User still owes a live validation** before relying on it: apply the two web migrations → `pnpm db:types` → run a chapter import (couldn't be E2E-tested in the build session).

Live/default-on: `significance` [0,1] on attributes/relationships/events; `importance_score` rewritten (significance + recurrence weighted, monotonic-up — popularity formula removed); retrieval significance-ranking + chapter-range anachronism guard; **Lever 1 fast-path disambiguation** (deterministic exact-match resolve of recurring known entities → the main cost cut, zero quality change); **Fork 1** the Validator now acts on rerun directives (stakes-gated).

**Fork 2 cascade is WIRED and now DEFAULT ON** (`settings.cascade_enabled=True`, PR #25 `386c78e`) — user said "go in fully," overriding the earlier conservative default. Phase 2 runs Haiku FastExtractor + triage (`pipeline/triage.py`), re-extracts only escalated passages with Sonnet; Phase 4 mirrors the escalation set (cheap passages → Haiku attr/rel, skip events). Safety nets force-escalate on new entity / contradiction / high stakes / significant fast-pass fact. Kill-switch: env `CASCADE_ENABLED=false`. Still un-validated live — user should compare quality + cost on a real import and tune `cascade_escalation_threshold` (default 0.5; lower if quality dips).

Still open from the original review: entity merge/split UI (wrong-merge recovery), selective LLM callback detection for retroactive promotion. Builds on [[feedback_anthropic_prompt_caching]].
