---
name: portless local TLS for InstantDocs in dev
description: Local dev runs InstantDocs behind portless at https://kb.helply.localhost; Node fetch needs NODE_EXTRA_CA_CERTS to trust portless's CA
type: project
originSessionId: f0eabda4-77f8-4de2-b6ea-29452a988001
---
InstantDocs is served via portless at `https://kb.helply.localhost` in local dev. portless ships a self-signed CA at `~/.portless/ca.pem` that the macOS keychain trusts (curl/browsers/Vite work) but Node does NOT (Node ships its own trust store). Any code in the Axis backend that uses `fetch()` to talk to `https://kb.helply.localhost` will fail with `SELF_SIGNED_CERT_IN_CHAIN` until `NODE_EXTRA_CA_CERTS=$HOME/.portless/ca.pem` is set in the backend's env.

**Why:** Axis → InstantDocs webhook delivery (`apps/backend/src/axis-webhook/axis-webhook-delivery.processor.ts`) uses Node `fetch`. Webhook URL is stored per RP in `ba_oauth_clients.webhook_url`; for InstantDocs it points at the HTTPS portless host.

**How to apply:** When debugging "fetch failed" or TLS errors from the backend reaching any `*.helply.localhost` host in dev, suggest adding `NODE_EXTRA_CA_CERTS` to root `.env`. The `dotenvx run -f ../../.env --` wrapper in `apps/backend/package.json` injects env vars before Node starts, so Node TLS picks it up. A plain HTTP fallback (`http://localhost:3001`) also exists if portless is unavailable.
