---
name: project-pnpm-run-deploy-shadowed
description: "`pnpm deploy` is a built-in pnpm command and shadows the package script — use `pnpm run deploy`"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T10:06:43.121Z
---

`deploy` is a reserved pnpm command (it copies a workspace package to a directory), so in `apps/kb-edge` the script in `package.json` is shadowed:

```
pnpm deploy      -> ERR_PNPM_NOTHING_TO_DEPLOY  No project was selected for deployment
pnpm run deploy  -> wrangler deploy --env=''    ✓
```

The handoff doc and several PR descriptions say `pnpm deploy` for the kb-edge Worker; they are wrong. Same trap applies to any script named after a pnpm builtin — `apps/kb-edge` also has `"secret"`, which is fine, but reach for `pnpm run <script>` by default in that package.
