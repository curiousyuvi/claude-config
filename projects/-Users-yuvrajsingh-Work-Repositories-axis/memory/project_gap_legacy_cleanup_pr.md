---
name: project-gap-legacy-cleanup-pr
description: "NEXT after compact (2026-11-22): run thermo-nuclear review of cleanup PR GrooveHQ/axis#2245 in a fresh subagent, fix genuine findings, commit+push"
metadata:
  node_type: memory
  type: project
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-22T17:37:56.053Z
---

State 2026-11-22 (IST evening):
- PR #2181 (gaps whole-article redesign + code features) MERGED as cf2d7fb18 and deployed to production. Production backfill `knowledge-gaps:article-edits-backfill --apply` ran: 75 written, 14 skipped, 0 redrafted; recheck left 2 never-drafted gaps (01a1a4a8 archived, 01a1f25e open), harmless.
- Drafter core eval on redesign: $1.43, tune 97% (35/36), grader scores >= round 3; recheck $0.20 showed export-kb-videos miss was noise; roles-admin-create-kb drops a correct Members sentence 1/3 (next tuning round).
- Cleanup PR GrooveHQ/axis#2245, branch `ys/chore/gap-legacy-section-columns` (commit 83985ce52, from master cf2d7fb18): drops 9 legacy columns + asset_ids/index on knowledge_gaps, section_heading/before_content on knowledge_gap_changes, refuseUnconverted, backfill script/rows/spec/package script; gap-detection.store dismissUndrafted now uses NOT EXISTS change with fix_edited_at; kb-content-migration drops the knowledge_gaps scope and beforeContent column; migration Migration20261122173038_GapLegacySectionColumns (down() hand-reordered: asset_ids added after its source columns; up+down tested in a rolled-back txn on axis_review2). Staging never ran the backfill (warned in PR body). Auto-fix NOT on for #2245.

NEXT (user asked, then compacted): "/thermo-nuclear-code-quality-review entire PR in a fresh sub agent and you fix all genuine findings" for #2245. Spawn a fresh general-purpose agent with the skill path (~/.claude/skills/thermo-nuclear-code-quality-review/SKILL.md), scope `git diff origin/master...HEAD` on that branch, read-only; then verify each finding, fix genuine ones, run kg tests (DB_HOST=localhost DB_NAME=axis_test), typecheck, biome, commit + push (user's request covers this). Keep the 5 local-only files out of every commit (see [[project-gap-article-edits-redesign]]).
