---
name: project_remotion_lambda_sizing
description: Remotion Lambda at 2048MB kills the compositor on Retina recordings; prod uses the max-spec function
metadata: 
  node_type: memory
  type: project
  originSessionId: b7d2c0f1-ac56-45e0-92bf-90c42f034c37
  modified: 2026-09-23T15:38:03.829Z
---

Snapshot renders run on `remotion-render-4-0-526-mem10240mb-disk10240mb-900sec` in us-east-1
(Groove AWS account 147889171041), deployed 2026-09-23. All three environments share one function;
sites are per-environment (`axis-snapshots-{dev,staging,prod}`).

The default 2048MB/2048MB function **silently kills the Rust compositor** on a 3456x1882 VP9
recording. It surfaces as `Could not extract frame from compositor` with `ECONNRESET`/`ECANCELED`,
plus a generic "disk space is low" hint that Remotion appends to every asset-fetch failure and which
is **boilerplate, not a diagnosis**. Peak usage at 10240MB is ~1540MB, so the ceiling was just above
2048. Lambda scales vCPU with memory, so the bigger function is also faster for roughly the same
GB-seconds on this CPU-bound work.

Read the function's own logs rather than the relayed error, which is usually downstream:

```
aws logs tail /aws/lambda/<function> --follow --profile groove --region us-east-1
```

AWS profiles on this machine: `groove` (SSO, PowerUserAccess, no iam:PassRole),
`remotion-production` / `remotion-staging` (the Terraform-created render users, which DO have
`iam:PassRole` + `lambda:CreateFunction`, so they can deploy functions).

Redeploy a differently-sized function with
`AWS_PROFILE=remotion-production pnpm exec remotion lambda functions deploy --region us-east-1 --memory <mb> --disk <mb> --timeout <s>`
from `packages/snapshot-composition`. Specs are part of the function name, so a new size coexists
with the old one.

See [[project_snapshot_render_lambda_migration]] and [[project_local_snapshot_render_needs_public_bucket]].
