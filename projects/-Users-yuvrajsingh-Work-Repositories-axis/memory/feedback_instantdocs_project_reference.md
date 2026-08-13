---
name: feedback-instantdocs-project-reference
description: "\"the instantdocs project\" always = the standalone sibling repo (its INTERNAL KB search UI), never the axis instantdocs-kb connector"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72140724-75e9-43ab-aa53-0f5eb97fecc6
---

When the user says to "reference the instantdocs project" (or "InstantDocs"), they ALWAYS mean the standalone sibling repo at `/Users/yuvrajsingh/Work/Repositories/instantdocs` (a Next.js + Radix/Tailwind internal KB app) — NOT the axis `apps/web/src/features/instantdocs-kb/` connector, which is only the ticket-sidebar proxy to InstantDocs.

For its search UI specifically, the reference is the **INTERNAL** KB search — `src/components/search-v2.tsx`, `src/components/search-inline.tsx`, `src/components/kb-filter-modal.tsx` — NOT the published/external KB search (`src/components/search-external.tsx`, `src/server/helper/published-kb-search.ts`).

The instantdocs repo also hosts the S2S integration surface with Axis under `src/app/api/axis/*` + `src/server/helper/axis-*`. As of 2026-07-08 the KB ticket-sidebar **read** API (`/api/axis/kbs` list/tree/collections/articles/search + `axis-kb-api-auth.ts`) was REMOVED (Axis now reads its own native KB — see [[project_kb_panel_published_only]]). Still live there: `/api/axis/kbs/:kbId/export` (Axis KB import), `/api/axis/webhook`, and the OAuth/SSO helpers (`axis-projection`/`axis-identity`/`axis-role-map`/`axis-end-session`/`kb-axis-auth`) gated by `AXIS_WEBHOOK_SECRET`. Repo checks: `rm -rf .next && yarn tsc-build` + `yarn lint --quiet` (base branch `main`; note stale `.next/types` cause false tsc errors until `.next` is cleared).

**Why:** Early in the axis KB-dashboard-search build I wrongly referenced the axis `instantdocs-kb` connector and also glanced at the published search; the user corrected that the design reference is always the standalone project's internal search.
**How to apply:** For any "like instantdocs" UI ask, read files under `/Users/yuvrajsingh/Work/Repositories/instantdocs/src/components/` (internal search + `kb-filter-modal`) as the source of truth. Related: [[project_portless_local_tls]], [[project_kb_search_island_build]].
