---
name: project_openapi_dto_glob
description: Backend OpenAPI gen resolves response schemas from *.dto.ts; bare contract return types → broken-ref failure in the Backend Build CI job
metadata: 
  node_type: memory
  type: project
  originSessionId: 795a0e99-a211-436b-b6ed-ee06e54baad5
---

`pnpm --filter backend openapi:generate` (nestjs-openapi, config `openapi.config.ts` → `dtoGlob: 'src/**/*.dto.ts'`) resolves each controller's response schema **by name** from a type exported — as a class OR a plain `export type { X } from '...'` re-export — in some `*.dto.ts` file. A GET controller that returns a bare `shared/schemas/*.contract` type not re-exported from any `*.dto.ts` fails generation with `brokenRefCount>0` / "missing schemas (check dtoGlob patterns)", which fails the **Backend Build** CI job (typecheck/build alone don't catch it).

**Fix:** add `interfaces/<name>.dto.ts` with `export type { FooResponse, BarList } from 'shared/schemas/....contract';` (mirrors `article.dto.ts`'s `export type { ArticleResponse }`) and import the response types from there in the controller. Nested/referenced types (items, nested objects, enums) resolve transitively — only the top-level response types need the re-export. `Record<SomeEnum, number>` mapped types resolve fine. `apps/backend/public/openapi.json` is generated + gitignored (not committed), so it never dirties the tree. Run `pnpm --filter backend openapi:generate` locally to reproduce the CI check. See [[project_run_axis_ci_locally]].
