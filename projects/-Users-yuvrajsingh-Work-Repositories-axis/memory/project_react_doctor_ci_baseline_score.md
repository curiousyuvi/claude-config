---
name: project_react_doctor_ci_baseline_score
description: "React Doctor PR comment headline score is the whole-apps/web baseline, not PR-attributable; the gate is diff-based and passes separately"
metadata: 
  node_type: memory
  type: project
  originSessionId: 18753834-9583-45f7-8c76-e3221775de5d
---

The `millionco/react-doctor` GitHub action (`.github/workflows/react-doctor.yml`, `directory: apps/web`, `diff: master`, `fail-on: error`) posts a PR comment whose **headline `Score: NN/100` is the score of the ENTIRE `apps/web` app** (a large pre-existing baseline — ~401 issues / 61 as of 2026-07). That number is NOT attributable to the PR.

The **gate** is the separate diff scan in the same comment body ("Scanning changes … No issues found! 100/100") — `fail-on: error` uses only the changed lines, so a clean diff **passes the check even while the headline shows 61**. Don't chase the headline: check whether the diff scan is clean and whether the "React Doctor" check is `pass` in `gh pr checks`.

Reproduce locally: diff score = `npx -y react-doctor@latest . --project web --diff origin/master --offline --fail-on error` (see [[project_react_doctor_version]]); whole-app baseline = same command WITHOUT `--diff`. Raising the baseline is a separate, broad cleanup — do NOT fold it into a feature/hotfix PR (react-doctor's own guidance + repo frontend rules). Run these gates only after committing ([[feedback_diff_checks_after_commit]]).
