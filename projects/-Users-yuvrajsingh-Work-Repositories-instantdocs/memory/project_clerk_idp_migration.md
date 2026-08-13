---
name: Auth migration — Clerk IDP, with better-auth explored as alternative
description: Auth migration initiative — Clerk SSO POC done, now also evaluating better-auth as a self-hosted alternative with Organizations + password hash migration
type: project
---

CTO is building a centralized IDP for SSO across the product suite. instantdocs is integrating with it.

**Phase 1 (DONE as of 2026-03-23):** SSO POC — added Clerk as custom OIDC provider in NextAuth. Tested and working.

**Phase 2 (PLANNING):** Migrate workspace/team management to an Organizations model. CTO confirmed team management will be handled by IDP, not internally.

**Alternative explored (2026-04-01):** User researched **better-auth** as a self-hosted alternative to Clerk. Findings:
- Has an Organizations plugin (CRUD, roles, invitations, teams) similar to Clerk Organizations
- Supports importing bcrypt-hashed passwords without forced resets
- Uses in-process lifecycle hooks instead of HTTP webhooks (no delete hooks, no retry guarantees)
- No decision made yet — still evaluating

**Why:** Centralized identity and team management across all products in the suite.

**How to apply:** When working on auth or workspace features, keep in mind that these are being migrated. Avoid adding new internal workspace management features that would need to be migrated later. The final IDP choice (Clerk vs better-auth) is still open.
