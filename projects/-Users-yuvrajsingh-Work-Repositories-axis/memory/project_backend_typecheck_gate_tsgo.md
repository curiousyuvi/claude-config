---
name: project-backend-typecheck-gate-tsgo
description: "Typecheck = `tsc -b` (TS 7 native) per package incl. bin/; as of 2026-10-20 `pnpm typecheck` dies on an unknown `--checkers` flag, run `../../node_modules/.bin/tsc -b --noEmit` instead"
metadata:
  node_type: memory
  type: project
  originSessionId: 95ec2c73-358c-4e03-a22e-92cff3042ffc
  modified: 2026-10-20T14:37:46.072Z
---

`scripts/typecheck.mjs` runs `tsc -b --noEmit` over each package's project references (covers `bin/` as well as `src/`). Root `node_modules/.bin/tsc` is TypeScript 7.0.2 (native); there is no `tsgo` binary any more.

As of 2026-10-20 the backend script passes `--checkers 2`, which tsc 7.0.2 rejects (`error TS5072: Unknown build option '--checkers'`), so `pnpm --filter backend typecheck` fails before checking anything. Workaround: `cd apps/<pkg> && ../../node_modules/.bin/tsc -b --noEmit` (backend takes ~30s). Note this when reporting checks; don't "fix" the script silently.

`tsc -p tsconfig.json` covers only `src/` and gives a false clean when `bin/*.ts` is broken.

Verify with the exit code, not by grepping output: the compiler colours `error` and `TS` separately, so `grep "error TS"` can match nothing on a failing run. `-b` is incremental; use `--force` after changing project refs.
