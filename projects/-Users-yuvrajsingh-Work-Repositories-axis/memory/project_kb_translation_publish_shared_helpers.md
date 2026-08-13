---
name: project_kb_translation_publish_shared_helpers
description: "Canonical shared KB translation-panel + publish-popover helpers; reuse them, don't clone per node type"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f4eb6af-afe5-4d93-9c88-4d488c76f691
---

Thermo-nuclear review of [[project_kb_custom_homepage_design]] de-duplicated the article/collection/homepage translation panels + publish popovers into canonical helpers. A NEW node type must reuse these, not clone a panel:

- **`TranslationLocaleList<T>`** + **`DeleteLanguageMenu`** in `kb-translation-sheet-parts.tsx` — the whole translation-sheet body (spinner, default/additional sections, exists/not-created rows, ⋮-delete menu). Callers pass typed callbacks (`getTitle`, `getDotClass`, `notCreatedTitle`, `onSwitch`, `renderExistingActions`, `renderTranslateAction`). Common minimum summary shape = `{ locale, isDefault, exists, updatedAt }`; per-type fields (title / translationStatus) stay in the caller's closures. Each panel keeps its OWN `TranslationSheet` wrapper + translation overlay + auto-open effect (article/collection mount the overlay INSIDE the sheet, homepage OUTSIDE — placement is load-bearing, don't fold it into the shared list).
- **`PublishPopoverShell`** + **`GatedAlert({noun})`** + **`UnpublishLine`** in `kb-publish-popover.tsx` — shared popover chrome (header/footer, `canPublish`/`actionLabel` derivation, gated alert). Article popover + `kb-homepage-publish-control.tsx` both consume it; body content (slug field, URL fallback copy) stays caller-supplied.

**Correctness invariant (do not re-break):** compare Plate documents with **`plateContentDiffers` (isDeepStrictEqual)** from `article-dirty.util.ts`, NEVER `JSON.stringify` — Postgres jsonb does not preserve object key order, so a stringify compare flags deeply-equal docs as dirty (phantom `hasUnpublishedChanges` on publish→edit→revert). Homepage had this bug; now fixed + unit-tested in `article-dirty.util.spec.ts`.
