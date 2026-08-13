---
name: feedback_branch_naming
description: "Branch names must be prefixed with ys/ (user's personal namespace), e.g. ys/feat/..."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6085a000-d530-487c-9862-290d55cc4c43
---

Prefix all new branches with `ys/` (the user's personal namespace), keeping the conventional-commit type after it: `ys/feat/<slug>`, `ys/fix/<slug>`, etc.

**Why:** team/personal branch-namespace convention in the axis repo.
**How to apply:** when branching off master (or any base), name it `ys/feat/...` from the start — don't push a bare `feat/...` and rename after. See [[feedback_no_git_writes_without_permission]].
