---
name: ferndesk-eval-setup
description: "Where the Ferndesk hands-on evaluation lives (accounts, test workspace, evidence folder, Playwright driver) and the headline findings from 2026-10-08 and the 2026-10-13 Pro re-run"
metadata:
  node_type: memory
  type: project
  originSessionId: 8762f395-5a08-4b94-a48d-4e8510a13031
  modified: 2026-10-13T12:30:00.000Z
---

Ferndesk eval (competitor for the docs agent feature) ran on 2026-10-08 (trial) and 2026-10-13 (paid Pro, $149/mo, renews 2026-11-13). Evidence and rerunnable Playwright scripts live in `~/ferndesk-eval/` (README.md is the report; `package/` and `~/ferndesk-eval-2026-10-13.zip` are the shareable bundle without credentials; `~/ferndesk-summary/` plus `~/ferndesk-summary.zip` is the short version with 26 screenshots and 4 videos). Notion write-up: https://app.notion.com/p/3f3b7d82b70780a3927ec742f2c95e81 (Yuvraj's voice, no AI mention).

Accounts: Ferndesk workspace on ysgaur9919@gmail.com (password login, user copies it via pbcopy). InstantDocs test workspace "Groove Eval Docs" on yuvraj+idtest@groovehq.com, password in `~/ferndesk-eval/notes/creds.env` (600, never in chat); brand colour is now green. InstantDocs signup silently rejects gmail addresses. Fake ticket endpoint is a secret gist, answer key in `notes/ticket-answer-key.csv`.

Headline findings (settled 2026-10-13): capture via demo login is strong, including dark mode, hover menus and 6-article batches (the 10-08 "1 of 6 screenshots" note was a reading error, all drafts had images). On the no-code track, Verify docs and continuous verification check against website, codebase and support tickets only; the Dashboard integration is never a verification source even with Website URL empty. An explicit task "re-check this article against my app" does walk the app and catches drift (menu label, KB rename, colour) and retakes screenshots. A ticket-driven fix rewrote the Export article into garbled text. Human Publish still marks an article "Verified as accurate". Ticket clustering strong, theme-to-article mapping weak. Automations (PR drafts, scheduled audits, continuous verification) are switched on in the workspace.

**Why:** Tirth asked for a deep dive; future sessions may extend the test (code track, more scenarios) and should reuse the driver (`scripts/lib.mjs`, `send-task.mjs`, `poll-task.mjs`, `50-fd-task-review.mjs`) rather than rebuild it.

**How to apply:** Run steps with `node scripts/<step>.mjs` from `~/ferndesk-eval`; use `PROFILE=profile2` or `profile3` for concurrent browsers (poll-task.mjs honours PROFILE too). Task output images: open each artifact chip on the task page, not just the first. Headroom hides ToolSearch in this setup, see [[headroom-toolsearch]].
