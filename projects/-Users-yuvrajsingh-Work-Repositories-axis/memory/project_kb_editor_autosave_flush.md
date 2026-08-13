---
name: project_kb_editor_autosave_flush
description: KB editor autosave — the default vs variant flush semantics and the true-drain invariant for useDebouncedAutosave
metadata: 
  node_type: memory
  type: project
  originSessionId: b72e2753-6bcb-4086-8871-5ad47be07d00
---

KB authoring editors share one debounce/coalesce/flush primitive: `apps/web/src/features/knowledge-base/lib/use-debounced-autosave.ts`, consumed by the default article editor (per-field last-write-wins PATCH) and by `use-variant-autosave.ts` (variant OCC PUT). Two editors, one primitive, DIFFERENT save models — see [[project_kb_panel_published_only]] for the default↔variant split.

**Load-bearing invariant — `flush()` MUST be a true drain:** on publish, `flush()` has to send a pending debounced edit AND await the in-flight save + any coalesced trailing run, or a publish can snapshot stale content. The original `useVariantAutosave` flush early-returned on an in-flight save (doSave short-circuited when `saving` was set) — fine for variants historically, but when the default editor was refactored onto the shared hook it silently DOWNGRADED the default's stronger await-in-flight flush → stale-publish regression. Fixed by tracking the in-flight promise and awaiting it (`runSave` returns a promise that settles only after its rerun chain drains).

**Error-path invariant:** the debounced + unmount paths are fire-and-forget → they must swallow a rejected save (`void runSave().catch(() => {})`) so a failing autosave surfaces via the mutation's own `isError`/toast, NOT an unhandled promise rejection. `flush()` must NOT swallow — it propagates so an explicit publish aborts. (Master's default used `content.mutate` which never rejects; `mutateAsync` in the shared hook does, hence the catch.)

**Why:** the default and variant flush/error/coalescing semantics genuinely differ; unifying them onto the weaker one is the recurring "collapsed a load-bearing distinction" trap ([[feedback_refactor_no_regressions]]). Making variant flush a true drain is a beneficial behavior CHANGE (fixes the same latent stale-publish for variants) — flag + test it, don't ship it silently.

**How to apply:** any change here needs manual test of "publish WHILE an autosave is mid-flight" (the narrow window the invariant protects), for both the default article editor and the variant editors. Presentation is separately extracted into `components/editor/{kb-article-editor-shell,kb-collection-editor-body,kb-editor-frame,kb-translation-banner}.tsx` (pure, behavior-preserving). Branch: `ys/refactor/kb-editor-shared-shell`.
