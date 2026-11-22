---
name: project-gap-diff-view-fix-plan
description: "NEXT after compact (2026-11-22) - fix gap Changes view diffs: random ids from withListNumbers, published gap shows only hunks, collapsed accordion hides changes"
metadata:
  node_type: memory
  type: project
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-22T12:56:51.064Z
---

User asked (2026-11-22): "think it through, best well thought out, solid, code judo fix", compact, then do ALL of it. Branch ys/feat/github-pr-gaps (PR #2181), all uncommitted. Part of [[project-gap-article-edits-redesign]].

Root causes (verified with a throwaway test on real data from gap 01a1f552-1ece, kb-permissions):
1. `apps/web/src/features/knowledge-base/lib/list-numbers.ts` `withListNumbers` builds a headless `createSlateEditor` whose normalize gives EVERY element a random `id`. Before and after get different ids, so `@platejs/diff` `computeDiff` cannot match nodes: a changed accordion shows as whole delete + whole insert, and unchanged blocks show orange "update" (only the id differs). Raw diff without numbering is correct (marks only the changed words inside the accordion item).
2. Published gap view: `apps/backend/src/modules/knowledge-gaps/application/mappers/gap.mapper.ts` `appliedSegments` shows only `change.undo.hunks` (topLevelHunks context 1): partial article, context blocks drawn as edits, reason repeated per hunk. Open gaps already use `editSegments` over the whole article.
3. Both views (and version history): a change inside a collapsed accordion item is marked but hidden until the item is opened.

Version history (`kb-version-preview.tsx` DiffContent -> `KbDiffContent`) shows the whole document and does not call withListNumbers, so cause 1 does not hit it.

Plan:
- withListNumbers: no node ids in the headless editor (check the platejs `nodeId: false` option in the .d.ts first).
- `version-diff.ts` `computeVersionDiff`: strip `id` (with the comment marks, in the same pass) so ids can never make a block look changed. Do not strip `listStart`.
- Published view, code judo: before = `revertHunks(liveArticle, hunks)` (exists in knowledge-base/domain/plate-blocks.ts), after = live article, then build SAME/EDIT segments from `topLevelChanges(before, after)`, reason once. If revertHunks returns null (article changed since), fall back to the hunks, marked stale. Consider one shared "segments from two documents" helper.
- Diff rendering: open an accordion item (and other collapsible containers) that holds a diff node, in the diff kit, for both views.
- Then: specs (web list-numbers + version-diff, backend mapper), typecheck, lint, wiki, then tell the user to look at the first link again.
