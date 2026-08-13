---
name: project-railway-tigris-bucket-object-acl
description: "Axis buckets are Railway-managed Tigris; object ACLs are accepted+recorded but inert (403) until enabled account-side, and Railway exposes no toggle"
metadata: 
  node_type: memory
  type: project
  originSessionId: c8716b6d-c7d1-4786-8736-b574c08cf999
  modified: 2026-08-05T12:04:46.486Z
---

The object store behind `BUCKET_*` is a **Railway "Buckets" resource** in the `Groove / axis` project
(production: `ai-digestion`, `axis-attachments`; staging: `attachments`, real name
`attachments-o-epfztlg-zm`). Railway provisions these on Tigris. Endpoint `https://t3.storageapi.dev`,
`region: auto`, `urlStyle: virtual-host`.

Inspect with the railway CLI (no MCP needed): `railway link -w Groove -p axis -e <env>`, then
`railway bucket list|info|credentials -b <name> -e <env> --json`. The credentials JSON is
`accessKeyId / secretAccessKey / bucketName / endpoint / region / urlStyle`.

**Measured 2026-08-05 against BOTH staging and production (`axis-attachments-9mdl1ys9`) — identical
results, so this is per-bucket-setting-off, not a staging quirk:**
- `PutObject --acl public-read` → **accepted**, no error
- `PutObjectAcl --acl public-read` → **accepted**, no error
- `GetObjectAcl` → shows the `AllUsers: READ` grant as recorded
- anonymous GET → **403 on all six** hostname forms (`{bucket}.` / path style, across
  `t3.storageapi.dev`, `t3.storage.dev`, `fly.storage.tigris.dev`)
- `Cache-Control` written at upload DOES round-trip (`head-object` returns it verbatim)
- `GetBucketAcl` → **AccessDenied**: the Railway-issued keys sit below bucket ownership, so bucket-level
  settings can be neither read nor changed with them

Two consequences for [[project_kb_asset_cdn_unsigned_urls]]: deploying the ACL code is **safe** (uploads
will not break, contradicting the worry that S3-style `AccessControlListNotSupported` would 500 the
confirm), and step 1 of the enable order fails **silently** — a clean `kb:asset-publish-acl` run proves
nothing. The only proof is `curl -w '%{http_code}'` on an asset URL returning 200. Enabling "Allow Object
ACL" is Railway/Tigris account-level work; `railway bucket` exposes no ACL toggle and no public domain,
so a public CDN base may require a Tigris bucket provisioned outside Railway.

Also measured on a real production asset: existing objects have NO `Cache-Control` and no `AllUsers`
grant, and staging has **zero** `kb-assets/` objects, so staging cannot rehearse the rollout.
