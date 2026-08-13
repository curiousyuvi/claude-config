---
name: project_ci_skips_shared_tests
description: "CI runs only backend + web vitest, never packages/shared — put shared unit tests in the backend"
metadata: 
  node_type: memory
  type: project
  originSessionId: 56d7856e-7b18-4944-b177-8ce2672cad34
---

`.github/workflows/ci.yml` runs `pnpm --filter backend test` and `pnpm --filter web test` only — **never** `packages/shared` (no `pnpm -r test`, no shared filter), even though `packages/shared/package.json` has a `test: vitest run` script and no vitest config of its own.

**Why:** A unit test placed only in `packages/shared/src/**/*.spec.ts` will NOT gate in CI — it silently never runs.

**How to apply:** Put unit tests for shared logic in `apps/backend` (or `apps/web`) and exercise the shared code through its re-export (e.g. `kb-url.ts` logic is tested via `apps/backend/.../kb-routes.spec.ts`, which re-exports it). Verified while building the custom KB URL scheme (`[[project_kb_panel_published_only]]` family). Same note applies to backend test filters: `pnpm --filter backend test kb` does NOT match `knowledge-base.service.spec.ts` (no "kb" substring) — filter on `knowledge-base` for those.
