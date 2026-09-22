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

## Current state, 2026-09-22

Branch `ys/feat/remotion-render-user` in `~/Work/Repositories/infrastructure`, not yet pushed. Adds `src/iam/remotion-render-user/` plus four lines in `src/iam/main.tf` and one in `src/iam/sensative-outputs.tf`. `terraform fmt -check` is clean.

Three deliberate choices to mention when Jared reviews:

1. `remotion-lambda-role` has a name Remotion hardcodes, and both workspaces share one account, so it is created only when the workspace is `groove-production` (the same conditional style already used in `src/kms/elasticsearch`). Production must be applied before staging can render.
2. Added `lambda:PutFunctionConcurrency` to Remotion's stock user policy, so we can cap our own share of the shared concurrency pool.
3. Dropped Remotion's `HandleQuotas` statement, which would let a service user raise account quotas. We don't need it in a production account.

Still to do: push the PR, get it applied, collect the two key pairs into 1Password and Railway, then deploy the function and three site bundles (dev, staging, prod) with the render user's keys. Axis has three environments but Terraform only has two workspaces, so dev shares the staging user; separation between them is the site name, which is just a CLI argument.

Related: [[project_recorder_snapshots_plan]]
