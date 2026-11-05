---
name: capture-agent-smarter-plan
description: "Agreed 2026-11-05 plan to make the screenshot agent act like a human using the app: explore-before-write (first), repeat guard, layered perception, write freedom, revise-after-capture. User decisions recorded."
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-05T15:50:48.625Z
---

Context: after #1962/#1965 merged, a deep study of 16 prod capture runs (InstantDocs + Helply, SigNoz logs `body CONTAINS 'capture run (gap_fix) ended'`) found:
- ~1/3 of agent turns repeat an action already tried from the same screen (downloads popup click x8, scroll loops, Helply billing<->plans 5-click cycle x3, same failing click x3). STALL_TURNS warning is advisory and ignored.
- Unnamed controls: InstantDocs share dialog = shadcn `<Switch>` with label in sibling `<p>` (no aria). readPage only uses the control's own names; no `<label for>` either. Search-indexing switch is commented out in InstantDocs source (skip was right).
- Missing data: numbered-list (needs a list; only the run that typed one succeeded), Helply Chats empty ("No AI agent chats yet") -> needs creating a test chat = a write.
- Read-only guard breaks harmless POSTs: Helply "Visit Billing Portal" -> "Error requesting checkout".
- Helply: 8 gaps, 5 correctly nothing_to_picture/outside_app; 2 real failures above; "Manage billing plans and invoice details" nothing_to_picture is suspicious, verify. Helply connection: agents.helply.com, sign_in_method live, 30 routes. Helply run 2026-11-05: 13 cand, 8 created.
- InstantDocs cost all-time (axis.ai.cost, increase): gaps $0.14, app-capture $0.73 (act $0.66). Browser: 28 min capture + 17 min live sign-in across orgs (Firecrawl price unknown).
- I wrongly told the user Helply had no app; always verify before claiming.

USER DECISIONS: write freedom default = "reversible changes" (per-connection setting: read-only / reversible / full within hard lines). Explore-before-write moves to FIRST (core change). User also wants a broader, well-thought plan for more human-like smartness and freedom beyond these items, before building.

PLAN (order agreed): 1) explore-before-write: agent walks the relevant app area first, builds a UI map (screens, controls, real labels, paths) in app memory; drafter writes against it; capture mostly replays found paths; map compounds across gaps. 2) repeat guard: refuse same action from same screen fingerprint (describePageElements) until a record/skip resets; covers loops/cycles/repeat failures. 3) perception layers: CDP accessibility tree names/roles/states; layout-based context naming (same row text, column header, legend, row of an icon); set-of-marks numbers drawn on screenshot; one cheap vision call per screen to name leftovers, cached in app memory; multi-signal ElementRef (role, own name, context name, icon, anchor-relative position) matched by score, replacing "every step named"; coordinate fallback for canvas. 4) write freedom: agent declares write-capable actions (kind + undo plan); constructive/low-stakes allowed no undo; critical-reversible allowed but journaled and must be undone before run ends; irreversible-critical skipped; hard code lines (DELETE unless undoing own, payments/checkout confirm, external sends). 5) revise-after-capture: per-step observations (real label, path, extra steps, unsupported/plan-gated) feed a revision pass on the draft; reviewer sees diff.
Eval: fixed set of real gaps (InstantDocs 6, Helply 3 via local org) measuring pictures/needed, turns, cost per gap.

Next step after compaction: produce the broader human-like-agent plan (user asked), then build in phases. Related: [[capture-agent-stuck-runs]], [[project-knowledge-gaps-feature]].
