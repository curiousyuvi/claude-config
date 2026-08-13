---
name: review-before-commit
description: Run /thermo-nuclear-code-quality-review on changes before any commit
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8a26c084-ea6a-4c39-9a35-4d08d4a7463c
---

Before committing, always run `/thermo-nuclear-code-quality-review` on the changes and address its findings first.

**Why:** The user wants a quality gate on every commit. Pairs with [[confirm-before-git-actions]].

**How to apply:** After finishing edits and before asking to commit, run the review. If that exact slash command isn't available in the session, say so and run the closest equivalent (e.g. `/code-review` / `/review-changes`) rather than skipping the gate.
