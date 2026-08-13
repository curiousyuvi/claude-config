---
name: feedback-minimal-comments
description: "Write minimum comments in code, usually zero; when truly needed, keep them short and only for the non-obvious why"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 454dfaea-526d-4faa-9286-447d8abd2015
  modified: 2026-08-06T05:19:03.358Z
---

Write the minimum number of comments code needs, which is usually zero. Default to
no comment. When one is genuinely required, keep it short and concise (one line,
two at most). Reaffirmed and promoted to a global rule on 2026-07-29: it now lives
in `~/.claude/CLAUDE.md` under "Comments in code", so it applies to every project,
not just axis.

**Why:** The user considers gratuitous comments noise; well-named code should speak
for itself, and long comment blocks above small functions read as AI output.

**How to apply:** Only comment to carry information the code cannot: non-obvious
*why*, invariants, gotchas, workarounds and their reason, issue/spec links. Never
comment *what* the code plainly shows. No step narration, no signature
restatements, no section banners, no reflexive docstrings on every function, no
unrequested TODOs (and never with AI attribution, see
[[feedback-no-claude-author]]). Match the comment density of the surrounding file:
if it has no comments, do not start adding them. Leave existing accurate comments
alone rather than expanding them.

**REPEATEDLY VIOLATED — re-read this before writing any new file.** Called out again
2026-08-06 (KB asset R2 work) after multi-paragraph class docblocks, a 35-line bin
script header, essays on every method, and prose in `.env` files. Two specific traps:

1. *This repo's existing files are densely commented*, so "match the surrounding
   density" reads as licence to write essays. It is not. The global rule wins; the
   old files are not the standard to imitate.
2. Explaining a hard-won design decision (why R2 not per-object ACLs, why a delete
   guard) feels like the "non-obvious why" the rule permits. One line, or the wiki
   page — not eight bullets in a docblock. Durable rationale belongs in `wiki/`,
   not above a class.

Concrete budget when unsure: one line per genuinely surprising thing, zero
otherwise. `.env` files get at most a single short line per block.
