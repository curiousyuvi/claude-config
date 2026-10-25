---
name: project-gaps-stacked-branches
description: "How knowledge-gaps work continues while PR #1792 waits on review — stacked branch for phase 7, a worktree for #1792 fixes"
metadata:
  node_type: memory
  type: project
  originSessionId: 5297b585-30e3-414e-8e5f-0ed29a5a3fce
  modified: 2026-10-25T10:46:43.082Z
---

Set up 2026-10-23 while #1792 (knowledge gaps) waits on Jared's review. #1803 (KB AI format) is merged.

- `ys/feat/screenshot-agent` (phase 7) branches from `ys/feat/knowledge-gaps`, checked out in the main folder `~/Work/Repositories/axis`. Its draft PR is #1810 (opened 2026-10-23), base `ys/feat/knowledge-gaps`, not master.
- Worktree `~/Work/Repositories/axis-gaps` stays on `ys/feat/knowledge-gaps` (pnpm install done). Every #1792 review fix happens there: commit, push, then in the main folder `git merge ys/feat/knowledge-gaps` into the phase 7 branch. Fixes only flow upward.
- When #1792 squash-merges (repo deletes the branch, GitHub retargets the stacked PR to master): merge origin/master into the phase 7 branch; if that conflicts, `git rebase --onto origin/master ys/feat/knowledge-gaps`.
- The worktree needs no dev server; tests and typecheck only.

Phase 7 progress (2026-10-24): slices 7a-7g and 7i committed on #1810 (7g = recipes on img node `capture` + replay/recapture + app memory, dfc5699ac). 7h (scheduled outdated-screenshot checks) DROPPED 2026-10-25 by the user as too costly/wasteful; it returns only with a GitHub integration where a merged PR's diff triggers recapture of just the affected screens. flagOutdated removed (8f66c272e); recipes + recapture kept for that. #1792 Sonar green; #1810 Sonar fix 9b762a148. 7i review fixes f10f5a490 + fcd3676c4 (steps editor, sign-in origins, live cancel), UI-verified.

#1792 review (2026-10-23): Konrad (jdarnok) left 18 findings; all fixed in dadcdd5c2, Sonar follow-up 274f3fcc0 (gate had failed on one S9383 unvoided promise), merged up into #1810 (78cf8e7cb). Summary comment + 12 inline replies posted. Sonar re-run on 274f3fcc0 not yet confirmed green. Jared's review still pending. Full state, live-test scripts and test-account details are in repo-root KNOWLEDGE-GAPS-PLAN.md (section "23 Oct: phase 7"); live specs and Firecrawl key live in ~/.claude/jobs/5297b585/tmp.

**Why:** the user didn't want to wait on review, and an accidental checkout in the main folder once interrupted work; two folders mean nobody switches branches under the other.
**How to apply:** never commit #1792 fixes on the phase 7 branch; never switch the main folder back to knowledge-gaps. Related: [[project-knowledge-gaps-feature]].
