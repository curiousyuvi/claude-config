---
name: feedback-ask-before-any-eval-run
description: "Before ANY eval run (any size), tell the user the approximate cost and wait for their yes"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-16T13:03:57.240Z
---

Before running any eval of any kind (full stage, `--only`, A/B, scenario, peek scripts that call models), state what it will run and its approximate cost in USD, and wait for the user to confirm. No exceptions for "small" runs.

**Why:** on 2026-11-16 the user saw large eval spend (round 3 about $27, round 4 about $21, mostly gap-judge A/B runs with the grader on and full-stage reruns) and said "no more big eval runs without asking, also before running any type of eval confirm with me what it would cost approximately, so that I can decide".

**How to apply:** estimate from earlier run files (`evals/runs/*.json` have `costUsd`; gap-judge full stage x2 is about $0.8-1, survey core x3 about $1.3, screenshot core x3 about $1.3, restore core about $0.2). Prefer `--no-grader` and `--only` for A/B checks, one full-stage confirm at the end. See [[eval-harness-plan]] and [[post-eval-pr-backlog]].
