---
name: project-railway-vars-incomplete-op-run
description: "`railway variables` shows only dashboard vars — the deployed app also gets everything in .env.production injected by `op run`"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T10:03:26.232Z
---

`railway variables --service api` lists **only what is set in the Railway dashboard**. The deploy also runs `op run --env-file=./.env.production`, which injects every key in that committed file (values are `op://` refs). So a var absent from `railway variables` can still very much be set in the running process.

This produced a string of wrong conclusions in one session: that `KB_EDGE_PURGE_URL`, `KB_EDGE_HOST_SECRET`, and the four `KB_ARTIFACT_BUCKET_*` were unset; that edge purging was a silent no-op; and a recommendation to *unset* vars that were load-bearing. All four were defined in `.env.production`. What disproved it was checking the actual effect — R2 had artifacts in it, which an unconfigured bucket could not have produced.

To see what the app really gets, read both:
```
railway variables --service api --kv | grep -oE "^[A-Z_]+"   # dashboard only
grep -oE "^[A-Z_]+" apps/backend/.env.production             # op-injected
```

Prefer confirming behaviour over reading config: query the resource (bucket contents, a live response header) rather than inferring from a var list.

Related: [[project_env_database_vs_db_prefix]], [[feedback_op_commands_user_runs]]
