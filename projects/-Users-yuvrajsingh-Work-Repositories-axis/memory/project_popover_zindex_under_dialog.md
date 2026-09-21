---
name: popover-zindex-under-dialog
description: A Popover inside a Dialog needs z-50 — a lower z-* on PopoverContent wins via tailwind-merge and hides it behind the z-50 DialogContent
metadata:
  type: project
---

`apps/web` `DialogContent` is `z-50`. `PopoverContent` ships `z-50` too, but any `z-*` passed in `className`
beats it through `cn`/tailwind-merge. Pass `z-20` (e.g. copied from another codebase) and the portaled
popover still OPENS — `document.querySelectorAll('[data-radix-popper-content-wrapper]').length` is 1 — but
paints behind the dialog, so it reads as "the button does nothing".

**Why:** cost two rounds on the snapshot editor toolbar (2026-09-21). jsdom has no stacking context, so
render/click tests pass; assert on the CLASS instead.
**How to apply:** never set `z-*` on `PopoverContent` inside a dialog. Diagnose "button does nothing" by
counting popper wrappers first — 1 means it opened and is hidden, 0 means the trigger never fired.
See [[radix-tooltip-needs-provider]], [[recorder-snapshots-plan]].
