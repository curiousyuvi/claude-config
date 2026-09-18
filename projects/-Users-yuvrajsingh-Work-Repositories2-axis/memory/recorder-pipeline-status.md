---
name: recorder-pipeline-status
description: "State of the recorder-to-article feature as of 2026-09-18 (all PRs merged, prod testing in progress) and where everything lives"
metadata: 
  node_type: memory
  type: project
  originSessionId: 887f294a-fcd7-4b6a-9b3a-6561b071b31d
  modified: 2026-09-18T08:42:03.261Z
---

Recorder → KB article pipeline shipped 2026-09-18. All PRs merged:
- axis #1453 (pipeline: shared/languages catalog, AssemblyAI client in integrations/assemblyai,
  RECORDER_ARTICLE queue + worker in modules/recorder/application, skeleton generator in
  ai/agents/recorder-article, Presets KB settings page with structured/relaxed articleStructure,
  generation loader page). Review fixes landed in b8d44f895 (handleFailedJob terminal marking,
  shared ai-draft-article.ts helper in kb import/, per-type structured nesting).
- helply-recorder-extension #3 (dark glass UI restored from instantdocs 90d697e, tab-only capture,
  KB-driven language picker). CI: typecheck-only workflow on PRs.
- helply-recorder-app #6 (KB-driven language picker + flagcdn CSP + hover fixes). CI slimmed to a
  single ubuntu tsc job (skipLibCheck added); the old 3-OS package/lint/jest matrix always failed
  and was removed.
- instantdocs-recorder-extension: helply branding commit d9c83b0 reverted (c95b449); repo is back
  to original InstantDocs dark UI.

Current phase: testing recorders against prod (next.helply.com), extension first — its .env is
pointed at prod and dist/ is built from merged master. Prod needs the deployed axis migration
(recorder_recordings: article_status, article_id, title) and ASSEMBLYAI_API_KEY from the
Production vault (item exists in all three vaults).

Deliberately deferred: real snapshot blocks (placeholders are [snapshot@hh:mm:ss] paragraphs),
tests for the recorder repos beyond typecheck CI, any large refactor of the rough recorder-client
code (fix-what-you-touch instead), word-level transcript is stored but unused. The mac app's
local-testing recipe is in that repo's AGENTS.md (see [[recorder-app-macos-testing]]).
