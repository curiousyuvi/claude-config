---
name: reference-notion-fetch-headroom-workaround
description: "Large Notion pages come back as a `<<ccr:...>>` placeholder through the Headroom proxy; refetch with include_file_urls + instructions_version so the result spills to a file instead"
metadata:
  node_type: memory
  type: reference
  originSessionId: 95ec2c73-358c-4e03-a22e-92cff3042ffc
  modified: 2026-10-20T15:54:29.935Z
---

Through the Headroom proxy, `notion-fetch` (and even short search highlights) can return only `<<ccr:HASH,html,NKB>>`, and `headroom_retrieve(HASH)` sometimes returns the placeholder itself (worked once on 2026-10-20, failed later the same day).

Workaround that worked 2026-10-20: call `notion-fetch` with `include_file_urls: true` and `instructions_version: "0.0.2"`. The result exceeded the token cap and Claude Code saved it to a `tool-results/*.txt` file uncompressed. Parse it with a script file (inline `node -e` / python heredocs are blocked by lean-ctx): the file is JSON whose `text` field holds the page markdown. Script used: scratchpad `extract-notion.mjs` (JSON.parse, take `.text`, JSON.parse again for `.text`).

Saved copies: `~/.axis/knowledge-gaps/jj-final-plan-reference.md` (JJ's Topics + Gaps plan, v1.4).
