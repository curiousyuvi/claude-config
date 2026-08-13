---
name: project_mikroorm_partial_load_optional_types
description: "MikroORM em.find with fields:[...] types nullable columns as string|null|undefined, so params fed by them must stay optional"
metadata: 
  node_type: memory
  type: project
  originSessionId: 43df3a8b-a611-47bd-826a-c0ee7b1b6097
---

When a value comes from `em.find(Entity, where, { fields: [...] })` (partial load), MikroORM types each **nullable** projected column as `string | null | undefined` (the `Loaded<Entity, …, "col", never>` shape adds `| undefined`), even though the entity property itself is `string | null`. Non-nullable columns (e.g. a `p.string()` title) stay `string`.

**Consequence:** a helper/param that receives partial-loaded rows must keep those fields **optional** (`description?: string | null`) or explicitly `| undefined`. "Tightening" them to required `string | null` (or `Pick<Entity, …>`, since the entity type lacks the `| undefined`) fails typecheck — this bit the `resolveNodeSeo` param in `kb-node-seo.service.ts`. The optionality there is NOT a hidden-invariant smell; it's required by the ORM's projection type.

**Why:** partial load means the field may be absent at runtime, so the type reflects that. The real "did we select it" contract lives in the `fields: [...]` array, not the type.

Related: [[feedback_run_lint_typecheck]] — this is exactly the class of thing typecheck catches that a code-quality reviewer reasoning from source alone will miss.
