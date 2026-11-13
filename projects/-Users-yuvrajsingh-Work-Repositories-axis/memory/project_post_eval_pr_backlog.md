---
name: project-post-eval-pr-backlog
description: "Every gaps and screenshot-agent change the user asked for during the eval grills (2026-11-13), to build together in the PR right after the eval PR"
metadata:
  node_type: memory
  type: project
  originSessionId: 0c25d5a6-97aa-413b-ac9c-0b06e96245af
  modified: 2026-11-13T13:11:40.737Z
---

User 2026-11-13: "after the eval PR the next PR we will cover all these together, along with any small work for later github work, like adding new action/gap types". Measure every item against the eval suite from [[project-eval-harness-plan]]. Order of PRs: [[project-github-integration-plan]].

Screenshot agent (app-capture):
- Restore the user's app after it changes things, by undo or by setting things back itself. Core and critical. Today `domain/capture-agent.prompt.ts:104` says the opposite ("change any setting ... and leave it").
- Restore budget comes ON TOP of the capture budget, never carved out of it (user: current limits are already tight).
- At the end, report what it changed and what it put back; never hide a change (eval compares the report with a DB snapshot diff).
- Write guard decides by whole context, not by action name: block only critical/severely bad actions; allow medium-severity actions when the picture cannot be taken without them; allow low-severity actions even when irreversible. A plain item delete can be low.
- Respect the user's read-only mode: then no writes at all.
- SAFETY BUG found by the guard eval (2026-11-13): in reversible mode the write guard ALLOWS `kb.revokeAllAccess` (3/3) and unpublishing a real doc (3/3), and BLOCKS deleting the run's own sample doc even when the context says it is a sample (3/3). Fix first.
- Image scan calls third-party screenshots (Crisp's own UI in a Crisp integration article) InstantDocs app screens, 3/3 on both cases (scan eval 2026-11-13), so the planner may try to retake pictures of another product.
- Sign-in recorded success (last_sign_in_at set) on an offline app: eval 2026-11-13, tunnel down, Firecrawl landed on ngrok's ERR_NGROK_3200 page and the password sign-in still passed. The sign-in check must confirm a signed-in app screen, not just the absence of a login form.
- Survey agent searched the app's own help articles instead of its UI and missed hover-only controls (eval 2026-11-13, duplicate-doc: marked 'Search results for duplicate doc', said no Duplicate control exists; it is in the doc's hover three-dots menu). Teach it to hover rows for hidden menus and to learn from screens, not from docs inside the app.
- Slow apps: current timeouts are too tight for real apps (action 5 s, settle 4 s, locate 5 s, after-write 5 s, run max 12 min / 80 turns, survey 6 min / 30 turns). Raise them, and give the agent a way to wait for a long process or loading to finish (sleep/poll until done) without burning turns.

- Gap judge drops findability verdicts when the article has no lead-in (starts with a heading) and the judge gives sectionHeading null: `resolveGapVerdict` in `domain/gap-verdict.ts` returns null on `article && !section`. Eval 2026-11-13 after video removal: clone-page-findability 0/3, take-down-findability 2/3. Findability fixes are article-level; accept null section for them.

Knowledge gaps (PR 2 scope, from the first grill):
- New KB action kinds as proposals: new collection, move, delete, merge gaps, multi-change groups per gap/PR; fixes may touch content outside the target section, judged by the grader, not blocked.
- Combined actions are normal (correction + retake, missing + new collection, findability + correction, release touching several articles, + translation).
- Fixes drafted on the working copy; intent-based gaps go Outdated and re-draft only on a substantive base change (normalized-text hash, 10-min debounce); a user just opening an article or a tiny edit must not trigger a re-draft.
- 409 when the same section was edited: auto re-draft + "Re-draft with my edits" button (still open: or a separate AI-merge button?).
- Help-center filter on gap search; OCR image scan for every image (dry run of cost, time and size first); never-published articles are invisible to gaps today.

GitHub (PR 3): more PR types welcome (UI label, behaviour, limit/price, new/removed feature, rename, bug fix with and without doc impact, refactor, dependency bump, copy-only, revert, multi-feature, feature-flagged).
