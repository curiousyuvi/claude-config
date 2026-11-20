# Plan: knowledge gaps as article edits (no sections)

Everything below was read in the repo. Paths are relative to `/Users/yuvrajsingh/Work/Repositories/axis`.

## 0. Core decisions (made so the design holds together)

- **The edit unit is a kbMdx block.** These are the blocks from `kbMdxBlocks` (`apps/backend/src/modules/knowledge-base/application/ai-format/kb-mdx-edits.ts:35-50`): a top-level node, a whole list run, or an accordion item.
  - Block ids (`b7`) depend on position, so they are only used inside one prompt.
  - What gets stored is a **fingerprint**: a sha256 of the block's nodes in "as-written" form (the `DERIVED_KEYS` stripping in `article-dirty.util.ts:37-50`, keys sorted), plus the block's index when it was drafted.
- **Finding a block again** (`locateEdit`): renumber the current body, then pick the block with the same hash, nearest index first. If no block matches, the edit is stale.
  - Publish, outdated check, capture write-back and the gap page all use this one function, so they cannot disagree. (Today they can: outdated uses `substantivelyChanged` at `gap-outdated.service.ts:96`, while publish uses `plateContentEdited` at `fix-sections.ts:110`.)
  - Exception: an `insert_*` anchor may also match on substance alone, using `section-substance.ts`.
- **Undo works on top-level hunks.** Whenever text is written into an article (publish or send-for-review), store `diff(bodyBefore, bodyAfter)` hunks with one context node. Undo finds each `after` run and swaps it back to `before`. Undo therefore does not depend on the kind of op.
- **`editsFromDocuments(base, after)`** is a single helper that turns any before/after pair into block edits. It diffs top-level nodes, widens each hunk to kbMdx block edges, emits `replace` plus `delete`s, and turns a pure insertion into an `insert_after` on the previous block. It is used by:
  - the data backfill
  - release pictures
  - the findability fix
  - capture write-back
- **`knowledge_gaps.article_id` stays**, but only as the subject article (list title, placement, translations panel). No text lives on the gap.
- **The detection judge, release scan and code agent give a `quote` instead of `sectionHeading`.** The quote resolves to focus blocks, generalising `quotedInSection` (`code-finding-quote.ts:29-42`). Dedup before drafting uses the focus hashes.

## 1. Schema

**`knowledge_gap_changes`** (`domain/entities/knowledge-gap-change.entity.ts`):
- **Kinds:** `edit_section` is renamed to `edit_article`, and `new_article` is added.
- **Nullable:** `article` becomes nullable; a new article gets its id at publish.
- **Dropped:** `sectionHeading`, `beforeContent`.
- **Kept:** `fixContent` (body of a new article), `fixEditedAt`, `appliedAt`, `undo`.
- **Added:**
  - `edits jsonb not null default '[]'`, holding `GapBlockEdit[]`
  - `touchedHashes text[] not null default '{}'`, set by code (a generated column cannot unnest jsonb)
  - `baseHash varchar(64) null`
  - `fixTitle varchar(200) null`
  - `description jsonb null`
  - `pictureMarks jsonb not null default '[]'`
  - `screenshotReport jsonb null` (typed `CaptureReport`)
  - `outdatedSince timestamptz(3) null`
  - `assetIds: kbAssetIdsProperty(['fix_content','edits','undo'])` with `kbAssetIdsIndex(...)`. The asset GC finds tables from entity metadata (`kb-asset-gc.service.ts:62,205`), so it picks this up automatically.

**`knowledge_gaps`** (`knowledge-gap.entity.ts`):
- **Dropped:** `sectionHeading`, `sectionHash`, `beforeContent`, `fixTitle`, `fixDescription`, `fixContent`, `beforeDescription`, `fixEditedAt`, `screenshotReport`, `assetIds` and its index (`:116`), and `uq_knowledge_gaps_live_section` (`:151-153`).
- **Kept:** `draftedAt`, which now marks a gap as drafted; `outdatedSince`, now the earliest of its changes'; `draftFailure`.

JSON shapes, as new file `apps/backend/src/modules/knowledge-gaps/domain/article-edits.types.ts`:
```ts
interface GapBlockEdit { id: string /* e1.. */; reason: string; action: KbMdxEditAction;
  target: { hash: string; index: number; nodes: PlateDocument };   // block before
  after: PlateDocument;   // written nodes (replace keeps media via withKeptAssets)
  editedAt: string | null }
type GapPictureMark =
  | { id: string; kind: 'retake'; assetId: string; why: string }
  | { id: string; kind: 'new'; after: { editId: string } | { hash: string }; shows: string;
      target: string | null; caption: string; frame: 'close' | 'whole'; outsideApp: string | null };
interface GapChangeUndo { /* existing :11-16 */ hunks?: { before: PlateDocument; after: PlateDocument }[];
  description?: string | null }
// description column: { before: string | null; after: string }
```

**Shared enum changes:**
- `GapChangeKind` (`packages/shared/src/knowledge-gaps.ts:10`): `EDIT_SECTION` becomes `EDIT_ARTICLE`; add `NEW_ARTICLE`.
- `GapDraftFailure.SECTION_GONE` becomes `ARTICLE_GONE` (`:127`).
- `GAP_LEAD_IN_HEADING` (`:250`) is deleted.
- `GapArticleProblem.SECTION_CHANGED` becomes `BLOCKS_CHANGED` (`knowledge-gaps-protocol.ts:152-158`).

### Migration and backfill (two releases)

**Release A (expand).**
- Change the entities, but keep the old gap and change properties with `/** @deprecated backfill only */`.
- Run `pnpm --filter backend migration:create`, then edit the generated file. Between the dropped and re-added check constraints, add:
  - `update knowledge_gap_changes set kind='edit_article' where kind='edit_section'`
  - `update knowledge_gaps set draft_failure='article_gone' where draft_failure='section_gone'`
- Drop the unique index.
- Run `pnpm --filter backend db:entities`.

**One-off backfill script.** New files `apps/backend/bin/knowledge-gaps-article-edits-backfill.ts` (Kysely, batches of 500 per org, idempotent: it skips any gap that already has `edits <> '[]'` or a `new_article` change). The pure conversion goes in `bin/_knowledge-gaps-article-edits-rows.ts` with a spec, following `_kb-link-backfill.ts`. Rows are handled as follows:

| Row | What the backfill does |
|---|---|
| Gap with an article, `before_content` and `fix_content` | Insert or reuse an `edit_article` change at position 0. `edits = editsFromDocuments(before_content, withoutReviewNotes(fix_content))` with reason = gap claim. Copy `fix_edited_at`, `screenshot_report`, `outdated_since`, and `description {before_description, fix_description}` when `fix_description` is set. |
| Old `edit_section` changes | Same conversion from their own `before_content` / `fix_content`. |
| Published gaps | `applied_at = published_at`, `undo.hunks` from the same diff (context-anchored), `touched_hashes` set to the after-block hashes. |
| `in_review` gaps | Same hunks, `applied_at` stays null. |
| `MISSING` gap with `fix_content` | `new_article` change: `fix_content`, `fix_title`, `description.after`. |
| Unsafe: `fix_content` set but `before_content` null on a non-missing undecided gap | Set `drafted_at = null`; the nightly redrafts it (`knowledge-gap-nightly.processor.ts:110`, whose predicate becomes `draftedAt: null`). |
| Unsafe: same, on a published gap | No undo is possible; revert already refuses these today (`gap-publish.service.ts:248-252`). |

**In-flight work during the window between deploy and backfill.**
- New code never reads the old columns.
- "Drafted" is `drafted_at`, so the nightly does not redraft converted gaps.
- A screenshot job for an old draft finds no marks and does nothing.
- `preflight`, `publish` and `revert` reply 409 "being upgraded" while the deprecated `fixContent` is set and the gap has no text change.

**Release B (contract).** Remove the deprecated properties, then generate the migration that drops the old columns and the GIN index.

## 2. Shared protocol (`packages/shared/src/knowledge-gaps-protocol.ts`)

**`GapDetail` (`:277-338`):**
- **Removed:** `sectionHeading`, `beforeContent`, `fixTitle`, `fixDescription`, `fixContent`, `fixEditedAt`, `screenshotReport`, `articleBody`.
- **Added:** `articleEdits: GapArticleEditView[]` and `newArticle: GapNewArticleView | null`.
- `changes` now lists only non-text actions.

```ts
interface GapArticleEditView { changeId; articleId; articleTitle; publishedUrl: string|null; reason;
  description: { before: string|null; after: string } | null;
  segments: ({ kind:'same'; nodes: PlateDocument } | { kind:'edit'; editId; reason; before: PlateDocument;
     after: PlateDocument; edited: boolean; stale: boolean })[];
  screenshotReport: CaptureReport|null; outdatedSince: string|null }
interface GapNewArticleView { changeId; title; description: string|null; content: PlateDocument; screenshotReport }
```

**Other protocol changes:**
- The server builds `segments` from the live draft body plus the edits, so the web never re-implements block matching.
- In `GapChangeView` (`:427-468`), the `EDIT_SECTION` variant and `GapChangeSection` go away.
- In `GapPublishPreflightResponse`, `sectionChanged` and `articleProblem` are replaced by `articles: { changeId; articleTitle; problem: GapArticleProblem|null; unpublishedEdits: boolean }[]`.
- `GapPublishResponse.articleId` becomes the first text change's article.
- `packages/shared/src/schemas/knowledge-gap-change-edit.schema.ts`: `editGapChangeSchema` stays as `{content}` for one block edit. Add `editGapArticleSchema { title?, description?, content? }`.

## 3. Backend, by area

### Knowledge-base helpers

- **`kb-mdx-edits.ts`:** split `applyKbMdxEdits` into `applyBlockEdits(blocks, {action, block, nodes}[], opts)` (no parsing) and add `applyKbMdxEditsEach`, which returns `{document, accepted, rejected: {edit, problems}[]}`. The current version throws on any problem (`:110`); the new one rejects per edit. Add `kbMdxBlockHash`.
- **`domain/plate-blocks.ts`:** add `plateNodesHash` and `topLevelHunks(before, after)` (LCS, generalising `unchangedEnds` at `:5-16`). Export both from the barrel.
- **`kb-article-plan.ts`:** move `withoutEchoedFaqAnswers` and `stepHeadingProblems` here from `plan-cleanup.ts:34,72`. They are generic and agree with the `ITEMS` rules (`kb-article-writing-guide.ts:8-12`). `isTitleCase` moves along with them.

### Domain (`modules/knowledge-gaps/domain`)

**Deleted files:**
- `article-sections.ts` (+spec)
- `fix-sections.ts`
- `publish-gate.ts`
- `section-substance.ts` (+spec): merged into `article-edits.ts` as the substance matcher
- `plan-cleanup.ts`:
  - `withoutLoneStep` is **dropped**: it fights the Structured preset ("Emit EVERY part of the task as a 'step'", `kb-article-writing-guide.ts:16`).
  - `withoutStepAnnouncements` is **dropped**: it rewrites the colon intro the presets require (`:16,18`).
  - The other two move to the shared plan (see above).

**New files:**
- `article-edits.ts`: `locateEdit`, `applyGapEdits`, `editsFromDocuments`, `editSegments`, `touchedHashes`, `undoHunks`, `applyUndo`.
- `article-quote.ts`: replaces `code-finding-quote.ts`. `blocksQuoting(article, quote)` returns focus hashes.
- `picture-marks.ts`: `extractPictureMarks(doc)` for compiled new articles; `marksToShots(afterDoc, marks)` converts marks to `{afterPath, indent}`, with indent taken from `blockGroups` slotIndent.
- `gap-publish-gate.ts`: per-change `editProblem(change, draft, {allowUnpublishedEdits})`.

**Changed files:**
- `gap-detection.types.ts`: `GapArticle.sections` becomes `content` plus `mdx` (`:32`).
- `gap-verdict.ts`:
  - `section` becomes `focus: string[]` (`:21`).
  - `EDIT_SECTION` proposals become `EDIT_ARTICLE` with `focus` (`:47-52,162-166`).
  - `matchSection`, `sectionFor` and `subHeadings` are removed (`:335-366`).
  - `resolveReleaseFindings` merges a repeated finding on the same article into that article's focus (`:255-269`).
  - `releasePicturesVerdict` takes the article (`:274`).
- `gap-judge.prompt.ts`: `sectionHeading` becomes `quote` (`:14-17`, `:57-60`), and `articleBlock` renders whole articles under the same budget (`:137-152`).
- `release-scan.prompt.ts`: `sectionHeading` becomes `quote` (`:10,79`).
- `code-review.prompt.ts`: same field change.
- `gap-draft.prompt.ts`:
  - `EDIT_RULES` describes the whole article and the per-edit `reason` (`:57-66`).
  - New `gapArticleEditsSchema`: edits gain `reason`, plus `pictures` and `description`.
  - `NEW_ARTICLE_RULES` (`:47-56`) is deleted. It contradicts the writing guide on the colon intro and FAQ placement. The new-article prompt keeps only `GAP_RULES`, the title and description rules, and the picture item.
  - `agreeWith` is removed (`:153-155`).
- `gap-auto-publish.ts`: counts changed top-level nodes across the edits (`:22-25`). Auto-publish needs exactly one text change and no actions.
- `release-pictures.ts`: targets are articles; skip an asset whose block a live change touches.

### Detection and writer

- **`knowledge-gap-writer.service.ts`:**
  - `create` (`:206-236`) writes no section fields and adds an `edit_article` change at position 0 with `touchedHashes = focus`.
  - `sameTargetProblem` and `fixedSinceEvidence` (`:160-204`) query `knowledge_gap_changes` by `article_id` plus `touched_hashes && $focus` (applied changes for "already fixed").
  - `recordOnce` takes `pg_advisory_xact_lock(hashtext(org||article))` through Kysely `sql`. This replaces the unique-index retry (`:94-102`).
  - `DetectedGap.fix/screenshotReport` (`:46-48`) becomes `edits?: {articleId; edits; report}[]`.
  - `proposableChanges` (`:137-141`) drops `EDIT_ARTICLE` once the gap is drafted.
- **`gap-change.repository.ts`:** `TEXT_CHANGES` becomes `[PUBLISH_DRAFT, EDIT_ARTICLE, NEW_ARTICLE]` (`:10`). Proposal key is `kind:article` (`:20`). Add `gapsEditingArticle` and `overlappingLiveChanges`; delete `pendingSectionEdit`. `gapChangeViews` (`:156-232`) drops the section branch and filters out text kinds.
- **`knowledge-gap-detection.service.ts`:** log `quote` instead of `sectionHeading` (`:307`).
- **`code-findings.writer.ts`:** `usable` uses `blocksQuoting` (`:76-83`); `asReleaseFinding` passes the quote (`:100-109`).
- **`code-verify.service.ts`:** counts distinct focus blocks instead of sections (`:335-338`).
- **`knowledge-gap-release-scan.service.ts`:** unchanged apart from types.
- **`gap-release-pictures.service.ts`** (`:100-135`): retakes over whole articles, then `editsFromDocuments(article, retaken)` feeds `recordReleaseCorrection`.
- **`gap-subtopic-lifecycle.service.ts`:** `restore` (`:272-299`) uses `distinctOn(article)` and "no live change overlapping".
- **`gap-triage.service.ts`:** the reopen guard (`:179-181`) becomes an explicit overlap check under the same advisory lock.

### Drafting

- **`gap-drafting.ts`** is rewritten.
  - `draftArticleEdits(model, attribution, input, article, pictures)`:
    - renders `renderKbMdxBlocks(kbMdxBlocks(withImageText(...)))` for the whole article
    - runs `applyKbMdxEditsEach` with `clean = withoutSentences(talksAboutSources)` and `keepMedia: true`
    - runs `denials` and `droppedUnits` per edit on its own target
    - feeds rejected edits back once with `kbMdxRetryNote`, asking only for those edits again
    - turns accepted edits into `GapBlockEdit`s
  - `draftNewArticle`:
    - uses `writeArticlePlan` + `compileArticlePlan` + `kbArticleWritingGuide(structure)`, like `recorder-article-worker.service.ts:218-238`
    - a `picture` visual item through `visualNode` writes a marker that `extractPictureMarks` lifts out
    - then applies `withoutLeadingAnswer` and the link passes (`:71-76`)
- **`gap-draft.service.ts`** (`:100-197`):
  - Loads every pending text change.
  - The `MISSING` path upserts the `new_article` change.
  - Otherwise it uses `loadWithDrafts` per article. A missing article removes its change; if none are left the failure is `ARTICLE_GONE`.
  - The findability path is `findabilityFix(whole content)` followed by `editsFromDocuments` (`findability-fix.ts:25-46` works unchanged on a whole article).
  - Articles are drafted in parallel. Merged-article text goes to the subject article's edit (`:266-270`).
  - Under the row lock, per change: skip it if `fixEditedAt >= startedAt`; otherwise save `edits`, `touchedHashes`, `baseHash`, `description`, `pictureMarks`, and null `screenshotReport` and `outdatedSince`.
  - `GapRedraft` gains `changeIds?`, so only stale edits are redrafted. `keepEdits` passes the team's edited `after` as MDX.
  - The refix "no change" check (`:153-162`) becomes "zero edits on every article".
  - The charge (`:184-193`) is unchanged: one per round, subject is the first article. No change is needed in `ai-action-billing.ts:76`, since the action still records in this file. `AiCallScope` (`:80-93`) already covers the parallel calls.
- **`gap-model.service.ts`:** `draftSectionEdits` becomes `draftArticleEdits`, which sends `namedImageParts` (`app-capture/domain/model-image.ts:26`, now exported) the way `reviewArticle` does (`capture-model.service.ts:176-190`).
- **`gap-draft-request.service.ts`:**
  - `draftSettled` uses `draftedAt` (`:24-27`).
  - `redraft` clears `draftedAt` and takes `changeIds` (`:54-62`).
- **`app-capture/application/services/article-pictures.service.ts`** (new, exported): the image and picture loading lifted from `article-review.service.ts:72-88`, used by both the reviewer and the drafter.

### Screenshots

- **`article-screenshots.service.ts`:**
  - `illustrate` and `picturePass` (`:221-292`), `plan` (`:294-309`) and the second review pass go away.
  - Add `pictureMarked(orgId, docs: {title; content; preset; shots: PlannedShot[]; retake: Set<string>}[], runKey, screens, options)`:
    - one `run()` with `only = retake`
    - a `plan` callback that returns the drafter's shots
    - one `review` per document, run as a whole article (the `ReviewedArticle.section` flag is deleted)
    - returns per document `{content, report: {...report, steps: stepsOfDoc(i)}, changes}`
  - `run()` and `CapturedRun.added` gain a document index. Today `const [doc] = docs` at `:405` and "single article" at `:194` limit new shots to the first document.
  - `retakeChanged` is kept for release pictures.
- **Supporting app-capture files:**
  - `plan-partition.ts:61`: handle more than one document.
  - `capture-plan.prompt.ts`: delete the planner schema, prompt and `plannedShots`. Keep `PlannedShot` (gaining `doc`), `CAPTURE_SHOTS_MAX` and `reportSteps`, which `capture-ledger.ts:154` uses.
  - `screenshot-slots.ts`: delete `screenshotSlots` and `inStepsChangedSince` (`:181-205`). Keep `pictureBlocks`, `blockGroups` and `stepMates`, which release rechecks and `plan-partition` need.
  - `article-visuals.ts`: keep `recheckIntent`, `findableStep` and `stepText`, which release pictures need.
  - `capture-model.service.ts`: delete `plan` (`:105-120`).
- **`gap-screenshot.service.ts`** (`:84-164`):
  - Builds one document per pending text change that has marks (after-document = `applyGapEdits(live)`, or the new-article content).
  - Makes one run with `gapShotsRunKey(gapId, draftedAt)`, so the cap and charge key are unchanged.
  - Writes back under lock with "unchanged" judged per change: `edits = editsFromDocuments(live, pictured)`, keeping reasons by target and giving new targets the capture's change sentence. It sets `screenshotReport`.
  - `capturing()` (`:66-78`) becomes: drafted, and some change has marks, no report and no edit.
- **`gap-capture-release.service.ts`** (`:25,73,94,109`): the same predicate, read from the changes.

### Outdated and refix

- **`gap-outdated.service.ts`:**
  - Uses `gapsEditingArticle` and `locateEdit` against the published content.
  - A stale change gets `outdatedSince`, and the gap gets the earliest of them.
  - If nobody edited it, `requests.redraft(orgId, gapId, false, [changeIds])`.
  - `SECTION_GONE` becomes `ARTICLE_GONE`, and only when the article itself is gone.

### Publish, undo, auto-publish, translations

- **`gap-publish.service.ts`:**
  - `swapSections`, `applySwap` and `rewriteSection` (`:325-517`) become `applyTextChanges(direction)`, which loops over the text changes the same way for each:
    - lock the drafts (`:463`)
    - `editProblem`
    - `liveEdit.write`, re-checking `locateEdit` inside the callback, as `:508-513` does today
    - store `undo.hunks` and the description before
    - `releases.release`
    - `wentLive`
  - Unpublished teammate edits: allowed for a manual publish on any article, and the preflight warns per article. Never allowed for auto-publish. This replaces the own-only rule at `:351`.
  - A new article is just one `new_article` change through `createArticle` (`:363-382`), which sets `change.article` and `gap.article`.
  - On a `BLOCKS_CHANGED` conflict, a fresh transaction marks the change outdated after the rollback.
  - `revert` (`:236-282`):
    - the rival check becomes `overlappingLiveChanges` against `undo.hunks` after-hashes (`:255-262`)
    - undo runs `applyUndo`; a missing run is 409 "changed since published"
    - the description is restored only when it is unchanged (`:269-274`)
  - `completeReviewed` (`:296-318`) loops over all text changes.
  - `refuseNotReady` and `autoPublishRefusals` (`:105-130`, `:409-416`): more than one text change, or any action, refuses.
- **`gap-changes.service.ts`:** `isOperation` excludes the two text kinds (`:49`). `sendDraftsForReview` takes the set of articles written into drafts (`:145-157`).
- **`gap-placement.service.ts`:** reads title and description from the `new_article` change (`:37-42`).
- **`gap-auto-publish.service.ts`:** select fields change (`:48-80`).
- **`gap-translation-fanout.service.ts`:** unchanged. It is called per article from `wentLive`.

### Interfaces, query, realtime, digest

- **`knowledge-gap-review.controller.ts`:**
  - `PATCH :gapId/fix` and `EditKnowledgeGapFixDto` are removed (`:187-197`; `knowledge-gaps.dto.ts:296-310`).
  - `PATCH :gapId/changes/:changeId` now takes `editGapArticleSchema`, handled by `triage.editArticle`.
  - New `PATCH :gapId/changes/:changeId/edits/:editId` takes `{content}`, handled by `triage.editBlock`. It sets `edit.after`, `edit.editedAt`, `change.fixEditedAt`, and recomputes `touchedHashes`.
  - Both use `@RequirePermission('knowledge_base.manage_gaps')`.
- **`gap-query.service.ts`:** `has_fix` becomes an `exists` over text changes with edits or content (`:111`). The detail builds `articleEdits` with `editSegments` over draft bodies (`:262-292`).
- **`gap.mapper.ts`:** drops the removed fields (`:100,112-121`).
- **Realtime (`gap-realtime.publisher.ts`) and digest (`gap-digest.service.ts`):** no change; neither reads section fields.

## 4. Web (`apps/web/src/features`)

**Knowledge base:**
- New `knowledge-base/components/versions/kb-diff-content.tsx`: `KbDiffContent({previous, next})`, extracted from `DiffContent` (`kb-version-preview.tsx:88-120`) together with the cached `diffIsInline`. `kb-version-preview.tsx` uses it.
- Export `KbDiffContent` from `knowledge-base/index.ts`.

**Knowledge gaps, new files:**
- `components/article-edit-view.tsx`: renders the segments. A `same` segment is `KbReadOnlyContent` at 55% opacity. An `edit` segment is `EditBlock`.
- `components/edit-block.tsx`: the reason, `data-change`, a stale badge, and either `KbDiffContent(before, after)` or, in edit mode, `KbDocumentEditor` keyed `${changeId}:${editId}`. This is the old `SectionEditor` (`gap-article-tabs.tsx:124-145`), now per edit.
- `components/new-article-view.tsx`.
- `hooks/use-gap-edits.ts`: on-screen edits keyed `${changeId}:${editId}`, debounced autosave through `saveBlock` / `saveArticle`. This replaces `OWN_SECTION` and the sections logic in `use-gap-review.ts:13,27-28,46-80`.

**Knowledge gaps, changed files:**
- `gap-article-tabs.tsx`: `articleTabs(gap)` comes from `newArticle` plus `articleEdits`; `own` and `SectionEdits` are removed.
- `gap-article.tsx`: the navigator total counts the open tab's edit segments (`:36-53`).
- `gap-article-body.tsx`:
  - `aroundSection`, `FixContent` and `FixEditor` are replaced by the views above.
  - Description editing is per change.
  - `FAILURE_TEXT` gets `ARTICLE_GONE` (`:184-191`).
- `gap-change-list.tsx`: the `EDIT_SECTION` entry is removed (`:19-23`).
- `publish-problems.tsx` and `use-publish-preflight.ts`: per-article problems.
- `gap-action-bar.tsx`, `gap-status-note.tsx`, `draft-working.tsx`, `capture-working.tsx`: name articles instead of sections.
- `screenshot-report-note.tsx`: one per change.
- `api/client.ts` and `hooks/use-gap-actions.ts`: `saveFix` / `saveChange` become `saveBlock` / `saveArticle`.
- `api/query-options.ts`: also poll while `data?.drafting` (`DRAFT_POLL_MS`, `:79-81`).

**Deleted:** `section-diff.tsx`, `lib/line-diff.ts` (+test), `lib/plate-lines.ts` (+test).

Every component stays under 300 lines; the review hook is split into `use-gap-edits`.

## 5. Evals (`apps/backend/evals`)

**Stages that change:**
- `stages/drafter.ts`:
  - `section` becomes an optional `focus` quote (`:39-49,85-91`).
  - The run uses `draftArticleEdits` on the whole corpus article.
  - The result gains `edits`, `pictures` and the after-MDX.
  - New checks:
    - `format_preserved`: every untargeted block is byte-identical
    - `edits_valid`: none rejected after the retry
    - `pictures_expected`: an optional `expected.pictures`
  - The grader's evidence shows each edit with its reason and before/after.
  - Mechanically rewrite the 21 drafter cases: `section:` becomes `focus:`.
- `stages/article-review.ts`: per-section snapshots (`:19,97-106`) move to an eval-only `harness/article-sections.ts` copied from the deleted domain file; the reviewer is called without `section`.
- `stages/capture-plan.ts`, `capture-plan.spec.ts` and the 13 `cases/capture-plan`: **deleted**, since the planner leaves production. Their outside-app and FAQ expectations become `expected.pictures` on drafter cases.
- `stages/gap-judge.ts` and `release-scan.ts`: the `section` expectation becomes `near` (a phrase the quoted block must contain), checked by `quote_resolves`. Rewrite 53 and 17 cases with a one-off script; heading text works as `near`. Update `baselines/gap-judge.json` with a fresh run.
- `stages/code-verify.ts`: count focus blocks.
- `cases/fix-pipeline/*` (24, labelled only): `edit_section` becomes `edit_article`; drop `section`.
- `bin/_eval-replay.ts`: field renames.

**New drafter cases**, built from corpus articles reshaped in the case input (add an inline `articleContent` override to the input schema):
1. `no-headings-prose`: a flat FAQ-like article with no headings, wrong limit in paragraph 3.
2. `prose-steps`: steps written as sentences in paragraphs, wrong menu path.
3. `images-before-text`: a screenshot precedes each step's text; the fix must keep each picture's place and mark one retake.
4. `table-limits`: plan limits in a table; only the changed cell's row block is touched.
5. `single-long-section`: about 40 blocks under one h2; one sentence wrong deep inside.
6. `numbered-h3-steps`: `### 1. Open settings` step headings; add a step between 2 and 3 plus a new picture after it.

## 6. Tests

**Domain (unit):**
- `article-edits.spec.ts`: locate, stale, substance anchors, `editsFromDocuments` on lists, accordions and pure insertions, `undoHunks` round-trip.
- `article-quote.spec.ts`, which replaces `code-finding-quote.spec.ts`.
- `picture-marks.spec.ts`.
- Update `gap-verdict.spec.ts`, `gap-auto-publish.spec.ts`, `release-pictures.spec.ts`, `gap-judge.prompt.spec.ts`, `gap-draft.prompt.spec.ts`, `findability-fix.spec.ts`.
- Delete `article-sections.spec.ts`, `section-substance.spec.ts`, `draft-cleanup-rules.spec.ts` (its kept rules move to `kb-article-plan.spec.ts`).
- In knowledge-base: `kb-mdx-edits.spec.ts` (per-edit acceptance, `applyBlockEdits`) and a `plate-blocks` spec.

**Services (DB-backed through `test-context`, routed to `integration`):**
- Rewrite:
  - `gap-draft.service.spec.ts` (two articles, rejection retry, hand edit wins)
  - `gap-publish.service.spec.ts` plus `gap-publish.spec-harness.ts` (multi-article apply, conflict marks outdated, undo hunks, review path, unpublished-edits rule)
  - `gap-outdated.service.spec.ts`
  - `gap-screenshot.service.spec.ts` (one run across two articles, write-back)
  - `knowledge-gap-writer.service.spec.ts` (overlap dedup, advisory lock, already fixed)
  - `gap-changes.service.spec.ts`
  - `gap-query.service.spec.ts` (segments)
  - `gap-subtopic-lifecycle.service.spec.ts`
  - `gap-release-pictures.service.spec.ts`
  - `gap-capture-release.service.spec.ts`
  - `gap-triage.service.spec.ts`
  - `code-findings.writer.spec.ts`
  - `knowledge-gap-detection.service.spec.ts`
- App-capture: `article-screenshots` specs through `article-screenshots.spec-harness.ts`, covering per-document new shots.
- Backfill: `bin/_knowledge-gaps-article-edits-rows.spec.ts` covering every row type in the backfill table.
- The `ai-action-billing.spec.ts` and `permission-coverage.spec.ts` gates must stay green.

**Web:** update `gap-article-tabs.test.tsx`, `use-gap-review.test.ts`, `publish-problems.test.tsx`, `use-publish-preflight.test.ts`, `gap-change-list.test.tsx`, `gap-publish-popover.test.tsx`. Add `article-edit-view.test.tsx`.

## 7. Build sequence

Define `T="DB_HOST=localhost DB_NAME=axis_test pnpm --filter backend exec vitest run"`.

1. KB helpers (`applyBlockEdits`, per-edit apply, hashes, `topLevelHunks`). Verify: `$T --project unit src/modules/knowledge-base/application/ai-format src/modules/knowledge-base/domain`.
2. Gap domain (`article-edits`, `article-quote`, `picture-marks`, types). Verify: `$T --project unit src/modules/knowledge-gaps/domain`.
3. Shared enums and protocol, entities (with deprecated fields), generated migration with the edits from section 1, then `pnpm --filter backend db:entities`. Verify: `pnpm --filter backend db:entities:check && DB_NAME=axis_test pnpm --filter backend migration:up`, then `pnpm --filter backend exec tsc --noEmit`.
4. Repository, writer, verdict, judge, release-scan and code-findings quote. Verify: `$T src/modules/knowledge-gaps/application/services/knowledge-gap-writer.service.spec.ts src/modules/knowledge-gaps/domain/gap-verdict.spec.ts`.
5. Drafter (prompt, `gap-drafting`, model images, `gap-draft.service`, request). Verify: `$T src/modules/knowledge-gaps/application/services/gap-draft*`.
6. Screenshots (`run` multi-document, `pictureMarked`, gap screenshot and capture-release). Verify: `$T src/modules/app-capture src/modules/knowledge-gaps/application/services/gap-screenshot.service.spec.ts`.
7. Publish, undo, changes, auto-publish, triage, controller. Verify: `$T src/modules/knowledge-gaps/application/services/gap-publish.service.spec.ts src/modules/knowledge-gaps/application/services/gap-changes.service.spec.ts`, then `$T --project unit src/modules/billing src/permission-coverage.spec.ts`.
8. Outdated, release pictures, lifecycle, query and mapper. Verify: `$T src/modules/knowledge-gaps`.
9. Backfill script and its spec. Verify: `$T bin/_knowledge-gaps-article-edits-rows.spec.ts`, then a dry run with `--dry-run` against a local copy.
10. Web: `KbDiffContent`, the views, the edits hook, polling. Verify: `pnpm --filter web test -- knowledge-gaps knowledge-base`, then `pnpm check`, then sandbox screenshots of a two-article gap, a new article, and a stale edit.
11. Evals. Verify: `pnpm --filter backend exec vitest run evals`, then `pnpm --filter backend evals -- --stage drafter --tier smoke`.
12. Release B: remove the deprecated properties, generate the drop migration, then `db:entities`. Verify: `pnpm --filter backend db:entities:check && $T`.

## 8. Risks and open questions

**Risks:**
- **Judge recall.** Asking for a quote instead of a heading may shift gap-judge recall. The quote is optional for a pure addition, and dedup falls back to the subtopic.
- **Formatting-only edits.** A teammate's formatting-only edit to a replaced block now triggers an automatic redraft instead of a silent publish refusal, which is safer but uses more model calls.
- **Accordion granularity.** Undo hunks work at top-level granularity, so an undo inside an accordion fails if someone edited another item. It fails with a 409; it never overwrites.
- **Backfill window.** Between deploy and backfill, converted gaps refuse publish (409) for minutes.

**Questions for the owner:**
1. **Auto-publish across articles.** Should the auto-publish rule allow a high-confidence correction that edits more than one article? This plan refuses it, matching today's "changes to other articles wait for a person".
2. **Deleting the capture-plan eval.** Is deleting the capture-plan eval stage and its 13 cases acceptable, given the planner leaves production?

### Critical Files for Implementation
- `apps/backend/src/modules/knowledge-base/application/ai-format/kb-mdx-edits.ts`
- `apps/backend/src/modules/knowledge-gaps/application/services/gap-draft.service.ts` (with `gap-drafting.ts` and `domain/gap-draft.prompt.ts`)
- `apps/backend/src/modules/knowledge-gaps/application/services/gap-publish.service.ts`
- `apps/backend/src/modules/app-capture/application/services/article-screenshots.service.ts`
- `packages/shared/src/knowledge-gaps-protocol.ts`
