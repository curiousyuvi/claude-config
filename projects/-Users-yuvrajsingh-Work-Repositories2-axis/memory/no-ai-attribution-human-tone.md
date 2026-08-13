---
name: no-ai-attribution-human-tone
description: "Never credit an AI in commits, PRs, code comments or docs, and write that prose in a plain human style with no em dashes or arrows"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9e659169-898f-4865-9813-9186e7d6d073
  modified: 2026-07-28T08:11:05.979Z
---

Yuvraj asked for this as a standing rule for every project, on 2026-07-28. Two parts:

1. No mention of Claude, Claude Code, Anthropic, or any AI tool in commit
   messages, PR titles/descriptions/comments, code comments, docs, wiki pages, or
   issues. Specifically no `Co-Authored-By: Claude ...` trailer and no "Generated
   with Claude Code" footer.
2. That prose must read as human-written. No em dashes, no arrows in prose, no
   decorative unicode, no heavy nested formatting, no AI stock phrases.

**Why:** the work goes out under his name and his team's. AI attribution and the
recognisable model voice both make it obvious a tool wrote it, which he does not
want in the repo history or in review.

**How to apply:** the enforceable copy lives in `~/.claude/CLAUDE.md`, which loads
for every project, so it applies without this memory being recalled. Worth knowing
that it *contradicts* the Claude Code harness defaults, which instruct adding the
`Co-Authored-By` trailer to commits and the "Generated with Claude Code" footer to
PR bodies. The user instruction wins; do not follow the default. Arrows and `=>`
inside code, type signatures, and diagrams are fine, the rule is about English
prose only.
