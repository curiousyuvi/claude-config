---
name: axis-prod-db-access
description: "How to reach the axis production Postgres from a laptop, and why plain UPDATEs fail there"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 39cb188d-cdf9-4253-8cb0-afeba2bc2e12
  modified: 2026-08-11T12:16:05.823Z
---

Axis production Postgres is **PlanetScale**, not a Railway service — Railway's
`axis` project lists only Redis under Databases. Credentials live in 1Password at
`Axis Production/Database`, referenced by `apps/backend/.env.production`, so
`railway run` is not involved; `op run --env-file=./.env.production` is enough.

The role is `pscale_api_*` with `default_transaction_read_only = on`. Writes fail
with `cannot execute UPDATE in a read-only transaction` until you prepend
`SET default_transaction_read_only = off;` in the same `-c` string. It's a USERSET
GUC, so no elevated grant is needed. `pg_is_in_recovery()` is false — it is the
primary, not a replica.

Reads go through `pnpm query` (`APP_ENV=production pnpm query -q "SELECT ..."`),
which refuses anything but SELECT/SHOW/EXPLAIN/WITH and sets a READ ONLY session.
For writes, `psql` (via `brew install libpq && brew link --force libpq`) with
`PGPASSWORD="$DB_PASSWORD" PGSSLMODE=require`.

Claude's own shell cannot hold the 1Password session — the user runs these in a
separate authenticated terminal and pastes output back. The `!` prefix does not
help, since it shares Claude's unauthenticated shell.
