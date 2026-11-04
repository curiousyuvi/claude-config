---
name: capture-agent-stuck-runs
description: "Why the screenshot agent added 2 pictures for 23 InstantDocs steps (2026-11-04), the fixes in PR #1954, and how to A/B a capture run locally against the real InstantDocs app"
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-04T13:29:06.895Z
---

Diagnosed 2026-11-04 from SigNoz traces, not guesses: count `chat` spans per capture trace (1 plan + N agent turns + validator calls). 5 of 6 prod runs had 8 turns and ZERO validator calls, so the agent was cut off before it ever tried to record.

Root causes, all fixed in PR #1954 (ys/fix/capture-agent-budget):
- `NO_PROGRESS_TURNS = 8`: any 8 turns with nothing recorded/skipped ended the WHOLE run. Now `turnsPerIntent` (12) per intent, skip only the oldest open one, give up after 2 in a row.
- `list_elements` tool returned `'listed'` (no-op; page is observed after every turn anyway) but the prompt told the agent to call it before each record and the brief opened with it. Removed; first page now goes with the brief.
- Icon-only controls unnamed: InstantDocs three-dots is a bare lucide `<Ellipsis>` SVG (`DropdownMenuTrigger asChild`, opacity-0 until row hover). Label ladder now ends with the icon name from lucide/tabler classes or `data-icon`.
- `record()` validated a preview taken BEFORE `screenshotPointingAt` moved the mouse, so hover states were judged absent. Shot first, then preview.
- `scroll` wheels at the mouse position (sidebar after a sidebar click). Optional `element` added; recipes keep it.

Still open (not code bugs): a feature the app lacks now costs 24 turns (agent doesn't skip on its own); planner plans shots for editor keystrokes and FAQ prose; InstantDocs route catalog has `/kb/null` junk.

Local A/B recipe: 5 "Gaps E2E" orgs in local dev are connected to https://app.instantdocs.com/ (password). Reset a gap to its text-only draft (drop top-level `img` nodes that have `capture`, null `screenshot_report`, `drafted_at = now()`), then insert an `outbox_events` row type `knowledge_gap.screenshots_requested`, queue `knowledge_gaps`, payload `{orgId, gapId, _jobOptions: {jobId: 'kg-shots-<gap>-<draftedAt ms>'}}` while `pnpm dev` runs (unified role runs workers). Run one gap per org at a time: two sessions on one Firecrawl profile get 409. Read results from `knowledge_gaps.screenshot_report`.

Related: [[project-knowledge-gaps-feature]], [[op-run-masks-prose-in-bin-output]].
