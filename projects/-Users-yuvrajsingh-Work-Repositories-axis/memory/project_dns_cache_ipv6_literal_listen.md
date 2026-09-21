---
name: dns-cache-ipv6-literal-listen
description: Backend dns-cache (cacheable-lookup) made server.listen on ::1/:: fail with EBADNAME; only reproducible with the OTel/instrumentation preload, so standalone probes pass while the app fails
metadata:
  type: project
---

`apps/backend/src/instrumentation.ts` calls `installDnsCache()` which replaces `dns.lookup` with cacheable-lookup.
Node routes IP literals through `dns.lookup` on `server.listen({host})`/`net.connect`; cacheable-lookup queried
`::1`/`::` as names and returned EBADNAME. Remotion's port probe (hosts `::1, 127.0.0.1, ::, 0.0.0.0`) then failed with
"No available ports found" (fixed 2026-09-21: literals bypass the cache via `net.isIP`).

**Why:** cost half a day: renders worked from `pnpm run esm` probes (no instrumentation preload) and failed only in the
running backend.
**How to apply:** when something network-y works in a script but not in the app, reproduce with the dev flags exactly:
`node --env-file=.env.local --experimental-strip-types --import ./dist/instrumentation.js dist/<probe>.mjs` (note
`nest build` wipes dist, so write the probe after building). See [[recorder-snapshots-plan]].
