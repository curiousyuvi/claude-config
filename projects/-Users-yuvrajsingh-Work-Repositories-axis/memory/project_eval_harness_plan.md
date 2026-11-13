---
name: project-eval-harness-plan
description: "Eval PR (first stacked PR of the GitHub AI phase): self-hosted Langfuse + InstantDocs corpus; all decisions locked 2026-11-13 via grill"
metadata:
  node_type: memory
  type: project
  originSessionId: 1a228b2e-c89d-439b-a376-11458407d5ae
  modified: 2026-11-12T19:15:49.738Z
---

Locked 2026-11-13 (grill). Eval PR comes FIRST, before the gaps-foundation PR and the GitHub AI PR ([[project-github-integration-plan]]).

- Platform: self-hosted Langfuse (MIT, kept after ClickHouse bought it Jan 2026), own pinned compose under `infrastructure/langfuse/`, `bin/langfuse up` with headless init; keys in apps/backend/.env.local. Local only; production tracing to Langfuse is a later decision. Jared fine with it; DeepEval rejected (human review + dashboard are paid Confident AI).
- Corpus: InstantDocs ONLY (Chatwoot dropped). Groove owns code/KB/app; user knows it fully. KB is stale/AI-written, so labels come only from a VERIFIED SET: I draft per-section verdicts from the InstantDocs code as one YAML per article, user confirms (25-40 articles). Score only against verified sections.
- KB source: the InstantDocs KB already in axis PROD; export only KB_TABLES (bin/_kb-move-org.ts) read-only, user runs it via op run; import locally with faked emails; freeze to fixtures.
- Tickets: all mocked (real InstantDocs tickets too few and biased by a migration), model-drafted then human-checked.
- Screenshot evals: local InstantDocs, but it uses a REMOTE PlanetScale dev branch. One "Helply Eval" org, idempotent seed script with a hard guard: never touch other orgs' data, reset = reseed that org only.
- Two levels: stage evals (frozen inputs, no DB, call domain functions) and scenario evals (seeded local axis eval workspace).
- Datasets in git (`apps/backend/evals/`, YAML per case + shared fixtures), synced to Langfuse; runs/scores/reviews in Langfuse. Code in apps/backend/evals, typechecked, not built.
- Scoring: code checks from labels (don't force where impossible), judge from a different model family, pinned, trusted per criterion only at >=80% agreement with human; human thumbs+comment on all failures + 10% of passes via annotation queues.
- Split 60% tune / 40% holdout (user paranoid about overfitting); report holdout per kind only with >=3 cases. N=1 default, `--repeat 3` for decisions. Runs named by sha+prompt versions+models, diff vs baseline. `--max-usd` cap. Real models, cost tagged as eval. Manual CLI, no CI.
- First version 60-80 cases. Stages: gap judge, release scan, drafter, screenshot agent; GitHub PR cases labeled now (real InstantDocs PRs vs verified sections), run in PR 3.
- Build order: gap judge end to end with ~10 cases first, then other stages. First run = `baseline` on unchanged prod prompts. PR done = harness + 4 adapters + seed + verified set + 60-80 cases + baseline numbers; NO prompt changes. Retire ~/Work/kg-eval/eval-round.sh after.

Still open for PR 2 (not evals): 409 case: auto re-draft + "Re-draft with my edits" button, or separate AI-merge button?

Progress 2026-11-13 (branch ys/feat/kb-evals off master, nothing committed):
- Built: infrastructure/langfuse/compose.yml (Langfuse 4.76.0, web 127.0.0.1:3100, minio 9190) + bin/langfuse up|down|reset|logs (secrets in infrastructure/langfuse/.env, keys into apps/backend/.env.local); bin/kb-eval-export.ts (`evals:kb-export`, READ ONLY tx, --list/--kb, writes evals/corpus/instantdocs.json); apps/backend/evals/ harness (corpus, cases YAML, stage contract, CostMeter span processor on axis.ai.cost_usd, Langfuse dataset sync + experiment + evals-review queue with human_correct + human.<criterion>, grader anthropic/claude-sonnet-4.5, report + baseline diff, `agreement` writes evals/grader-trust.json); gap-judge stage; AI feature `evals`; extracted toGapArticle/toGapCollections mapper.
- Smoke run passed end to end on Node 24 ($0.012). Must run evals on Node 24 (RegExp.escape); pnpm in Claude shell only via `sh ~/Library/pnpm/.tools/pnpm/12.15.0/bin/pnpm`.
- NEXT: user runs the prod export, then I draft verified sections + ~10 gap-judge cases, then baseline.
- 2026-11-13 later: corpus exported (InstantDocs KB 019fb817-d86d-7300-ad6b-f306d5e7864f, 24 collections, 139 articles). Verified set for 12 articles in evals/verified (checked against instantdocs origin/main b2966b7cb via a scratch worktree). 12 gap-judge cases (7 tune, 5 holdout); cases.spec.ts enforces labels vs verified verdicts. Baseline (repeat 3) = 100% on every check, $0.748: cases too easy (one retrieved article, consistent agents). NEXT: harder cases (distractor articles, mixed/vague answers, near-miss sections, findability, conflict), user to confirm verified set.
- 2026-11-13 round 2: 20 verified articles, 36 gap-judge cases (21 tune/15 holdout; 20 correction, 6 covered, 5 not_knowledge, 3 missing, 2 findability, 0 conflict: the KB has no real conflict pair). Baseline repeat 3 = 100% again ($2.54). The 3 steady failures in the 32-case run were MY case errors (extra fact in covered tickets, too-narrow article label, refund vs written no-refund policy); article may now be a list. Errored items are now excluded from rates and block --save-baseline. Verifier was wrong once (SEO indexing default): spot-check every verdict used as a label.
- 2026-11-13 user: NO videos in the frozen KB. bin/_kb-eval-content.ts withoutVideos (video + media_embed) runs in the export and was applied to corpus/instantdocs.json (565 img kept). The gap-judge baseline predates this, so rerun it.
- Grill round 2 answers: survey agent = new scenario stage (yes); drafter runs with real/none/wrong field notes (yes); freeze all 565 KB images (not in git: manifest + gitignored cache), replace unfit ones with new screenshots; screenshot agent may write in settings (only critical actions blocked) unless the user picked read-only mode, so test both; split must not be by app area (areas differ in difficulty), stratify instead; drop the "nothing outside the section" code check (asSectionFix already enforces it; PR 2 multi-change = grader criterion); combined action cases are real; more GitHub types welcome; wants eval modes (smoke/core/full); asked for scoring options beyond thumbs. Open: Q19-Q24 (assets, write modes, stratified split, fix-pipeline stage, scoring format, tiers).
