---
name: radix-tooltip-needs-provider
description: Axis web has no global TooltipProvider — a Radix Tooltip without one throws and silently blanks its whole subtree, making controls look inert
metadata:
  type: project
---

`apps/web` has NO app-level `TooltipProvider`. Components that use `Tooltip` wrap their own (support-hours,
kb-tree, message actions). Miss it and Radix throws `Tooltip must be used within TooltipProvider`, React
unmounts that subtree, and the UI renders *partially* — siblings without tooltips still work, so it reads as
"these buttons do nothing" rather than as a crash. Cost a full round trip on the snapshot editor toolbar
(2026-09-21); fixed by putting the provider inside the toolbar shell itself.

**How to apply:** any new toolbar/menu using `Tooltip` gets its own `TooltipProvider` at its root. Prove it
with a jsdom render test — stub `ResizeObserver` and the pointer-capture methods, which jsdom lacks and the
Radix slider/select need. See [[recorder-snapshots-plan]].
