---
name: project-capture-signin-dead-hold
description: "Sign-in hold SHIPPED (PR #2046, merged+deployed 2026-11-11); Groove still signs out ~75 min after sign-in — root cause NOT confirmed, user wants it confirmed and fixed before any more Groove runs"
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-11T13:09:42.764Z
---

PR #2046 (merged, deployed 2026-11-11): refresh-token POSTs pass the guard (token endpoint + grant fields only), log-out/session-expired pages count as signed out (incl. hosted signInOrigins, after last turn), a refused sign-in HOLDS gap work (capture_held_at, knowledge_gap_releases.held_screens) with bell notice `app_sign_in_needed` + banner; re-sign-in/new details/disconnect publishes `app_capture.sign_in_hold_lifted` -> GapCaptureReleaseService requeues. "Sign-in did not finish" does not hold.

Groove prod (org 019edaf0-b76c-770a-bd5a-ece5bd417a92, password sign-in graham@tropicaltees.store, app tropical-tees.groovehq.com):
- 2026-11-11 15:20 IST re-signed in (fresh profile, gen 2). Reset top 20 signed-out gaps (g7, backup CSV in ~/Work/kg-eval/prod), cleared survey jobs, resumed group, removed 9 stale shots jobs.
- 8 gaps finished well; 13 now HELD: at 16:35 IST (11:05 UTC) Groove's own page called POST /oauth/revoke + /api/v1/widget/session/logout (guard blocked both), run landed on /logout, hold + notice fired. Day's 20 runs were spent at 10:59 UTC.
- No /oauth/token was ever blocked. Hypothesis (UNPROVEN): refresh-token rotation + reuse detection; back-to-back Firecrawl sessions open the profile before the previous session's save lands (code waits only PROFILE_SAVE_SETTLE_MS=3s in one place), so a stale refresh token is reused and Groove revokes the family. Alternative: fixed session lifetime.
- Gap found: password connections can't self-heal because a dead session lands on /logout (no form) and signIn stops ("No sign-in form was found at .../logout"). Fix idea: sign-in from a log-out page goes to the app's sign-in page; password connections re-sign-in instead of holding.
- Remaining: 9 signed-out gaps not yet reset (g7 batch, surveyed_at 2026-11-10 17:00-24:00 UTC). Cap reset idea: delete Redis key app_capture:runs:day:<org>:<UTC date> (user rejected writing the script for now).

Investigation 2026-11-11 (Groove JS in scratchpad/groove/js, trace c8ff2b017f39cfd11cbe3356468f1e4a):
- Last run opened 11:04:36 UTC, sign-in check PASSED 11:04:48, Groove's own code went to LOGOUT_PAGE ~8s later (revoke + Helply widget logout = doLogout). LOGOUT_PAGE comes from a GraphQL HTTP 401 or a failed refresh reply.
- Groove refresh: every GraphQL call + a 5-min timer call doRefreshIfNecessary; fires when localStorage groove-auth.expiresAt < now+30min; POST https://api.groovehq.com/oauth/token JSON {grant_type, client_id, subdomain}, refresh token in cookie. expiresAt comes from GET oauth/token/info (Doorkeeper).
- No run ever logged POST /oauth/token (blocked or changed), and the already-signed-in load is guarded, so the page never tried a refresh: the server rejected a token the page thought had >30 min left. Server-side reason UNKNOWN; Groove is our own company, so its backend logs can say why.
- Definite bug anyway: isTokenRefresh refuses Groove's refresh because of the extra `subdomain` field, so near expiry every refresh would be blocked.

**Why:** user said "first really confirm the actual cause if possible and we need to fix it first, before continuing groove runs". **How to apply:** next step was investigating via SigNoz traces/logs (workers, 10:45-11:06 UTC), worker log run timeline, and Groove's public front-end JS (what triggers /oauth/revoke, how refresh works, where tokens live). No repo git changes while another chat works on master; scripts go in ~/Work/kg-eval/prod; user runs op/psql/railway ssh commands. See [[project-capture-article-review-design]].
