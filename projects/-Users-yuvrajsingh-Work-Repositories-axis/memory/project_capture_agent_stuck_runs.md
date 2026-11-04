---
name: capture-agent-stuck-runs
description: "Why the screenshot agent added 2 pictures for 23 InstantDocs steps (2026-11-04), the fixes in PR #1954, and how to A/B a capture run locally against the real InstantDocs app"
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-04T19:11:12.461Z
---

Diagnosed 2026-11-04 from SigNoz traces, not guesses: count `chat` spans per capture trace (1 plan + N agent turns + validator calls). 5 of 6 prod runs had 8 turns and ZERO validator calls, so the agent was cut off before it ever tried to record.

Root causes, all fixed in PR #1954 (ys/fix/capture-agent-budget):
- `NO_PROGRESS_TURNS = 8`: any 8 turns with nothing recorded/skipped ended the WHOLE run. Now `turnsPerIntent` (12) per intent, skip only the oldest open one, give up after 2 in a row.
- `list_elements` tool returned `'listed'` (no-op; page is observed after every turn anyway) but the prompt told the agent to call it before each record and the brief opened with it. Removed; first page now goes with the brief.
- Icon-only controls unnamed: InstantDocs three-dots is a bare lucide `<Ellipsis>` SVG (`DropdownMenuTrigger asChild`, opacity-0 until row hover). Label ladder now ends with the icon name from lucide/tabler classes or `data-icon`.
- `record()` validated a preview taken BEFORE `screenshotPointingAt` moved the mouse, so hover states were judged absent. Shot first, then preview.
- `scroll` wheels at the mouse position (sidebar after a sidebar click). Optional `element` added; recipes keep it.

Still open (not code bugs): a feature the app lacks now costs 24 turns (agent doesn't skip on its own); planner plans shots for editor keystrokes and FAQ prose; InstantDocs route catalog has `/kb/null` junk.

2026-11-04 night, #1954 deployed, 9 InstantDocs gaps re-queued via outbox SQL (scratchpad kg-shots-queue.sql; retry jobIds get a `-retry-<ms>` suffix). 6 real runs: Export KB 2/2 added (icon-name fix), password links 1 added, numbered list 0/3 (needs keyboard), HTML blocks 0 new (2 kept), Groove migration 0/1, downloads popup 0/1. The 3 "nothing_to_picture" gaps log no `capture run (` line at all. BIG finding: the agent could only click/hover/fill/scroll + 9 keys, so editor steps were impossible. Branch `ys/feat/capture-agent-interactions` (c2368bb14, not pushed, no PR): editor lines listed as `(editor text)` found by xpath under the host (ProseMirror redraws tagged lines), caret/selection reported, click options (right/double/triple/at text edge/modifiers), type at caret key by key, press any key or shortcut (ControlOrMeta resolved by remote browser platform), select_text, drag, pick_option; recipes replay all. Local A/B done 2026-11-04 23:05 IST on local gap 01a186ea (numbered-list draft swapped in via scratchpad ab-numbered.sql): runs 1-5 went 0, 1, 2, 2, 3 of 3 pictures. Fixes along the way: caret drawn in shots (page CSS hides it), clicking editor text isn't "just clicked", validator told a box is on editor text (Highlighted.editorText), do earlier steps first. PR #1962 MERGED 2026-11-04 23:51 IST as 9d85135b0 (squash). Prod rerun 2026-11-05 00:35 IST: numbered list 2/3 (was 0; shot-2 rejected, recorded after pressing Backspace), HTML blocks +4, password links 0 (agent skipped plan-gated share options), downloads popup 0 (needs a download), Groove + Legacy = nothing_to_picture. Queuing during a deploy made 4 jobs fail: two workers both ran jobs, Firecrawl 409 on the shared profile, and base retries (3, 1s exponential) gave up in ~40s. Suggested fix (not done): screenshot jobs get their own backoff ~30s over ~15min. After deploy: re-queue InstantDocs gaps with scratchpad kg-shots-queue.sql (user runs via op run psql) to see editor steps on prod. Open: run-5 step-3 shot targets "Choose Members." after Backspace (user to eyeball).

Local A/B recipe: 5 "Gaps E2E" orgs in local dev are connected to https://app.instantdocs.com/ (password). Reset a gap to its text-only draft (drop top-level `img` nodes that have `capture`, null `screenshot_report`, `drafted_at = now()`), then insert an `outbox_events` row type `knowledge_gap.screenshots_requested`, queue `knowledge_gaps`, payload `{orgId, gapId, _jobOptions: {jobId: 'kg-shots-<gap>-<draftedAt ms>'}}` while `pnpm dev` runs (unified role runs workers). Run one gap per org at a time: two sessions on one Firecrawl profile get 409. Read results from `knowledge_gaps.screenshot_report`.

Related: [[project-knowledge-gaps-feature]], [[op-run-masks-prose-in-bin-output]].
