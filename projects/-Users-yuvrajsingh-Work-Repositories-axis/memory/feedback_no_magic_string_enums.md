---
name: feedback_no_magic_string_enums
description: "Define string enums as `as const` companions and compare via named members — never magic-string literals"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fade3e66-a4a5-4e62-9f85-4408b9bc8229
---

When adding or touching a string enum in this project — especially zod enums (the `Kb*` schemas in `packages/shared/src/schemas/`, but this applies anywhere) — do NOT scatter bare string literals. Define a named `as const` companion and route the zod schema + every comparison/default/option through it.

**Template** (matches AGENTS.md "as const objects with companion types"):
```ts
export const Thing = { Foo: 'foo', Bar: 'bar' } as const;
export type Thing = (typeof Thing)[keyof typeof Thing];
export const KbThing = z.enum([Thing.Foo, Thing.Bar]); // when a validator is needed; derived, can't drift
```
Then everywhere: `import { Thing }` and compare `x === Thing.Foo` (also `.default(Thing.Foo)`, picker `value={Thing.Foo}`, mapper records `{ …: Thing.Foo }`). Test fixtures may stay string literals.

**Why:** magic strings drift from the enum, hide typos (no compile error), and scatter the same literal across many files — exactly what accumulated in the KB settings code and had to be cleaned up in bulk. A named member is compile-checked, greppable, and rename-safe.

**How to apply:** write new enums this way from the start; when reviewing/editing any file, treat a bare `=== 'literal'` (or literal default/option) against a known enum as a finding and route it through the companion. Reference implementation: the KB settings enums (`LayoutStyle`, `ThemeMode`, `Alignment`, `ContentOrder`, `LogoSize`, `HeroBgType`, `GradientDirection`) in `kb-settings.schema.ts`. See [[project_kb_enum_magic_strings_cleanup]] for what's done vs still open (iconType, node type).
