---
name: feedback_ask_decisions
description: "Always surface multi-option decisions to Yuvraj and let him choose, rather than unilaterally picking"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

When there are multiple valid options/approaches for how to do something, ASK Yuvraj and let him decide — don't silently pick one and run. Present the options concisely with a recommendation, then wait for his call. Applies to architecture/design forks, library/tool choices, scoping, and naming where it matters.

Also **confirm findings before acting on them** — when you discover issues/things that could be fixed, or the exact scope of a fix is ambiguous (esp. when his instruction was broad like "remove that entirely"), surface what you found and let him decide what to fix vs skip. Do NOT unilaterally decide scope (e.g. "I'll keep X for back-compat"). He said explicitly: "confirm findings with me, don't decide yourself what to fix and what not to."

**Why:** Yuvraj wants to stay the decision-maker on his projects; reinforces [[feedback_collaboration_style]].
**How to apply:** Proceed autonomously on determined/obvious work and things he's already approved; at a genuine fork with meaningful tradeoffs, or when scoping a fix from a broad instruction, pause and ask (AskUserQuestion or a concise inline options list). Don't over-ask on trivial/low-stakes choices.
