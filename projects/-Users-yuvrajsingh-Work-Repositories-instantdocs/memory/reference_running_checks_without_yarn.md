---
name: reference_running_checks_without_yarn
description: yarn is not on PATH in Claude shells and corepack is blocked by lean-ctx; run tsc and next lint via npx instead
metadata:
  node_type: memory
  type: reference
  originSessionId: 7bd71b4c-21bb-40e4-8050-bd55afc8e291
  modified: 2026-10-27T15:29:45.569Z
---

In Claude Code sessions, `yarn` is not on PATH (it comes from corepack under nvm node v22) and the lean-ctx allowlist blocks `corepack`. The CLAUDE.md checks still work through npx, since `tsc-build` is `tsc -p tsconfig.json` and `lint` is `next lint`:

- `npx tsc -p tsconfig.json`
- `npx next lint --quiet`

Dependencies are usually already installed, so skipping the `yarn` install step is fine unless package.json changed. Related: [[feedback_prisma_types]].
