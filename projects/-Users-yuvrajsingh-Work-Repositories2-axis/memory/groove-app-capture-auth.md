---
name: groove-app-capture-auth
description: "How Groove (GrooveHQ/Groove + mobile-frontend) web auth behaves, and why the app-capture connection to it signs out"
metadata:
  node_type: memory
  type: project
  originSessionId: a300d626-ed21-434c-8d87-057134e35e90
  modified: 2026-11-13T11:47:12.181Z
---

Groove web auth (checked 2026-11-13 in GrooveHQ/Groove and GrooveHQ/mobile-frontend):
- Login (`app/graphql/mutations/login.rb`) returns `user.web_token`, which REUSES the user's latest accessible web token (24h expiry from its creation), so a fresh login can get a token close to expiry, shared with every other browser of that user.
- Access token sits in localStorage `groove-auth`; refresh token in encrypted httponly cookie `refresh_tokens` (domain .groovehq.com). Frontend refreshes when <30 min left (boot) or <1 h (5-min interval), via POST api.groovehq.com/oauth/token.
- Doorkeeper rotates: each refresh makes a new token pair and the old one dies once the new one is used. A dead token gives 401/invalid_grant, then the frontend goes to /logout and calls /oauth/revoke.

Axis app-capture with LIVE sign-in opens the Firecrawl profile with save=false, so a refresh inside one run is lost and the next run (even in the same job) signs out. Seen in prod 2026-11-10..13, org 019edaf0-b76c-770a-bd5a-ece5bd417a92.

**Why:** explains the repeated "app signs out after a few gaps" reports.
**How to apply:** any fix must persist the rotated token (save the profile for LIVE too), and a password sign-in must not stall on /logout (the guard blocks the app's /oauth/revoke, so Groove never reaches /login).
