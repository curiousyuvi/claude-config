---
name: project-knowledge-gaps-feature
description: "Knowledge Gaps + screenshot agent build in axis; plan at repo-root KNOWLEDGE-GAPS-PLAN.md (untracked); user owns gaps, JJ owns topics; GitHub deferred"
metadata:
  node_type: memory
  type: project
  originSessionId: 95ec2c73-358c-4e03-a22e-92cff3042ffc
  modified: 2026-10-20T12:41:49.595Z
---

Started 2026-10-20. Build Knowledge Gaps + screenshot agent ("App access") for real in axis, final mature version, no "fix later" shortcuts. JJ builds Topics.

- Plan: `KNOWLEDGE-GAPS-PLAN.md` at axis repo root (untracked, never commit it). Research notes and meeting transcript: `~/.axis/knowledge-gaps/` (research.md, meeting transcript). Read both after any compaction before continuing. Estimate ~45 working days (~9 weeks), screenshot agent ~12 of those.
- Spec source of truth: Notion page "Knowledge Gaps" (id 3d3b7d82b70780c39e17c839bf673349, Helply Roadmap) incl. its "changes after writing" list. Fathom walkthrough 19 Oct by Tirth.
- Notion fetch through the Headroom proxy compresses the body, but `headroom_retrieve` on the hash in the main session DID return full text (a subagent's retrieve failed).
- Prototype GrooveHQ/helply-prototype HEAD dropped "Rewrite with AI" and simplified auto-publish settings after the walkthrough.
- axis already has a basic gap feature inside `topic-insights` (behind AI_TOPIC_INSIGHTS_ENABLED); plan is a new `knowledge-gaps` module + `app-capture` module, Topics via a `GapTopicsPort`.
- Missing infra: help-center search logging, "was this helpful" votes, changelog ingestion, digests, any browser automation.
- References: GrooveHQ/knowledge-gap (Jared, InstantDocs; judge saw only the question, no clustering/scoring/ledger), kroto-learn/screenshot-agent (user's spike; prompt invited destructive actions).
- Demo: demo.helply.com (password from user, don't store).

**Why:** two devs split one prototype; the Topics contract is the coupling point.
**How to apply:** open decisions are listed in section 7 of the plan; check which the user answered before building. GitHub source stays deferred.
