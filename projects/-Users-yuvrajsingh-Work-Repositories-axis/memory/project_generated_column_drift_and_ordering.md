---
name: project_generated_column_drift_and_ordering
description: "Adding a STORED generated column that calls a db:objects function — the two gotchas (varchar cast for the drift gate, function-before-schema ordering)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 1e927e1c-86e1-4d35-94a1-f2ea8187e4d2
  modified: 2026-07-30T17:46:39.909Z
---

MikroORM 7 supports generated columns first-class (`p.array().columnType('uuid[]').generated('(expr) stored').ignoreSchemaChanges('extra')`; precedent: `textValueNormHash` on the custom-field value entities). Two things bite:

**1. Cast varchar sources to `::text` BEFORE `coalesce`, or the drift gate fails forever.** Postgres normalizes `coalesce(icon_value, '')` on a `varchar` column to `COALESCE(icon_value, ''::character varying)::text`, which no longer matches the entity's declared expression, so `migration:check` reports changes on every run. `coalesce(icon_value::text, '')` normalizes to `COALESCE((icon_value)::text, ''::text)` — identical for text, varchar, and jsonb alike. Symptom: only *some* tables drift (the varchar ones), which is the tell.

**2. A function the schema depends on must exist before the schema is built, and there are two build paths.**
- `bin/seed-fresh.ts` runs extensions → migrations → functions, so the migration adding the column must carry its own `CREATE OR REPLACE FUNCTION` copy (canonical copy still lives in `objects/functions/`).
- `src/test-utils/setup-db.ts` builds the schema from entities via `orm.schema.refresh()`, so `functions` had to be hoisted into its pre-schema phase alongside `extensions` (safe: every function file is CREATE OR REPLACE, and all the pre-existing ones are plpgsql, whose bodies aren't parsed at creation). Without this, every DB-backed spec dies with `42883 function does not exist`.

Verified behaviours: `CREATE OR REPLACE` of the function succeeds while a generated column depends on it (so repeated `db:objects` is fine), `DROP FUNCTION` is blocked by the dependency, and the column recomputes on every UPDATE. Replacing the function does NOT recompute existing rows — a pattern change needs a migration that touches the rows.

Generating a clean migration: build a replica with extensions + committed migrations + **functions only** (NOT `tables` — `objects/tables/` creates `ably_realtime_nodes`, which MikroORM then bakes into the snapshot and pollutes the diff), generate against `DB_NAME=axis_migr`, confirm `diff` vs `.snapshot-axis.json` shows only your changes, then copy `.snapshot-axis_migr.json` over `.snapshot-axis.json` (the snapshot has no db-name field, so it's a safe promote). See [[project_mikroorm_snapshot_local_drift]] and [[project_migration_drift_entity_checks]].
