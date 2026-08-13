---
name: feedback-anthropic-prompt-caching
description: "Anthropic prompt caching is now wired through agents/base.py — cache_control fires on the tool block, system + tools cached together. Cost tracker accounts for cache_creation (1.25×) and cache_read (0.10×) tokens. Don't re-add `cache_control` per-agent."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 79e97dfd-6c88-43e4-a2d4-0f0def85294f
---

Every Anthropic call in this codebase funnels through `agents/base.py::Agent.invoke`, which already attaches `cache_control: {"type": "ephemeral"}` to the trailing tool block. That caches **tools + system** together (Anthropic's prefix order). No per-agent caching code is needed.

**Why:** prompt caching was the biggest single cost lever on this product — for fan-out agents (Disambiguator, WikiGenerator, EntityExtractor, AttribRel, Event) the system prompt + tool schema is identical across every call within a pipeline run, so it should be billed at 0.10× of input price after the first call. Adding cache_control elsewhere risks creating a second cache breakpoint inside an already-cached prefix, which silently fragments cache entries and burns the 1.25× write penalty for no benefit. Discovered 2026-05-26 while cutting Sonnet spend on chapter imports.

**How to apply:**
- For a new agent, just inherit from `Agent` — no extra wiring.
- The minimum cacheable prefix is 1024 tokens (Sonnet/Haiku). If a new agent's `system + tool_schema` is shorter, caching simply won't fire. Don't pad the prompt with filler — instead either include the project's entity-type catalog (see `agents/_entity_type_catalog.py::format_entity_type_catalog`) when it's contextually useful, or accept that this agent's tiny prefix doesn't benefit.
- Token breakdown is captured per-call in `ai_operations.metadata.cache_creation_tokens` and `cache_read_tokens`. Audit hit rates with:
  ```sql
  SELECT agent_name,
         SUM((metadata->>'cache_creation_tokens')::int) AS writes,
         SUM((metadata->>'cache_read_tokens')::int)     AS reads
  FROM ai_operations
  WHERE pipeline_run_id = '<run>'
  GROUP BY agent_name;
  ```
  If `reads = 0` on a fan-out agent, the prefix is under 1024 tokens.

Related: [[feedback-realtime-rls-setauth]], [[feedback-commit-cadence]]
