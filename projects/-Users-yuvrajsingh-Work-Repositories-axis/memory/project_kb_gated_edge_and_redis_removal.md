---
name: kb-gated-edge-and-redis-removal
description: "Slices 5+6 of KB caching — gated KBs served from edge artifacts, Redis deleted from published-KB path except host resolution (LOCKED plan 2026-08-08)"
metadata: 
  node_type: memory
  type: project
  originSessionId: ea441c8c-9d1f-4fc1-9ef3-73ac33678184
  modified: 2026-08-08T11:18:31.836Z
---

Decided with Yuvraj 2026-08-08, spec written into `KB-CACHING-IMPLEMENTATION-HANDOFF.md` (Slices 5 and 6). Builds on [[kb-artifact-bake-pipeline]] / [[kb-published-r2-worker-caching]]. PR #1083 is the prerequisite and merges first.

**Access modes are EXCLUSIVE (added 2026-08-08, implemented in commit f3529816c on `ys/feat/kb-edge-gated`).** A KB is public, password, OR members-only — never two. Was independent booleans that could stack (entity comment even said "independent and stackable"); stacking demanded two credentials since middleware runs password then member. Enforced 4x: `kb_access_gates_one_access_mode` CHECK, service setters clearing the other mode in-transaction, `KbAccessModeArtifact` discriminated union in the artifact contract, single Select in Share dialog. **IP allow-list is NOT a mode and still stacks.** Migration backfill drops the password (not require_auth) for rows with both — clearing require_auth would widen access to anyone holding the password.

**Slice 5 — gated KBs at the edge.** One serving architecture; `origin:gated` dies. Gate split by what each gate needs: IP allowlist + password (`kb_pw` cookie vs non-secret `passwordToken`, constant-time) are pure computation in the Worker from a v2 host artifact `gate` object; member gate = HMAC verify at edge (`KB_AUTH_SECRET` becomes a Worker secret) + a backend recheck `GET /_kb/member-recheck?sub=` (EDGE_SECRET-authed, runs BEFORE origin gates) cached in `caches.default` 300s per (kbId, sub) per colo — Yuvraj's "worker calls backend" idea bounded to the one gate that needs the DB. Worker never renders prompts/sets cookies/rate-limits; any gate failure = `toOrigin('gate-ip'|'gate-password'|'gate-member')` and origin owns every deny byte. Strip Cookie/Authorization before the loopback call. Key ordering fix: **host artifact written FIRST in buildArtifacts** (was last — a public→private flip left the edge ungated for the whole bake). Settings artifact gets `Cache-Control: private` when restricted. Version bump means v1 artifacts read as host-unknown until rebake; no dual-format code. Parity fixes folded in: trailing-slash 308 at edge, IGNORED_QUERY_PARAMS stripped before loopback (cache-key fragmentation). `ipMatchesAllowlist` moves to packages/shared.

**Slice 6 — Redis removal (AFTER slice 5 + route cutover, or gated pages become per-request DB renders).** Delete `KbReaderCacheService` (also deletes suspected cause of flapping bake counts), `KbNodeMetaCacheService`, the member `getOrSet` in kb-reader-gate.handler (direct DB call). `invalidationTags()` shrinks to host-resolution tags. KEEP: host resolver + custom host registry on Redis (Yuvraj's explicit call), and `bumpRateLimit` on unlock/callback (rate limiting is not caching; argon2 DoS guard — flagged, keep unless told otherwise). Delete `kb-reader-jsx-classic.tsx` if dead.

**Revocation contract**: gate-config changes land in seconds (KB_UPDATED → scope Kb rebake, host-first). Member revocation bounded by 300s recheck TTL per colo (today's Redis TTL, minus tag-bust immediacy — accepted). Cookie TTLs unchanged. Denied-at-edge self-heals via origin's direct DB check; stale-allow bounded by TTL.

**Full Redis touchpoint sweep done 2026-08-08** (all TagCacheService consumers + every kb-cache-tags helper) — inventory is in the handoff doc and is complete. Notables beyond kb-public: `membership-events.service.ts:91` + `better-auth/organization-hooks.ts:69` bust `kbMemberOrgTag` (die with the member cache); `kb-node-seo.service` needs no change (outbox events, not direct busts); **`bin/_kb-move-steps.ts` is a live gap since slice 2** — kb:move-org busts Redis tags but never rebakes artifacts, so a moved KB serves pre-move artifacts until an unrelated publish. Fix: bakeKb + edge purge in the script. `kb-cache-tags.ts` shrinks to `kbTag` alone; kb-edge should import it for its Cache-Tag header.

Watch after: `X-Kb-Edge` reason distribution; if `?embed=1` (ticket KB panel) shows real volume, bake embed variants — do not resurrect the cache.
