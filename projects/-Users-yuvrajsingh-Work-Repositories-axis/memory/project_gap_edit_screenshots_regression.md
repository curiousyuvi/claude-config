---
name: project-gap-edit-screenshots-regression
description: "RESUME: prod GitHub tests on Groove mostly done (see body, 2026-11-24); PR GrooveHQ/axis#2260 MERGED 2026-11-23 (deploying); next: redraft an edit gap on Groove prod to confirm screenshots: edit fixes ask for screenshots again (EDIT_PICTURES), drafter eval runs capture on, Copilot code-check card refetch, signed-out banner redesign"
metadata:
  node_type: memory
  type: project
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-23T17:05:08.579Z
---

Cause (found 2026-11-23 on Groove prod): #2181 deleted the capture planner; the new-article prompt got a "when to add a picture" rule, the edit prompt only got the tag format, so edit drafts asked for 0 screenshots (prod: 21/26 edit fixes had screenshots before, 0 after). Missed because the drafter eval was hard-coded `capture: false`, the capture-plan eval was deleted with the planner, local checks looked at the UI only, and the backfill kept old screenshot reports until a redraft.

PR #2260 (MERGED 2026-11-23) also fixed a prod bug CodeRabbit found: draftNewArticle lifted picture paths before withoutSentences dropped blocks, so new-article pictures landed one step late; now cleanup runs first.

PR #2260 contents:
- `EDIT_PICTURES` in gap-draft.prompt.ts, shared `NO_PICTURE_FOR` line; "happens off screen" dropped (contradicted `outside=`).
- drafter eval: capture on by default, `pictures_asked` check, `asks_for_pictures` grader criterion (appliesTo capture on), version hash covers rendered user prompts.
- Eval (10 tune edit cases, 30 runs, no grader): 0 screenshots before; 47 with first wording; 32 with final wording; text checks 29/30 each time. Final wording lost the in-app picture on domains-apex-record (n=1, may be noise).
- CodeCheckCard: `refetchOnMount: 'always'` + loading until `isFetchedAfterMount` (replaced a global staleTime 0).
- AppSignInBanner redesigned like the connect-app callout (option A).

Running drafter evals: `--only` needs full variant ids (`case--real-notes`, `--no-notes`, `--wrong-note`); ~$0.007/run without grader; needs op Touch ID in a terminal tab.

Local banner preview trick: app DB is postgres.axis.orb.local (unreachable from my shell); patch window.fetch in the page to add `signInNeeded: true` to /api/knowledge-gaps/app-access, banner appears within 60s.

Follow-up PR GrooveHQ/axis#2261 MERGED+deployed 2026-11-24: CodeRoutesService.learn had mergeRoutes args swapped (crawl filled 150-route list, code routes dropped: Groove lost 9 of 65); mergeRoutes now variadic newest-first. Open decision: a later crawl can still evict code routes (priority or reserved share?). Prod checks 2026-11-23: both redrafts asked for screenshots (01a1b41a: 2 new; 01a1b41b: 2 new + 1 retake, all done) but NO capture_hint run ever happened for Groove (hints fire only when the agent is stuck); Groove routes refresh only on the next routes run.

Prod GitHub test state 2026-11-24 03:22 IST (Groove): PR #2262 merged+deployed (workers 02:29 IST). mobile-frontend linked (it draws the real settings/billing/Insights UI; GrooveHQ/Groove only has old Backbone views, so hints from it said "not found"). Replays via base64 REPL (terminal tool refuses parens/lone r): Groove #14695 + mobile-frontend #7753/#7752 (#7752 found nothing). PR run opened NEW gap 01a20a3d "Panel button now named Insights" with code guidance steps; drafted 03:11 (25 edits, 8 retakes). Screenshot agent reached the Insights panel but it shows "Authentication failed: Failed to fetch" in the capture test account, so all 6 retakes unchecked. Code hints have fired (01:28, 02:08, 02:46, 03:16), all found:false. code_routes: 48 pages from mobile-frontend, 0 from Groove. Insights auth cause found 2026-11-24: panel is an iframe from https://agents.helply.com that signs in with POST /auth; capture browser blocks cross-site POSTs (capture-safety.ts floorFor) so it showed "Authentication failed: Failed to fetch". User added allowed write prefix https://agents.helply.com/ (confirmed in DB 14:06 IST, write_mode read_only). RESUME HERE: redraft of 01a20a3d queued ~14:20 IST; check with scratchpad check-final.sql pattern (gap 01a20a3d: drafted_at, marks, screenshot_report steps outcome/detail, capture_hint runs) whether Insights signed in and the 8 retakes were taken. Prod DB checks need op run + Touch ID in a terminal tab; REPL commands go base64-encoded via railway ssh (user types SSH passphrase). replay script bin still not written.

Production GitHub App made public 2026-11-23 (user said so 2026-11-24); staging/dev apps may still be private. PR replay script not written. Prod 2026-11-24: redraft of 01a1be67 (Billing Overview plan management) took all 3 screenshots; hints on 01a20a3d found screens but the test account lacks the Insights add-on. Still unseen on prod: hint that leads to a taken screenshot, a real (not replayed) merged PR, manual verify that finds a mistake, Insights sign-in via write prefix, GrooveHQ/Groove 0 code pages.

See [[project-gap-legacy-cleanup-pr]] and [[project-gap-article-edits-redesign]].
