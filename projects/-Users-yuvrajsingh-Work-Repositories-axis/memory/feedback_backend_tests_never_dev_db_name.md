---
name: backend-tests-never-dev-db-name
description: Never run backend vitest with DB_NAME set to the dev database; the test setup DROPs its base DB
metadata:
  type: feedback
---

Backend DB tests (`src/test-utils/test-schema-template.ts`) run `DROP DATABASE <DB_NAME> WITH (FORCE)` and recreate it from a template. Running vitest with `DB_NAME=axis` (e.g. after `source <(grep DB_ .env.local)` for a migration in the same command) wiped the user's dev database twice (2026-11-11 and 2026-11-12: seed data + local GitHub connection lost).

**Why:** the user had to re-seed and reconnect GitHub; data loss in their dev DB.
**How to apply:** for tests export only `DB_USER`/`DB_PASSWORD` (+ `DB_HOST=localhost`), never `DB_NAME` (default is `axis_test`). Run migrations and tests in separate commands. Related: [[run-lint-typecheck]].
