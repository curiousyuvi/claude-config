---
name: project-gap-edit-screenshots-regression
description: "PR GrooveHQ/axis#2260 MERGED 2026-11-23 (deploying); next: redraft an edit gap on Groove prod to confirm screenshots: edit fixes ask for screenshots again (EDIT_PICTURES), drafter eval runs capture on, Copilot code-check card refetch, signed-out banner redesign"
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

Also open: GitHub Apps all private (Slack ask to Jared drafted). PR replay script not written.

See [[project-gap-legacy-cleanup-pr]] and [[project-gap-article-edits-redesign]].
