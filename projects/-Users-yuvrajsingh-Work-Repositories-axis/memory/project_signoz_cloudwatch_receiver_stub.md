---
name: project_signoz_cloudwatch_receiver_stub
description: "The SigNoz collector cannot read CloudWatch metrics; its awscloudwatchmetrics receiver is a no-op stub. CloudWatch is polled by a separate otel-contrib service, with an AWS/Usage heartbeat. And \"boots clean\" is not \"emits\"."
metadata:
  node_type: memory
  type: project
  originSessionId: 37833cef-2ea3-4a31-935a-0974e560e82c
  modified: 2026-09-29T05:56:58.506Z
---

`signoz/signoz-otel-collector:v0.144.x` (newest is v0.144.12, tracks contrib v0.144) bundles
`awscloudwatchmetricsreceiver` **v0.133.0**, a 67-line stub whose `startPolling` is a `select` on the
shutdown channels. It validates, boots, reports healthy and never calls CloudWatch. Its
`awscloudwatchreceiver` v0.144.0 is logs-only; metrics (`metrics.queries`) start at **v0.153.0**.
Verified 2026-09-29 by grepping the binary for `receiver/awscloudwatch...receiver\tv` and reading the
tagged source. Caught by Jared's review on axis #1522 (P1), after I had shipped the stub.

**Why:** I verified the receiver loaded and the process stayed up, never that it emitted, because I had no
AWS credentials. A clean boot proved nothing.

**How to apply:**
- CloudWatch is read by `ops/signoz/cloudwatch/` (`signoz-cloudwatch` on Railway): stock
  `otel/opentelemetry-collector-contrib:0.153.0`, one `awscloudwatch` receiver, `otlphttp` to
  `signoz-ingester.railway.internal:4318`. `verify.sh` fails if `awscloudwatchmetrics` returns to the ingester.
- To prove a receiver actually polls without real creds: run it with `AWS_ACCESS_KEY_ID=AKIA...` fake and look
  for `GetMetricData ... 403 InvalidClientTokenId` on the first tick. A stub cannot produce that line.
- Missing-data alert = heartbeat on `amazonaws.com/AWS/Usage/CallCount{Resource=GetMetricData}`: CloudWatch
  counting the poller's own calls, present iff the feed is alive, idle Lambda or not. Never alert on the Lambda
  series being absent. Metric names arrive as `amazonaws.com/{Namespace}/{MetricName}` with a `stat` attr.
- Live confirmation still pending: needs the Railway service created with the reader keys from infra #163.

See [[project_snapshot_render_lambda_migration]].
