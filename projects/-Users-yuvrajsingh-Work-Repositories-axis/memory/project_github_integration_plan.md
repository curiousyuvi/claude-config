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

**Why:** user wants the GitHub plumbing complete and reviewed separately before any AI work.
**How to apply:** keep PR 1 free of AI and of tables nothing uses; don't re-ask settled points. Related: [[project-knowledge-gaps-feature]].
