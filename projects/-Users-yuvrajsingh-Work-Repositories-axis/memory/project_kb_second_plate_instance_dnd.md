---
name: project_kb_second_plate_instance_dnd
description: A second Plate editor mounted over the live KB article editor must drop DndKit — react-dnd allows one HTML5 backend per page
metadata: 
  node_type: memory
  type: project
  originSessionId: 39c3a9d8-7c3f-4057-85f3-2cad7c64a476
  modified: 2026-07-27T14:39:39.004Z
---

Any Plate instance mounted while the KB article editor is alive (template preview, template editor, translation review panes) must use `kbSecondaryEditorPlugins` from `apps/web/src/features/knowledge-base/components/editor/plate-editor-kit.tsx` — it is `kbEditorPlugins.filter((p) => p.key !== DndPlugin.key)`.

**Why:** `DndKit` renders `<DndProvider backend={HTML5Backend}>` via `render.aboveSlate`, i.e. once per Plate instance, and react-dnd permits exactly one HTML5 backend per page. A second one throws *"Cannot have two HTML5 backends at the same time"* — which the app's error boundary mislabels as **"Authentication error: …"**, so the message points nowhere near the cause.

**How to apply:** reach for `kbSecondaryEditorPlugins` for any read-only or secondary editing surface; only the live article/homepage editor keeps the full kit. Everything else (node components, input rules, slash menu, floating toolbars) is identical — you only lose the drag handle. A headless `createPlateEditor` (e.g. `lib/import-article-content.ts`) is unaffected: `render.aboveSlate` only runs inside `<Plate>`. The shared read-only renderer is `KbReadOnlyContent` (`components/editor/kb-read-only-content.tsx`) — it also deep-clones its value, since Slate keys node→path maps by object identity. See [[project_kb_article_templates_feature]] and the wiki page `wiki/pages/kb-article-templates.md`.
