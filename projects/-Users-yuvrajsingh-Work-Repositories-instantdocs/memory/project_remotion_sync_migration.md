---
name: Remotion sync migration — replacing FFmpeg on Fargate
description: Exploring migrating video sync rendering from FFmpeg on AWS Fargate to Remotion Lambda for speed and simplification
type: project
---

User is exploring replacing the current FFmpeg-on-Fargate video syncing approach with Remotion Lambda (as of 2026-04-01).

**Current approach:** FFmpeg on AWS Fargate applies variable playback speeds to sync AI voiceover with screen recordings. Uses SQS queue, webhook callbacks, intermediate S3 uploads. User reports it is slow.

**Proposed approach:** Use Remotion Lambda to handle all syncing — variable speed via `<OffthreadVideo playbackRate={rate}>`, freeze frames via frame repetition, audio overlay via `<Audio>`, section stitching via `<Sequence>`. Eliminates Fargate tasks, SQS, container management.

**Feasibility research (DONE):** Every FFmpeg operation has a Remotion equivalent. Sync logic already exists in `sync-video-mapping.ts`. Playback rate edge cases (extreme slow/fast) can be handled with frame extension/trimming. Performance should be better (one render step vs two).

**Why:** Current Fargate approach is slow (Fargate cold start + two rendering steps + SQS latency). Remotion Lambda is already set up in the project for final video rendering.

**How to apply:** When working on video rendering or sync code, be aware this migration is being explored. The existing sync-video-mapping logic is reusable.
