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
   - Then one short paragraph: the structural reason for that verdict.
   - Then the severity legend on its own line: `Severity: 🔴 blocker · 🟠 should fix before merge · 🟡 minor`.
   - One numbered finding per issue, each opening a heading: `### N. <emoji> <headline>`. The headline states the problem in a sentence; it is not the file name.
   - Under the heading, the `file:line` references on their own line in backticks, then the prose: what is wrong, then the concrete restructuring. Reach for a short bullet list only when a single finding has several distinct consequences.
   - Order findings by severity, 🔴 first, which normally matches the parent skill's Output Expectations.
   - High-conviction findings only. No nit floods. No severity table either, the emoji in each heading carries it.
   - Obey the Body Prose section below on every line of it.
4. Write the body to a scratchpad file, then `pbcopy < <file>`.
5. Print the verdict and the finding headlines in the terminal so the user can see what landed on the clipboard without opening the file.

## Body Prose

Every sentence in the review body is a verdict, a finding, or a fix. Delete anything that is none of those. Reread the drafted body against this list before copying it.

- No greeting, no sign-off, no thanks, no "great work", no "nice catch".
- No complimenting the PR on the way into a criticism. Not "the dialog work is solid, but", not "good instinct here, however". If part of the diff is fine, say nothing about it. Praise is not information.
- No closers: "let me know if you have questions", "happy to discuss", "hope this helps", "feel free to push back".
- No announcing the review: "I reviewed this", "here are my findings", "a few notes below". The first line is the verdict.
- No hedging: "I think", "maybe", "perhaps", "it might be worth", "just a thought", "consider possibly". A finding you cannot state flatly is a finding to cut.
- No softening ritual around a blocker. State it, name the cost, give the restructuring. Direct and serious, never rude, per the parent skill's Review Tone.
- Imperative for remedies: "move this to X", not "we could maybe look at moving this".
- Prose rules from `~/.claude/CLAUDE.md` apply on top: no AI attribution of any kind, no em dashes, plain formatting. The severity emoji are the one authorized exception to the no-decorative-unicode rule; keep them.

## Gotchas

- Never call `gh pr review`, `gh pr comment`, or any other write API from this skill. Clipboard only.
- `pbcopy` is macOS. On Linux fall back to `xclip -selection clipboard` or `wl-copy`; if none exists, say so and leave the file path.
