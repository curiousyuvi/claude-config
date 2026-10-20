---
name: feedback-track-jj-topics-merges
description: "During knowledge-gaps work, periodically fetch master and merge in JJ's Topics changes, fixing conflicts"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 95ec2c73-358c-4e03-a22e-92cff3042ffc
  modified: 2026-10-20T17:40:17.806Z
---

While building knowledge gaps on `ys/feat/knowledge-gaps`, periodically run `git fetch origin master` and check `git log HEAD..origin/master` for Topics work (topic-insights module, shared topic-insights files, ticket topic columns, anything from JJ). When something lands, merge master into the branch and fix conflicts (watch `.snapshot-axis.json` and `entities.generated.ts`, see [[project-mikroorm-snapshot-merge-corruption]]).

**Why:** the user asked for it on 2026-10-20; gaps reads Topics through `GapTopicsPort` and the signals contract, so JJ's changes can break or replace our stand-ins.
**How to apply:** check at the start of each work block and before every commit; after merging, re-run gaps tests, typecheck and the migration drift check, and update the stand-in adapter if JJ's real implementation landed. See [[project-knowledge-gaps-feature]].
