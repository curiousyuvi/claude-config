---
name: feedback-demo-app-is-ui-north-star
description: Knowledge gaps (and screenshot agent) UI must match the demo app (GrooveHQ/helply-prototype) exactly until Tirth sends Figma
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5297b585-30e3-414e-8e5f-0ed29a5a3fce
  modified: 2026-10-21T08:41:05.049Z
---

For knowledge gaps and the screenshot agent UI, the demo app (demo.helply.com, source GrooveHQ/helply-prototype origin/main, components/gaps/*) is the design north star. Ours must look the same: layout, tabs, header, queue rows, brief, article column, footer actions, copy. Only a Figma from Tirth overrides it.

**Why:** 2026-10-21 the user compared my first review screen against the demo and said it looked much different; they want parity, not a reinterpretation.

**How to apply:** port the prototype components structurally (read them from `git show origin/main:components/gaps/<file>.tsx` in ~/Work/Repositories/helply-prototype, local checkout is stale), swap mock data for real API data, keep axis conventions (feature folder, <300-line components, query options, keymap registry). Where axis lacks data the demo shows, say so rather than inventing it. Related: [[project-knowledge-gaps-feature]].
