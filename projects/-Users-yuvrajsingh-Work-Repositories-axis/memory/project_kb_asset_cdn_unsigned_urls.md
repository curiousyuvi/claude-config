---
name: project-kb-asset-cdn-unsigned-urls
description: "Published-KB asset CDN = own public Tigris bucket + unsigned immutable URLs rewritten at render; Intercom's signature params are provably unenforced"
metadata: 
  node_type: memory
  type: project
  originSessionId: 77ab6d5a-7d22-4f52-8ed4-702edb51c357
  modified: 2026-08-06T06:30:44.930Z
---

Built 2026-08-04/05 on `ys/feat/kb-asset-cdn`. `KB_ASSET_CDN_BASE_URL` makes `KbPageRenderer` rewrite
`{apiOrigin}/api/kb-assets/{id}` to `{cdnBase}/kb-assets/{id}` (`rewriteKbAssetUrls`), and
`KB_ASSET_BUCKET_NAME` puts KB media in its own public-read bucket.

**The object store is Tigris, not R2** (`BUCKET_ENDPOINT` = `https://t3.storageapi.dev`; `region:'auto'`
plus the R2 mention in `storage.service.ts` misled me at first). Tigris IS the CDN: public objects serve
from its global edge, no egress charge, honouring the `Cache-Control` written WITH the object (else it
defaults public objects to `max-age=3600`). So there is no cache in front to purge — deleting the object
is the invalidation. A Cloudflare `purge_cache` hook was built and then deleted as wrong for this.

**CORRECTION to what I first concluded**: Intercom's help-center HTML carries
`expires`/`signature`/`req` params (15-min bucketed) on `downloads.intercomcdn.com`, and I initially
called that a design worth copying. It is NOT enforced. Measured: same URL returns 200 with the query
stripped, with a long-past `expires`, and with a tampered `expires`; a never-requested bare URL returns
200 `image/png`, 400 KB. Their `Cache-Control` is `max-age=86400, private`. Don't restore signing for
"parity" on the strength of those params.

**Gated KBs get CDN URLs like any other** (user's call, 2026-08-05): media is fetchable by URL, matching
Intercom, where audience targeting gates the article page not the CDN media. Zendesk is stricter (a
restricted article's attachment 404s anonymously — served through their app with a permission check);
reaching that here needs the owning KB id at presign time, which `presign` doesn't receive.

**SAME bucket + per-object ACL, not a separate bucket.** A separate public bucket was built and then
reverted: it forces every asset to MOVE, and between "service points at the new bucket" and "copy
finished" every pre-existing image 404s. An ACL flip moves nothing, so no such window, and the backfill is
a metadata op instead of copying tens of MB per video. Safety comes from deriving public-read from the KEY
(`PUBLIC_READ_PREFIX = 'kb-assets/'` in storage.service.ts) with NO `publicRead` param anywhere, so no
call site can make an attachment public; `setPublicRead` throws outside the prefix. Server-side writes get
the ACL inline; the browser path gets it in `confirm` (after size/type checks, so a rejected upload is
never briefly public).

**Enable order** (wrong order = 403s): enable object ACLs on the bucket (Tigris dashboard, OFF by
default) → deploy → `pnpm --filter backend kb:asset-publish-acl` until clean → only then
`KB_ASSET_CDN_BASE_URL`. Verify first on a throwaway bucket that enabling object ACLs does not change
existing objects' effective access.

**Object ACLs are a HARD dependency of the deploy, not just of the CDN var.** Once deployed, every KB
upload sends `ACL: public-read` on PutObject (`aclFor`) and `confirm` calls `setPublicRead`, with no
try/catch and no fallback. A store that rejects object ACLs (S3 BucketOwnerEnforced returns
`AccessControlListNotSupported`; MinIO is the local-dev question mark) fails the upload outright rather
than degrading. Verify a KB image upload against local MinIO and against Tigris before merging.

**SUPERSEDED 2026-08-05: moving to Cloudflare R2, not Tigris.** Konrad's call — R2 is where the CDN and
future caching work lives. A public R2 bucket needs no per-object ACL, so `PUBLIC_READ_PREFIX`, `aclFor`,
`setPublicRead` and `bin/kb-asset-publish-acl.ts` all get deleted, and the
[[project_railway_tigris_bucket_object_acl]] blocker evaporates. The render-time rewrite
(`rewriteKbAssetUrls`, `KB_ASSET_CDN_BASE_URL`, `resolveKbAssetCdnConfig`) is provider-agnostic and
survives unchanged.

Discovered via the Cloudflare MCP (2026-08-05), account `65e296b71eaf0e794c6e4f90e0f6f27c`
(Sharedservices@groovehq.com):
- buckets `helply-production` and `helply-staging` ALREADY EXIST, reused rather than new ones; our
  content goes under a `kb-assets/` prefix and must never delete anything else there (Konrad's
  condition), so the KB store gets a hard prefix guard on delete
- custom domains are **`cdn.helply.com`** and **`cdn.helplystaging.com`**, both SSL-active — NOT
  `cdn.helplydocs.com`, which was only a suggestion in Slack and would 404 every image
- `r2.dev` managed domains are disabled on both (correct: rate-limited, not for production)
- CORS on both was `*` origins / **GET+HEAD only**, so browser presigned PUTs need an added rule
  (`origins: [https://next.helply.com | https://next.helplystaging.com]`, `methods: [PUT]`,
  `headers: [content-type, cache-control]` — `cache-control` is signed into the URL so the preflight
  must allow it). Read-modify-write, never replace: the bucket is shared.
- 1Password: `Object Storage` item gains `kb_asset_bucket_{endpoint,name,access_key_id,secret_access_key}`
  per vault. Writing R2 config to Cloudflare from Claude Code hits the auto-mode permission classifier.

**MIGRATION DONE 2026-08-06, BEFORE the deploy.** All 1,245 objects / 5.64 GB copied Tigris → R2 by
`bin/kb-asset-migrate-r2.ts` (not rclone — a bin script, so the skip/resume logic is ours), zero failures.
Verified: `https://cdn.helply.com/kb-assets/019f1dea-...` returns 200 with the immutable Cache-Control,
which those objects did NOT have in Tigris, so the copy also repaired the missing TTL. Running the copy
BEFORE merging removes the 404 window entirely; only assets uploaded between the copy and the deploy need
a second run. Source bucket is untouched, so rollback is still one env var.

Gotcha for any future run: the source bucket's `BUCKET_NAME`/`BUCKET_ACCESS_KEY_ID`/`BUCKET_SECRET_ACCESS_KEY`
are **Railway service variables, not in `.env.production`** (which carries only `BUCKET_ENDPOINT`), so the
invocation needs both injectors nested:
`railway run --service api -- op run --env-file=./.env.production -- pnpm run esm ./bin/kb-asset-migrate-r2.ts`

See also [[project_kb_asset_gc_design]], [[project_kb_panel_published_only]], and
[[project_kb_image_layout_shift_dimensions]] (shipped separately on
`ys/fix/kb-content-shift-on-asset-load`).
