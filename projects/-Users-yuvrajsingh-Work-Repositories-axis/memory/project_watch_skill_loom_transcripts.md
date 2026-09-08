---
name: watch-skill-loom-transcripts
description: /watch skill is set up with a Groq Whisper key; Loom videos need Whisper (yt-dlp subtitle fetch 400s) or the signed VTT embedded in the share page
metadata: 
  node_type: memory
  type: project
  originSessionId: b6e7adcc-2116-4bcb-a78b-82d22f3979b1
  modified: 2026-09-08T12:47:26.702Z
---

The `/watch:watch` skill is fully configured on this machine as of 2026-09-08: `~/.config/watch/.env`
has `GROQ_API_KEY`, `WATCH_DETAIL=balanced`, `SETUP_COMPLETE=true`. Preflight returns `ready`.

Loom share links: yt-dlp's GraphQL subtitles call returns HTTP 400, so the skill reports "no transcript"
unless Whisper runs. Re-run on the already-downloaded `download/video.mp4` with `--detail transcript`
to transcribe without re-downloading. Fallback with no key: the share page HTML embeds a signed
`cdn.loom.com/mediametadata/captions/<id>-N.vtt` URL (grep the page for `captions/`).

**Why:** Loom bug reports from the team (e.g. Adri Jordaan) arrive without captions; the first run
wasted a round-trip discovering this.

**How to apply:** for a Loom URL, run the skill normally (Whisper kicks in). The user pastes API keys
in chat when asked; never run `op` to fetch them ([[feedback-op-commands-user-runs]]).
