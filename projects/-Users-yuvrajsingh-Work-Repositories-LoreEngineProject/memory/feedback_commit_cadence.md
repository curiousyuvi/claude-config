---
name: Git commit cadence preference
description: User wants commits on medium-substantial changes and PRs on very-big-substantial changes when building LoreWeaver
type: feedback
originSessionId: 79e97dfd-6c88-43e4-a2d4-0f0def85294f
---
For the LoreWeaver project (and likely other long-running coding projects): commit after each medium-substantial change (e.g., completing a scaffolding phase, finishing a migration set, implementing an agent end-to-end), and open a PR for very-big-substantial changes (major milestone completion, architectural refactor, multi-file feature addition that needs review).

**Why:** User wants version-control discipline that preserves meaningful progress checkpoints without spamming micro-commits for every file tweak, and wants PR review ceremony only for changes that warrant human-gate review.

**How to apply:**
- Don't commit after every file edit or tiny fix — let related changes batch into one logical commit.
- Commit triggers: completed scaffolding, working migration set, agent implemented + tested, subsystem wired up end-to-end, milestone completion.
- PR triggers: major milestone (e.g., "full extraction pipeline working end-to-end"), architectural refactors touching many files, risky changes, changes where user input on design would be valuable.
- Always write clear commit messages (imperative mood, explain the why not just the what).
- Never skip git hooks (`--no-verify`) or force-push to main without explicit permission.
