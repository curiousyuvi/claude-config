---
name: project-github-integration-plan
description: Next gaps feature = GitHub integration via Albato; decided no long-lived customer repo copies; Albato requirements PDF sent via PK
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-02T16:35:08.433Z
---

Started 2026-11-02, after #1810 merged. GitHub feeds: scheduled article verification, gaps citing real code, PR merge leads to gap + article update (+ screenshot rerun), code hints for the screenshot agent.

Decided: no long-lived copy of customer repos (user's call). Model is Ferndesk/Promptless/CodeRabbit style: diff-first on merge, agent reads GitHub live pinned to a commit SHA, store only anchors {repo, path, blob_sha} + PR refs + summaries, tree-SHA change detection for scheduled checks, ephemeral shallow/sparse clone only for deep audits, blob-SHA cache with hours TTL. No GitHub code search API (10/min, default branch only).

Ask to Albato (PDF ~/Downloads/helply-github-integration-requirements.pdf, source HTML in job tmp): GitHub App install, read-only token exposed via credential API (main ask); fallback = raw passthrough action; webhooks pull_request, push, delete, installation(_repositories); MCP lowest. User sends via PK, who talks to Albato.

Deep research 2026-11-02 (non-PR code reading), recommended design:
- Fetch tiers: 1-10 files REST raw by commit SHA; 10-300 files trees API + GraphQL alias batches (~50/query, text cut at 512KB, check isTruncated); whole-repo = git binary `clone --depth 1 --filter=blob:none --no-checkout --single-branch` + sparse/backfill into tmp, delete after. isomorphic-git/nodegit lack partial clone. Fresh token per git cmd (1h expiry), serialize clones per repo, hooks/LFS off.
- Agent: grep/glob/ranged reads with hard caps (SWE-agent ACI), no embeddings (Cursor turned them off Jul 2026, Claude Code dropped RAG), no LSP/SCIP per job. Seeds from locale/i18n files, routes, OpenAPI, flags, e2e titles. Cheap model scouts (<=16 calls) and writes <=2k handoff; strong model judges handoff only. Target < $0.10 per article check.
- Scheduled verification funnel: rolling 1/30 per day, tree-SHA gate, deterministic checks (quoted UI strings vs locale files, schemas, limits), LLM only on claims whose anchored span changed (span_hash, not just blob_sha), re-anchor fallback. Tables article_claim / claim_anchor / repo_state.
- Privacy: keep paths, SHAs, symbol names, i18n keys, HMAC'd hashes; never code embeddings (Vec2Text inverts); treat AI summaries of code as code.

**Why:** prod scale + customer trust; Ferndesk's security page promises no persistent code index.
**How to apply:** design the integration around these choices; don't propose indexing/embedding customer code unless live reads prove too slow. Related: [[project-knowledge-gaps-feature]].
