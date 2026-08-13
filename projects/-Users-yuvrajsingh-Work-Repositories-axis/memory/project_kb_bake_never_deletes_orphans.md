---
name: project-kb-bake-never-deletes-orphans
description: "A KB re-bake used to only PUT, leaving unpublished routes live at the edge; fixed 2026-08-10 so the bake reaps"
metadata:
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T18:47:36.209Z
---

**Fixed on branch `ys/feat/kb-edge-static-surface` (2026-08-10), not yet merged.** Until that lands, the behaviour below is still live in production.

`KbArtifactBaker.bakeKb` used to write artifacts and never delete them. When a route stopped being published — an article unpublished, a collection converted to a documentation layout that 302s — the next re-bake simply stopped emitting that key, the old object stayed in R2, and `CachedKb` kept serving it. **For an unpublished article that meant it stayed publicly readable.**

The fix: `bakeKb` collects the keys it wrote, lists the KB prefix, and deletes the difference (`reap()`). Safe because every dirty scope but a purge runs a *full* `bakeKb`, so anything under the prefix the bake did not write is genuinely stale.

Host objects live **outside** the KB prefix (`kb-artifacts/host/{host}.json`), so a prefix diff cannot find them. A `hosts.json` manifest inside the prefix names the host keys the KB owns; the next bake reads the previous manifest and reaps any hostname it no longer claims. That is what makes a renamed slug or a disconnected custom domain stop answering.

Consequences of the fix worth remembering:
- `KbArtifactReconciler` no longer deletes the prefix before repairing, so `--repair` no longer drops the KB off the edge for the length of a rebake.
- `purgeKb(kbId)` lost its `canonicalHost` argument; it reads the manifest (before deleting the prefix) to find every host key.

Legacy cleanup for anything baked before the fix is still per-KB:
```
APP_ENV=production pnpm --filter backend kb:artifact-bake <kbId> --repair
```

Related: [[project_kb_artifact_bake_pipeline]], [[project_kb_edge_serving_live]], [[project_kb_edge_static_surface]]
