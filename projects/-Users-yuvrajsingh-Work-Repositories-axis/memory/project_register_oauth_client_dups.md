---
name: register-oauth-client CLI creates duplicate ba_oauth_clients rows
description: bin/register-oauth-client.ts always inserts a new row; re-running it leaves stale rows that webhook fan-out still hits, causing 401s from old secrets
type: project
originSessionId: f0eabda4-77f8-4de2-b6ea-29452a988001
---
`apps/backend/bin/register-oauth-client.ts` inserts a fresh `ba_oauth_clients` row every run with no upsert / dedupe by `name`. The webhook fan-out at `apps/backend/src/axis-webhook/axis-webhook.service.ts` (query: `webhookUrl IS NOT NULL`) delivers each event to every matching row. So if a dev re-runs the CLI for the same RP (e.g. to point at a new URL), they end up with two rows and every webhook fires twice — once correctly, once with the orphaned old secret → 401 → BullMQ retries 5× → DLQ.

**Why:** the second run rotates `client_secret` and `webhook_secret`; the RP's `.env` only knows the latest pair, so deliveries to the stale row always fail signature verification.

**How to apply:** When debugging webhook 401s or duplicate deliveries on local dev, check `SELECT name, client_id, webhook_url FROM ba_oauth_clients` for duplicate rows per `name`. Resolution is to delete (or `disabled=true`) the stale row. Future-proofing the CLI with `--update`/`--upsert-by-name` is out of scope but worth flagging if it bites repeatedly.
