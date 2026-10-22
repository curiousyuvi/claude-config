---
name: project-gaps-stacked-branches
description: "How knowledge-gaps work continues while PR #1792 waits on review — stacked branch for phase 7, a worktree for #1792 fixes"
metadata:
  node_type: memory
  type: project
  originSessionId: 5297b585-30e3-414e-8e5f-0ed29a5a3fce
  modified: 2026-10-22T20:40:04.375Z
---

Set up 2026-10-23 while #1792 (knowledge gaps) waits on Jared's review. #1803 (KB AI format) is merged.

- `ys/feat/screenshot-agent` (phase 7) branches from `ys/feat/knowledge-gaps`, checked out in the main folder `~/Work/Repositories/axis`. Its draft PR is #1810 (opened 2026-10-23), base `ys/feat/knowledge-gaps`, not master.
- Worktree `~/Work/Repositories/axis-gaps` stays on `ys/feat/knowledge-gaps` (pnpm install done). Every #1792 review fix happens there: commit, push, then in the main folder `git merge ys/feat/knowledge-gaps` into the phase 7 branch. Fixes only flow upward.
- When #1792 squash-merges (repo deletes the branch, GitHub retargets the stacked PR to master): merge origin/master into the phase 7 branch; if that conflicts, `git rebase --onto origin/master ys/feat/knowledge-gaps`.
- The worktree needs no dev server; tests and typecheck only.

**Why:** the user didn't want to wait on review, and an accidental checkout in the main folder once interrupted work; two folders mean nobody switches branches under the other.
**How to apply:** never commit #1792 fixes on the phase 7 branch; never switch the main folder back to knowledge-gaps. Related: [[project-knowledge-gaps-feature]].
