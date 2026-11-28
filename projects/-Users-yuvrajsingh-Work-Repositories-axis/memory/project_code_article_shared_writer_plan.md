---
name: project-code-article-shared-writer-plan
description: "Shared writer for code articles + missing gaps is BUILT and committed (9fcc618c5, not pushed); open work = propose solid fixes for the problems found in app testing (resume from handoff \"2026-11-28 night\")"
metadata:
  node_type: memory
  type: project
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-28T16:08:04.590Z
---

The plan approved 2026-11-27 is built: commit 9fcc618c5 on `ys/feat/article-from-code` in worktree ~/Work/Repositories/axis-gh-integration, not pushed. More work sits uncommitted on top (picture rule, upload retry, picture report + migration, article-id check); the user wants to test, then commit all together.

Resume point: section "2026-11-28 night: state before compact (RESUME HERE)" at the end of `.claude/handoffs/github-integration.md` in the main checkout. It lists what is committed, what is uncommitted, eval results, debug recipes and the open problem list.

Current ask from the user (2026-11-28): deep dive, then PROPOSE proper fixes for all open problems before building anything: the open editor missing the final picture fill, the capture agent repeating a saving action and skipping its clean-up, slow picture runs, scope drift, pictures in bullet lists.

**Why:** user wants one system for both features, code-judo not hacks, and a proposal before code.
**How to apply:** propose first and wait for approval; gap prompts stay byte-identical unless a shared rule changes on purpose; ask eval cost before any run. Related: [[project-github-integration-plan]], [[feedback-ask-before-any-eval-run]].
