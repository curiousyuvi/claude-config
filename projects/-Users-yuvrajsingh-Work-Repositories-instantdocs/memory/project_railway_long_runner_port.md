---
name: project-railway-long-runner-port
description: "Railway long-runner runs `yarn start` with PORT=3000 injected — never pin a port in package.json scripts"
metadata: 
  node_type: memory
  type: project
  originSessionId: a6505c38-ce3b-4645-abf0-e2eb1f8e45c8
  modified: 2026-08-14T11:36:34.175Z
---

The `instantdocs` service in the Railway project `instantdocs-long-runner`
(Instantdocs workspace) builds from the same repo and boots via the
`package.json` `start` script. Railway injects `PORT=3000` and its edge proxy
forwards there, so pinning a port in `start` silently breaks the whole service.

On 2026-08-12, #2655 set `"start": "next start -p 3001"` while moving local dev
off the Portless proxy. Every request to the long-runner 502'd in ~5ms for two
days. The container logged `✓ Ready` and nothing else, because no request ever
reached it. Fixed in 569c53ab3 by returning both `dev` and `start` to the Next
defaults.

**Why:** the failure is invisible from the app side. Railway reports the
deployment SUCCESS, the container is healthy, and only the HTTP logs
(`get_logs` with `log_type: "http"`) show the 502s.

**How to apply:** never add `-p <port>` to `dev` or `start`. When something
routed through `LONG_TASK_SERVER_URL` hangs, check Railway HTTP logs for 502s
before digging into the feature code. Related: [[project-voiceover-dispatch-silent-failure]].
