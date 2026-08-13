---
name: feedback_tailwind_no_arbitrary_px
description: "In apps/web Tailwind, never use arbitrary [Npx] values — convert to the spacing scale (px ÷ 4) or a named token"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fade3e66-a4a5-4e62-9f85-4408b9bc8229
---

Do not use arbitrary pixel values in Tailwind classes (`h-[118px]`, `gap-[3px]`, `w-[77px]`, `left-[41px]`, `rounded-[2px]`). Convert them to the theme spacing scale.

**Rule:** the repo is on **Tailwind v4**, where 1 spacing unit = `0.25rem` = **4px** and the scale accepts fractional numbers. So divide the px by 4 and use that as the scale value:
- `h-[118px]` → `h-29.5`  (118 ÷ 4)
- `h-[5px]` → `h-1.25`
- `gap-[3px]` → `gap-0.75`
- `w-[77px]` → `w-19.25`
- `left-[41px]` → `left-10.25`, `top-[26px]` → `top-6.5`, `top-[18px]` → `top-4.5`

Use a **named token** when one maps exactly rather than a raw number: `rounded-[2px]` → `rounded-xs`.

**Why:** consistent, theme-driven spacing instead of magic px; matches the design system; keeps classes readable. (Established by the user, who reworked `kb-layout-section.tsx`'s wireframe skeletons this way — 2026-07-09.)

**How to apply:** when writing OR reviewing any `apps/web` Tailwind, replace every `[Npx]` with `N/4` on the scale (or the nearest named token); treat leftover arbitrary `[Npx]` as a review finding. Values are behavior-preserving (N/4 × 4px = N px).
