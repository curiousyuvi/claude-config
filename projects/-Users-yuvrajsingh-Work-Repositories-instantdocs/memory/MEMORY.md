# Memory Index

- [feedback_prisma_types.md](feedback_prisma_types.md) — Run `yarn` instead of `npx prisma generate` for Prisma type regeneration
- [feedback_ask_before_deciding.md](feedback_ask_before_deciding.md) — Always ask the user before making decisions or choices during planning/execution
- [feedback_no_ai_author_attribution.md](feedback_no_ai_author_attribution.md) — Never attribute commits/PRs to Claude or any AI (no Co-Authored-By, no "Generated with")
- [feedback_minimal_comments.md](feedback_minimal_comments.md) — Use minimal, necessary comments only; don't comment what doesn't need it
- [feedback_confirm_before_commit.md](feedback_confirm_before_commit.md) — Always confirm with the user before any git commit or push
- [feedback_axis_migrations_and_op.md](feedback_axis_migrations_and_op.md) — Axis: never hand-write migrations (use migration:create); hand op-gated commands to the user
- [feedback_refetch_editors.md](feedback_refetch_editors.md) — Keep refetchOnMount "always" only in article-editing-provider.tsx; editor must wait for fresh data
- [user_db_knowledge.md](user_db_knowledge.md) — User not deeply familiar with DB indexing — explain DB decisions clearly
- [project_clerk_idp_migration.md](project_clerk_idp_migration.md) — Auth migration: Clerk SSO POC done, better-auth also being evaluated as alternative
- [project_remotion_sync_migration.md](project_remotion_sync_migration.md) — Exploring replacing FFmpeg-on-Fargate video sync with Remotion Lambda
- [project_single_logout.md](project_single_logout.md) — Single logout ID↔Axis: end-session + webhook reuse; enableEndSession-before-login sid gotcha
- [project_dual_mode_workspaces.md](project_dual_mode_workspaces.md) — Permanent dual-mode: legacy vs Axis workspaces partitioned by login origin (auto-linked same-email user)
- [project_data_residency.md](project_data_residency.md) — Data residency map: PlanetScale us-east-1, S3 us-east-1 + ap-south-1, SES us-east-1, US-routed LLMs
- [reference_ccfind_ccresume.md](reference_ccfind_ccresume.md) — ccfind/ccresume zsh helpers in ~/.zshrc find old Claude Code chats the /resume picker doesn't display
- [project_planetscale_cascade_index_gotcha.md](project_planetscale_cascade_index_gotcha.md) — Vitess 3024 on page/KB delete has two causes: unindexed inbound FK full scan, and large SetNull/Cascade writes needing pre-drain in deletePageSubtree
