---
name: feedback_refactor_no_regressions
description: "Refactors must be behavior-preserving with zero regressions; Claude must prove it, not the user via manual re-testing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b72e2753-6bcb-4086-8871-5ad47be07d00
---

For refactors/DRY cleanups (esp. the KB default↔variant unification), the code was already working — nothing may break or gain a bug. The user does NOT want to manually re-test everything afterward.

**Why:** Regression risk is the user's #1 concern for this class of work; a "cleaner" refactor that changes behavior is a net loss. They will not be the safety net.

**How to apply:**
- Prefer pure, behavior-preserving transforms (extract shared util, parameterize) over rewrites. Keep the exact same inputs/outputs, mutation semantics, and edge-case handling.
- Do NOT collapse load-bearing distinctions (publish state, slug/dirty tracking, ordering/rank, relations, access, tenant scoping) just to look DRY — see the KB audit's "do NOT merge" list.
- The proof of no-regression is mine: run `pnpm check` + `pnpm typecheck`, run/adjust tests, and for UI use `bin/sandbox` + screenshots (see [[feedback_run_lint_typecheck]], the verify/run skills). Diff-based gates run AFTER committing ([[feedback_diff_checks_after_commit]]).
- Go incrementally, layer by layer, verifying each step — never one big-bang merge.
- Still: no commits/pushes without explicit permission ([[feedback_no_git_writes_without_permission]]).
