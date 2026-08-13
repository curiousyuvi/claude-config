---
name: No AI/Claude attribution in any git artifacts
description: Yuvraj wants all commits, PRs, branches, and GitHub Actions to look fully human-authored — no Co-Authored-By Claude, no "Generated with Claude Code" footers, no AI mentions anywhere visible
type: feedback
originSessionId: bcef0bbe-dab8-4443-8005-65b8e65e1a84
---
In **any** git/GitHub artifact produced for Yuvraj's work, do not include AI or Claude attribution. This overrides the default commit/PR templates that add `Co-Authored-By: Claude` and `🤖 Generated with Claude Code`.

**Why:** Work needs to look fully authored by him for professional/team-visibility reasons (CTO, GrooveHQ team, public repos).

**How to apply:**
- Commit messages: NO `Co-Authored-By: Claude ...` trailer. NO emoji robot footer. NO mention of AI assistance.
- PR descriptions: NO `🤖 Generated with [Claude Code]` footer. Body should read like a human wrote it — first person, no agent voice.
- Branch names: regular human-style names, no `claude/`-style prefixes.
- GitHub Actions / workflow files: no comments referencing AI/Claude as author.
- Code comments: no "// added by Claude" style notes.
- Applies to ALL repos he works in, not just one project.
