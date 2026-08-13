---
name: kb-editor-playwright-automation
description: "Gotchas for driving the KB Plate editor with Playwright (selection, autosave persistence, New article dialog)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c5af0c9-ed68-43fe-a98c-58a7a45b869f
  modified: 2026-07-29T14:21:32.865Z
---

Driving the KB article editor via Playwright (see [[local-verify-login]] for login):

- Slate ignores programmatic `window.getSelection()` + `keyboard.press` — set a caret by `mouse.click()` at a character boundary computed from `Range.getBoundingClientRect()` over the target text node, then send keys.
- `Meta+ArrowDown` / `ControlOrMeta+End` do NOT move to end of doc in the editor; click the actual target block instead.
- Autosave is debounced: typing followed by `browser.close()` within ~1s does not persist; wait 5-6s after the last keystroke before closing (also how to make an intentional repair stick).
- Sidebar "+" next to "Knowledge Base" → menu (New collection / New article) → "New article" opens a Title/Slug DIALOG; keystrokes go there until Create is clicked.
- Slash menu: click the body `[data-slate-editor="true"]`, type `/steps` etc.; options appear as `[role="option"]`. Inside a Steps list, Enter = next step, Shift+Enter = soft line break within the step.

**Why:** first attempt typed `/steps` into the middle of a seeded article's link text and the damage autosaved; repair required the mouse-click caret trick.
**How to apply:** reuse for any KB editor visual verification instead of rediscovering; prefer creating a scratch article over editing seeded ones.
