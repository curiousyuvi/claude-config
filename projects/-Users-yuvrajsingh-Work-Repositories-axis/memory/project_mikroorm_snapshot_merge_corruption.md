---
name: project_mikroorm_snapshot_merge_corruption
description: Pulling master silently corrupts .snapshot-axis.json (git line-merges adjacent tables); rebuild deterministically as master + your additive tables
metadata: 
  node_type: memory
  type: project
  originSessionId: 54cc5d59-d550-4f7b-9295-f3495adbdfcb
  modified: 2026-08-11T10:34:04.565Z
---

When merging/pulling master into a branch that ADDS entities, git's line-based 3-way merge of `apps/backend/src/database/migrations/.snapshot-axis.json` can auto-resolve **without conflict markers but semantically wrong**: your new table objects insert alphabetically adjacent to an existing table master also edited, so git takes YOUR (stale-base) copy of that neighbor table wholesale and drops master's column change. Seen with the KB-comments branch: `kb_comment*` tables sit right before `kb_custom_domains`, so the merge kept our stale `is_apex` and dropped master's `status_changed_at`.

**Why:** the snapshot is one big JSON blob; a textual merge has no notion of table objects. `entities.generated.ts` line-merges fine (append-only imports), but the snapshot does not.

**Subtractive case (REMOVING a table), learned 2026-08-11 dropping `kb_guests`:** the same "rebuild from master's snapshot" rule applies, mirrored. Restore master's snapshot with `git checkout --`, then parse it in node, `tables.filter((t) => t.name !== '<table>')`, and write back with `JSON.stringify(snapshot, null, 2)` and NO trailing newline (assert the input round-trips byte-identically first, and assert exactly 1 table was removed and no `<table>` substring survives). Result was a 222-line pure deletion, 0 insertions.

**Two traps that cost a full redo that day, both worth checking BEFORE `migration:create`:**
1. **Run `migration:pending` (and `migration:up`) first.** A local DB even 3 migrations behind makes MikroORM diff entities against a stale schema, so *other people's* pending migrations get folded into your `up()` (here: five `contact_notes` columns, six `company_notes` columns, an index swap).
2. **ROOT CAUSE, found 2026-08-11: the local dev DB is missing the `db:objects`-managed objects**, so MikroORM introspects a database that genuinely lacks them and "helpfully" removes them from the snapshot. Measured on a fully-migrated local DB: the regen dropped `triggers` on 14 tables (to `[]`), `checks` on 29, `indexes` on 85, and changed `columns` on 59 (including generated columns like `kb_articles.asset_ids` and `public_id`). That is also exactly why `down()` re-creates trigger functions with empty bodies. **Try `pnpm --filter backend db:objects` on the local DB before trusting any regen**; until then, always patch the snapshot surgically.

   Additive recipe (adding columns/checks, used for the KB privacy slice): keep the regen in a temp file, `git checkout --` the snapshot, then copy ONLY the new column and check objects out of the regen into HEAD's table objects, re-sorting `columns` by key and `checks` by `name` (MikroORM emits both alphabetically and the drift gate is byte-comparing). Assert the target round-trips canonically first, and assert each added name was absent. Result: 66 insertions, 0 deletions. Never copy a whole table object across, and never take a *shared* column from the regen: `kb_articles.asset_ids`/`public_id` differed there purely from local drift.

3. **Regenerating the snapshot corrupts index metadata even on a current DB** — 1222 insertions / 2334 deletions of pure damage: `columnNames` arrays emptied (156x), `composite` true→false (138x), `constraint`/`unique` flags flipped. Presumably local Postgres introspects indexes differently from whatever produced master's file. So NEVER commit a regenerated snapshot; always surgically edit from master's copy.

Also: the generated `down()` re-creates ~20 trigger functions with EMPTY bodies (`begin ; end;`) because MikroORM cannot see bodies owned by `db:objects`. Replaying it would silently gut `tickets_assign_number`, `outbox_events_notify`, the contact primary-email trigger, etc. Delete those stubs from the generated file (AGENTS.md explicitly allows editing a generated migration) and leave a one-line note so nobody "fixes" it by regenerating.

**How to apply:** don't trust a clean (marker-free) snapshot auto-merge. If your branch is purely additive (only NEW tables, 0 views/enums — verify by diffing table `name`s vs master; the file keys tables under `name`, NOT `tableName`), rebuild deterministically WITHOUT a DB: take master's authoritative snapshot, append your new table objects, re-sort tables by `name` (MikroORM canonical order — master is already fully sorted). Serialize with `json.dumps(obj, indent=2, ensure_ascii=False)` and NO trailing newline — that byte-matches MikroORM's `JSON.stringify(x,null,2)` output exactly (verified by round-tripping master's file). Validate: every master table object byte-identical, diff purely additive (0 deletions), your tables present. See [[project_mikroorm_snapshot_local_drift]] (regen path, needs DB) and [[project_kb_comments_architecture]].
