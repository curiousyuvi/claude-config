---
name: project-backend-typecheck-gate-tsgo
description: "The backend typecheck gate is `tsgo -b`, which covers bin/ — `tsc -p tsconfig.json` only covers src/ and gives false clean"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T10:02:54.839Z
---

`apps/backend/package.json` defines `"typecheck": "tsgo -b --noEmit"`, and lefthook's pre-commit runs `pnpm -s typecheck` (root: `pnpm -r --filter backend --filter web typecheck`). That covers `bin/` as well as `src/`.

Running `pnpm --filter backend exec tsc --noEmit -p tsconfig.json` covers **only `src/`**. It reports clean while `bin/*.ts` is broken, so a commit then fails the hook — and if you don't read the hook output carefully, the commit silently doesn't happen while `git push` still "succeeds" by pushing an unchanged branch.

Two traps that compound it:

- **Grepping tsgo output for `error TS` matches nothing.** tsgo emits ANSI colour codes between `error` and `TS`, so `grep "error TS"` returns empty and reads as success. Grep the `pnpm -r` runner's output for `error|Failed|ERR_PNPM`, or check `$?`.
- **`tsgo -b` is incremental.** After deleting build info or changing project refs, use `--force` to be sure.

Verify with the exit code, not the absence of matched output:
```
pnpm -s typecheck; echo "exit=$?"
```

After pushing, confirm the remote actually moved (`git log origin/<branch> -1`) rather than trusting that push printed something.

Related: [[feedback_run_lint_typecheck]], [[feedback_diff_checks_after_commit]]
