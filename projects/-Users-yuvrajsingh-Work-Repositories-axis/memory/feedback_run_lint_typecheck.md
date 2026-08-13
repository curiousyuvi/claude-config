---
name: feedback-run-lint-typecheck
description: "After any significant change in axis, run the local pre-flight: pnpm check, pnpm typecheck, pnpm run check:react-doctor, pnpm exec knip, and the relevant test suites — before declaring the task done"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6c827962-d2a7-4b55-9d3f-d69ead777bdf
---

After any significant change, run the full set of local CI-equivalent checks from the repo root before reporting the task as done. "Significant" = anything beyond a one-line tweak, doc edit, or pure comment change. Run **all** of these, not just lint+typecheck:

- `pnpm exec biome check` (or `pnpm check`) — Lint & Format gate
- `pnpm typecheck` — Backend Build + Web Build typecheck portion
- `pnpm run check:react-doctor` — React Doctor gate (web-only; can be slow but runs offline). Exit 0 means no `✗` errors; warnings are fine.
- `pnpm exec knip` — Unused Dependencies gate
- `pnpm --filter web build` if touching web code — surfaces Vite-only issues
- `pnpm --filter web test` if touching web code — 155+ tests, ~1s
- `pnpm --filter backend test` if touching backend code or shared/ — needs DB running; ~65s
- `pnpm --filter backend test:e2e` if touching auth/routes — needs DB
- `bash scripts/check-file-size.sh` if adding/expanding components — Architecture Checks

Fix everything flagged in files I touched. Pre-existing errors in unrelated files are fine to leave, but call them out so the user knows they weren't introduced by this change.

**Why:** User explicitly asked for this. Three separate PRs in this repo have failed CI on gates that would have caught locally (typecheck, react-doctor `only-export-components`, SonarCloud patterns). Each failure wastes a CI cycle plus a round-trip with the user.

**How to apply:** Treat the full set as part of the definition of done. Run from the repo root (not a filtered workspace) so both backend and web get covered. SonarCloud can't run locally — but the patterns it flags are well-known (see [[feedback-sonar-rules]]): scan changed files for `Math.random`, non-Readonly props, nested ternary, nested template literals, `children` as a JSX prop, hardcoded external URLs without SRI, inline component definitions, unstable context provider values, `window` references that should be `globalThis`. If a check surfaces unrelated pre-existing failures, note them in the final summary instead of silently skipping or "fixing" them.
