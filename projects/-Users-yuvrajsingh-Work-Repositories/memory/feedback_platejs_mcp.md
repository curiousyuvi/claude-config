---
name: feedback_platejs_mcp
description: "Always use the Plate.js MCP server when working on anything Plate.js — don't guess the API or spelunk node_modules"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

When building or modifying ANY Plate.js code (the Axis native KB editor — [[project_kb_native_in_axis]] — or any Plate editor), use the **`plate` MCP server** as the source of truth for editor setup, plugin configs, components, API, and examples. Tool names appear as `mcp__plate__*` once a session loads it.

**Config (rebuilt & verified 2026-07-01):** `plate` is now a **USER-scope** stdio server (top-level `mcpServers` in `~/.claude.json`) so it loads in EVERY project/dir, not just axis. Command: `/bin/sh -c 'cd /Users/yuvrajsingh/.claude/plate-registry && exec npx shadcn@latest mcp'`. It points at a dedicated standalone `~/.claude/plate-registry/components.json` (declares `"registries": { "@plate": "https://platejs.org/r/{name}.json" }`), decoupled from any repo. Backup of the pre-change config: `~/.claude.json.bak-plate`.

**CRITICAL GOTCHA — `shadcn mcp -c/--cwd` is IGNORED for registry resolution.** The `mcp` subcommand resolves `components.json` from its actual PROCESS cwd, NOT from the `-c` flag (empirically proven: `-c <regdir>` → only `@shadcn`; process-cwd=<regdir> → `@shadcn` + `@plate`). So you MUST launch it with a shell wrapper that `cd`s into a dir containing a `components.json` with `@plate` — hence the `/bin/sh -c 'cd … && exec …'` form. A plain `npx shadcn@latest mcp -c <dir>` will silently fail to load `@plate`. The old axis project-local `plate` entry (used `-c apps/web`) was broken for exactly this reason and has been removed. Per https://platejs.org/docs/installation/mcp.

**7 tools exposed:** get_project_registries, list_items_in_registries, search_items_in_registries, view_items_in_registries, get_item_examples_from_registries, get_add_command_for_items, get_audit_checklist.

**Why:** Plate's API is large and version-sensitive; the MCP returns authoritative, version-correct plugin/component/API usage. Reading node_modules `.d.ts` or guessing is slow and error-prone — Yuvraj explicitly wants the MCP used for efficiency. He rejected an Explore/node_modules-archaeology approach in favour of this.

**How to apply:** Before writing Plate editor code, query the `plate` MCP for the relevant plugin/component/API. If `mcp__plate__*` tools are NOT loaded in the running session, the session must be RESTARTED (mid-session `claude mcp add`/config edits don't load into a live session); also the axis project may need its trust dialog accepted (`hasTrustDialogAccepted` was false). To verify the server works without a restart, probe it over stdio: pipe an `initialize`+`tools/list` JSON-RPC into `npx shadcn@latest mcp --cwd apps/web` (it exits on stdin EOF). The "An AI editor" template = registry item `@plate/editor-ai` (type registry:block) at https://platejs.org/blocks/editor-ai; it pulls 31 registryDependencies (mostly `*-kit` plugin bundles).
