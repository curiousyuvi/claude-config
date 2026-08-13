---
name: project-kb-review-publish-feature
description: KB Review & Publish approval gate — design decisions and where the invariants live
metadata: 
  node_type: memory
  type: project
  originSessionId: 1f368ced-bc49-45c4-bdbe-3a4e237f4c75
  modified: 2026-08-13T07:19:10.583Z
---

Built 2026-08-13 on branch `ys/feat/kb-review-publish` (from the Notion "KB Access & Publishing" spec, §6-9 only; the KB/article access half of that spec was separate work — see [[project_kb_access_publishing_task]]).

Load-bearing decisions that aren't obvious from the code:

- **Approval is invalidated by edits, never consumed by publish.** `dropApprovedKbReview` deletes the row only when status is `approved`, called from the points every draft edit already converges on (`ArticleService.update`, and the `publishUpdated` private helper in `article-variant.service.ts` / `kb-homepage.service.ts` — those two were made `async` for it). Consuming on publish would break publishing a second locale of an approved article.
- **Editing while `in_review` deliberately does NOT drop the request.** The reviewer reads the latest, and a `changes_requested` note must survive the edit it asked for.
- **The setting is jsonb, not a column**: `KnowledgeBase.settings.review = { enabled, reviewerAgentIds }`, so it inherits the settings PATCH's OCC version and `parseKbSettings` section isolation. Only `kb_review_requests` needed a migration.
- **One row per subject**, article-or-homepage (`article_id` null = homepage), two partial unique indexes. No cycle history.
- Approval is **article-level**, so every locale of an article shares one review state.

Wiki page: `wiki/pages/kb-review-and-publish.md`.

Side effect worth knowing: `AgentMultiSelect` + `agentSearchQueryOptions` moved out of `features/teams/` into `shared/components/` and `shared/api/agents-query.ts`.
