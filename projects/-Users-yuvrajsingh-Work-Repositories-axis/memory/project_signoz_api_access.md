---
name: project_signoz_api_access
description: "How to query production SigNoz from a session (URL, key file convention, the endpoints that work on v0.135.1 and the ones that don't)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 37833cef-2ea3-4a31-935a-0974e560e82c
  modified: 2026-09-30T10:40:11.880Z
---

Production SigNoz: https://signoz-signoz-production-420d.up.railway.app (Railway domain, v0.135.1 ee). Staging: `signoz-signoz-staging-1f88.up.railway.app`.

**Credential:** the user creates a Service Account (Settings > Service Accounts, role Viewer, 1-day expiry) and saves the key with `pbpaste > ~/.config/signoz/api-key` so it never enters chat. Read it with `$(cat ~/.config/signoz/api-key)` into the header, never echo it. The key expires; ask for a fresh one rather than assuming the file is live. "API Keys" no longer exists as a menu item in this version; Service Accounts is the same thing.

**Header:** `SIGNOZ-API-KEY: <key>`. `Authorization: Bearer` returns 401.

**Endpoints that work (Viewer):**
- `GET /api/v3/autocomplete/aggregate_attributes?aggregateOperator=max&dataSource=metrics&searchText=<q>` lists stored metric names + types.
- `POST /api/v4/query_range` with `compositeQuery.queryType=builder`, `panelType=graph`, one builderQuery (`aggregateAttribute.key`, `type`, `timeAggregation`, `spaceAggregation`, `stepInterval`). Returns `data.result[].series[].values[]` of `{timestamp(ms), value}`.
- `GET /api/v1/rules` lists alert rules.
- `GET /api/v1/version` and `/api/v1/health` need no auth.

**Endpoints that don't:** `/api/v1/dashboards` is deprecated (501, use `/api/v2/dashboards`); `/api/v1/metrics` is not an API (returns the SPA); `/api/v1/user` is admin-only.

**Metric name facts:** CloudWatch series arrive verbatim as `amazonaws.com/AWS/Lambda/Errors` etc. and `amazonaws.com/AWS/Usage/CallCount` (all Gauge). OTel histograms are stored split: `axis.recorder.snapshot.render_ms.{bucket,count,sum,max,min}`.

Scripts from 2026-09-30 in the session scratchpad: `signoz-query.sh <minutes>` (names + series summary). The lean-ctx shell guard blocks inline `$(date …)`; put such logic in a script file.
