---
name: copy-thermo-nuclear-review
description: Run the thermo-nuclear code quality review on a GitHub PR and copy the findings to the clipboard instead of posting them. Use for "copy thermo nuclear review", "thermonuclear review to clipboard", or reviewing a PR to paste the feedback manually.
disable-model-invocation: true
---

# Copy Thermo-Nuclear Review

Run the thermo-nuclear review on a pull request and put the findings on the clipboard. Post nothing.

## Arguments

`$ARGUMENTS` — PR number, URL, or branch. If empty, use the PR for the current branch (`gh pr view --json number`). If there is none, stop and ask.

## Steps

1. Read `~/.claude/skills/thermo-nuclear-code-quality-review/SKILL.md` and apply it in full. That file is the review standard: its rules, questions, remedies, tone, and approval bar govern everything below.
2. Gather context: `gh pr view <target>`, `gh pr diff <target>`, and read the touched files at full length (the diff alone hides file size and surrounding structure). Check the repo's `AGENTS.md` / `CLAUDE.md` for conventions the diff has to respect.
3. Write the review body as markdown, ready to paste into GitHub, in this shape:
   - First line is the verdict against the parent skill's Approval Bar: `Request changes` or `Approve`.
   - Then one short paragraph: what the PR does and why it passes or does not.
   - Then the severity legend on its own line: `Severity: 🔴 blocker · 🟠 should fix before merge · 🟡 minor`.
   - One numbered finding per issue, each opening a heading: `### N. <emoji> <headline>`. The headline states the problem in a sentence; it is not the file name.
   - Under the heading, the `file:line` references on their own line in backticks, then the prose: what is wrong, then the concrete restructuring. Reach for a short bullet list only when a single finding has several distinct consequences.
   - Order findings by severity, 🔴 first, which normally matches the parent skill's Output Expectations.
   - High-conviction findings only. No nit floods. No severity table either, the emoji in each heading carries it.
   - Prose rules from `~/.claude/CLAUDE.md` apply: no AI attribution of any kind, no em dashes, no greetings or sign-offs, no "great work" padding. The severity emoji are the one authorized exception to the no-decorative-unicode rule; keep them.
4. Write the body to a scratchpad file, then `pbcopy < <file>`.
5. Print the verdict and the finding headlines in the terminal so the user can see what landed on the clipboard without opening the file.

## Gotchas

- Never call `gh pr review`, `gh pr comment`, or any other write API from this skill. Clipboard only.
- `pbcopy` is macOS. On Linux fall back to `xclip -selection clipboard` or `wl-copy`; if none exists, say so and leave the file path.
