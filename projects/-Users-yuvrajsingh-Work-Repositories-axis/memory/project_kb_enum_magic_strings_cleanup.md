---
name: project_kb_enum_magic_strings_cleanup
description: KB zod-enum magic-string cleanup — settings enums DONE via as-const companions; iconType/node-type still open
metadata: 
  node_type: memory
  type: project
  originSessionId: fade3e66-a4a5-4e62-9f85-4408b9bc8229
---

Ongoing effort (user, 2026-07-09): replace magic-string comparisons for KB enums with named `as const` companions that derive the zod enum, in `packages/shared/src/schemas/kb-settings.schema.ts`. Every production comparison/default/picker/mapper routes through the const; test fixtures stay literal.

**DONE** (on `ys/feat/kb-panel-native-kb`): all `kb-settings.schema.ts` enums have companions and every KB call site was converted —
- `LayoutStyle` (modern_help_center/documentation/classic_help_center)
- `ThemeMode` (system/light/dark) — incl. internal `ReaderTheme.mode`
- `Alignment` (left/center), `ContentOrder` (collections_first/articles_first)
- `LogoSize` (small/medium/large), `HeroBgType` (solid/gradient/image), `GradientDirection` (linear/radial)

Pattern template: `export const X = { A: 'a', … } as const; export type X = (typeof X)[keyof typeof X]; export const KbX = z.enum([X.A, …]);` then `import { X }` and compare `=== X.A`.

**Still magic-string (possible further pass, NOT yet done)** — KB enums OUTSIDE kb-settings.schema:
- `iconType` (`node.iconType === 'emoji' | 'iconify' | 'image' | 'url'`) in the reader `Icon` component + editors — defined in `kb-authoring.schema.ts`.
- node/hit `type === 'article' | 'collection'` across reader + web tree code.
- Do NOT touch: element text-align (`el.align === 'left'|'right'`, has 'right', not KbAlignment), BlockNote import `item.type === 'image'`, ticket `scope.mode`, and other non-KB `mode`/`type`/`direction`/`size` usages.

Related: [[project_kb_panel_published_only]].
