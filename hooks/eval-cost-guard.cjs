#!/usr/bin/env node
// PreToolUse(Bash|mcp__terminal__run_in_terminal): an eval run needs the user's yes on its cost first.
// The command must carry EVAL_APPROVED_USD=<estimate>, added only after the user approved that estimate in chat.

const EVAL_COMMAND = /evals\/run\.ts|pnpm\s+(run\s+)?evals(:pairwise|:reviews)?\b|peek-judge|evals\/pairwise\.ts/;
const APPROVED = /\bEVAL_APPROVED_USD=\d+(\.\d+)?\b/;

const REASON = [
  'Eval run blocked: the user must approve its cost first (memory: feedback_ask_before_any_eval_run).',
  'Tell the user which stage/cases/repeats it runs and the approximate cost in USD (estimate from costUsd in',
  'evals/runs/*.json), wait for an explicit yes in chat, then put EVAL_APPROVED_USD=<that estimate> at the start',
  'of the command. Prefer --no-grader and --only for A/B checks.',
].join(' ');

let raw = '';
process.stdin.on('data', (chunk) => {
  raw += chunk;
});
process.stdin.on('end', () => {
  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    process.exit(0);
  }
  const command = String(input?.tool_input?.command ?? '');
  if (!EVAL_COMMAND.test(command) || APPROVED.test(command)) process.exit(0);
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: REASON },
    }),
  );
  process.exit(0);
});
