---
name: multi-platform-status
description: "Which freelance platforms the upwork-agent covers, their account state, and known limits (as of 2026-11-04)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4e6647c6-a683-4e14-b1a4-235e4748ec0e
  modified: 2026-11-04T15:45:38.667Z
---

Agent covers Upwork (browser), Freelancer.com (REST API, token in .env), and Contra/Wellfound/Braintrust (browser, config in src/platforms.ts). Contra is inbox-only (`searchable: false`): free tier shows 3 of ~120 jobs; flip if Yuvraj buys Pro. Wellfound searches /role/r/full-stack-engineer and /role/r/machine-learning-engineer (mostly full-time roles). Arc.dev dashboard renders blank in automation; Toptal, A.Team, Lemon.io push jobs by email only (Lemon waitlisted).

Accounts all use curiousyuvi.work@gmail.com. Toptal verified and in screening. Braintrust is fully set up: bank details, screening test and KYC all done on 2026-11-04, so applications there go through without a stop. Contra ID verification in review.

Phone alerts go through ntfy (topic in .env as NTFY_TOPIC, app installed and tested 2026-11-04). Urgent alerts (MESSAGE, OFFER, INVITE, NEEDS YUVRAJ) also play an alarm sound on the Mac.

Freelancer account is on the Plus plan (100 bids/month, 84 skill slots). On 2026-11-04 seven AI skills were added to the profile (AI Development, AI Chatbot Development, AI Automation, AI Workflow Automation, AI Integration, Chatbot Development, AI App Development; 32 skills total) because Freelancer refuses bids on projects that share no skill with the profile.

Earn Connects modules on Upwork did not credit when the agent opened the help articles (tried twice on 2026-11-02); free Connects need Yuvraj to do them by hand.

**Why:** Yuvraj wants one agent applying across every platform; these limits explain why some platforms don't produce jobs.
**How to apply:** check this before adding platform features; resume/headshot/screenshots live in data/assets/ (gitignored). Upwork Connects were at 0 on 2026-11-04, blocking Upwork applies.
