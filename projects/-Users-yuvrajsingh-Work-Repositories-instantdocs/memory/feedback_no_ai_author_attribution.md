---
name: feedback-no-ai-author-attribution
description: "Never attribute commits/PRs to Claude or any AI — no Co-Authored-By, no \"Generated with\" lines"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1985cacb-734e-4712-95fa-d406d20ebc72
---

Hard rule: never mention myself (Claude) or any other AI as an author or contributor anywhere — git commit messages, commit trailers, PR titles/descriptions, etc.

**Why:** The user does not want AI attribution in their VCS history or PRs. This overrides the harness default that appends a `Co-Authored-By: Claude ...` trailer to commits and a "🤖 Generated with Claude Code" line to PR bodies.

**How to apply:** Omit the `Co-Authored-By` trailer from every commit message. Omit any "Generated with" / "Made with Claude" footer from PR descriptions. Write commits and PRs as if authored solely by the user.
