---
name: feedback_diff_checks_after_commit
description: "Run react-doctor / diff-based new-code gates AFTER committing — they diff committed refs, not the working tree"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 68700ce7-404c-40d0-9439-98fba805e05f
---

Diff-based checks compare **committed refs** (`--base origin/master`), NOT the working tree — so run them AFTER `git commit`, matching how the PR CI runs them.

**Why:** `npx -y react-doctor@latest . --project web --scope changed --base origin/master --offline --blocking error` scans the git diff between the branch and the base. With uncommitted changes it sees an empty/partial diff and reports "No issues / 100 / 100" — a **false pass**. The same holds for the SonarCloud / react-doctor new-code gates on the PR: they only judge committed lines. So a clean local react-doctor run on unstaged edits proves nothing.

**How to apply:** commit first, then run react-doctor — and re-run it after every review-fix commit (and after any amend). Working-tree tools (Biome, typecheck, tests) can run before committing; the lefthook pre-commit hook already runs `biome check` + file-size + typecheck, and pre-push runs migration-drift. See [[project_react_doctor_version]] and [[project_run_axis_ci_locally]].
