---
name: micro-saas-gap-hunting
description: "Yuvraj's micro-SaaS hunt: method in the skill, ledger at skills/micro-saas-gap-hunting/references/"
metadata:
  node_type: memory
  type: project
  originSessionId: beae5e59-ca52-435b-9c4b-95c244dfe26e
  modified: 2026-08-20T13:33:44.651Z
---

Yuvraj is hunting a solo micro-SaaS at roughly $10-15K MRR (100-300 buyers at $50+/mo), preferring
API-shaped products. Method and all history live in the skill: `~/.claude/skills/micro-saas-gap-hunting/`
(SKILL.md, `references/verdict-ledger.md`, `references/screened-index.md`, `references/tooling.md`).
Run `scripts/check.py "idea"` to dedupe; never read the index or ledger whole.

**Hard constraint: customer support is contractually off limits** — helpdesks, ticketing, help centres,
support AI agents, conversation QA, support analytics, and anything sold as an app to Zendesk /
Intercom / Freshdesk / Help Scout / Gorgias / Front. It is a legal bar, not a preference, and it is
invisible from the code. The test is the BUYER: developer/API documentation tooling sold to DevRel,
docs and product teams is in scope (confirmed 2026-08-20). Support is where his domain knowledge is
deepest, so it is the standing temptation of every round.

**State as of 2026-08-20: 311 candidates scored, 6 above 40, none above 69, so nothing is build-ready.**
Top live candidates are one family — tenant-aware retrofits onto an existing pooled Postgres database,
which platform owners (Neon, Nile, Citus, Azure) serve only via migrate-to-us: per-tenant restore (58,
the wedge), retention/purge policy engine (54), per-tenant query attribution (52). Separately, safe
feature-flag removal (47) is the only candidate ever found with tier-2 commitment language behind it.
The 78-scoring Zendesk DSAR fan-out is verified alive but barred by the constraint above.

**Why:** the binding constraint is no longer coverage, it is demand evidence. Position is verifiable
from desk research; money-already-spent is not. Four sourcing methods are now measured as exhausted
(axis brainstorming 0 of 200, guessed buyer access, complaint-first mining, Atlassian-tracker
demand-first), and every survivor came from his own working domain or from evidence-first mining.
Sector expansion is blocked by tooling, not by absence of opportunity: no Reddit (403 and the search
user-agent is refused) and no G2 bodies means non-developer verticals can only be researched through
vendor content, which is inverted signal.

**How to apply:** do not run another volume round of invented candidates — it predictably returns
zero and the skill now says so. Push instead for the two designed cheap tests (20 outreach emails on
per-tenant restore; ten more people like the dated "I would happily pay for safe flag removal"
commenter), or ask him the unblocking question: whose operations can he get on a call this week, or
can he supply a Reddit credential. Related: [[yuvraj-profile]].
