---
name: helply-recorder-repos
description: "New helply-recorder-extension and helply-recorder-app repos (rebranded from instantdocs), their axis API contract, R2 update bucket, and remaining blockers"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8740c10e-4dbf-4535-82ac-5dcbcef87f9b
  modified: 2026-09-14T21:01:06.328Z
---

Created 2026-09-15 from the instantdocs recorder repos (kept intact next to them in Work/Repositories): private repos GrooveHQ/helply-recorder-extension and GrooveHQ/helply-recorder-app, both v1.0.0, fresh git history, builds verified.

Stripped everywhere: Supabase (progress now via chrome.runtime port / IPC), BetterStack, Sentry, credits/plan billing. Clicks payload simplified to `{x, y, t}` (0..1 fractions of the recorded surface, t = ms from recording start).

Phase 2 BUILT (axis branch `ys/feat/recorder-backend`, uncommitted as of 2026-09-15): `modules/recorder` facade `/api/recorder/*` — session/me/workspaces (BA listOrganizations, incl slug)/knowledge-bases (KnowledgeBaseService export)/recordings (create+presign)/:id/audio-upload-url (sized presign AFTER client audio extraction)/:id/complete-multipart/:id/status/:id. `RecorderRecording` entity + Migration20260914204545 (hand-trimmed: the committed MikroORM snapshot on master was STALE — regen re-emitted ticket_forms etc; kept the corrected snapshot). Org scoping via `x-axis-org-id` header. Desktop auth: `/api/recorder/auth/callback` mints BA session token (prod-enabled CLI-flow mirror) → deep link `helply-recorder://auth?sessionToken=`, app sends Authorization Bearer (csrf/cookie machinery deleted). Web: `features/recorder` polling status page at `/{workspaceSlug}/recordings/{id}` — both clients open it post-upload. Wiki: `wiki/pages/feature-recorder.md`.

URLs (real): app https://next.helply.com, api https://next.helply.com/api (same origin). Extension ID pinned via manifest `key` → `chrome-extension://kgijlpfmjhnlcpgmbhpmkhkleijelklg` (private key at ~/Downloads/helply-recorder-extension-key.pem — must go to 1Password); that origin must be added to `CORS_ALLOWED_ORIGINS` + `BETTER_AUTH_TRUSTED_ORIGINS` on deployed backends. Recordings buckets: private R2 `helply-recordings{,-staging}`; user must add `recordings_bucket_{endpoint,access_key_id,secret_access_key}` fields to the "Object Storage" items in Axis Production + Axis Staging vaults (endpoint = https://65e296b71eaf0e794c6e4f90e0f6f27c.r2.cloudflarestorage.com).

Machine gotchas hit: taskforce npm token lives in vault field `npm_taskforcesh_token`-ish on the Taskforce item (the `token` field is a placeholder); pnpm/mise/global-npmrc were lost in a machine cleanup and reinstalled.

Auto-update: R2 bucket `helply-recorder-apps` on the Sharedservices CF account (`CLOUDFLARE_ACCOUNT_ID=65e296b71eaf0e794c6e4f90e0f6f27c` — must export it, login has two accounts). Public feed https://pub-435ede51c76b45338f90b1dcf3d79bf6.r2.dev (r2.dev enabled; custom domain later). electron-builder publish = [generic feed, s3 upload via the account endpoint]; publishing needs an R2 API token as AWS_* env.

Never touch `assets/scripts/makewindowtransparent.node` (original dev: Windows recorder dies). Root cause of its phantom git diff was `* text eol=lf` in .gitattributes with no `*.node binary`; fixed in the new repo. Old repo still has the bug.

Open items: Helply icons/logos (user provides), R2 API token for publishing, Chrome Web Store listing, mac/win code signing certs, [[kb-access-publishing-task]] phase 3 = step-article generation from recordings.
