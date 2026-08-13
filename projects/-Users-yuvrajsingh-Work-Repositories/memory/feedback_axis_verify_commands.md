---
name: feedback_axis_verify_commands
description: "Axis repo — verify with the repo's own typecheck (tsgo) and knip, not tsc, before pushing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7d7bc585-6c10-4113-8c75-ceab1d984a78
---

In the Axis monorepo, the `typecheck` script is `tsgo -b --noEmit` (TypeScript-Go), NOT classic `tsc`. They diverge: `tsc --noEmit` passed locally while `tsgo` failed CI on a recursive `Omit<>`-over-`.passthrough()`-inferred type that collapsed to its index signature.

**Why:** verifying with the wrong compiler ships type errors that only CI's `tsgo` catches.

**How to apply:** before pushing, run the exact CI commands — `pnpm --filter web typecheck` / `pnpm --filter backend typecheck` (tsgo), `pnpm exec knip` (unused deps), `pnpm --filter backend openapi:generate` (broken refs). The CI "Web Build" job runs `tsgo` typecheck separately from `vite build`, so `pnpm --filter web build` passing is NOT sufficient. Also: `tsgo -b` incremental cache is flaky on the merged master Kysely code (spurious `never` table errors); a from-scratch build after deleting `*.tsbuildinfo` is clean.

**Never run `pnpm build` / `nest build` while Yuvraj's `pnpm dev` server is running** — `nest build` uses `deleteOutDir:true` and wipes the shared `apps/backend/dist` the dev server serves from, 502-ing his live reader (happened during the react-dom reader migration; needed a `pnpm dev` restart to recover). For verification use the non-destructive checks (tsgo typecheck + vitest); only `nest build` when no dev server is up. Related: [[project_kb_in_sidebar]].
