---
name: feedback_figma_pull_source
description: "When given a Figma design, pull it via the Figma MCP and build to the source — don't eyeball screenshots"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

When Yuvraj gives a Figma design (a link, or "match the Figma"), pull the actual nodes via the `claude_ai_Figma` MCP and build to the source in one pass: `get_design_context` for structure/sizes/design tokens, `get_screenshot` (→ curl → Read) for visuals.

**Why:** On the KB settings UI he had to manually point out mismatch after mismatch (back-button band + bg, page headers, content centering, layout-skeleton diagrams) because I was eyeballing his screenshots instead of reading the Figma — even though [[reference_kb_settings_figma]] already had the fileKey + node IDs. He was frustrated: "why can't you match everything correctly yourself."

**How to apply:** If you only have a node id, ask for the file link (the MCP needs the fileKey). Map Figma design tokens to the app's Tailwind tokens. Match the shared chrome + every flagged component precisely from the source before declaring done — don't iterate screenshot-by-screenshot.
