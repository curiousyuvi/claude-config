---
name: project-voiceover-requeue-recovery
description: "How to re-dispatch stuck AI_AUDIO_GENERATE tasks, and the guards that make it safe"
metadata: 
  node_type: memory
  type: project
  originSessionId: a6505c38-ce3b-4645-abf0-e2eb1f8e45c8
  modified: 2026-08-14T12:09:22.599Z
---

`scripts/requeue-stuck-voiceover-tasks.ts` (untracked, local only) re-dispatches
stranded voiceover tasks. Written 2026-08-14 to recover from the long-runner
port outage ([[project-railway-long-runner-port]]).

It POSTs straight to the Railway `/api/tasks/process-voiceover-sync` endpoint
reusing the existing task row and taskId, rather than going through
`startVoiceoverGenerationWithRemotionSync`.

**Why:** that entry point calls `checkIfTaskAlreadyRunningForPage`, which counts
any PENDING row for the page with no staleness check. A stuck PENDING row
therefore blocks every retry, including the customer's own retries from the UI.
Reusing the row sidesteps the guard. The tradeoff is that it also bypasses the
credit check, so only re-run tasks that failed for infrastructure reasons.

**How to apply:** always dry-run first (no `--execute`). Only re-dispatch tasks
at `processedClips: 0` — anything partial would re-render and re-charge clips
that already completed. Reset FAILED rows to PENDING before dispatching or the
UI shows an error for the whole run. `LONG_TASK_SERVER_URL` in local `.env`
points at localhost, so it must be overridden for a prod run; the script refuses
`--execute` against localhost. Stagger dispatches: the single Railway container
also serves live traffic.
