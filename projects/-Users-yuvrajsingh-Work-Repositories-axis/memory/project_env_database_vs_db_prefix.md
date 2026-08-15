---
name: env-database-vs-db-prefix
description: "RESOLVED 2026-08-08: .env.production now sets DB_* (was DATABASE_*), so `APP_ENV=production` + op run IS the way to run a bin script against production. 1Password is authoritative; Railway's DB_* are dead."
metadata: 
  node_type: memory
  type: project
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-15T07:29:02.932Z
---

**READ THE RESOLUTION BELOW BEFORE ACTING ON THIS.** The headline hazard was fixed on 2026-08-08 and the fix is verified still in place as of 2026-08-15 (`grep -c '^DATABASE_' apps/backend/.env.production` → 0; `DB_HOST`/`DB_PORT`/`DB_USER`/`DB_PASSWORD`/`DB_NAME` are lines 8-12). Quoting the original hazard as current guidance cost a wasted debugging round on 2026-08-15, where `railway run` was recommended over `op run` on the belief that `.env.production` had no `DB_*`. It does.

**Original hazard (HISTORICAL):** `APP_ENV=production pnpm --filter backend <bin script>` ran against your LOCAL dev database while injecting real production buckets/credentials. Discovered 2026-08-08 when a "production" artifact bake wrote dev KB content into the production R2 bucket.

Mechanism: `apps/backend/.env.production` defines `DATABASE_HOST/PORT/USER/PASSWORD/NAME` (→ `op://Axis Production/Database/*`), but the app reads **`DB_HOST/PORT/USER/PASSWORD/NAME`** (`configuration.ts:79`, `mikro-orm.config.ts`, `outbox-listener.service.ts`). So `DATABASE_*` is **dead config, read by nothing**. `op run` only overrides a parent env var when that key is present in the file, so `DB_*` falls through to `_load-env-local.js` → `.env.local` → `postgres.axis.orb.local`. Everything else (buckets, OpenSearch host) IS production.

`.env.staging` has neither `DATABASE_*` nor `DB_*`.

**Why production still works:** the deployed app runs `op run --env-file=./.env.${APP_ENV:-production} -- node dist/main` (backend `package.json` `start`), and **Railway injects `DB_*` directly**. Since `.env.production` never mentions `DB_*`, `op run` doesn't clobber it.

**RESOLVED for production 2026-08-08**: verified `op://Axis Production/Database/*` matches Railway's `DB_*` exactly (`us-east-1.pg.psdb.cloud` / `6432` / `axis-production` / `pscale_api_…`), then renamed `DATABASE_*` → `DB_*` in `.env.production` and added a literal `DB_SSL_ENABLED=true` (Railway had it; without it a local run inherits `.env.local`'s `false` and PlanetScale refuses the connection). Port **6432 is PlanetScale's pooled/PgBouncer endpoint**, not direct 5432 — worth remembering before anyone moves the outbox `LISTEN` connection.

**Consequence: 1Password is now authoritative for production DB config and Railway's `DB_*` are dead** (op run overrides them). Rotating the PlanetScale password in Railway alone would silently break production — rotate in 1Password, and preferably delete `DB_*` from Railway to keep one source.

**`.env.staging` deliberately has NO `DB_*`** — confirmed 2026-08-08 that the **"Axis Staging" vault has no `Database` item at all** (`op read op://Axis Staging/Database/host` → "isn't an item in the vault"). Adding refs would break the staging deploy, because `start` runs through `op run` and one missing ref fails the whole file — exactly how the missing `Axis Staging/Hookdeck` item already breaks every local staging `op run`. Railway supplies staging's `DB_*`. To make local staging scripts work, someone must first create a `Database` item in that vault (host/port/user/password/name from Railway staging) plus the missing `Hookdeck` item; a comment in `.env.staging` records this.

**Guard added:** `apps/backend/bin/_env-target.ts` → `assertEnvTarget()` prints APP_ENV + db host/name + bucket and throws when `APP_ENV` is production/staging while `DB_HOST` is local. Called from `bin/kb-artifact-bake.ts`; other bin scripts should adopt it.

**Correct way to run a bin script against a deployed env** (already the documented pattern in `bin/kb-asset-migrate-r2.ts`): `railway run --service api -- op run --env-file=./.env.production -- pnpm run esm ./bin/<script>.ts`. Related: [[run-app-context-bin-without-op]], [[kb-artifact-bake-pipeline]].
