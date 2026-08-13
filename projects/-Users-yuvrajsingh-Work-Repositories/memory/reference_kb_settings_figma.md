---
name: reference_kb_settings_figma
description: Figma source for the KB settings UI — file key, URL, key node IDs, token map
metadata:
  node_type: memory
  type: reference
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

KB settings dashboard design = Figma file **"ID - Dashboard"**, fileKey `msmcrEnrKJuoECfgXMroVQ`, root settings frame node **61:3413**.
URL: https://www.figma.com/design/msmcrEnrKJuoECfgXMroVQ/ID---Dashboard?node-id=61-3413

PULL IT via the `claude_ai_Figma` MCP — don't eyeball screenshots ([[feedback_figma_pull_source]]). `get_design_context` for structure/sizes/tokens; `get_screenshot` → curl → Read for visuals; `get_metadata` is huge (parse in a subagent with jq).

Key nodes:
- **Sidebar** 59:2579 (each page embeds its own copy). Groups: Settings (General, Header & Footer) / Customize (Layout, Labels, Branding, Presets) / Publishing (Domains and redirects, SEO, Advanced) / Languages (Supported languages, Localization). Header = KB switcher + collapse icon + "Search settings"; then a "Back to editing articles" banner (bg base/sidebar #fafafa, border-y, px-4 py-3). Group label text-xs medium opacity-70; items h-8 gap-2, icon 16px + text-sm regular foreground.
- **Section pages** (1440×800): General 47:690 · Header & Footer 58:1158 · Layout 59:2520 · Labels 59:3491 · Branding 60:454 · Domains 61:533 · SEO 61:2168 (title "Search engine optimization") · Advanced 61:2884. **Presets / Supported languages / Localization are sidebar-only** (no page → "coming soon" stubs are correct). Page chrome = full-width title header (border-b) + centered content column (~max-w-3xl); header title left, cards centered.
- **Layout-style picker** (in Layout page): row 59:3284; cards Help centre 59:3283, Documentation 59:3282, Help centre (Legacy) 59:3281. Selected card border = base/primary #171717; each card = wireframe (browser top-bar + style-specific body) + centered label.

Token map: base/muted #f5f5f5 → `bg-muted` · base/border #e5e5e5 → `border-border` · base/input #e5e5e5 → `border-input` · selected base/primary #171717 → `border-foreground` · base/sidebar #fafafa → `bg-sidebar` · base/foreground #0a0a0a → `text-foreground` · Geist, text-sm 14 / text-xs 12.

NOTE: per-SECTION field designs (e.g. Header & Footer's inline add-link form + reorderable "Added links" list + full social list) are richer in Figma than the Slice-9 build — a remaining match pass. Part of [[project_kb_native_in_axis]].
