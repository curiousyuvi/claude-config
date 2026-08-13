---
name: pr-replies-no-filler
description: "PR comments and review replies get the answer only, with no greetings, thanks-for-the-review, or closing pleasantries"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 9e659169-898f-4865-9813-9186e7d6d073
  modified: 2026-07-28T08:13:11.062Z
---

Yuvraj asked for this as a standing rule for every project, on 2026-07-28. When
posting a PR comment, a reply to a review comment, or an issue reply: give the
answer and stop. No greeting, no "thanks for catching this", no "let me know if
you have questions", no restating the reviewer's point before answering it, no
announcing work instead of reporting it.

**Why:** these are working notes between engineers. The pleasantries are the
clearest tell that a model wrote the reply, and they bury the one or two sentences
that actually matter.

**How to apply:** the enforceable copy is in `~/.claude/CLAUDE.md` under "PR
comments, review replies, and issue replies", so it loads for every project
without needing recall. Include the answer, the reasoning when it is not obvious,
and a sha or file:line reference. Disagreement needs no softening: state it and
give the evidence. Pairs with [[no-ai-attribution-human-tone]], which covers the
same voice rules for commits, PR descriptions, code comments, and docs.
