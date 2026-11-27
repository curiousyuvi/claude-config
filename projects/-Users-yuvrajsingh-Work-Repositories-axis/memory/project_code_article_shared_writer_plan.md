---
name: project-code-article-shared-writer-plan
description: Approved 2026-11-27 plan to merge code-article and missing-gap article writing into one shared writer + picture pipeline, all in the article-from-code PR; build after compact
metadata:
  type: project
---

Approved 2026-11-27 (user: "all in this PR", "first we compact then start building"). Full plan and state: section "2026-11-27 evening" at the end of `.claude/handoffs/github-integration.md` in the main checkout. Work is in worktree ~/Work/Repositories/axis-gh-integration, uncommitted.

Key decisions: code articles use the gaps plan writer (no streaming; loader option 1 already built); Stop keeps current state (before text: delete draft, no charge; during pictures: keep text); writer model per caller (code: Sonnet 5.5 ZDR); review ON; no per-article 5 cap; missing-article gaps with a linked repo run the same code research. Open: cap 12 counting taken pictures instead of planned.

**Why:** user wants one system for both features, no parallel copies, code-judo not hacks.
**How to apply:** gap prompts must stay byte-identical (zero-regression proof); ask eval cost before running. Related: [[project-github-integration-plan]].
