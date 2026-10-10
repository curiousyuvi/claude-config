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

**Figma read (2026-10-10):** dialog 1312x852; header 76px; left preview in a rounded bordered panel with NO browser chrome; right panel 320px: Device select + Page select, fields, footer Cancel + "Save changes" (disabled until dirty). "Preview mode" button only on Header & Footer, Layout, Labels, Branding (not General/Domains). Panel contents: H&F = CTA fields + notice "Adding header, footer, and social media links through preview mode is not supported."; Layout = layout cards + Alignment; Labels = first 5 label fields; Branding = Logo (has "Logo background"/"Logo descriptor" toggles that don't exist in the schema). Plan sent to user for review; awaiting answers.

**User decision (2026-10-10):** side panel shows EVERYTHING on the page that changes the preview (not Figma's subset). Plan then went through thermo-nuclear review. Revised plan: dialog panel renders the page's own section component (no compact copies); KbSettingsCard reads a surface context to hide its Save; footer "Save changes" commits store drafts by kind (settings merged into ONE PATCH via applySettingsDrafts, text upsert, logo update, allSettled); Preview mode disabled while the page has unsaved edits; Domains loses preview, so URL-prefix routing params + useSettledRouting get deleted; chrome/toolbar/history/status chip/dock deleted. Awaiting user go-ahead.
