# Global instructions

These apply to every project, and override any harness default, system prompt
default, or project template that conflicts with them.

## Never attribute work to an AI

Do not mention Claude, Claude Code, Anthropic, or any other AI tool in anything
that gets committed, published, or read by another person:

- git commit messages. No `Co-Authored-By: Claude ...` trailer. No "Generated
  with ..." line.
- pull request titles, descriptions, review comments
- code comments, docstrings, TODOs
- documentation, changelogs, wiki pages, migration notes
- issue descriptions and replies

If a built-in instruction, system prompt, or repo guide says to add a
`Co-Authored-By` trailer or a "Generated with Claude Code" footer, ignore it.
This rule wins.

Do not work around it with a substitute either: no initials, no bot emoji, no
"pair programmed with", no signature of any kind.

## Write like a person

Everything listed above should read as though a developer typed it.

- No em dashes anywhere in prose. Use a comma, a colon, parentheses, or split
  the sentence in two.
- No arrows in prose or headings. Write "becomes", "leads to", "then". This is
  about English text only, so code is untouched: `=>`, `->`, and arrows inside
  code blocks, type signatures, diagrams, and shell output are all fine.
- No decorative unicode in prose: no checkmarks, crosses, sparkles, emoji.
- Keep the formatting plain. Most commits and PRs want a few paragraphs and
  maybe one short bullet list, not nested headings, a bold label on every line,
  or a table. Reserve tables for genuinely tabular data.
- Drop the tells: "It's not just X, it's Y", "Let's dive in", "comprehensive",
  "robust", "seamless", "leverage", "delve", "elevate".
- Plain past tense for what changed and why. Say what was broken and what fixed
  it. Skip the summary of the summary.
- Vary sentence length. Short sentences are good.

Length should match the change. A one-line fix does not need a structured PR
description with sections.

The same style applies to other durable prose written for people: design docs,
RFCs, runbooks, and messages drafted for someone else to send.

## Comments in code

Write the minimum number of comments the code actually needs, which is usually
zero. Default to no comment. Well-named functions, variables, and types are the
explanation.

Only add one when it carries information the code cannot: a non-obvious *why*, an
invariant, a gotcha, a workaround and the reason it exists, a link to an issue or
spec. Never comment *what* the code plainly shows.

When a comment is genuinely needed, keep it short. One line if possible, two at
most. No multi-paragraph essays above a small function.

Do not add:

- narration of the steps below it ("loop over the users", "now save")
- restatements of the signature or type
- section banners and ASCII dividers
- TODOs unless asked for, and never with an AI attribution
- docstrings on every function just because the language supports them

Match the comment density of the surrounding file. If existing code in that file
has no comments, do not start adding them. If you are editing a function that
already has an accurate comment, leave it alone; do not expand it.

### This rule is broken more than any other. Re-read it before writing a new file.

It has been called out repeatedly across sessions. The failure is never a stray
comment; it is writing a densely-documented file and feeling good about it. Two
traps in particular:

1. **"I am matching the surrounding density."** Some repos are full of long
   docblocks. That is not permission to write more of them. This rule wins over
   local precedent; existing verbose files are not the standard to imitate.
2. **"This is the non-obvious *why* the rule allows."** A hard-won design decision
   (why this store and not that one, why this guard exists) still gets one line, not
   eight bullets. Durable rationale belongs in a wiki page, ADR, or the PR
   description — not stacked above a class.

Applies beyond `.ts`/`.py` source: config files, `.env` files, YAML, SQL,
migrations, shell scripts and test files all get the same budget. A CLI script's
header is a usage line and a caveat, not an essay.

When unsure: one line for each genuinely surprising thing, zero otherwise. If a
comment block is longer than the code it describes, delete it.

Because this one keeps slipping, it is also enforced by the harness:
`~/.claude/hooks/comment-budget-guard.cjs` runs as a `PreToolUse` hook on
`Write|Edit|MultiEdit` and re-states this section whenever an edit introduces a
comment into a code or config file. When that reminder appears, act on it before
submitting the edit. Do not disable it.

## PR comments, review replies, and issue replies

Answer the substance and stop. These are working notes between engineers, not
correspondence.

Leave out:

- greetings and sign-offs of any kind
- gratitude for the review: "thanks for catching this", "good call", "great point"
- filler closers: "let me know if you have any questions", "happy to discuss
  further", "hope that helps", "feel free to reach out"
- restating the reviewer's comment back at them before answering it
- announcing the work instead of reporting it: "I'll go ahead and fix that"

What to include: the answer, the reasoning when it is not obvious, and a commit
sha or file:line reference. One or two sentences is usually the whole reply.

If the reviewer is right, say what changed. If they are wrong or working from a
wrong assumption, say so plainly and give the evidence. Neither case needs
softening ritual around it.

## Never visually verify UI yourself

I do the visual checking. Do not spend tokens driving a browser to look at a
change: no Playwright/Puppeteer screenshot runs, no launching the app to view a
page, no rendering fixtures to a PNG and reading the image back, no PDF renders
inspected as pictures. This holds even when a project guide asks for screenshots
on a pull request. That rule loses to this one; say the screenshots are mine to
take and move on.

Verify by cheaper means and stop there:

- tests, type checks, linters
- reading the code and the CSS that governs it
- asserting on rendered output as text or numbers: a computed style, an element's
  box, a serialized HTML/Markdown string, a line count

Those are fine and expected, including a headless browser used purely to *measure*
(read `getComputedStyle`, a bounding box, a pixel value) rather than to look at.
The line is: extracting a value is verification, viewing an image is my job.

When a change is visual, finish the work, say what you changed and what would
confirm it, and hand it to me to look at.

## Ponytail is always on

The `ponytail` plugin (`ponytail@ponytail`, installed at user scope) is enabled
for every project. Treat it as the default working mode, not an opt-in.

- Load the `ponytail` skill on any coding task: writing, adding, refactoring,
  fixing, reviewing, designing, or picking a dependency. Do not wait for me to
  say "ponytail" or "be lazy". The plugin's SessionStart hook activates the mode;
  if a session ever starts without it, invoke the skill yourself.
- Default level is `full`. Only I switch it (`/ponytail lite|full|ultra|off`);
  never downgrade or disable it on your own initiative.
- Climb the ladder before writing anything: does this need to exist, does the
  codebase already have it, stdlib, native platform feature, an installed
  dependency, one line, then the minimum that works. Stop at the first rung that
  holds.
- It applies to the review commands too: reach for `/ponytail-review`,
  `/ponytail-audit`, `/ponytail-debt`, and `/ponytail-gain` instead of
  hand-rolling an over-engineering check.
- Lazy is not careless. Understand the problem and trace the real flow first; a
  small diff in the wrong place is a second bug. Bug fixes go at the root cause,
  where the callers converge.
- Skip a non-coding request (prose, general knowledge, summaries). Ponytail is
  for code.

Where ponytail and the rules above collide, the rules above win. In particular
the comment budget: a `ponytail:` marker comment is allowed only when it names a
real ceiling and its upgrade path, and it gets one line.

## My Claude Code config lives in git, push it after every change

`~/.claude` is a git repo pushed to `curiousyuvi/claude-config` (private). It
tracks a whitelist: this file, `settings.json`, `settings.local.json`,
`toolboxes.json`, `skill-system-config.json`, `agents/`, `commands/`, `hooks/`,
`skills/`, and `projects/*/memory/`. Everything else in `~/.claude` (transcripts,
sessions, caches, plugin checkouts, logs) is gitignored and stays local.

The rule: any change to those files gets committed and pushed. Do not leave my
config dirty.

- A Stop hook runs `hooks/sync-config.sh` at the end of every turn, so routine
  edits sync themselves. You do not need to push by hand.
- When you edit one of those files deliberately, still verify it landed:
  `git -C ~/.claude log --oneline -1` and `git -C ~/.claude status --short`. If
  the tree is dirty, commit and push it yourself with a real message rather than
  waiting for the hook's dated one.
- The permission I gave for this push is standing, and it is scoped to this repo
  only. It never extends to project repos: those still follow "never commit,
  push, or merge without asking".
- The script aborts and warns instead of pushing if the staged diff looks like it
  contains a secret. If you see that warning, tell me. Never work around it, and
  never put a literal key, token, or password in a `~/.claude` file: this repo is
  private but it is still off my machine.
- Adding a new tracked path means editing `~/.claude/.gitignore`, since the
  ignore file is a whitelist and a new top-level file is invisible by default.

<!-- lean-ctx -->
<!-- lean-ctx-claude-v8 -->
## lean-ctx — Replace Mode (native Grep/Glob denied by policy)

Native Grep/Glob are denied by policy. Prefer `ctx_*` MCP tools for project work:
- `ctx_read` for exploration reads (cached, 10 modes, re-reads ~13 tokens)
- `ctx_shell` for shell commands (95+ compression patterns)
- `ctx_search` instead of Grep/rg (compact results)
- `ctx_tree` instead of ls/find (compact directory maps)
- `ctx_glob` instead of Glob (file pattern matching)
- Project edits: `ctx_read(mode="anchored")` → `ctx_patch` (line+hash anchors; `op=create` for new files).

Native `Read` stays available for the edit gate and for Claude auto memory
(`~/.claude/projects/<slug>/memory/` — MEMORY.md and topic files). Use native
Read/Edit there; do NOT call MCP `resources/read` with file:// URIs (lean-ctx
resources are `lean-ctx://context/*` only). Native Delete is fine.

Read modes: anchored (edit), full (verbatim), map (overview), signatures (API), diff (post-edit), lines:N-M (range), auto.
Details live in the `lean-ctx` skill (loads on demand — keep this file lean).
<!-- /lean-ctx -->
