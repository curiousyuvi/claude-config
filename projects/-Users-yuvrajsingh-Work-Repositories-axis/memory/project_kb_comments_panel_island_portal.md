---
name: project_kb_comments_panel_island_portal
description: "Peer-island right panels use AppShell useShellRightRail portal (display:contents host), not a border-l side-pane; convention for new right rails"
metadata: 
  node_type: memory
  type: project
  originSessionId: 54cc5d59-d550-4f7b-9295-f3495adbdfcb
  modified: 2026-07-27T08:44:20.304Z
---

To render a panel as its OWN island to the right of `<main>` (on the soft `bg-sidebar` page bg, gap-separated, own `rounded-xl border border-sidebar-border` card) rather than a `border-l` side-pane inside the main card: use `useShellRightRail()` from `@/shared/components/app-shell` and `createPortal(panel, rightRail)`. AppShell hosts a `<div className="contents" ref={setRightRail}>` as a peer of `<main>`; `display:contents` means the portaled panel becomes a peer flex item of the page row (gets the row's `gap-2`) only while mounted — nothing/no phantom gap otherwise. Fall back to inline render when the host is null (tests).

**Why:** the KB comments panel state lives in the view (below the router Outlet); AppShell is above it. Portal keeps state in place while positioning the DOM as a sibling of `<main>`. Chosen over the `data-borderless-shell` island pattern (company/contact detail pages) because that would require restructuring the complex KB editor/TOC/translations layout — the portal leaves it untouched (lower regression risk, same visual per Figma 45-136).

**How to apply:** reuse `useShellRightRail` for any future peer-island right panel; don't reinvent or go back to `border-l`. Matches [[project_kb_comments_architecture]]. Comments panel is mounted (and portals) from article/collection/both homepage modes; see [[project_kb_panel_published_only]].
