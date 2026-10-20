---
name: project-backend-typecheck-gate-tsgo
description: "Typecheck = `tsc -b` (root @typescript/native 7.x) per package; a stale apps/backend/node_modules/.bin/tsc (TS 5.9 shim) shadows it and fails with `Unknown build option '--checkers'`"
metadata:
  type: project
---

`scripts/typecheck.mjs` spawns `tsc -b --noEmit` from PATH; pnpm puts the package's own `node_modules/.bin` first. Root `tsc` is TypeScript 7 native (`@typescript/native`), which accepts `--checkers`.

On 2026-10-20 `pnpm --filter backend typecheck` (and the lefthook pre-commit) failed with `error TS5072: Unknown build option '--checkers'`. Cause: a leftover `apps/backend/node_modules/.bin/tsc` and `tsserver` shim from Sep pointing at `typescript@5.9.3`, which the backend no longer depends on, so pnpm never pruned it. Fix: delete those two shims (check `grep typescript@5.9.3 node_modules/.bin/tsc` first). Not a master bug.

`tsc -p tsconfig.json` covers only `src/` and gives a false clean when `bin/*.ts` is broken. Verify with the exit code, not by grepping for `error TS` (colour codes split it). `-b` is incremental; use `--force` after changing project refs.
