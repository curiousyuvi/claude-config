---
name: axis-local-dev-control
description: "The user wants Claude to stop, start and restart the Axis local dev server itself, end to end, and how that is set up on this machine"
metadata:
  node_type: memory
  type: user
  originSessionId: a300d626-ed21-434c-8d87-057134e35e90
  modified: 2026-11-15T10:58:09.964Z
---

The user wants Claude to run Axis local dev by itself (stop, start, restart, read logs) rather than hand them commands. Asked 2026-11-15; applies to all future Axis work. Keep it personal: nothing about this goes into the Axis repo or its committed docs.

Setup on this machine:
- `op run` works from Claude's shell only through a 1Password service account token in the GLOBAL mise config `~/.config/mise/config.toml` `[env] OP_SERVICE_ACCOUNT_TOKEN` (read-only, Axis Dev vault). Check with `mise env | grep -c OP_SERVICE_ACCOUNT_TOKEN` (count only, never print the value). Without it, fall back to giving the user commands per [[no-op-signin-from-claude]] in CLAUDE.local.md.
- Stop: `pkill -f "start:dev:portless"` then `pnpm portless:proxy:stop` (the pkill pattern leaves evals in ~/Work/Repositories/axis and InstantDocs on :3000 alone).
- Start: `mise dev` from the repo root, in the Terminal panel via `mcp__terminal__run_in_terminal` so the user can watch and Claude can read logs; if `mise dev` fails on its GitNexus step, `pnpm dev`. App at https://inbox.helply.localhost.
- Local Postgres/Redis are Docker containers `axis-postgres` / `axis-redis`; Claude's sandboxed shell can't reach postgres.axis.orb.local, so query through `docker exec` (needs the sandbox off). Local traces: Jaeger at localhost:16686. The Terminal panel only keeps recent output and the dev log is noisy with SQL lines, so grep it.
- Permission allow rules for these commands belong in the repo's `.claude/settings.local.json` (the whole `.claude/` dir is gitignored). Claude may not add them itself; the user adds them.

**Why:** the user does not want to run these commands manually, and wants the setup reusable across Axis tasks.
**How to apply:** for any Axis task needing a local server restart or local verification, do it directly with the steps above.
