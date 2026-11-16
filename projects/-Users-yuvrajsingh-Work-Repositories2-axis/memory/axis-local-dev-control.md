---
name: axis-local-dev-control
description: "The user wants Claude to stop, start and restart the Axis local dev server itself, end to end, and how that is set up on this machine"
metadata:
  node_type: memory
  type: user
  originSessionId: a300d626-ed21-434c-8d87-057134e35e90
  modified: 2026-11-16T16:49:24.891Z
---

The user wants Claude to run Axis local dev by itself (stop, start, restart, read logs) rather than hand them commands. Asked 2026-11-15; applies to all future Axis work. Keep it personal: nothing about this goes into the Axis repo or its committed docs.

Setup on this machine:
- `op run` works from Claude's own shell through the 1Password desktop app's CLI integration (Settings, Developer, "Integrate with 1Password CLI", turned on 2026-11-15; a service account was not an option). The app must be unlocked; it may ask the user for Touch ID. Check with `op vault list --account groove --format json | jq length` (count only). If it says "not signed in", ask the user to unlock the app or re-enable the integration; otherwise fall back to the user signing in inside the Terminal panel tab and running commands there.
- Stop: `pkill -f "start:dev:portless"` then `pnpm portless:proxy:stop`. The pattern kills the dev server of EVERY checkout: the user also runs one from ~/Work/Repositories/axis (another agent's evals), and both claim inbox.helply.localhost, so only one can run. Check which checkout owns it first (`lsof -a -p <pid> -d cwd`) and ask before killing another checkout's server. Eval scripts and InstantDocs on :3000 are not matched.
- Start: in the Terminal panel via `mcp__terminal__run_in_terminal` (tab title "axis dev") so the user can watch and Claude can read logs. `mise dev` starts the Docker services but then fails its `check-op` step, which runs `op whoami` (that ignores the app integration even though `op run` works), and its GitNexus step also errors on Safe Chain. So run `mise dev` once for the services, then `pnpm dev` in the same tab. Ready when the log shows "Nest application successfully started"; https://inbox.helply.localhost:1355 and https://api.inbox.helply.localhost:1355/health answer 200 (curl needs the sandbox off).
- Proxy port: the setup expects portless on 443 (`apps/backend/.env.local` CORS/trusted origins are `https://inbox.helply.localhost`, no port). On 2026-11-16 a stray proxy was on 1355 and nothing on 443, so the web app called the API without a port and got CORS errors. Workaround without touching files (443 needs sudo): `O="https://inbox.helply.localhost:1355,https://inbox.helply.localhost" CORS_ALLOWED_ORIGINS=$O BETTER_AUTH_TRUSTED_ORIGINS=$O FRONTEND_URL=https://inbox.helply.localhost:1355 BETTER_AUTH_URL=https://api.inbox.helply.localhost:1355 VITE_API_URL=https://api.inbox.helply.localhost:1355 pnpm dev`. `op run` can stall with "authorization timeout" until the user unlocks/approves 1Password.
- Claude has no Helply login for the local web app; to test backend flows without the UI, a temporary untracked `apps/backend/bin/_*.ts` script with `NestFactory.createApplicationContext(AppModule)` (APP_ROLE=console) run via `op run --env-file=./.env -- pnpm -s run esm ./bin/<script>.ts` works. Add `--no-masking` and print only result lines, since masking can hide plain words like `false`. Don't overwrite the local orgs' app connections (Groove, InstantDocs eval).
- The user may need the server free for other agents: stop it when asked, at once.
- Stopping the old processes: plain `kill` (SIGTERM) is ignored by the safe-chain/op wrappers; send SIGINT via `xargs kill -INT`, then `kill -9` what is left (zsh does not word-split `$pids`, so use xargs).
- Local Postgres/Redis are Docker containers `axis-postgres` / `axis-redis`; Claude's sandboxed shell can't reach postgres.axis.orb.local, so query through `docker exec` (needs the sandbox off). Local traces: Jaeger at localhost:16686. The Terminal panel only keeps recent output and the dev log is noisy with SQL lines, so grep it.
- Permission allow rules for these commands belong in the repo's `.claude/settings.local.json` (the whole `.claude/` dir is gitignored). Claude may not add them itself; the user adds them.

**Why:** the user does not want to run these commands manually, and wants the setup reusable across Axis tasks.
**How to apply:** for any Axis task needing a local server restart or local verification, do it directly with the steps above.
