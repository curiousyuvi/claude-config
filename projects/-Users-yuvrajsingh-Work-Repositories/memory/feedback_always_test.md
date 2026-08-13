---
name: always-test
description: "Always write tests alongside the code — unit for pure logic, integration for persistence/services"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

Write tests wherever relevant as a standing practice, not an afterthought. Unit tests for pure logic (ordering, slug utils, mappers, sanitizers, renderers), integration tests (repo's `forkEm`/`setup-db` harness) for persistence and service behavior (CRUD, tree move/cascade/restore, outbox emit, etc.). If a slice shipped without tests, go back and add them.

**Why:** Yuvraj wants a genuinely verified codebase, not compile-green-only. Surfaced after several Axis KB backend slices shipped type-checked but unrun against a live DB.

**How to apply:** Include tests in the same slice as the feature; don't defer. Verify with [[feedback_axis_verify_commands]] before pushing. Pairs with [[feedback_code_quality_review]].

**Axis test-file naming:** backend (apps/backend) vitest matches `*.spec.ts`; web (apps/web) vitest only matches `*.test.ts` — a `.spec.ts` under apps/web is silently not run. Backend integration tests need the live `axis_test` DB (reachable at `postgres.axis.orb.local` in Yuvraj's env); pure-logic units run anywhere.
