---
name: feedback-comment-budget-hook
description: "A global PreToolUse hook now re-injects the \"Comments in code\" rule on every Write/Edit of a source file"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: becdf0f5-7b3c-491e-9678-c79ee5939510
  modified: 2026-08-07T06:06:01.443Z
---

The "minimum comments, usually zero" rule was being violated constantly across
sessions despite living in `~/.claude/CLAUDE.md`, so it is now enforced by a
harness hook, not just by the instruction file:

- `~/.claude/hooks/comment-budget-guard.cjs` — PreToolUse on `Write|Edit|MultiEdit`.
  Fires only when the payload targets a code/config extension AND introduces a
  comment marker; stays silent for pragma-only edits (`biome-ignore`,
  `@ts-expect-error`, `eslint-disable`, shebangs), for markdown, and for `//`
  inside URLs/strings. Registered in `~/.claude/settings.json` under
  `hooks.PreToolUse` (backup at `settings.json.pre-comment-guard`).

**Why:** the failure mode was never a stray comment, it was writing a whole
densely-documented file and feeling good about it. A rule read once at session
start loses to that; a reminder delivered at the moment of writing does not.

**How to apply:** when the reminder appears in a `<system-reminder>` before an
edit, treat it as binding: strip step narration, signature restatements, section
banners and reflexive docstrings before submitting the edit. Do not disable or
loosen the hook. If it turns out to be noisy, tighten the matcher, do not remove it.

Related: [[feedback-minimal-comments]], [[feedback-no-claude-author]].
