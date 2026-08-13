---
name: project-backend-full-suite-needs-streaming-output
description: "The backend suite takes ~2.5min; a bg job is killed after 120s with no NEW stdout, so never redirect it only to a file"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T18:47:48.511Z
---

`pnpm test` in `apps/backend` runs 691 files / ~7415 tests in roughly 145s. That exceeds the 110s foreground cap, so it auto-backgrounds — and a background job is killed after **120 seconds without new stdout**.

This makes the obvious invocations fail, and fail *silently misleadingly* (the harness reports a timeout, but the partially-written file looks like a normal run that just stopped):

```
pnpm test > out.txt 2>&1              # all output to file → zero stdout → killed
pnpm test 2>&1 | tee out.txt | tail   # tail buffers to EOF → zero stdout → killed
```

What works is letting output keep flowing to stdout while also capturing it:

```
cd apps/backend && pnpm test --reporter=dot 2>&1 | tee "$CLAUDE_JOB_DIR/tmp/be-full.txt"
```

Then poll with `sleep 100; grep -aE "Test Files|Tests " "$CLAUDE_JOB_DIR/tmp/be-full.txt"`. Use `grep -a` — vitest output has ANSI/control bytes and plain `grep` may treat the file as binary.

Related: [[project_backend_typecheck_gate_tsgo]], [[feedback_run_lint_typecheck]]
