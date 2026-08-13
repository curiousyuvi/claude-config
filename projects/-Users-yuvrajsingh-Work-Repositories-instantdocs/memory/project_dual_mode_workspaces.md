---
name: project_dual_mode_workspaces
description: Permanent dual-mode model — legacy vs Axis workspaces partitioned by login origin
metadata: 
  node_type: memory
  type: project
  originSessionId: 1985cacb-734e-4712-95fa-d406d20ebc72
---

Permanent model (PR `ys/feat/dual-mode-legacy-axis-workspaces`, 2026-06): a person can have BOTH a legacy InstantDocs account and an Axis/Helply account under the SAME email. They're auto-linked into ONE `User` row (email is unique, so linking is forced; `allowDangerousEmailAccountLinking: true` on the axis provider — reverses the old §10.2 "no linking"). Safe because Axis verifies email on signup.

**Partition by login origin (not identity):** `session.user.loginOrigin` ("axis"|"legacy") is exposed on the session in `auth.ts`; `isHelply` mirrors `loginOrigin === "axis"` (so a linked user in a legacy session gets legacy branding). `computeIsHelplyUser` was deleted. A session sees ONLY its bucket: `workspace.getAll` filters `baOrgId` ({not:null} for axis, null for legacy) AND `workspaceProtectionHandler` enforces the same on every workspace-scoped procedure (cross-bucket access → NOT_FOUND with `WORKSPACE_NOT_IN_SESSION`). This is permanent — many legacy users will never move to Axis; the ones who want to are handled case-by-case.

**UPDATE (PR `ys/feat/host-first-auth-world`, 2026-06-11): origin is now HOST-derived, not provider/token-derived.** `loginOrigin`/`isHelply` are no longer written to the JWT — the session callback computes the world fresh from the request host via `getServerAuthWorld()` (in `server/helper/auth-method.ts`) → `authWorldForHost(host)` (in `helper/auth-world.ts`). Prod hosts map directly (`app.instantdocs.com`→legacy, `kb.helply.com`→axis, both hardcoded); other hosts fall back to env `NEXT_PUBLIC_DEFAULT_AUTH_WORLD` ("axis"|"legacy", default legacy) — this REPLACED the old `NEXT_PUBLIC_HELPLY_IDP_SIGNUP_ENABLED` flag. So even a user with only an Axis account hitting `app.instantdocs.com` gets the legacy flow. `resolveAuthMethodForEmail` short-circuits to `{kind:"axis"}` in the axis world (dropped the old provider-inspection ladder). Safe to drop the token field because the two worlds are separate cookie-jar domains (a session minted on one host is never read on the other). See [[project_host_first_auth_world]] if split out.

**Decisions baked in:** axis-mode blocks `create`/`joinWorkspace`/`getJoinableWorkspaces` (those make legacy workspaces → would be invisible in axis mode). `organization.deleted` webhook HARD-DELETES the ID workspace (via shared `deleteWorkspaceCascade`), no preservation. `member.removed` bumps `sessionVersion` only if it was the user's LAST workspace; demotion no longer bumps (live authz reads role per request). Stray cross-bucket deep links redirect to /home via `WorkspaceOriginGuard`; the workspace-provider gates its queries to the active bucket so stale localStorage ids never false-fire.

**Accepted limitation (don't re-flag):** the origin partition is enforced in `getAll` + `workspaceProtectionHandler` (the workspace*ProtectedProcedure variants), but a few plain `protectedProcedure`s that resolve to a workspace bypass it — `comment.create`/`delete`/`update`/`toggleReaction`, `userPresence.updatePresence`, `articleQuery.isArticleSlugAvailable`. Left as best-effort on purpose: the only exposure is a LINKED user reaching their own cross-bucket data (non-linked users are blocked by existing membership checks), so it's a consistency gap, not a security one. If revisited, the fix is a small `assertWorkspaceInSession(db, workspaceId, loginOrigin)` helper (origin-only, reuses WORKSPACE_NOT_IN_SESSION) added to those procedures.

Related: [[project_clerk_idp_migration]], [[project_single_logout]].
