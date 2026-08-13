#!/usr/bin/env node
// PreToolUse(Write|Edit|MultiEdit): re-injects the "Comments in code" rule from
// ~/.claude/CLAUDE.md right before Claude writes a comment into a source file.
// The rule is the most-violated one in that file; a reminder at read time is not
// enough, it has to land at write time.

const CODE_EXT =
  /\.(ts|tsx|js|jsx|mjs|cjs|py|go|rs|java|kt|swift|rb|php|c|h|cc|cpp|hpp|cs|scala|sh|bash|zsh|sql|css|scss|less|yaml|yml|tf|hcl|vue|svelte|graphql|prisma|toml)$/i;

// Anything that looks like a comment being introduced.
const COMMENT_MARKER = /(^|[^:\w"'`\\])\/\/|\/\*|^\s*#(?!!)|^\s*--\s|<!--/m;

// Comment-shaped text that is a pragma, not prose. Never worth nagging about.
const PRAGMA =
  /(biome-ignore|eslint-|@ts-(expect-error|ignore|nocheck)|prettier-ignore|istanbul ignore|v8 ignore|c8 ignore|@vitest-environment|noqa|type:\s*ignore|golangci|#!\/)/;

const MESSAGE = [
  'Comment budget (~/.claude/CLAUDE.md > "Comments in code"). You are about to write a comment.',
  'Default is ZERO comments — names are the explanation. Delete before you write:',
  'step narration, restatements of the signature/type, section banners, reflexive docstrings,',
  'and multi-paragraph essays above small functions.',
  'A genuinely non-obvious *why* (invariant, gotcha, workaround + reason, spec link) gets ONE line, two at most.',
  'Two traps: "I am matching the surrounding density" is not permission — this rule beats local precedent.',
  'And hard-won design rationale still gets one line; it belongs in the PR description or wiki, not stacked above a class.',
  'If a comment block is longer than the code it describes, delete it.',
  'This applies to config, YAML, SQL, migrations, shell, and test files too.',
].join(' ');

function textOf(input) {
  const parts = [input.content, input.new_string];
  if (Array.isArray(input.edits)) {
    for (const e of input.edits) parts.push(e.new_string);
  }
  return parts.filter((p) => typeof p === 'string').join('\n');
}

let raw = '';
process.stdin.on('data', (c) => {
  raw += c;
});
process.stdin.on('end', () => {
  try {
    const payload = JSON.parse(raw || '{}');
    const input = payload.tool_input || {};
    const path = input.file_path || '';
    const text = textOf(input);

    if (!CODE_EXT.test(path)) return;
    if (!COMMENT_MARKER.test(text)) return;
    if (PRAGMA.test(text) && text.split('\n').filter((l) => COMMENT_MARKER.test(l)).length <= 2) return;

    process.stdout.write(
      JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'PreToolUse',
          permissionDecision: 'allow',
          additionalContext: MESSAGE,
        },
      }),
    );
  } catch {
    // A guard must never break the edit it guards.
  }
});
