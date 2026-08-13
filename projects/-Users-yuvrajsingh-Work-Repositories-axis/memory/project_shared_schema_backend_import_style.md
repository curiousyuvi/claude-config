---
name: project_shared_schema_backend_import_style
description: "Shared schema files imported by the backend must self-reference siblings via bare `shared/...`, not relative `./x.js`"
metadata: 
  node_type: memory
  type: project
  originSessionId: dd1289fc-94e0-42f6-b729-237bd5916549
  modified: 2026-07-20T06:49:29.252Z
---

A `packages/shared/src/schemas/*.ts` file that the **backend** imports must reference sibling shared files with the bare self-reference specifier (`import { X } from 'shared/schemas/foo.schema'`), NOT a relative `./foo.schema.js`.

**Why:** the backend dev server (`start:dev:portless`) runs the shared package's `.ts` source directly via `node --experimental-strip-types`, which strips types but does NOT map a relative `./foo.schema.js` specifier to the on-disk `.ts` — so it throws `ERR_MODULE_NOT_FOUND` for the non-existent `.js`. The bare `shared/...` specifier resolves through the package `exports` map (`"./*": "./src/*.ts"`) to the real `.ts`. This is why `ticket-bulk-actions.schema.ts` imports `from 'shared/enums'`.

Web-only shared files (e.g. `kb-authoring.contract.ts`) can still use relative `./x.js` because Vite resolves `.js`→`.ts`; the two styles coexist. When unsure, use the bare `shared/...` form — it works for tsc (self-reference), Vite, AND the backend runtime.

Verify runtime resolution with: `node --experimental-strip-types --input-type=module -e "import('file://<abs path to .ts>').then(m=>console.log(Object.keys(m)))"`. See [[project_openapi_dto_glob]] for the related shared-contract/OpenAPI gotcha.
