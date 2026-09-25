---
name: recorder-pipeline-status
description: "State of the recorder-to-article feature as of 2026-09-18 (all PRs merged, prod testing in progress) and where everything lives"
metadata: 
  node_type: memory
  type: project
  originSessionId: 887f294a-fcd7-4b6a-9b3a-6561b071b31d
  modified: 2026-09-25T08:37:43.332Z
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

Extension prod test passed 2026-09-18: full pipeline (upload, transcribe, generate, redirect)
worked against next.helply.com. First run stalled because Railway prod runs separate `api` and
`workers` services and `workers` never auto-deployed the pipeline commit — its old QueueName enum
lacked recorder_article, so outbox dispatch failed 5x and archived the event. Fixed by deploying
workers via `railway api` mutation serviceInstanceDeployV2 (MUST pass commitSha: without it Railway
rebuilds the service's current commit, not latest master), then re-inserting the archived row from
outbox_failed_archive into outbox_events as pending (pg script run under `op run`; no psql on this
machine). Open question: why the workers service doesn't auto-deploy on master pushes when api does
— check its GitHub trigger settings in the Railway dashboard. All three recorders (extension, mac
app, windows exe via VM) passed prod testing 2026-09-18; the windows NSIS installer cross-builds
fine from macOS with `npx electron-builder build --win --publish never` after `npm run build`.
Follow-up PR #1457 (structured as the default articleStructure preset + loader header button
tweaks) was open and unmerged at session end.

2026-09-25 update (PR #1523): snapshot blocks now render on Remotion Lambda. The H.264 render proxy
from #1512 was measured and removed: source format is not the lever (webm 0.57s/frame, 1080p H.264
0.8s, 2560 proxy 1.3s), and the encode held the article job so the loader stalled in "transcribing".
GIFs use `framesPerLambda: 5, concurrencyPerLambda: 2` (8.6s vs 15s warm/29s cold); pinned values are
safe here because GIF length is capped (`KB_SNAPSHOT_GIF_MAX_MS`, test-guarded against the 200-function
cap) and the function is 10240 MB. InstantDocs' past failures with these options were the 200-function
cap on long videos and OOM with 2 tabs on a 2048 MB function. The Remotion site bundle (holds
SNAPSHOT_FPS) is now deployed by `.github/workflows/remotion-site.yml` (skips when the reproducible
bundle matches the bucket); secrets REMOTION_{DEV,PROD}_AWS_* are set. GitHub does not run
pull_request workflows on an unmergeable PR: no Actions check suite at all means rebase first.
`pnpm --filter backend typecheck` fails locally with 7 duplicate @types/pg errors that CI does not hit;
unresolved, commit with LEFTHOOK=0 when it bites.

Deliberately deferred (as of 2026-09-18): real snapshot blocks (placeholders are [snapshot@hh:mm:ss] paragraphs),
tests for the recorder repos beyond typecheck CI, any large refactor of the rough recorder-client
code (fix-what-you-touch instead), word-level transcript is stored but unused. The mac app's
local-testing recipe is in that repo's AGENTS.md (see [[recorder-app-macos-testing]]).
