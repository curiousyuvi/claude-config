---
name: ferndesk-eval-setup
description: "Where the Ferndesk hands-on evaluation lives (accounts, test workspace, evidence folder, Playwright driver) and the headline findings from 2026-10-08"
metadata:
  node_type: memory
  type: project
  originSessionId: 8762f395-5a08-4b94-a48d-4e8510a13031
  modified: 2026-10-08T10:24:26.008Z
---

Ferndesk eval (competitor for the docs agent feature) ran on 2026-10-08. Evidence and rerunnable Playwright scripts live in `~/ferndesk-eval/` (README.md is the report; `package/` and `~/ferndesk-eval-2026-10-08.zip` are the shareable bundle without credentials). Comparison doc: https://claude.ai/code/artifact/987b8ce1-4945-43c0-a160-cbeae07f464f.

Accounts: Ferndesk workspace on ysgaur9919@gmail.com (Pro trial, password login, user resets it and copies via pbcopy). InstantDocs test workspace "Groove Eval Docs" on yuvraj+idtest@groovehq.com, password in `~/ferndesk-eval/notes/creds.env` (600, never in chat). InstantDocs signup silently rejects gmail addresses. Fake ticket endpoint is a secret gist, answer key in `notes/ticket-answer-key.csv`.

Headline findings: screenshot capture via demo login works reliably; verification caught 1 of 5 planted errors and used the public website because Settings > General had Website URL = instantdocs.com (now cleared); the dashboard was never listed as a verification source; team decision (Yuvraj, 2026-10-08): treat verification as working per their demo; write-ups assume the full loop exists and position our edge as owning tickets plus better ticket-to-article matching. Trial expired 2026-10-08 evening; ticket clustering strong, theme-to-article mapping weak; a human Publish click marks an article "Verified as accurate".

Round 2 (started 2026-10-13, Pro subscription bought): re-run everything the trial cut short, then update README (~/ferndesk-eval), summary (~/ferndesk-summary), both zips, and the Notion page https://app.notion.com/p/3f3b7d82b70780a3927ec742f2c95e81 (written in Yuvraj's voice, no AI mention). Pending list: (1) Verify docs with Website URL empty on the same 8 articles, planted errors still live: billing "15th"/"$40", "Click Appearance in the top navigation bar", KB renamed to "Groove Eval Docs"; check whether Dashboard now appears under Review sources; (2) audit finding "Draft with Fern" flow; (3) re-run the 6-article batch to see if screenshots drop again; (4) harder capture scenarios: seeded data states, dark mode, permission-restricted page, hover menus; (5) Automations toggles: continuous verification and scheduled audits; (6) widget and Chrome extension quick look; (7) brand colour change that did not save last time (Theme & Styling has a Save button). Notion images are uploaded via notion-create-file-upload then a multipart POST from scripts/notion-upload.mjs.

**Why:** Tirth asked for a deep dive; future sessions may extend the test (code track, more scenarios) and should reuse the driver (`scripts/lib.mjs`, `send-task.mjs`, `poll-task.mjs`) rather than rebuild it.

**How to apply:** Run steps with `node scripts/<step>.mjs` from `~/ferndesk-eval`; use `PROFILE=profile2` for a second concurrent browser. Headroom hides ToolSearch in this setup, see [[headroom-toolsearch]].
