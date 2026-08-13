---
name: project_single_logout
description: Single logout (ID ↔ Axis) design + the runtime enablement gotcha
metadata: 
  node_type: memory
  type: project
  originSessionId: 1985cacb-734e-4712-95fa-d406d20ebc72
---

Single logout between instantdocs (ID, NextAuth) and Axis (better-auth OIDC IdP), implemented 2026-06-08. Part of [[project_clerk_idp_migration]].

**Two directions, two transports:**
- **ID→Axis (RP-initiated end-session):** ID captures `account.id_token` into the NextAuth JWT (`token.axisIdToken`). On logout, `axisAwareSignOut()` (`src/helper/logout.ts`) fetches `/api/auth/axis-logout-url` (server reads the id_token via `getToken`), `signOut({redirect:false})`, then navigates to Axis `${AXIS_OIDC_ISSUER}/oauth2/end-session?id_token_hint=…&post_logout_redirect_uri=${base}/login&client_id=…`.
- **Axis→ID (back-channel):** reuses the EXISTING HMAC webhook pipeline — Axis `before` hook on `/sign-out` (`auth-instance.ts` → `enqueueLogoutFanOut`) enqueues a new `user.logged_out` event via `RpWebhooksService`; ID's `/api/axis/webhook` `handleUserLoggedOut` bumps `sessionVersion` (invalidates on next request, ≤60s). No new endpoint/JWKS — deliberately reused the org-webhook channel.

**Runtime enablement gotcha (NOT derivable from code):** the Axis `ba_oauth_clients` row for InstantDocs must have `enableEndSession=true` + the post-logout URL in `postLogoutRedirectUris`. Run `pnpm --filter backend update-oauth-client --client-id <id> --enable-end-session --post-logout-redirect <base>/login`. Critical: better-auth only embeds `sid` in the id_token when `enableEndSession` is already true AT LOGIN TIME (oauth-provider index.mjs line ~378), and `/oauth2/end-session` throws without `sid`. So existing logged-in sessions only single-logout AFTER the user re-logs-in post-flag. No re-registration needed.

**No fan-out loop:** RP-initiated logout hits `/oauth2/end-session` (not `/sign-out`), so it doesn't re-trigger the Axis→ID webhook.

**Two hard-won gotchas in the Axis→ID revocation last-mile (cost the most to find):**
1. Returning `null` from the NextAuth v4 jwt callback does NOT cleanly log out — it crashes the session re-encode (`JWT_SESSION_ERROR: JWT Claims Set MUST be an object`) leaving a half-session (`userId: undefined` → FORBIDDEN storm). Fix: set `token.invalidated = true` (a valid object) and have the `session` callback return null on that flag. `middleware.ts` also checks `token.invalidated` (getToken only decodes the raw cookie, never runs the jwt callback). This also fixes the latent same-bug in the existing member.removed/demotion path.
2. InstantDocs mounts `SessionProvider` with `refetchOnWindowFocus={false}` and no `refetchInterval`, so the client NEVER refetches the session — `useSession()` stays "authenticated" forever even after server revocation. Nothing server-side can drop a stateless-JWT cookie. Fix: `src/components/session-revocation-guard.tsx` (mounted in `(internal-app-layout)`) watches the React Query cache and calls real `signOut({callbackUrl:"/login"})` when a protected query returns UNAUTHORIZED — the only reliable client logout signal.

**Host-first regression + the JWT/session boundary (2026-06-12):** after [[project_dual_mode_workspaces]]'s host-first change, `isHelply`/`loginOrigin` are NO LONGER persisted on the JWT — they're derived from the request host in the `session` callback. The `axis-logout-url` route still gated on `token.isHelply` (read via `getToken`) → always `undefined` → `{url:null}` → ID→Axis logout silently broke again. Fix: gate on `token.axisIdToken` presence (the direct, still-on-the-JWT signal). Hardening to prevent recurrence: `src/server/helper/app-jwt.ts` `getAppToken()` → `AppJwtClaims` (strict type, NO index signature); app-custom-claim consumers (middleware, axis-logout-url) go through it, so reading a session-only field off the token is a COMPILE error. Gotcha: a `declare module "next-auth/jwt"` augmentation does NOT enforce this — NextAuth v4 `JWT extends Record<string, unknown>`, the inherited index signature can't be removed by merging, so `token.isHelply` would still type as `unknown`. The accessor (strict return type) is the only thing that actually catches it. Standard-claim readers (AI routes reading `sub`/`email`) keep using raw `getToken`.

Note: `serverLogger.sendLog` is a no-op (BetterStack body commented out) — `serverLogger.*` prints nothing in dev; use `console` when tracing locally.
