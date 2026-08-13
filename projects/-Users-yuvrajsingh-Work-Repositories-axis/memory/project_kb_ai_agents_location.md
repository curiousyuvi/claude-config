---
name: project_kb_ai_agents_location
description: KB AI agent code lives in src/ai/agents (moved out of the KB module per Konrad)
metadata: 
  node_type: memory
  type: project
  originSessionId: d3b79d16-3f98-49cd-863e-4209d7ce9622
  modified: 2026-07-18T05:16:53.579Z
---

Konrad's directive (2026-07-17): all KB AI-agent logic must live under `apps/backend/src/ai/agents/`, NOT inside the knowledge-base domain module — "keep ai agents related logic in one place for better management," "keep the same pattern with the envs (so we could swap models quickly) + separate files for prompts etc."

Done: the KB translator moved from `src/modules/knowledge-base/application/translation/` to `src/ai/agents/kb-translator/`:
- `kb-translator.ts` (@Injectable `KbTranslator`), `plate-translate.ts`(+spec, pure helper), `prompts/translation.prompt.ts` (`buildTranslationSystemPrompt` + language-name helpers), `schemas.ts` (zod + `ArticleTranslation{Input,Output}`), `kb-translator.module.ts` (`KbTranslatorModule` — self-contained, providers+exports `KbTranslator`, imports nothing), `index.ts` barrel.
- Wiring: `KnowledgeBaseModule` imports `KbTranslatorModule` (NOT a bare provider); `KbTranslationService` + `KbTranslationWorkerService` inject `KbTranslator` from the barrel. A dedicated tiny module (not `AiAgentsModule`) avoids a circular dep — `KbTranslator` only needs global `ConfigService`.

**Convention going forward:** new KB AI-agent code (LLM-using) goes in `src/ai/agents/`, following the `ticket-answer`/`copilot` pattern (prompts/ dir, schemas.ts, index.ts barrel). Env-driven model selection is THE pattern — read the model from `configuration.ts` `ai.*` (translator: `ai.kbTranslationModel` ← `KB_TRANSLATION_MODEL`), never hardcode. Note: KB *retrieval/ingestion* AI (RAG, reranker, qdrant, embeddings) already lived under `src/ai/store|workers|tools`; the translator was the only LLM code still inside the KB module. Related: [[project_kb_editor_autosave_flush]].
