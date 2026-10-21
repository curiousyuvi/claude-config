---
name: reference-notion-fetch-headroom-workaround
description: "Notion tool results arrived as `<<ccr:...>>` placeholders because the Headroom proxy compressed them; fixed 2026-10-21 via ~/.headroom/settings.json protect_tool_results"
metadata:
  node_type: memory
  type: reference
  originSessionId: 95ec2c73-358c-4e03-a22e-92cff3042ffc
  modified: 2026-10-21T14:32:48.700Z
---

Root cause: the Headroom proxy (`headroom proxy --port 8787`, started detached by `headroom wrap claude`) lossy-compresses MCP tool results, so Notion pages and comments came back as `<<ccr:HASH,...>>` and `headroom_retrieve` often returned the placeholder again.

Fix (2026-10-21): `~/.headroom/settings.json` = `{"protect_tool_results": "mcp__claude_ai_Notion__*"}` (glob patterns are supported, see `is_tool_excluded` in headroom/config.py). Setting is read only at proxy startup, so the proxy must be restarted after editing (it is not a managed service, `headroom install status` says no deployment; restarting cuts the running Claude session's API connection, so the user does it).

Verify: `curl -s http://127.0.0.1:8787/settings` shows the stored value; after a restart a Notion fetch returns plain text.

Fallbacks if it regresses: `notion-search` scoped with `page_url` returns short highlights that survive; comments cannot be searched; ask the user for screenshots.

Saved copies: `~/.axis/knowledge-gaps/jj-final-plan-reference.md` (JJ's Topics + Gaps plan, v1.4).
