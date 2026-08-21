---
name: post-thermo-nuclear-review
description: Run the thermo-nuclear code quality review on a GitHub PR and post the result as a GitHub review, requesting changes or approving based on the verdict. Use for "post thermo nuclear review", "review this PR and request changes", or a thermonuclear review posted to the PR.
disable-model-invocation: true
---

# Post Thermo-Nuclear Review

Run the thermo-nuclear review on a pull request, then submit it as a real GitHub review.

## Arguments

`$ARGUMENTS` — PR number, URL, or branch. If empty, use the PR for the current branch (`gh pr view --json number`). If there is none, stop and ask.

## Steps

1. Read `~/.claude/skills/thermo-nuclear-code-quality-review/SKILL.md` and apply it in full. That file is the review standard: its rules, questions, remedies, tone, and approval bar govern everything below.
2. Gather context: `gh pr view <target>`, `gh pr diff <target>`, and read the touched files at full length (the diff alone hides file size and surrounding structure). Check the repo's `AGENTS.md` / `CLAUDE.md` for conventions the diff has to respect.
3. Decide the verdict against the parent skill's Approval Bar:
   - Any presumptive blocker present, or any actionable structural finding: **request changes**.
   - Bar met, nothing beyond cosmetic notes: **approve**.
4. Write the review body as markdown, in this shape:
   - One short paragraph verdict up top: what the PR does and why it passes or does not.
   - Then the severity legend on its own line: `Severity: 🔴 blocker · 🟠 should fix before merge · 🟡 minor`.
   - One numbered finding per issue, each opening a heading: `### N. <emoji> <headline>`. The headline states the problem in a sentence; it is not the file name.
   - Under the heading, the `file:line` references on their own line in backticks, then the prose: what is wrong, then the concrete restructuring. Reach for a short bullet list only when a single finding has several distinct consequences.
   - Order findings by severity, 🔴 first, which normally matches the parent skill's Output Expectations.
   - High-conviction findings only. No nit floods. No severity table either, the emoji in each heading carries it.
   - Prose rules from `~/.claude/CLAUDE.md` apply: no AI attribution of any kind, no em dashes, no greetings or sign-offs, no "great work" padding. The severity emoji are the one authorized exception to the no-decorative-unicode rule; keep them.
5. Submit:
   ```
   gh pr review <target> --request-changes --body-file <file>
   gh pr review <target> --approve --body-file <file>
   ```
   Write the body to the scratchpad first; never inline a long body on the command line.
6. Report the verdict and the review URL back to the user.

## Gotchas

- GitHub refuses `--approve` and `--request-changes` on your own PR. On that error, resubmit the same body with `--comment` and say which verdict it stands for in the first line.
- A verdict of request-changes blocks the PR for everyone. Get the target right before submitting: confirm the PR number, title, and head branch from `gh pr view` output match what the user meant.
- Re-running on the same PR stacks another review. Check `gh pr view <target> --json reviews` first and say so if a prior review from the user is already there.
- To reword a review already posted, edit it in place rather than stacking a second one. Get the id from `gh api repos/<owner>/<repo>/pulls/<n>/reviews`, build the payload with `jq -Rs '{body: .}' <file> > <json>`, then `gh api --method PUT repos/<owner>/<repo>/pulls/<n>/reviews/<id> --input <json>`. The verdict stays as submitted. That PUT can fail with a transient `tls: bad record MAC`; retry, then read the stored body back to confirm rather than trusting the response.
