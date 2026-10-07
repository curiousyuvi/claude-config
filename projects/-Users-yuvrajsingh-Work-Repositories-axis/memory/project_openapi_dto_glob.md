---
name: project_openapi_dto_glob
description: Backend OpenAPI gen resolves response schemas from *.dto.ts; bare contract return types → broken-ref failure in the Backend Build CI job
metadata: 
  node_type: memory
  type: project
  originSessionId: 795a0e99-a211-436b-b6ed-ee06e54baad5
  modified: 2026-10-07T16:24:59.358Z
---

`pnpm --filter backend openapi:generate` (nestjs-openapi, config `openapi.config.ts` → `dtoGlob: 'src/**/*.dto.ts'`) resolves each controller's response schema **by name** from a type exported — as a class OR a plain `export type { X } from '...'` re-export — in some `*.dto.ts` file. A GET controller that returns a bare `shared/schemas/*.contract` type not re-exported from any `*.dto.ts` fails generation with `brokenRefCount>0` / "missing schemas (check dtoGlob patterns)", which fails the **Backend Build** CI job (typecheck/build alone don't catch it).

**Fix:** add `interfaces/<name>.dto.ts` with `export type { FooResponse, BarList } from 'shared/schemas/....contract';` (mirrors `article.dto.ts`'s `export type { ArticleResponse }`) and import the response types from there in the controller. Nested/referenced types (items, nested objects, enums) resolve transitively — only the top-level response types need the re-export. `Record<SomeEnum, number>` mapped types resolve fine. `apps/backend/public/openapi.json` is generated + gitignored (not committed), so it never dirties the tree. Run `pnpm --filter backend openapi:generate` locally to reproduce the CI check. See [[project_run_axis_ci_locally]].

**Second cause, same symptom (2026-10-07, PR #1648):** a response type that is in a `*.dto.ts` but reaches `KbSettings` (= `z.infer<typeof KbSettingsSchema>`, and the schema is a CALL result, `.prefault({})`) crashes ts-json-schema-generator (`TSJ-109 … reading 'flags'` in `CallExpressionParser`), and nestjs-openapi silently reports it as a missing schema. Diagnose in seconds instead of a 2-4 min full run: `node ../../node_modules/.pnpm/ts-json-schema-generator@2.9.0/node_modules/ts-json-schema-generator/bin/ts-json-schema-generator.js --path <file>.dto.ts --type <Name> --tsconfig tsconfig.json --no-type-check` from apps/backend. Fixes: `createZodDto` (what the settings GET does) or `@ApiExcludeEndpoint()` for internal-only responses (the settings preview endpoint). Local full gen needs `NODE_OPTIONS=--max-old-space-size=8192` or it OOMs.
