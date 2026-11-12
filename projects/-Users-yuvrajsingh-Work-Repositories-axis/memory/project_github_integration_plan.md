---
name: project-github-integration-plan
description: "GitHub integration for gaps/capture: own GitHub App (Albato dropped); PR 1 = GitHub base only, decisions locked 2026-11-11 via grill session"
metadata:
  node_type: memory
  type: project
  originSessionId: ba864d9c-3e4d-41f5-aee8-0b4e06cc8e27
  modified: 2026-11-11T11:14:14.063Z
---

Started 2026-11-02. Albato route dropped 2026-11-06 (no GitHub connector, polls). Research brief: Notion "Code-aware knowledge base: research brief" (app.notion.com/p/410b7d82b70781938e63e3a459e55c33). Handoff: `.claude/handoffs/github-integration.md` in the main checkout (git-ignored; also a copy in ~/Work/Repositories2/axis). Work happens in ~/Work/Repositories/axis, NOT Repositories2.

Decisions locked 2026-11-11 (grill session), PR 1 = GitHub base, no AI, branch `ys/feat/github-integration` off origin/master:
- Module `src/modules/github/`, GitHub only (no provider abstraction), github.com only (no GHES/GHE.com).
- One workspace <-> one GitHub org (both unique). User does not care about multi-org now.
- Links: repo (by GitHub repo id) -> help center (KB), many-to-many, optional plain folder prefixes (no globs). Store repo id, full name, default branch; keep current via webhooks.
- 3 apps: "Helply" (prod, public), "Helply Staging", "Helply Dev" (private to GrooveHQ). I write form values, an org owner registers; keys in 1Password op:// refs.
- Permissions: Contents/Pull requests/Metadata read only. Events: installation, installation_repositories, repository, pull_request, push, release. User wants everything GitHub-side done in PR 1.
- pull_request/push/release in PR 1: verify, store in webhook_events, mark ignored. No unused tables (user rejected a merged-PR table in PR 1).
- Install flow verifies install via user OAuth + state; "waiting for GitHub admin approval" state auto-completes.
- Disconnect in Helply also uninstalls on GitHub. Uninstall/suspend stop access, keep links off; reinstall/unsuspend restores; separate Delete removes links.
- Permission key `knowledge_base.manage_code_sources` (admin+owner; migration grants to custom roles holding manage_gap_settings).
- UI under Settings > Integrations, link from gap settings. NO feature flag (user said no need to hide).
- Metering: same as all other AI features (AiAttribution + axis.ai.actions), no separate billing ever planned.
- Later PRs: merged PR = row in knowledge_gap_releases with new `source` column; new GapSource `code`; Chatwoot offline eval before tuning triage; no symbol graph stored.
- Open on purpose: order of later PRs, sandbox host, Agent SDK/ZDR spike, deep-pass cadence.

PR 1 opened 2026-11-11 as draft GrooveHQ/axis#2048 (commit af8dd5244). Blocked on Jared (CTO) registering the 3 apps and creating 1Password item `GitHub App` (fields app_id, slug, client_id, client_secret, private_key, webhook_secret) in Axis Dev/Staging/Production; setup doc artifact https://claude.ai/artifact/5x4S8uz8Jjyqc6zATUJFBz. Staging host https://next.helplystaging.com unconfirmed. Screenshots still owed. Local `tsc --checkers 2` shows a TS2859 in scheduled-message-list.service.spec.ts on this branch only (passes with 1 or 4 checkers; CI uses bun check).

2026-11-12: Jared registered the DEV app. Webhooks go GitHub > Hookdeck (verifies GitHub secret, retries) > app; provider trusts only hookdeck sourceVerified (like Slack). App has NO GitHub webhook secret; delivery reconciler REMOVED (user agreed). 1Password item now 5 fields (no webhook_secret). Local dev: `hookdeck listen https://api.inbox.helply.localhost github`. Staging/prod apps still pending.

2026-11-12: local test passed on `pnpm dev` (not bin/sandbox: sandbox host api-inbox-<id> does not match the Dev app callback). Dev app installed on GrooveHQ org, connection active, repos synced, Hookdeck delivered installation.created (ignored: arrived 2s before callback bound it, expected). UI changed (uncommitted): GitHub is a card under Developer on Integrations; Connect goes straight to GitHub; Manage opens GithubSettingsSheet; the /settings/integrations/github route is gone; the callback returns to Integrations and useGithubInstallResult toasts. Local DB was rebuilt 2026-11-11 (prod Helply snapshot gone, only Seed org). DEFERRED until the AI PRs need it: import the prod Helply help center into the local Seed org (read-only prod export of KB_TABLES from bin/_kb-move-org.ts, user runs it) and link it to the Helply repo in GrooveHQ.

2026-11-12 night (user asleep, Auto-fix on, PR marked ready by user): pushed 6d254d989 (thermo review fixes: queued github.resync on per-org worker groups, connection_id index migration 20261111221913, HmacTokenCodec state, githubConnectionView, NativeIntegration registry + IntegrationCardFrame) and 78e856749 (CodeRabbit fixes). Replies posted on 12 CodeRabbit threads, NOT resolved (user rule), no AI footer. OPEN for user decision: CodeRabbit critical 4543855603 — /user/installations proves repo read access, not org admin; a member with read access to one repo of an org whose install is unbound could bind it. Real fix needs org-admin check (GET /user/memberships/orgs/{org} needs "Members: read" app permission, i.e. Jared re-registers) — not replied. Screenshots in PR via new release screenshots-2. Web test suggested-snooze-banner fails only with non-UTC TZ (not ours).

2026-11-12 ~05:xx IST: Jared's Precog review REQUEST_CHANGES with two P1 blockers awaiting the USER's decision: (1) install authority (thread 4543855603): options A = bind only when the installation.created webhook's sender equals the OAuth user (no new GitHub permission; binding completes on webhook), B = org-admin check via GET /user/memberships/orgs/{org} (needs "Members: read" on the 3 apps); (2) owner approval can bind the wrong org (thread 4544138412): proposal = stop auto-completing requests; after approval the member clicks Connect again (changes a locked decision). P2 4544138427 (one lifecycle transition API) deferred to the P1 redesign. Fixed + replied: 4544138423 (refreshOne per created repo), 4544138432 (named org constraint). Head 2461349ac.

2026-11-12 (user back): user chose fix A + requests wait for a click. Shipped a6a19a7d8: authority = stored installation.created sender/requester (GithubWebhookTargetService.installerOf, partial index idx_webhook_events_github_installation_created, online migration 20261112075634); lifecycle API request/claim/confirm/remove/suspend; callback-before-webhook waits as requested+installationId (pendingInstall); approvals finish via OAuth-only "Finish connecting" (state purpose finish, client.authorizeUrl), NOT_APPROVED/AMBIGUOUS errors. Replied on 4543855603, 4544138412, 4544138427, 4543855608; PR description updated. Locked decision "requested auto-completes" is REVERSED.

2026-11-12: user ACCEPTED fix A's repo-admin limit (a repo admin may install on their repos; later repo additions are an org owner's choice); no Members: read permission. Replied on 4543855603. CodeRabbit thread 4548062203 stays unresolved by us.

2026-11-12 ~14:45 IST: new flow VERIFIED locally by the user: uninstall + reinstall bound install 181182974 (GrooveHQ) via the stored installation.created sender, first repo load done (repos_synced_at set). Head 646474037 (adds reinstall_required for an existing install with no stored installer).

2026-11-12 evening: PR 1 review loop DONE. Head cf660c74e; all CodeRabbit threads resolved, CodeRabbit check green, Sonar gate passes, CI green except a pending shard at last look. Only blocker: Jared's 4 threads + his CHANGES_REQUESTED (he must re-review). Design now (supersedes the pendingInstall/webhook_events notes above):
- Status `confirming` (installed, waiting for webhook) with claimant_github_user_id + claimant_user_id (Helply member); `requested` = waiting for owner approval, finish via "Finish connecting". Check constraints enforce each status's shape.
- Installers recorded in `github_installation_origins` at verified intake (webhook_events index removed). Only live rows (active/suspended) hold an install/account (partial unique indexes); waits hold nothing; different claimants on one install => delivery unbound.
- Callback requires the Helply session to be the state's baUserId (WRONG_SESSION) — fixes install-link takeover. confirm rechecks GithubManagerAuthority and reads the install from GitHub (suspension/404).
- Repo events all go through refreshOne; selection changes > 20 or all<->selected switch (repository_selection stored) => full resync; first loads deduped per connection+install (BullMQ deduplication, not jobId: GITHUB queue keeps 1000 completed jobs); repos_synced_at cleared on bind/unsuspend/selection change; API exposes repositoriesLoaded.
- ONE schema migration Migration20261112115827_GithubIntegration (regenerated from the branch-point snapshot each time; local DB rows backed up + restored). Permission data migration 20261111113500 unchanged.
- Personal GitHub accounts are SUPPORTED on purpose (user choice); copy says "GitHub account".
- Org FKs intentionally have no cascade (orgs are soft-deleted; repo convention).
NEXT (user, after compact): start the next phase (AI PRs on top of PR 1) with a grill round.

**Why:** user wants the GitHub plumbing complete and reviewed separately before any AI work.
**How to apply:** keep PR 1 free of AI and of tables nothing uses; don't re-ask settled points. Related: [[project-knowledge-gaps-feature]].
