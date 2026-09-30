---
name: project_signoz_ingester_opensearch_403
description: signoz-ingester's elasticsearch receiver has been getting 403 unauthorized from OpenSearch every minute since at least the 26 Aug 2026 deploy; OpenSearch metrics in SigNoz are empty
metadata:
  type: project
---

Found 2026-09-30 while checking the new `signoz-cloudwatch` service. `signoz-ingester` (deploy `6ff36671`, 26 Aug 2026,
the only live one) logs `Error scraping metrics` from `otelcol.component.id=elasticsearch` with
`error: status 403, unauthorized` once a minute. So the `elasticsearch.*` metric families in SigNoz
(`ops/signoz/README.md` "Infrastructure metrics" table) have had no data for weeks.

**Why it matters:** any SigNoz alert on OpenSearch health is blind, and the log line was never noticed.

**How to apply:** 403 (not 401) from the OpenSearch security plugin usually means the credentials authenticate
but lack `cluster:monitor/*` for `_cluster/health` and `_nodes/stats`. The README says the ingester reuses the
backend's OpenSearch user, so the likely fix is a role mapping on the OpenSearch side, not a Railway variable.
Second possibility: `OPENSEARCH_ENDPOINT` unset in Railway, so the committed default hostname is a guess.
Never call `list_variables` on the ingester to check; it prints the password. Not fixed; reported to the user.
Pull the receiver id and error from Railway with `railway logs --json` (the MCP log tool drops attributes).
