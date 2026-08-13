---
name: project-kb-import-instantdocs-contract
description: "Non-obvious InstantDocs data locations the Axis KB importer depends on (internal-link hrefs, snapshot↔block id, homepage in uiCustomizations, private-CF signing)"
metadata: 
  node_type: memory
  type: project
  originSessionId: d6e19c6d-7d2e-40f2-b9b2-b73e2d2d05ac
  modified: 2026-07-30T12:30:48.092Z
---

Facts about the InstantDocs side that are NOT discoverable from the Prisma schema and that the Axis KB
importer (`apps/backend/src/modules/knowledge-base/application/import/`) relies on:

- **Internal links inside BlockNote blocks are relative id hrefs**: `/doc/<pageId>`, `/article/<pageId>`,
  `/col/<collectionId>`, `/collection/<collectionId>` — see `getHTMLWithInterlinkURLs` in
  `src/server/helper/publish.ts`. The importer parses these into Axis `KbLinkRef`s. Cards additionally
  carry `linkToId` + `linkToType` (`ARTICLE|COLLECTION|URL`); `linkArticle` blocks carry `linkId`.
- **A `snapshot` block stores NO url.** Its rendered still lives in `PublishedSnapshot`, and
  `PublishedSnapshot.id` **IS the BlockNote block id** (`src/blocknote/blocks/snapshot.tsx` renders
  `src={`snapshot://${props.block.id}`}`). That id is the only correlation available.
- **The custom homepage is not its own table.** It lives in `KnowledgeBase.uiCustomizations` →
  `KbCustomization.isCustomHomePage` + `customHomePageSections[]` (each: `id`, `title`, `columns`,
  `defaultCards[]` = icon cards, `featureCards[]` = icon-or-image cards). Per-locale copy is in
  `customization.localized[locale].customHomePage.sections[sectionId].cards[cardId]`.
  `KnowledgeBase.content` is NOT the homepage.
- **Asset URLs are stored as `CF_DOMAIN`/`PRIVATE_CF_DOMAIN` tokens**, hydrated to absolute https by the
  `db.$use` middleware (`src/server/db.ts` → `hydrateCFDomain`). Private-distribution URLs 403 for an
  external fetcher unless CloudFront-signed, and signing must happen **exactly once** (a second
  `getCloudFrontSignedUrl` appends a second policy and breaks the URL) — the export route does it in one
  recursive pass right before serialization.
- **`fetchPublishedPage` already returns `videoUrl`/`videoPosterUrl`**; the export route just never
  emitted them. Video/snapshots exist only for **published + rendered** articles.

**Publish state is part of the contract (added 2026-07-30).** The export used to call
`fetchPublishedKbTree` — the public help center's read — so every unpublished article was silently dropped.
It now uses its own `src/server/helper/axis-kb-export-tree.ts` (all non-deleted pages + all collections, no
"has a published page" pruning; knowledge-gap articles still excluded), and each article AND each locale
variant carries `status: 'published' | 'draft'`. `draft` collapses both InstantDocs non-live states (never
published, and published-then-`isUnPublished`), since Axis has nowhere to keep a retained snapshot. Rules
that fall out of it, all in `kb-import.service.ts`:
- a draft's `blocks` are the author's editor body (no `draftBlocks`); a published article's `blocks` are the
  snapshot and `draftBlocks` is the pending edit
- title/description/icon come from the published snapshot ONLY while published, else from the page row
- Axis cannot publish a locale of an unpublished article ("Publish the default language first"), so every
  variant of a draft article stays a draft
- the internal-link rebake pass must skip drafts — republishing them would push them live
- the health tally counts `articlesPublished + articlesDraft` as imported, else a KB of drafts reads
  `incomplete`

Axis-side gotchas hit while building this:
- `instantdocsThemeToKbSettings` must read logos, all four favicon/social images, and the URL structure
  off the export's top-level **`kb`** block, not `theme` (and keywords/indexable off nested `theme.seo`).
  Reading them from `theme` silently imported defaults. Do not early-return on a missing `theme`.
- `ArticleVariantService.upsertVariant` bumps `textVersion` **only when the write changed something**, and
  a first write that CREATES the row returns version **0**, not 1. Never hardcode the next version — read
  it off the returned envelope.
- `<video poster>` was already in the sanitizer allowlist but the renderer never emitted it; `poster` is
  now a real `KbMediaNode` prop.

See [[project_kb_custom_homepage_design]], [[project_kb_interlink_durability]],
[[project_kb_reader_serves_stored_html]].
