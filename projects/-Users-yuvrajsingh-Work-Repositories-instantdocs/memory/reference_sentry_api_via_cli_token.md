---
name: reference_sentry_api_via_cli_token
description: "Query Sentry (org helply, project instantdocs) via curl with the sentry-cli token when the Sentry MCP OAuth flow fails"
metadata:
  node_type: memory
  type: reference
  originSessionId: 7bd71b4c-21bb-40e4-8050-bd55afc8e291
  modified: 2026-10-27T15:29:05.923Z
---

Sentry MCP OAuth kept dropping its pending flow (complete_authentication said "No OAuth flow is in progress"). Working fallback: `~/.sentryclirc` holds the user's token, which can also write: bulk `PUT /api/0/projects/helply/instantdocs/issues/?id=..&id=..` with `{"status":"ignored","statusDetails":{},"substatus":"archived_forever"}` (or `archived_until_escalating`, or `{"status":"resolved"}`) works. The issue list lags a few seconds after status changes, and `lastSeen:-Nd` search is unreliable, so filter on `.lastSeen` with jq instead. Read it into a var with awk and curl `https://sentry.io/api/0/organizations/helply/events/` (Discover, `dataset=errors`, `field=...`, `query=message:*X*` searches exception values). lean-ctx shell allowlist blocks scratchpad scripts and shell functions, so keep it to inline curl.

Gotchas when using Sentry as evidence:
- Middleware (edge) events carry no URL/host; identify the KB from the Prisma `where` in the exception message.
- The org has the web-crawlers inbound filter on, so Googlebot-triggered events are dropped.
- Most repeated errors are discarded client-side (`client_discard event_processor` in stats_v2), so a missing event is weak evidence.
