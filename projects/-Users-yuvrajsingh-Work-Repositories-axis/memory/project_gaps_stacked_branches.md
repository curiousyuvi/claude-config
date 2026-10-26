---
name: project-gaps-stacked-branches
description: "How knowledge-gaps work continues while PR #1792 waits on review — stacked branch for phase 7, a worktree for #1792 fixes"
metadata:
  node_type: memory
  type: project
  originSessionId: 5297b585-30e3-414e-8e5f-0ed29a5a3fce
  modified: 2026-10-26T22:05:48.726Z
---

Set up 2026-10-23 while #1792 (knowledge gaps) waits on Jared's review. #1803 (KB AI format) is merged.

- `ys/feat/screenshot-agent` (phase 7) branches from `ys/feat/knowledge-gaps`, checked out in the main folder `~/Work/Repositories/axis`. Its draft PR is #1810 (opened 2026-10-23), base `ys/feat/knowledge-gaps`, not master.
- Worktree `~/Work/Repositories/axis-gaps` stays on `ys/feat/knowledge-gaps` (pnpm install done). Every #1792 review fix happens there: commit, push, then in the main folder `git merge ys/feat/knowledge-gaps` into the phase 7 branch. Fixes only flow upward.
- When #1792 squash-merges (repo deletes the branch, GitHub retargets the stacked PR to master): merge origin/master into the phase 7 branch; if that conflicts, `git rebase --onto origin/master ys/feat/knowledge-gaps`.
- The worktree needs no dev server; tests and typecheck only.

Phase 7 progress (2026-10-24): slices 7a-7g and 7i committed on #1810 (7g = recipes on img node `capture` + replay/recapture + app memory, dfc5699ac). 7h (scheduled outdated-screenshot checks) DROPPED 2026-10-25 by the user as too costly/wasteful; it returns only with a GitHub integration where a merged PR's diff triggers recapture of just the affected screens. flagOutdated removed (8f66c272e); recipes + recapture kept for that. Whole-branch thermo-nuclear review fixes 03e633139 (2026-10-25): shared AppConnectionInput, illustrate returns content|null. FIRST FULL LOCAL RUN PASSED 2026-10-26 (68a4fa98c): gap draft → InstantDocs capture → staging R2 → Lambda render → img in fix. Needs .env.local KB_ASSET_* pointed at staging (helply-staging bucket + cdn.helplystaging.com; MinIO lines commented `# minio:`) plus master's #1834 (renders read assets from the CDN). Local test connection = InstantDocs password login, account app-24a0ccdec657206e@screenshotagentlogin.helply.com (password reset via inbox, copy in session scratchpad id-pass). Linear blocks the Firecrawl browser as a bot even in the live view; InstantDocs only emails OTP to brand-new accounts and refuses personal domains, so emailed-code sign-in is still unproven end to end. #1792 Sonar green; #1810 Sonar fix 9b762a148. 7i review fixes f10f5a490 + fcd3676c4 (steps editor, sign-in origins, live cancel), UI-verified.

#1792 review (2026-10-23): Konrad (jdarnok) left 18 findings; all fixed in dadcdd5c2, Sonar follow-up 274f3fcc0 (gate had failed on one S9383 unvoided promise), merged up into #1810 (78cf8e7cb). Summary comment + 12 inline replies posted. Sonar re-run on 274f3fcc0 not yet confirmed green. Jared's review still pending. Full state, live-test scripts and test-account details are in repo-root KNOWLEDGE-GAPS-PLAN.md (section "23 Oct: phase 7"); live specs and Firecrawl key live in ~/.claude/jobs/5297b585/tmp.

Second review round (2026-10-27): Konrad approved; JJ (jswietoniowski) review all fixed in 425f51cca (due-clock scheduler on knowledge_gap_settings, server-side Yjs merge + reattach pull, findability out of auto-publish, revert refuses over unpublished edits, holding baseline stored, per-subtopic fingerprint, writer retry, outbox drafts, migrations squashed to Migration20261020144754_KnowledgeGaps + the permissions data migration). Merged up as e6486da12 (screenshots job also moved to the outbox). Local dev DB bookkeeping was patched by hand (old migration rows deleted, new columns added). Replies posted on #1792.

27 Oct work block done except the final 1:1 UI match (user asked me to STOP before it; they have something to do first). #1792 head b7fd4cba9 (one article plan d0224aba3 + gap metrics). #1810 head b86e99cc7 (screenshots per step, snapshot look, replacement + release checks, tips, cap, metrics). Status lives in KNOWLEDGE-GAPS-PLAN.md "27 Oct" sections.

**Why:** the user didn't want to wait on review, and an accidental checkout in the main folder once interrupted work; two folders mean nobody switches branches under the other.
**How to apply:** never commit #1792 fixes on the phase 7 branch; never switch the main folder back to knowledge-gaps. Related: [[project-knowledge-gaps-feature]].
