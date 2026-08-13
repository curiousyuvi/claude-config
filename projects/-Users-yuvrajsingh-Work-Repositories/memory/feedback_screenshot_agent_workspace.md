---
name: feedback-screenshot-agent-workspace
description: "When running screenshot-agent against InstantDocs, always pin browser-use to Yuvraj's Workspace + Test KB via TARGET_APP_LOGIN_INSTRUCTIONS env var"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcef0bbe-dab8-4443-8005-65b8e65e1a84
---

When iterating on screenshot-agent's capture/annotation pipeline against
`https://app.instantdocs.com`, the agent **must** be constrained to "Yuvraj's
Workspace" and within it the knowledge base named "Test". This is wired via
the `TARGET_APP_LOGIN_INSTRUCTIONS` env var, which is appended to both the
login task and every per-intent task prompt that browser-use receives.

**Why:** the test account has access to multiple workspaces (Rose's, "InstantDocs's",
etc.). Without explicit pinning, browser-use lands wherever the workspace switcher
defaults to — usually a free-plan workspace where Custom Domain settings show
upgrade/pricing prompts instead of input fields. This makes correctness testing
impossible because every capture fails on state, not on the agent's actual
ability. We've lost a full debug session twice now to this drift (once before
the initial run setup, once after a `/compact` wiped the env value).

**How to apply:**
- Set `TARGET_APP_LOGIN_INSTRUCTIONS` in `screenshot-agent/.env.local`. The current
  text (~2026-05-13): "After signing in, immediately switch to the workspace
  named 'Yuvraj's Workspace' using the workspace switcher in the top header...
  Within that workspace, all screenshot intents target the knowledge base named
  'Test'. Never switch to ... any other workspace under any circumstance."
- After any conversation compaction in this project, verify `.env.local` still
  has this value before running anything. If it's gone, restore it — losing it
  silently corrupts every subsequent capture.
- Related code: `screenshot_agent/service/sessions.py:_credential_from_env`,
  `screenshot_agent/browser/runner.py:_build_login_task` and `_build_intent_task`.

Also remember the visual rule the user added at the same time: "screenshots
should be zoomed in or cropped to highlight main area, and use arrow elements
to point to where to click or view." (The arrow rule is enforced in
`agents/annotator.py`; the crop rule was tried, regressed quality, and dropped
in [[feedback-no-crop-screenshots]] — see commit history.)
