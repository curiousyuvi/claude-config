---
name: project_kb_panel_published_only
description: "Ticket-sidebar KB panel must only ever expose PUBLISHED content, searched via the published-KB OpenSearch index"
metadata: 
  node_type: memory
  type: project
  originSessionId: fade3e66-a4a5-4e62-9f85-4408b9bc8229
---

The ticket-workspace KB panel (web `features/knowledge-panel`, backend native reader serving `/api/knowledge/*` in the `knowledge-base` module) must surface **only published KB content** — published articles (`ArticleVariant.publishedAt`/`Article.status=PUBLISHED`, resolved via kb-public `KbReaderService`) and its search must use the **published-KB OpenSearch index** (`kb_published` via `KbSearchQueryStore`), never draft content or the admin/Postgres search.

**Why:** the panel is an agent-facing reader for inserting help-center links into replies; drafts must never leak, and search parity with the public help center is expected.

**How to apply:** tree/collection/article go through `KbReaderService` (published-only); search goes through `KbSearchQueryStore` (already published-only, org-scope enforced by verifying the KB belongs to `@OrgId()` first). This replaced the old InstantDocs proxy (note the axis instantdocs-kb connector is distinct from the standalone [[feedback_instantdocs_project_reference]] repo).
