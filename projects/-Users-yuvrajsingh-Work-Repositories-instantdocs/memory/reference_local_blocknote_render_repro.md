---
name: local-blocknote-render-repro
description: How to reproduce a "Failed to render blocks to HTML" publish error locally with ServerBlockNoteEditor under tsx
metadata:
  type: reference
---

To render a page's stored block JSON locally with the same server editor the `/api/blocknote/render` route uses:

- Run with `npx tsx --env-file=.env --import <css-register.mjs> script.ts`. The register file calls `register("./css-loader.mjs", import.meta.url)` and the loader returns `export default {}` for `.css` imports, because `@/helper/article-schema` pulls in highlight.js CSS.
- Set `globalThis.React = React` before importing `@blocknote/server-util`, or custom block renders fail with "React is not defined".
- Read the row with `@planetscale/database` `Client.execute` on `PageVariant (pageId, locale)`. The project's Prisma client needs the PlanetScale adapter and does not load `.env` under tsx.
- The permission classifier denies production DB reads in my shell. The user runs that one step in their own terminal (without a leading `!`) and tees output to the scratchpad. Everything after that runs locally on the saved JSON. The JSON is customer content: never publish or edit that page, and delete the saved copies when done.

**Why:** Sentry only shows the outer "Failed to render blocks to HTML". The real exception lives in the render route, which used to swallow it (fixed Nov 2026 to report the message and capture to Sentry).

Local `.env` has `NEXT_PUBLIC_ENV=production`, so a server-side `getClientBaseUrl()` self-call targets app.instantdocs.com. Override `NEXT_PUBLIC_ENV=development` when running the render helper against a local dev server.

**How to apply:** Use this when INSTANTDOCS publish errors point at `blocksToHTML`. Related: [[project_publish_sfn_debugging]].
