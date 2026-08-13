---
name: prefer-library-options
description: "Check a library's own options/APIs before hand-rolling; don't patch symptoms in bespoke code"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4c5af0c9-ed68-43fe-a98c-58a7a45b869f
  modified: 2026-07-30T07:18:38.007Z
---

Before writing bespoke handling around a library, READ ITS OPTIONS AND EXPORTED TYPES FIRST (`dist/index.d.ts`, the options type, the exported helpers). Use the managed switch when one exists. Only hand-roll what the library genuinely does not support, and say in a comment WHY there was no option.

**Why:** the user called this out directly ("are we not using platejs mcp recommended code, why are we self handling all this... we want managed, code judo code, not such nit-picking self handled code"). I had hand-written 7 mark rules and per-node list bookkeeping that `@platejs/markdown` exposes as plain options, because I never opened `SerializeMdOptions`. Symptom-patching bespoke code also caused a chain of follow-on bugs (character references, loose lists), each needing another patch.

**How to apply:** grep the package's `.d.ts` for the options type and exported helpers before the first line of workaround code. Also relevant: a `plate` MCP server is connected (`mcp__plate__*`) for Plate registry items. Related: [[kb-markdown-serialization-managed-vs-hand-rolled]].
