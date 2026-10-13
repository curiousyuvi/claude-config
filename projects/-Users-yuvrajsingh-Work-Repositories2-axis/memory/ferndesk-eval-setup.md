---
name: ferndesk-eval-setup
description: "Where the Ferndesk hands-on evaluation lives (accounts, test workspace, stand-in app, evidence folder, Playwright driver) and the headline findings from 2026-10-08, the 2026-10-13 Pro re-run and the code-track test"
metadata:
  node_type: memory
  type: project
  originSessionId: 8762f395-5a08-4b94-a48d-4e8510a13031
  modified: 2026-10-13T18:19:38.139Z
---

Ferndesk eval (competitor for the docs agent feature) ran on 2026-10-08 (trial), 2026-10-13 (paid Pro, $149/mo, renews 2026-11-13) and 2026-10-13 evening (code track). Evidence and rerunnable Playwright scripts live in `~/ferndesk-eval/` (README.md is the report; `package/` and `~/ferndesk-eval-2026-10-13.zip` are the shareable bundle without credentials; `~/ferndesk-summary/` plus `~/ferndesk-summary.zip` is the short version with 31 screenshots and 4 videos). Notion write-up: https://app.notion.com/p/3f3b7d82b70780a3927ec742f2c95e81 (Yuvraj's voice, no AI mention).

Accounts: Ferndesk workspace on ysgaur9919@gmail.com (password login, user copies it via pbcopy; sessions expire after a few hours, re-login with `scripts/02b-fd-login-pw.mjs` per profile). InstantDocs test workspace "Groove Eval Docs" on yuvraj+idtest@groovehq.com, password in `~/ferndesk-eval/notes/creds.env` (600, never in chat); brand colour is green; it contains a "Fern test article" Fern published. Fake ticket endpoint is a secret gist, answer key in `notes/ticket-answer-key.csv`. Stand-in app for the code track: "Lumen Docs" in `~/ferndesk-eval/fakeapp/`, repo github.com/curiousyuvi/lumen-docs (personal), live at https://lumen-docs-three.vercel.app on the personal Vercel scope "curiousyuvis-projects" (deploy with `npx vercel --prod --scope curiousyuvis-projects`, not git-connected), demo login demo@lumendocs.test / lumen-demo-2026 (fake, fine to share). Connected to the same Ferndesk workspace as a second Dashboard integration plus the GitHub app; PR #1 merged as the trigger test.

Headline findings: capture via demo login is strong (dark mode, hover menus, error states, batches; off-domain pages come back without arrows; Fern writes to the demo account when asked). Without code, Verify docs and continuous verification read website, tickets and code only; the Dashboard is never a verification source; an explicit "re-check against my app" task does walk the app and retake screenshots. With code: GitHub becomes a verification source, Fern reads source (not just diffs) and catches unenforced behaviour, and a merged PR became a reviewed draft with a retaken screenshot in five minutes. One workspace treats its one repo as the product, so InstantDocs articles got "fixed" against Lumen code. Audits never pre-draft: every finding needs a "Draft with Fern" click; with code connected the clicked draft did capture live-app screenshots (the 8 Oct no-code one did not). Fern says its capture tool refuses login and error screens. Ticket clustering strong, theme-to-article mapping weak. Human Publish marks an article "Verified as accurate". The 10-08 "1 of 6 screenshots" note was a reading error.

**Why:** Tirth asked for a deep dive; future sessions may extend the test and should reuse the driver (`scripts/lib.mjs`, `send-task.mjs`, `poll-task.mjs`, `50-fd-task-review.mjs`, `63-dump.mjs`) rather than rebuild it.

**How to apply:** Run steps with `node scripts/<step>.mjs` from `~/ferndesk-eval`; use `PROFILE=profile2` or `profile3` for concurrent browsers (poll-task.mjs honours PROFILE). Task output images: open each artifact chip on the task page, not just the first. Kill local test servers by port (`lsof -ti:PORT | xargs kill`), pkill by script name misses them. Headroom hides ToolSearch in this setup, see [[headroom-toolsearch]].
