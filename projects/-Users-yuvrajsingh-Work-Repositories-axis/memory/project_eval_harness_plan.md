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
