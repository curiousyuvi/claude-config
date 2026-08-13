---
name: project-run-app-context-bin-without-op
description: "Env vars needed to boot any AppModule bin script locally when `op` isn't signed in (kb:move-org, kb:asset-gc, graph-rag:*)"
metadata: 
  node_type: memory
  type: project
  originSessionId: cf4559da-6d1d-4711-9be5-10ce3c24b1ea
  modified: 2026-08-04T09:39:54.015Z
---

`op run` fails for me non-interactively (`error initializing client: You are not currently signed in`), so
`pnpm --filter backend <script>` won't work for anything that boots the Nest app context. Run the script
directly through the esm runner with the env supplied by hand — DI validates config at construction, so it
fails one missing var at a time:

```
DB_HOST=localhost DB_PORT=5432 DB_USER=username DB_PASSWORD=password DB_NAME=axis \
APP_ROLE=console MAIL_FROM=dev@example.com BUCKET_ENDPOINT=http://localhost:9000 \
AI_DIGESTION_BUCKET_NAME=axis-ai SESSION_SECRET=0123456789abcdef0123456789abcdef \
pnpm run esm ./bin/<script>.ts <args>
```

(run from `apps/backend`; `bin/query.ts` needs only the `DB_*` five since it uses `pg` directly, not DI.)

Two gotchas found the hard way:

- `falkordb` (a declared dependency) was missing from node_modules, so EVERY app-context script died with
  `Cannot find module 'falkordb'` and `pnpm typecheck` showed 5 errors in `src/ai/store/graph-rag/*`. Fixed by
  `pnpm install --frozen-lockfile` at the root — the local install was just stale. If those graph-rag typecheck
  errors reappear, that is the cause, not the branch.
- A scratchpad script that imports `pg` must live inside `apps/backend` (pnpm won't resolve workspace deps for
  a file under /tmp). Write it to `apps/backend/.something.ts`, run it, delete it.

Dev DB state as of 2026-08-04: db `axis` has ONE org (`00000000-0000-7000-8000-000000000001`) and 5 KBs, the
biggest being `convious` (177 articles, 25 comments) and `instantdocs` (159). Anything needing a second org has
to create one; `organizations` rows stand alone, so insert + delete is a clean round trip.

Related: [[project-run-axis-ci-locally]]
