---
name: project-github-integration-plan
description: Next gaps feature = GitHub integration via Albato; decided no long-lived customer repo copies; Albato requirements PDF sent via PK
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-02T16:24:44.838Z
---

Started 2026-11-02, after #1810 merged. GitHub feeds: scheduled article verification, gaps citing real code, PR merge leads to gap + article update (+ screenshot rerun), code hints for the screenshot agent.

Decided: no long-lived copy of customer repos (user's call). Model is Ferndesk/Promptless/CodeRabbit style: diff-first on merge, agent reads GitHub live pinned to a commit SHA, store only anchors {repo, path, blob_sha} + PR refs + summaries, tree-SHA change detection for scheduled checks, ephemeral shallow/sparse clone only for deep audits, blob-SHA cache with hours TTL. No GitHub code search API (10/min, default branch only).

Ask to Albato (PDF ~/Downloads/helply-github-integration-requirements.pdf, source HTML in job tmp): GitHub App install, read-only token exposed via credential API (main ask); fallback = raw passthrough action; webhooks pull_request, push, delete, installation(_repositories); MCP lowest. User sends via PK, who talks to Albato.

**Why:** prod scale + customer trust; Ferndesk's security page promises no persistent code index.
**How to apply:** design the integration around these choices; don't propose indexing/embedding customer code unless live reads prove too slow. Related: [[project-knowledge-gaps-feature]].
