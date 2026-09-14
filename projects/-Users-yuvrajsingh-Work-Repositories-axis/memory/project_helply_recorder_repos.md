---
name: helply-recorder-repos
description: "New helply-recorder-extension and helply-recorder-app repos (rebranded from instantdocs), their axis API contract, R2 update bucket, and remaining blockers"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8740c10e-4dbf-4535-82ac-5dcbcef87f9b
  modified: 2026-09-14T19:32:36.682Z
---

Created 2026-09-15 from the instantdocs recorder repos (kept intact next to them in Work/Repositories): private repos GrooveHQ/helply-recorder-extension and GrooveHQ/helply-recorder-app, both v1.0.0, fresh git history, builds verified.

Stripped everywhere: Supabase (progress now via chrome.runtime port / IPC), BetterStack, Sentry, credits/plan billing. Clicks payload simplified to `{x, y, t}` (0..1 fractions of the recorded surface, t = ms from recording start).

Axis API contract both clients expect (backend does NOT exist yet, phase 2): `GET /recorder/session` (ext), `GET /recorder/me` (app), `GET /recorder/workspaces`, `GET /recorder/knowledge-bases?workspaceId=`, `POST /recorder/recordings` (ext gets videoMultipart+audioUploadURL+taskId, app gets videoUploadURL+audioUploadURL+taskId — return both), `POST /recorder/recordings/:id/complete-multipart`, `POST /recorder/recordings/:id/status`. Extension auth: axis session cookie (credentials include). App auth: browser deep link `helply-recorder://` from `/native-app-login` carrying csrfToken/sessionToken, forwarded as headers + `helply.*` placeholder cookies.

URLs: extension via .env (`HELPLY_APP_URL`, `HELPLY_API_URL`, dotenv-webpack); app via `src/shared/config.ts` (placeholders app.helply.com / api.helply.com, finalize in phase 2).

Auto-update: R2 bucket `helply-recorder-apps` on the Sharedservices CF account (`CLOUDFLARE_ACCOUNT_ID=65e296b71eaf0e794c6e4f90e0f6f27c` — must export it, login has two accounts). Public feed https://pub-435ede51c76b45338f90b1dcf3d79bf6.r2.dev (r2.dev enabled; custom domain later). electron-builder publish = [generic feed, s3 upload via the account endpoint]; publishing needs an R2 API token as AWS_* env.

Never touch `assets/scripts/makewindowtransparent.node` (original dev: Windows recorder dies). Root cause of its phantom git diff was `* text eol=lf` in .gitattributes with no `*.node binary`; fixed in the new repo. Old repo still has the bug.

Open items: Helply icons/logos (user provides), R2 API token for publishing, Chrome Web Store listing, mac/win code signing certs, [[kb-access-publishing-task]] phase 3 = step-article generation from recordings.
