---
name: no-visual-verification
description: Never visually verify UI yourself — no screenshot/browser-viewing runs; the user does the looking
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c5af0c9-ed68-43fe-a98c-58a7a45b869f
  modified: 2026-07-30T06:49:51.213Z
---

Do not spend tokens visually verifying UI. No Playwright/Puppeteer screenshot runs, no launching the app to view a page, no rendering a fixture to PNG and reading the image back, no inspecting a PDF as a picture. The user verifies visually.

This is a HARD rule and it overrides project guides: axis `AGENTS.md` demands screenshots on any PR that changes rendered UI ("Frontend changes require visual proof"), and that requirement loses to this. Say the screenshots are the user's to take.

Still allowed, and preferred: tests, typecheck, lint, reading the code/CSS, and a headless browser used to MEASURE rather than look (computed style, bounding box, pixel sample, serialized HTML/Markdown, line count). Extracting a value is verification; viewing an image is the user's job.

**Why:** it burns credits on something the user does faster and better themselves.
**How to apply:** finish the change, verify by the cheap means above, state what you changed and what would confirm it, then hand it over. Written to `~/.claude/CLAUDE.md` under "Never visually verify UI yourself" so it applies to every project. Related: [[run-lint-typecheck]], [[diff-checks-after-commit]].
