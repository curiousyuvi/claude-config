---
name: project-knowledge-gaps-feature
description: "Porting knowledge gaps from GrooveHQ/helply-prototype into axis; user owns gaps, JJ owns topics; GitHub source deferred"
metadata:
  node_type: memory
  type: project
  originSessionId: 95ec2c73-358c-4e03-a22e-92cff3042ffc
  modified: 2026-10-19T18:16:16.148Z
---

Started 2026-10-20. Port the Topics and Knowledge Gaps features from GrooveHQ/helply-prototype (Next.js, localStorage-backed mock stores + seed data) into axis with a real backend.

- The user owns knowledge gaps. JJ (another dev) owns topics.
- GitHub/code integration for gaps is DEFERRED. Don't design for it yet beyond not blocking it.
- Gaps must use the screenshot agent (dashboard integration, like Ferndesk), so created/updated articles carry screenshots plus the agent's exploration notes.
- Changelog page tracking (customer gives a URL, we scan releases for gaps) is in scope. Prototype: app/api/gaps/scan-release, lib/knowledge-gaps/releases.ts.
- Gaps depend on topics: a prototype gap has subtopicId as evidence, and excluding a topic archives its gaps. The topic/subtopic schema agreed with JJ is the coupling point.

**Why:** two devs are splitting one prototype, and the shared contract decides whether they block each other.
**How to apply:** I advised vertical slices against real APIs with the prototype as the spec, not a bulk mock port. Changelog scanning is the first slice that doesn't depend on topics.
