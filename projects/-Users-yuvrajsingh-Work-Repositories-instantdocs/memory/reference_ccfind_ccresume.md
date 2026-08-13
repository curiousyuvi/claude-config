---
name: ccfind / ccresume helpers for old chats
description: Zsh helpers ccfind/ccresume in ~/.zshrc grep across all Claude Code transcripts for the current project when the /resume picker doesn't show an old chat.
type: reference
originSessionId: abe14289-6b52-4a26-88b2-2313ab619553
---
The `/resume` picker in Claude Code only renders a recency window of transcripts — older `.jsonl` files stay on disk and resume fine by ID, but don't appear in the picker (even via its in-picker search, which only filters the displayed window). This is NOT account-based filtering; all transcripts in `~/.claude/projects/<encoded-cwd>/` are accessible regardless of which Anthropic account is currently logged in.

Two zsh functions live in `~/.zshrc` between the clearly-marked `# --- claude-code transcript search ---` fences:

- `ccfind <keyword...>` — grep every `.jsonl` in the current project's transcript dir (AND-ed keywords, case-insensitive, fixed strings), print newest-first as `DATE  sessionId  first-real-user-prompt`.
- `ccresume <keyword...>` — same search, then `claude -r <newest-match-sessionId>`.

Both rely on `_cc_project_dir` (maps `$PWD` to `~/.claude/projects/<slashes-to-dashes>`) and only look at top-level `*.jsonl` (skips subagent sidecars).

When user asks about missing/old Claude Code chats in this repo or others: suggest `ccfind <keyword>` in the relevant project `cwd`. If they're in a new project where `~/.claude/projects/<encoded-cwd>/` doesn't yet exist, the helper prints that and exits cleanly.
