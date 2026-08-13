---
name: project_react_doctor_version
description: "Local react-doctor MUST use @latest to match CI — the repo's pinned react-doctor is stale/laxer"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c18f6b5-7571-4b19-9866-bc5a9c9f0484
  modified: 2026-07-29T09:59:19.326Z
---

CI's React Doctor check (`.github/workflows/react-doctor.yml`, `millionco/react-doctor` action) runs **`npx -y react-doctor@latest`** — an unpinned, newer, much STRICTER version than the repo's pinned dep (`pnpm exec react-doctor` = v0.1.2). Running `pnpm check` / `pnpm exec react-doctor` locally under-reports (it scored 93/100 while CI @latest scored 76/100 and FAILED with 14 errors on the same code).

**Why:** the two versions classify rules differently — patterns that are warnings in the pinned version are ERRORS in `@latest` (e.g. `query-destructure-result`, `no-adjust-state-on-prop-change`). CI uses `--fail-on error` (newer alias `--blocking error`), so only ✖ errors gate; ⚠ warnings don't.

**How to replicate CI exactly (always use this before pushing web changes):**
```
git fetch origin master && git branch -f master origin/master   # MUST do this first, see below
npx -y react-doctor@latest apps/web --diff master --offline --fail-on error
```
`apps/web` (not `. --project web`) matches the current workflow, which passes `directory: apps/web` + `diff: <base_ref>` — a comment there notes `.` made it walk the whole monorepo until the run died. Exit 0 = passes. Fetch the real CI failure with `gh run view --job <id> --log` when in doubt.

**GOTCHA: `--diff master` resolves the LOCAL `master` ref, not `origin/master`.** A stale local master silently widens the diff to include other people's already-merged PRs and reports a false failure. Seen 2026-07-29 on PR #941: local master 2 commits behind gave 84/100 with a failure; after `git branch -f master origin/master` the same tree gave 100/100 clean (and CI agreed). Sanity-check with `git rev-parse master origin/master | uniq -c` — one output line means in sync.

**Do NOT** trust `pnpm check`'s react-doctor portion for the CI gate — it uses the stale pinned version. Consider pinning react-doctor in the action or adding a repo config to stop `@latest` drift [[feedback_run_lint_typecheck]].

**Recurring gotcha — "Ref mutated during render" (a `fail-on error` bug):** the common `const fooRef = useRef(...); fooRef.current = () => {...}` "latest-closure" pattern (used across this codebase, e.g. KbPageHeader flushHandle) is flagged as an ERROR by react-doctor@latest when the assigned closure captures a per-render value (props/hook returns), because a discarded render could leak. It's only reported once you TOUCH that line in the diff (diffs vs origin/master). Fix = move the ref assignment into a commit-time `useEffect(() => { fooRef.current = ... })` (no deps) — behavior-identical for handles only called post-mount, and no biome-ignore needed (biome doesn't flag the deps-less effect). Assignments that close over ONLY refs are NOT flagged. Also: react-doctor's diff gate reads the WORKING TREE here (a committed fix and an uncommitted fix both scored 100), but confirm authoritatively against the committed state per [[feedback_diff_checks_after_commit]].
