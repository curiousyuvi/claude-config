---
name: feedback_always_use_humanizer_skill
description: Run every piece of human-facing prose through the humanizer skill before delivering it
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ae4542e5-3909-4a0d-b982-779f52522c7d
  modified: 2026-09-01T13:45:09.332Z
---

Always invoke the `humanizer` skill on prose written for people: PR titles and
descriptions, review comments and replies, issue text, commit message bodies,
docs, changelogs, design docs, RFCs, runbooks, wiki pages, drafted emails and
Slack messages, and generated documents (PDF, slides, reports). Not code,
comments, config, or short chat answers.

**Why:** hand-written style rules catch some tells but not all; the skill is the
checklist. The user asked for it as a standing global rule, not a per-request
opt-in.

**How to apply:** draft, then run the skill on the draft, then deliver the
humanized version. Stacks with [[feedback_no_claude_author.md]] and the "Write
like a person" section of the global CLAUDE.md, where it now lives as a section
too.
