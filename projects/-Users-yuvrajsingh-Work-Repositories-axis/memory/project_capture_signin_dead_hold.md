---
name: project-capture-signin-dead-hold
description: "Decided 2026-11-10 — when a connected app's sign-in dies, hold gap work (no drafting) until re-sign-in or disconnect, no time limit; plus 2 small fixes found from Groove's prod run"
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-10T18:11:24.684Z
---

Groove prod redraft (2026-11-10, org 019edaf0-b76c-770a-bd5a-ece5bd417a92) ran every survey on `/logout`. Likely cause (from logs, not proven): the write guard's ACCESS_PATH floor blocked the app's `POST /oauth/token` refresh once the morning token expired, so the app revoked and logged itself out; `isSignedIn` then missed `/logout`. Groove gap group is PAUSED via BullMQ Pro `pauseGroup` (script ~/Work/kg-eval/prod/gap-group.mjs over `railway ssh --service workers`); resume after fixes deploy, then requeue the ~8 gaps surveyed logged out (22:56–23:03 IST).

Plan agreed with the user:
1. Allow OAuth `grant_type=refresh_token` POSTs through the guard (keeps the session alive); revoke/logout/credential changes stay blocked.
2. `isSignedIn` treats log-out pages as signed out — done on `ys/fix/capture-signed-out-page` (uncommitted).
3. Detect a signed-out page mid-run and stop the run with a sign-in error.
4. Feature: connection state "sign-in needed"; survey/screenshot/draft jobs for that workspace HOLD (no daily runs spent, no drafts without notes); banner on gaps page + connected-app settings and admin notification ("sign in again or disconnect"); re-sign-in resumes held gaps; disconnect drafts them without screenshots.

**Why:** users assume drafts get screenshots; a dead sign-in silently produced weak drafts and burned daily runs. **How to apply:** user decided NO time limit on the hold — never draft while sign-in is dead, only after re-sign-in or full disconnect. See [[project-capture-article-review-design]].
