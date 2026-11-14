---
name: groove-app-capture-auth
description: "How Groove (GrooveHQ/Groove + mobile-frontend) web auth behaves, why the app-capture connection to it signed out, and what fixed it"
metadata:
  node_type: memory
  type: project
  originSessionId: a300d626-ed21-434c-8d87-057134e35e90
  modified: 2026-11-14T11:41:36.449Z
---

Groove web auth (checked 2026-11-13 in GrooveHQ/Groove and GrooveHQ/mobile-frontend):
- Login (`app/graphql/mutations/login.rb`) returns `user.web_token`, said to reuse the user's latest unexpired token. Unconfirmed in practice: on 2026-11-14 logging out in a person's own browser did NOT sign the capture profile out.
- Access token in localStorage `groove-auth`; refresh token in httponly cookie `refresh_tokens`. Refresh is POST api.groovehq.com/oauth/token `{grant_type, client_id, subdomain}`; on a dead token the app goes to /logout and calls /oauth/revoke (our guard blocks it).
- Breaking the token does not produce a 401 our `response` listener sees, so a "first 401" log line is useless for Groove.

Prod org 019edaf0-b76c-770a-bd5a-ece5bd417a92 (tropical-tees) signed out repeatedly 2026-11-10..14. Shipped: profile always saved + save-settle wait (#2111), renewal/opened-signed-out logs (#2112), password connections sign in again up to 3 runs (#2120), clear the dead login before that start-over (#2123). The old connection kept getting signed out ~20 s into every run even from a fresh profile; after a full disconnect and reconnect with email+password on 2026-11-14 10:38 UTC it ran 7+ captures with no sign-out. Root cause never proven (Groove-side data was to come from Matt); a guess is something the old connection remembered (screens/pages).

**Why:** explains the repeated "app signs out after a few gaps" reports.
**How to apply:** if it recurs, check SigNoz for `signed out partway`, `opened signed out`, `renewed the app's sign-in`, and blocked `/oauth/revoke`; try a full disconnect/reconnect before chasing code.
