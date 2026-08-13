---
name: project_migration_drift_entity_checks
description: "Migration Drift CI gate fails if a hand-added CHECK constraint isn't ALSO declared on the entity via `checks:`; how to reproduce the gate locally without op run"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54cc5d59-d550-4f7b-9295-f3495adbdfcb
  modified: 2026-07-27T11:38:24.390Z
---

The **Migration Drift** CI job (`scripts/check-migration-drift.sh`) runs two probes that BOTH compare the ENTITY metadata to reality: `migration:check` and `bin/check-schema-drift.ts` (`orm.schema.getUpdateSchemaSQL()`). A cross-column/manual CHECK constraint added by hand-editing a migration (e.g. `kb_comments_single_anchor_check` = article XOR collection) is invisible to the entity metadata, so the gate flags drift (`getUpdateSchemaSQL` emits `drop constraint …`). The committed `.snapshot-axis.json` is NOT the gate's baseline here (the drift DB has its own per-dbName snapshot), so rebuilding the snapshot does NOT fix it.

**Fix:** declare the CHECK on the entity too, matching `note.entity.ts`:
`defineEntity({ …, checks: [{ name: 'kb_comments_single_anchor_check', expression: \`not ("article_id" is not null and "collection_id" is not null)\` }] })`.
The expression must round-trip against Postgres introspection — verify with the local repro; if `getUpdateSchemaSQL` shows a drop+add, adjust the expression until it's empty. Keep the check in the migration too (it applies it); the entity declaration just makes MikroORM aware. Also normalise the committed snapshot's KB tables to the entity-derived form so a dev `migration:create` shows no spurious drift.

**Run the gate locally (no `op run` / 1Password — the drift script + ORM CLI use plain `DB_*` env):** local `axis-postgres` container = `username`/`password`@localhost:5432. `docker exec axis-postgres psql -U username -d postgres -c 'create database axis_drift_check'`, then with `DB_HOST=localhost DB_PORT=5432 DB_USER=username DB_PASSWORD=password DB_NAME=axis_drift_check DB_SSL_ENABLED=false` run (via `pnpm --filter backend run esm …`, NOT the op-run-wrapped `orm`/`db:objects` scripts): `./bin/db-objects.ts --type extensions` → `migration:deploy` → `./bin/db-objects.ts --type tables --type functions --type triggers --type grants` → `./node_modules/@mikro-orm/cli/cli.js migration:check` → `./bin/check-schema-drift.ts`. Both must exit 0 / empty. Snapshot filename is per-dbName (`.snapshot-<DB_NAME>.json`) — clean up stray `.snapshot-axis_*.json` files, never commit them. See [[project_mikroorm_snapshot_merge_corruption]], [[project_run_axis_ci_locally]].
