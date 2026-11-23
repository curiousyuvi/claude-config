---
name: project-gap-edit-screenshots-regression
description: "ACTIVE 2026-11-23: #2181 regression — gap EDIT fixes no longer get screenshots (planner deleted, edit prompt has tag format but no 'when' rule). User wants a plain-words explanation of what happened + how local testing/evals missed it, after compact."
metadata:
  node_type: memory
  type: project
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-23T14:04:25.139Z
---

Found 2026-11-23 IST while user tested GitHub/screenshot features on the Groove prod workspace (org 019edaf0-b76c-770a-bd5a-ece5bd417a92, repo GrooveHQ/Groove linked to KB `groove`, auto-publish off).

What happened:
- Before #2181 (cf2d7fb18): after any fix was drafted, GapScreenshotService called ArticleScreenshotsService.illustrate (a capture PLANNER that read the fix and chose screens itself). No picture marks were stored.
- #2181 deleted the planner on purpose (design: writer places `<screenshot …/>` tags; `pictureMarked` captures only those). New-article prompt got a WHEN rule (`NEW_ARTICLE_PICTURES` in gap-draft.prompt.ts). Edit prompt (`gapArticleEditsPrompt`) only gets the tag FORMAT (`PICTURE_TAG_GUIDE` from picture-marks.ts, when capture on) and no rule on when to use it.
- Prod evidence (pending changes): edit_article before #2181 = 26 changes, 21 with screenshot_report, 0 marks; after = redrafts of gap 01a1b41a (card declined) twice → 0 marks, 0 reports. new_article before: 40 changes, 37 reports, 0 marks.
- Consequence: edit fixes get no pictures, the screenshot agent never runs for them, so its code-hint (GitHub) path is never exercised.
- Why missed: drafter eval measures text criteria only (facts, fixes_claim, keeps_what_was_right, no_invention, voice, links) — nothing counts picture requests; #2181 deleted the capture-plan eval stage + 13 cases; local visual check looked at diff/edit UI, not whether an edit draft triggers screenshots; backfill copied old screenshot_report so existing gaps still showed pictures in prod/local, hiding it until a REDRAFT.

Proposed fix (not started, user not yet approved): add an edit rule mirroring NEW_ARTICLE_PICTURES ("in blocks you write, put a <screenshot/> tag right after each step whose screen a reader needs to see; none for off-screen/fact/contact-only steps"), plus a drafter eval criterion counting picture requests on step-style edits; eval run ~$0.50, ask first.

Pending in prod: billing gap 01a1b41b-6629-7934-a2d4-9a778f7570ed redraft was waiting on user's SSH passphrase in terminal tab c31 (may not have run). Redraft method: `railway ssh --service workers --environment production -- 'cd /app/apps/backend && echo "await get(GapDraftRequestService).redraft(\"<org>\", \"<gap>\", false); console.log(\"REDRAFT-QUEUED\")" | APP_ENV=production pnpm repl 2>&1 | grep -E "REDRAFT|Error|rror:"'` (pipe must be remote-side; user types SSH passphrase; new terminal tab each time if user typed in the old one).

Also open: branch ys/fix/code-check-card-stale (uncommitted, web: articleCodeCheckQueryOptions staleTime 0 + test) fixes Copilot check card showing a cached old error; awaiting user OK to commit/PR. GitHub Apps all private (Slack ask to Jared drafted). PR replay script not written.

See [[project-gap-legacy-cleanup-pr]] and [[project-gap-article-edits-redesign]].
