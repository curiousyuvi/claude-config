---
name: feedback_never_delete_applied_migration
description: Revert a migration BEFORE regenerating it — deleting an applied migration file leaves the DB unrecoverable by the migrator
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1e927e1c-86e1-4d35-94a1-f2ea8187e4d2
  modified: 2026-07-30T19:31:17.862Z
---

When regenerating a migration that has already been applied anywhere (including a local dev DB), run `migration:down` FIRST, then delete the file and regenerate.

**Why:** MikroORM builds its migration list from files on disk. If the file is gone but `mikro_orm_migrations` still records it, `migration:down` silently reverts nothing and still prints "Successfully migrated down to previous version" — a false success. The next `migration:up` then fails with `42P07 relation ... already exists`, and the DB is stuck in a state the migrator cannot reach from either direction.

**How to apply:** if it has already happened, repair by hand — drop exactly what the deleted migration's `up()` created, then `DELETE FROM mikro_orm_migrations WHERE name = '<deleted migration>'`, then `migration:up`. `ALTER TABLE ... DROP COLUMN IF EXISTS` takes dependent indexes with it, so generated columns + their GIN indexes come out in one statement each. Verify afterwards against `information_schema.columns` / `pg_indexes` / `pg_proc` rather than trusting the migrator's output.

Also worth checking before assuming the worst: `migration:down` with a missing file may instead run the down() of the *previous* migration. Diff `mikro_orm_migrations` against the files on disk and inspect whatever that previous migration touches before concluding nothing else moved.

See [[project_generated_column_drift_and_ordering]] for the replica-rebuild recipe that regeneration needs anyway.
