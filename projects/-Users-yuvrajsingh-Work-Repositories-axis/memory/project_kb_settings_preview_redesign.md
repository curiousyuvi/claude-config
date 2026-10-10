---
name: project_kb_settings_preview_redesign
description: "NEXT TASK (2026-10-10): rebuild the KB settings live preview to Shreyansh's new Figma design — Preview mode button opens a full-screen dialog with the KB preview + that page's settings in a side panel"
metadata:
  node_type: memory
  type: project
  originSessionId: 4339431e-433d-4efe-89ab-6d716a453cb6
  modified: 2026-10-10T13:51:40.601Z
---

PR #1648 (settings live preview + /search removal) is MERGED. Next: redesign the preview UI per Figma from Shreyansh (designer). Not started yet; user compacted first.

**Design (from user's WhatsApp screenshot + Figma):**
- Each visual settings section header gets a dark "Preview mode" button (replaces today's docked side panel + Preview toggle).
- Clicking opens a large near-full-screen Dialog titled "Preview" / "Preview how your knowledge base looks and feel.", close X top right.
- Left: the KB preview (the existing renderer/frame). Right: a settings side panel for THAT page (e.g. Layout: Desktop/device select, page select "Home page", layout cards Help centre / Documentation / Help centre (Legacy), Alignment select "Centre aligned"), footer with Cancel + "Save changes".
- So settings are edited INSIDE the dialog; Save changes persists.

**Figma (file msmcrEnrKJuoECfgXMroVQ "ID---Dashboard"; file has much old UI, use only these):**
- 594-4197, 594-2902, 594-5407, 594-6084 (frames), 61-3413 (whole group)
- URL form: https://www.figma.com/design/msmcrEnrKJuoECfgXMroVQ/ID---Dashboard?node-id=594-4197&m=dev
- Figma MCP is `mcp__claude_ai_Figma__*` (get_design_context / get_screenshot / get_metadata); load via ToolSearch.

**Existing code to reuse:** `apps/web/src/features/knowledge-base/components/kb-settings/preview/` (renderer, frame-buffer, use-kb-preview, store with `unsaved` drafts, browser chrome) + backend `GET .../settings/preview`. See [[project_kb_settings_live_preview]].
