---
name: project_local_snapshot_render_needs_public_bucket
description: "Local snapshot rendering needs recordings in a real bucket, not MinIO; a tunnel does not work"
metadata: 
  node_type: memory
  type: project
  originSessionId: b7d2c0f1-ac56-45e0-92bf-90c42f034c37
  modified: 2026-09-23T15:38:34.316Z
---

Lambda fetches the recording over a presigned URL, so local snapshot rendering cannot use MinIO on
`localhost:9000`. Set the four `RECORDINGS_BUCKET_*` vars in `apps/backend/.env.local` to point
recordings at a real R2 bucket (there is no Dev recordings bucket, so the staging one is the
practical choice: `op://Axis Staging/cloudflare/KB Recordings/*`, bucket `helply-recordings-staging`).
`apps/backend/.env` carries the commented block. Leave them unset and everything except snapshot
rendering behaves as before, because `createDedicatedBucketClient` falls back to the main bucket.

**Do not try to tunnel MinIO.** ngrok fails because the S3 client addresses the bucket
virtual-hosted style (`<bucket>.<host>`), and ngrok's single-level wildcard cert does not cover that
sub-subdomain: `ERR_TLS_CERT_ALTNAME_INVALID`. Setting `BUCKET_ENDPOINT` to the tunnel also breaks
ordinary attachment uploads.

`op://` refs in `.env.local` are **not** resolved: `apps/backend/package.json` runs
`op run --env-file=./.env` only, and `.env.local` is read directly by ConfigModule afterwards. Put
literal values there (it is gitignored, and already holds literal minio creds).

Separately, `op run` can fail with "could not find item" from a stale 1Password CLI cache;
`OP_CACHE=false mise dev` works.

See [[project_remotion_lambda_sizing]].
