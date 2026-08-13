---
name: LoreWeaver design system + brand asset locations
description: Pointers to the authoritative design spec, logo files, and typed theme tokens. Read these before doing any UI work.
type: reference
originSessionId: 79e97dfd-6c88-43e4-a2d4-0f0def85294f
---
The LoreWeaver design system is fully documented and committed to the repo. **Don't infer brand/UI decisions — read the canonical files.**

## Where to look

- **Full spec (read first for any UI work)**: `docs/design-system.md`
  - Brand foundation, color tokens (dark + light), typography (5 fonts), spacing scale, components, motion, citation pattern
- **Typed code tokens**: `loreweaver-web/app/lib/theme.ts`
  - Import from here in any component code; never hardcode hex values
- **Logo source files**: `docs/brand/`
  - `logo-mark.png` (480×480 master, transparent bg)
  - `logo-presentation.jpg` (designer reference, NOT for production)
- **App-deployed logo + favicons**: `loreweaver-web/public/`
  - `logo-mark.png`, `favicon-16/32/48.png`, `apple-touch-icon.png`, `icon-192/512.png`
- **Reference UI**: 21 Banani-generated JPEGs from May 2026 covering every screen. User originally placed at `~/Downloads/banani-ui-export/` but those may have moved. Designs were reviewed and approved with notes captured in `docs/design-system.md`.

## Quick recall (so I don't re-research)

- **Aesthetic**: "Twilight Library" — literary, calm, dark-first. Not TTRPG/game-fantasy. Closer to Penguin Classics / Linear.
- **Logo**: woven labyrinth/spiral on warm-gold rounded square. Designed by user.
- **Wordmark font**: Hedvig Letters Serif (logo only — never used elsewhere).
- **App fonts**: EB Garamond (headings), Inter (UI), Lora (prose), JetBrains Mono (logs/quotes).
- **Accent**: gold `#C9A75F`, used SPARINGLY for primary CTAs + citation links.
- **Citation pattern**: `(Chapter 3)` rendered as italic EB Garamond gold — sacred typography. Every cited fact uses this exact treatment.
- **Mode**: dark default, light is a toggle.
- **One primary CTA per screen.** No purple/teal accent introductions allowed.

## Pending asset work

- SVG version of the spiral mark (currently only 480×480 PNG)
- Horizontal lockup as single SVG (mark + Hedvig wordmark)
- 1200×630 Open Graph image for social link previews
- Mobile variants for Reader View, Wiki Entity Detail, Ask Your Story (Banani only produced desktop)

## Why this lives in memory

The design system is committed to the repo (canonical location), but pinning a memory entry means I don't have to re-discover where things are or re-read 21 JPEGs of UI mockups every session. When any UI question comes up: read the doc, then proceed.
