---
name: project_backend_build_heap_ceiling
description: Backend Build fails intermittently because backend tsc needs ~2.33GB and that CI step alone has no raised heap — not caused by whatever PR is red
metadata: 
  node_type: memory
  type: project
  originSessionId: 1e927e1c-86e1-4d35-94a1-f2ea8187e4d2
  modified: 2026-07-31T04:54:49.657Z
---

The backend type-check needs about **2.33 GB** of heap. Measured 2026-07-31 with `pnpm exec tsc --project tsconfig.build.json --noEmit --extendedDiagnostics` from `apps/backend`: master reported `Memory used: 2330250K` / 878k types / 8.80M instantiations.

Node's default old-space ceiling is ~2 GB, and in `.github/workflows/ci.yml` the `build-backend` job sets `NODE_OPTIONS: --max-old-space-size=4096` on the **Generate OpenAPI documentation** step only. The bare `- run: pnpm --filter backend build` (and the `typecheck` step) inherit nothing. So the job survives on GC luck and fails nondeterministically with either `FATAL ERROR: Ineffective mark-compacts near heap limit` (exit 134) in the build step, or the typecheck step showing `cancelled` when the runner process is killed.

**How to apply:** when Backend Build goes red on a PR, do NOT assume the PR caused it. Measure both sides before concluding — on #972 the branch used 2,307,058K against master's 2,330,250K, i.e. the branch was 23 MB *cheaper*, yet Backend Build passed twice then failed twice on near-identical commits. Rerunning is a coin flip, not a diagnosis.

Two traps that made this hard to see:
- `pnpm typecheck` runs **tsgo** (the Go port, `tsgo -b --noEmit`) while `nest build` runs real **tsc**. A green local typecheck says nothing about tsc's memory, so this passes every local check.
- Reading the GitHub check-runs list per commit is the fast way to spot pass/pass/fail/fail patterns: `gh api "repos/GrooveHQ/axis/commits/<sha>/check-runs" --jq '.check_runs[] | select(.name=="Backend Build") | .conclusion'`.

The fix (three lines, mirrors the pattern already used twice in the same file) was NOT applied, since `ci.yml` affects every contributor and needed the user's call:

```yaml
      - run: pnpm --filter backend build
        env:
          NODE_OPTIONS: --max-old-space-size=4096
```

If Backend Build is still flaking on master, propose this again.
