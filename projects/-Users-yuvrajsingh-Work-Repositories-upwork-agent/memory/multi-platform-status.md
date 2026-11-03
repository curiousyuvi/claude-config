---
name: multi-platform-status
description: "Which freelance platforms the upwork-agent covers, their account state, and known limits (as of 2026-11-04)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4e6647c6-a683-4e14-b1a4-235e4748ec0e
  modified: 2026-11-03T18:32:50.784Z
---

Agent covers Upwork (browser), Freelancer.com (REST API, token in .env), and Contra/Wellfound/Braintrust (browser, config in src/platforms.ts). Contra is inbox-only (`searchable: false`): free tier shows 3 of ~120 jobs; flip if Yuvraj buys Pro. Wellfound searches /role/r/full-stack-engineer and /role/r/machine-learning-engineer (mostly full-time roles). Arc.dev dashboard renders blank in automation; Toptal, A.Team, Lemon.io push jobs by email only (Lemon waitlisted).

Accounts all use curiousyuvi.work@gmail.com. Toptal verified and in screening, Braintrust has bank details but its 10-min screening test starts on first application (Yuvraj takes it), Contra ID verification in review.

**Why:** Yuvraj wants one agent applying across every platform; these limits explain why some platforms don't produce jobs.
**How to apply:** check this before adding platform features; resume/headshot/screenshots live in data/assets/ (gitignored). Upwork Connects were at 1 on 2026-11-04, blocking Upwork applies.
