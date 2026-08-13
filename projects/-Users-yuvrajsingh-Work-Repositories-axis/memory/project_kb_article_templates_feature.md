---
name: project_kb_article_templates_feature
description: "KB article templates (Save as / Load a Template) — org-scoped kb_article_templates, apply goes through the editor's importContent seam"
metadata: 
  node_type: memory
  type: project
  originSessionId: 39c3a9d8-7c3f-4057-85f3-2cad7c64a476
  modified: 2026-07-27T14:40:06.679Z
---

Shipped on `ys/feat/kb-article-templates` (PR #913, 2026-07-27), ported from the instantdocs article-template feature. Full detail lives in `wiki/pages/kb-article-templates.md` — read that before touching it. The parts worth carrying between sessions:

- **Org-scoped**, not KB-scoped: `kb_article_templates` is offered from every KB in the org (matches instantdocs' workspace scope), and it stores a **copy, not a link** to the source article. Endpoints at `knowledge-base/article-templates`; no domain events (dashboard-only data).
- **Applying is client-side on purpose** — `useApplyKbTemplate` calls the editor's `KbEditorApi.importContent(content, replace: true)`. A server-side write would be clobbered by the article's debounced last-write-wins autosave. Anything else that wants to rewrite an open article body must use that same handle. Save-as-Template flushes the editor first, because the server snapshots the *saved* draft.
- **Apply sets body + icon only.** Title/description are left alone — partly because they name *that* article, partly because `AutoTextarea` in `KbPageHeader` re-seeds only on node-id change, so a PATCHed title would persist while showing stale text until remount.
- Both menu entries are **default-locale only** (the variant editor registers no replace handle), same gate as Import.
- The `(org_id, name_norm)` unique index is the **only** name-collision arbiter (its violation → 409); duplicate enumerates its 50 candidate names up front so one exact `$in` picks the first free one.
- See [[project_kb_second_plate_instance_dnd]] for the react-dnd constraint every secondary editor here hits.
