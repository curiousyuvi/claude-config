---
name: project_snapshot_render_lambda_migration
description: "Moving KB snapshot rendering off our pods to Remotion Lambda in the Groove AWS account — accounts, who owns what, plain-English Terraform notes, and what is left to do."
metadata: 
  node_type: memory
  type: project
  originSessionId: b7d2c0f1-ac56-45e0-92bf-90c42f034c37
  modified: 2026-09-22T13:18:49.004Z
---

Snapshot rendering is moving from "Chrome runs inside our backend pods" to AWS Lambda, the same way instantdocs does it. Started 2026-09-22.

**Why:** Jared found `POST /api/recorder/recordings/:id/snapshots/render` taking 18.2s as a plain HTTP request. Rendering on our pods also caused three production problems in two days: missing Chrome system libraries, replicas crashing because the boot warm-up starved the healthcheck, and Remotion's download progress printer flooding past Railway's 500 logs/sec limit. Lambda removes Chrome from our images entirely and scales sideways. Per-render cost is a wash (pods are ~2x cheaper per render, both are cents per thousand); the win is no idle capacity and no blast radius on the API.

**How to apply:** the queue comes first and is needed either way, because the editor waits for the rendered URL to write into its Plate node. `KbSnapshotRenderService.render()` is the seam: it takes a config plus a video URL and returns `{assetId, url, naturalWidth, naturalHeight}`. Lambda is a second implementation behind that method, not a rewrite.

## Two AWS accounts, do not mix them

- **786844223641** is instantdocs. It is the `default` profile on this machine. Never create anything there for axis.
- **147889171041** is Groove, where this work goes. Use `AWS_PROFILE=groove`, SSO via `https://groove.awsapps.com/start`, region us-east-1. Log in with `aws sso login --profile groove` (browser, so run it yourself).
- Your access there is `PowerUserAccess`, which can do almost everything **except** IAM. So you cannot create the role or the user, and cannot create a Lambda function either (attaching a role needs `iam:PassRole`, an IAM action). Jared or another admin applies that part once.
- Lambda concurrency in that account is the default 1000, shared with `axis-runner-*`, `graphql-gateway-*` and friends. The quota increase you remembered was on the instantdocs account. Cap our function's reserved concurrency so a render burst cannot throttle production.

## Terraform, in plain terms

The repo is `GrooveHQ/infrastructure`, cloned at `~/Work/Repositories/infrastructure`.

- Terraform is a text description of cloud resources. You write `.tf` files, it figures out the API calls. It only manages resources it created, tracked in a **state** file (here, S3 bucket `groove-147889171041-terraform-state`). Anything created outside Terraform is invisible to it, so hand-made and Terraform-made resources coexist fine.
- **Workspaces are environments.** This repo has `groove-production` and `groove-staging`, both in the *same* AWS account. `terraform.workspace` is the current one, and most resources are named `${terraform.workspace}-thing` so the two don't collide.
- Terraform runs **inside their Docker container**, not on your Mac: `make build` then `make console`. `make console` is gated on a `secrets/` directory existing at the repo root; it is gitignored and empty is fine (`mkdir -p secrets`).
- `terraform fmt` is the formatter, `terraform validate` is the syntax and type check. Validate offline fails on `rds/chat` because it wants `rules-default.json` for the `default` workspace. That error is pre-existing and not yours.

## Who owns what

- **Terraform owns the IAM pieces**, because they are static and account-sensitive: the policy, the execution role, one render user per workspace, and its access keys (their existing modules already put keys in state and in `src/iam/sensative-outputs.tf`, so we follow that).
- **The Remotion CLI owns the function and the site bundles**, because they are versioned artifacts. The function name encodes the Remotion version, so upgrading Remotion means deploying a new function, and the CLI handles that lifecycle. Terraform would fight it.
- Remotion has **no official Terraform guide**. Its IaC examples are AWS CDK and the Serverless Framework. The policies come out of the CLI as JSON (`npx remotion lambda policies role|user`), which drops straight into Terraform.

## Current state, 2026-09-23 evening

**Everything the Remotion CLI created is deleted** (bucket `remotionlambda-useast1-1h87biwva3`, function, log groups; all regions checked clean). Jared raised compliance findings (public bucket, no TLS enforcement, no lifecycle) and said all changes must go through Terraform; Matt Beedle owns `GrooveHQ/infrastructure` and applies by hand (no CI). Only the PR #158 IAM pieces remain (role + two render users, applied).

**Kill switch is live in prod** (axis #1499, commit `aff1aa4a1`): `REMOTION_LAMBDA_FUNCTION_NAME` is commented out in all three backend env files, so the renderer refuses before any AWS call. Needed because every render and `sites create` calls `getOrCreateBucket`, which would recreate a public bucket while the render user still has `s3:CreateBucket`. `op run --env-file` beats Railway variables, so the switch had to be a commit, not a Railway var. Restore the key with the new function name after the Terraform apply.

**Terraform rebuild is DONE (infrastructure#160 merged and applied by Matt, 2026-09-24).** Root `remotion/` owns bucket `remotionlambda-useast1-axis`, function `remotion-render-4-0-526-mem10240mb-disk10240mb-900sec`, log group, concurrency 100, zip committed under `remotion/lambda/`. Render user trimmed to invoke + object read/write. Verified live: nodejs24.x, cap 100, only `sites/*` public, plain HTTP 403, `renders/` expires after 1 day. Run Terraform via `docker run --rm --env-file <creds> -v $PWD:/infrastructure groove/infrastructure:1.3.0` (write `aws configure export-credentials --profile groove --format env` to a file; `eval` is blocked in my shell). Matt: bumping the main root's provider would tear down production EKS, so separate roots are the rule for anything needing a newer provider.

**Axis follow-up is PR #1507 (open 2026-09-24):** `presignUrl` download, env keys restored (kill switch lifted), serve URL on the new bucket, `deploy:site --privacy=no-acl`. All three sites redeployed with `AWS_PROFILE=remotion-production REMOTION_SITE_NAME=<site> pnpm run deploy:site` from `packages/snapshot-composition`. Local end-to-end test passed: 5 stills + the first ever GIF render (4 chunks), 25 invocations, 0 errors, peak 1968 MB. After merge: ping Jared to re-check compliance. Replication deferred (Jared said "enable for now"); would need versioning + a replica bucket + role, all in the `remotion/` root.

**Agreed plan (user decisions):** sites stay public via a bucket policy scoped to `sites/*` (Remotion requires a public URL for the headless browser); `renders/` private, backend switches to `presignUrl` from `@remotion/lambda-client`; TLS deny on `aws:SecureTransport`; lifecycle expires `renders/` after 1 day; no replication for now; concurrency cap 100 via `reserved_concurrent_executions`; function zip (`remotionlambda-arm64.zip` from the npm package, byte-identical to what the CLI deploys) uploaded to S3 under `lambda/` and referenced by key; sites stay CLI-owned (`sites create --privacy no-acl`); render user loses create/delete perms. Terraform can name the bucket anything starting with `remotionlambda-`; Remotion finds it by prefix.
