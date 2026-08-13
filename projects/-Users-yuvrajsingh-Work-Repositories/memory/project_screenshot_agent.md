---
name: Screenshot agent for InstantDocs
description: New agent project at GrooveHQ — drives a browser to capture/annotate screenshots and inject them into KB articles. Ferndesk-inspired. CTO-assigned 2026-05-11.
type: project
originSessionId: bcef0bbe-dab8-4443-8005-65b8e65e1a84
---
**What:** New Python agent that reads a draft InstantDocs KB article, logs into the customer's product with stored credentials, captures the screenshots the article needs, annotates them (arrows, highlights, blur), and injects them as image blocks into the draft for human review. Inspired by Ferndesk's automated-screenshots feature (https://www.youtube.com/watch?v=LAl3MVOQUOk).

**Why:** Competitive parity with Ferndesk on AI-driven KB authoring. Solves the "stale screenshots" pain point in serialized doc maintenance.

**How to apply:**
- Plan file: `/Users/yuvrajsingh/.claude/plans/my-cto-has-told-humming-stallman.md`
- Two goals per CTO: (1) standalone demo spike to iterate on, (2) full integration into InstantDocs.
- Yuvraj decided (2026-05-11): new repo `screenshot-agent`, browser-use lib for v1, call ID's existing `/api/render-image-with-elements` Remotion pipeline for annotations, full end-to-end integration with InstantDocs from v1 (not bare-bones).
- Sister project: knowledge-gap (`/Users/yuvrajsingh/Work/Repositories/knowledge-gap`) — same Python/FastAPI/Pydantic AI/DBOS stack; reuse InstantDocs API client (`knowledge_gap/core/instantdocs/`), BlockNote models (`pydantic_agent/agents/writer.py`), and the `decrypt_integration_response` crypto pattern.
- InstantDocs repo (`/Users/yuvrajsingh/Work/Repositories/instantdocs`) already has the image-block annotation infra: `src/blocknote/blocks/custom-image.tsx`, `src/components/image-editing-modal.tsx`, `src/pages/api/render-image-with-elements.ts` — agent reuses these.
- Open CTO questions tracked in the plan file ("Questions for CTO" section).
- **Dev test corpus** cloned from prod help-center KB (`help.instantdocs.com`) on 2026-05-11: dev workspace id `ws_sa_lx2gekzptks0xblq0f`, KB id `kb_sa_h1ajeb459x8xys3uoy`, slug `screenshot-agent-test-20260511t114622z`. 26 collections, 138 published pages, owned by Yuvraj's dev user. Snapshot (video-frame) blocks stripped post-clone; 551 blocks across 126 pages removed.
- **Target page for iterative testing**: "Domains & Redirects" — page id `pg_sa_hfmo8hshavxyxm8sur`, slug `domains-and-redirects`. Yuvraj's workflow: agent runs against this page, he manually deletes the resulting image blocks before each next iteration.
- Use this corpus as the agent's article-context source when wiring real InstantDocs API calls in Phase 2/3.
