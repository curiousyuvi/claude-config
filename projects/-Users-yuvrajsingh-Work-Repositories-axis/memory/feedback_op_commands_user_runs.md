---
name: op-commands-user-runs
description: "Never run `op` (1Password CLI) commands directly — give the command to the user to run in their authenticated terminal and use the pasted result"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-08T03:05:27.945Z
---

Never execute `op` / `op run` commands myself (2026-08-08 instruction, applies always in this project).

**Why:** Claude's shell is not the user's authenticated 1Password session; runs would block or fail, and secrets handling stays with the user.

**How to apply:** When a step needs `op` (migrations/seeds via `op run`, reading vault refs), print the exact command, ask Yuvraj to run it in another authenticated terminal, and continue from the output they paste back. Related: [[run-app-context-bin-without-op]] for bypassing `op` entirely with plain env vars.
