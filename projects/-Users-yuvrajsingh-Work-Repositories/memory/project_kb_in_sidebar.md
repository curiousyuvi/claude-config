---
name: project-kb-in-sidebar
description: "KB-in-ticket-sidebar feature — Axis inbox browses/searches published InstantDocs KB via /api/axis; built + code-verified, not yet committed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7d7bc585-6c10-4113-8c75-ceab1d984a78
---

"KB in ticket sidebar" (Notion 372b7d82b707809588d5c30951395e4b): the Axis inbox ticket sidebar browses + searches a workspace's published InstantDocs KB and inserts article links into the composer. Built across both repos (Axis `master`, InstantDocs `main`); all typecheck/lint/build green; **not committed yet**.

Key architecture (verified, non-obvious):
- **Direction**: SPA → Axis `/api/knowledge/*` → InstantDocs `/api/axis/*` (S2S, backend-to-backend; secret never in the browser).
- **Org-id linchpin**: Axis `Organization.id` === better-auth org id === InstantDocs `workspace.baOrgId` — the org-mirror inserts `Organization { id: baOrgId }` (`organization-mirror.processor.ts`). So Axis passes `@OrgId()` straight through as the workspace key; no mapping.
- **Auth**: Axis presents the InstantDocs RP's clear-text `webhookSecret` — read from `ba_oauth_clients` in the DB (like rp-webhooks; the OIDC `clientSecret` column is HASHED/unrecoverable, so it can't be presented) — as a **Bearer** token; InstantDocs validates it against its matching `AXIS_WEBHOOK_SECRET`. No new secret, nothing in env. Axis finds the InstantDocs client row by `webhookUrl` origin === `INSTANTDOCS_API_ORIGIN`. Act-as identity in `X-Axis-Org-Id`/`X-Axis-User-Id` headers. (History: first shipped a bespoke `AXIS_KB_API_SECRET`, then tried OIDC client_secret — both corrected by the user. See [[feedback-collaboration-style]] — surface drifts from an agreed proposal, and prefer reusing existing credentials.)
- **Authorization**: per-KB ≥READ via `resolveWorkspaceKbAccess` (extracted from trpc.ts `workspaceProtectionHandler` into `kb-access.ts`). InstantDocs models per-KB access (`workspaceMembersAccess`/`workspaceAdminsAccess` + `SpecificWorkspaceUserKBSharing`).
- **Published data**: tree/collection/article fetchers extracted verbatim into `published-kb-data.ts`; the public help-center tRPC procedures now delegate to them (single source of truth). Reuse existing Next cache tags (`entire-locale-kb-*`, `kb-structure-*`, `locale-doc-*`). Article mapped published-safe (HTML + published video; remotion/blocknote stripped). Grouped search = Typesense (articles) + dependency-free in-memory fuzzy (collections).
- **Frontend**: `src/features/knowledge/` — nav store models search as a stack frame (Back→results, Clear→origin). Rail's "Knowledge base" button repurposed to a `KNOWLEDGE` panel kind. Composer insert reuses the `useReplyEditor` registry.

Open follow-ups: sandbox screenshots (AGENTS.md; needs both apps + OIDC creds + seeded KB data); language switcher only has per-entity `availableLocales` for articles (root/collection need a backend addition); staging origin guessed `kb.staging.helply.com`; the InstantDocs OAuth client row (`ba_oauth_clients`) must have a `webhookUrl` on the InstantDocs origin + a `webhookSecret` for the auth lookup to resolve (same prerequisite as the webhook feature) — else `/api/knowledge/*` 502s with "No Better Auth OAuth client with a webhook on …".
