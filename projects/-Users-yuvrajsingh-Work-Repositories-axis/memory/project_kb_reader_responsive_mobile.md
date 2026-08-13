---
name: project_kb_reader_responsive_mobile
description: Published KB reader mobile responsiveness — CSS-only drawer/menu at 768px (InstantDocs parity)
metadata: 
  node_type: memory
  type: project
  originSessionId: e2d6bdd1-c1eb-4450-96a2-d76764ad9a98
  modified: 2026-07-21T09:30:31.095Z
---

Published-KB reader mobile nav was fixed to match InstantDocs (ref repo `/Users/yuvrajsingh/Work/Repositories/instantdocs`, layouts: DOCUMENTATION→`documentation`, HELP_CENTRE→`modern_help_center`, GROOVE→`classic_help_center`). Breakpoint is **767.98px** (InstantDocs `md`/`useIsMobile`=768), NOT the old 820px.

**Two mobile behaviors, both PURE CSS** (reader is server-rendered HTML under strict CSP `script-src 'self'` — NO inline JS; interactivity = CSS checkbox/`<details>` or a `/_kb/*.js` script only):
- **Documentation sidebar → off-canvas drawer.** `#kb-doc-nav-toggle` (sr-only focusable checkbox, first child of `.kb-doc`) + `<label>` hamburger (`PanelLeftIcon`) in the top-nav + a `.kb-drawer-scrim` label. `:checked ~ .kb-doc-sidebar{transform:translateX(0)}`. Also a mobile-only `.kb-doc-topnav-brand` (the rail carries the logo on desktop). Replaced the old broken "sidebar becomes 60vh stacked block".
- **Help-center header nav+CTA → dropdown menu.** In `HeaderActions`: `#kb-menu-toggle` + `.kb-menu-btn` (`MenuIcon`) + `.kb-header-menu` (nav links + CTA). Desktop = inline row; mobile = absolute dropdown. Language switcher + search box stay outside the collapse.

**Key trick:** each navigation is a fresh server-rendered document → the checkbox starts unchecked → the drawer/menu **auto-closes on link click, no JS needed**.

**Help-center horizontal gutter (must all align):** InstantDocs help-center uses `px-2` (8px) + `max-w-[972px] mx-auto` for header, hero, AND home content — they line up at 8px. Article/collection/search use `px-4` (16px, wider prose gutter). Axis had drifted to header 24px / hero 8px / content 16px (misaligned). Fix: the shared gutter is now ONE token `--kb-hc-gutter` (:root, 0.5rem) consumed by `.kb-hc-hero .kb-header` (`padding:14px var(--kb-hc-gutter)`), `.kb-hc-hero-inner` (base + 640 variant), and `.kb-layout-help_center.kb-hc-home` — change the token, all move together (don't reintroduce scattered literals). Home gets a `kb-hc-home` class (kb-reader-jsx.tsx help-center `<main>` when `view.kind==='home'`); article/collection stay 1rem (16px). Verify by measuring `getBoundingClientRect().left` of `.kb-header .kb-logo` / `.kb-hc-hero-text` / `.kb-hc-hero-inner .kb-search` / `.kb-main .kb-content` — home = all 8, article = 8/8/8/16.

Files: `kb-reader-chrome.tsx` (HeaderActions + DocumentationShell JSX), `kb-reader.css` (`@media (max-width:767.98px)` block + `.kb-hc-hero .kb-header`/`.kb-hc-home` gutters), `kb-reader-jsx.tsx` (`kb-hc-home` modifier), `kb-reader-icons.tsx` (`MenuIcon`,`PanelLeftIcon`). CSS is `readFileSync` at module-load from `dist/` (nest-cli `watchAssets:true` copies `kb-reader.css`); chrome+CSS render live per request (no re-publish needed — only the article `.kb-prose` body is stored publish-time HTML). Also fixed doc content max-width 40rem/46rem→**42rem/48rem** (InstantDocs `xl:max-w-2xl 2xl:max-w-3xl`). Card grids / hero / TOC-hide(<1280) / breadcrumb / prev-next already matched — no change. Verify via [[project_kb_reader_offline_render_verify]]. INVARIANT: sr-only toggle checkbox must NOT be `display:none` (kills focusability); keep it clip-rect sr-only so keyboard Space still toggles.
