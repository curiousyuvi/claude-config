---
name: project-data-residency
description: "InstantDocs hosted-region map — PlanetScale, S3 buckets, SES, LLMs"
metadata: 
  node_type: memory
  type: project
  originSessionId: c68497ab-17a9-4598-8ef3-5c3a89d02ab1
---

InstantDocs data residency map:
- PlanetScale (primary MySQL): **us-east-1**
- AWS S3 buckets: **us-east-1** and **ap-south-1 (Mumbai)** — public + private buckets
- AWS SES (transactional email): **us-east-1**
- AWS MediaConvert / Step Functions / Remotion Lambda: AWS (region per `remotion-config.js` and SFN ARN)
- Vercel Functions: **3 regions** — `iad1` (us-east), `fra1` (Frankfurt), `bom1` (Mumbai). Fluid Compute enabled. Function CPU: Performance tier (2 vCPUs / 4 GB).
- Vercel Edge Network: global CDN.
- LLM providers (Anthropic, OpenAI, AssemblyAI, ElevenLabs): US-routed by default

Effective residency: **US**. EU edge compute exists (fra1) but every request hits us-east-1 PlanetScale + SES, so EU residency claims would be misleading.

**Why:** Confirmed by the user on 2026-05-12 while preparing the CTO compliance doc (PlanetScale region + Vercel Functions settings screenshot).

**How to apply:** Use these regions when answering data-residency / GDPR / EU-customer questions, and when reasoning about cross-region latency or replication. Re-verify before publishing externally — regions can change with infra moves. Related: [[project-clerk-idp-migration]], [[project-remotion-sync-migration]].
