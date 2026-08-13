---
name: feedback_axis_migrations_and_op
description: Axis repo — never hand-write migrations; hand op-gated commands to the user to run
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1985cacb-734e-4712-95fa-d406d20ebc72
---

For the **axis** repo (`/Users/yuvrajsingh/Work/Repositories/axis`):

1. **Never hand-write MikroORM migrations.** Generate them with the tooling (`pnpm --filter backend migration:create`), which also updates the schema snapshot (`apps/backend/src/database/migrations/.snapshot-axis.json`). A hand-written migration leaves the snapshot stale → drift / "no snapshot update" review flags.
2. **Don't run commands that need `op` (1Password) access** — migrations, seeds, `register/update-oauth-client`, anything via `op run --env-file`. Claude has no op access. Write out the exact command and give it to the user to run, then continue from their output.

**Why:** Jared flagged a hand-written migration with no matching snapshot update; op-gated DB commands can't run in Claude's environment.

**How to apply:** When an axis change needs a schema migration, edit the entity, then give the user the `migration:create` command to run. For any `op run`-backed script, hand over the command instead of attempting it.
