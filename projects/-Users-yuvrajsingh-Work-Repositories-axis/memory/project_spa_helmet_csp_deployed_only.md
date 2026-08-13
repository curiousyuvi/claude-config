---
name: project-spa-helmet-csp-deployed-only
description: "Deployed-only \"asset renders broken but its URL works in a tab\" = a missing directive in the SPA's helmet CSP (app.middleware.ts); local Vite sends no CSP at all"
metadata: 
  node_type: memory
  type: project
  originSessionId: f591ca5d-fa21-4296-8dd1-14eceb2e4c43
  modified: 2026-08-06T11:02:37.100Z
---

The SPA's Content-Security-Policy is the `@fastify/helmet` block in
`apps/backend/src/app.middleware.ts`, and it **governs the app/editor document in deployed envs**
because production serves the Vite build from `apps/backend/public` via `ServeStaticModule`
(`apps/web/vite.config.ts` outDir points there; `apps/web/railway.toml`'s `staticDirectory = "dist"`
is dead config). Locally the Vite dev server serves `index.html` with **no CSP header**, so the whole
policy is invisible in dev. `useDefaults` is on, so the served header is the explicit directives plus
helmet's own (`base-uri`, `form-action`, `frame-ancestors`, `object-src`, `script-src-attr`,
`upgrade-insecure-requests`).

**Why:** this produces a recurring bug class whose symptoms mislead. An asset type with no directive
of its own inherits `default-src 'self'` and is refused, so it renders broken in the app while the
same URL plays/loads perfectly pasted into a tab (CSP does not police top-level navigation) and works
in the published KB (the reader sets its own wider per-response policy in
`kb-public/interfaces/reader-http.util.ts`) and works locally (no header). It has now happened THREE
times: commit `d19e2f3ba` added storage origins to `img-src` for attachment image previews, `media-src`
was missing entirely until video/audio blocks were reported broken in prod, and PR #1051 had to add the
new KB asset bucket after the R2 CDN migration (#1043) shipped.

**THE #1051 CASE IS THE ONE TO GENERALISE: adding a NEW BUCKET is a CSP change.** `getStorageCspSources`
derived its list from `BUCKET_ENDPOINT`/`BUCKET_NAME` alone, so a second bucket was invisible to it, and
that list feeds BOTH `imgSrc` AND `connectSrc`. Two distinct symptoms from one omission: KB icons and
homepage card covers rendered blank (img-src, via the `/api/kb-assets/:id` 302), and KB logo UPLOADS
failed (connect-src, because the browser PUTs straight to the presigned bucket URL). Uploads breaking
looks like a signing/CORS bug and is not. It now also allow-lists `KB_ASSET_CDN_BASE_URL`'s origin,
needed because the pre-publish preview renders through `KbPageRenderer` (so it emits rewritten CDN URLs)
while served from the app origin under this policy.

**Verification lesson:** the R2 work was verified thoroughly against the bucket, the CDN and the
published reader, and still shipped this, because nothing exercised *the dashboard rendering a KB asset*.
Any storage/URL change needs one check from inside the authed app, not only from the public side.

**How to apply:** when a UI asset is broken *only* in a deployed env, diff the directive list in
`app.middleware.ts` against the asset kind before suspecting URLs, signing, expiry, CORS or
Content-Type. Uploaded KB assets are fetched from `{apiBase}/api/kb-assets/{id}`, which **302s to a
presigned bucket URL** — CSP re-checks redirect targets, so allow-listing only the app origin is not
enough. Note media node URLs have three provenances (upload, paste-a-link/"Insert via URL" verbatim
from any host, and the InstantDocs importer), so host-narrow policies break the linked ones. Staging
resolves `BETTER_AUTH_URL` and `FRONTEND_URL` from separate vault items, so the API origin is not
necessarily `'self'` there. Related: [[project_kb_youtube_error153_referrer]],
[[project_kb_reader_serves_stored_html]], [[project_kb_import_instantdocs_contract]].
