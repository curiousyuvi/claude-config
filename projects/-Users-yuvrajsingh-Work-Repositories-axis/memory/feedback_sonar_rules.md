---
name: SonarQube/SonarCloud rules that fire on this repo
description: Common Sonar rules to pre-empt while writing code so PRs don't bounce on the SonarCloud quality gate
type: feedback
originSessionId: fc7a0aac-4c44-4183-9c03-29cde28a5fb4
modified: 2026-07-31T04:24:54.144Z
---
The Axis repo runs SonarCloud as a quality gate on every PR. To avoid trips, write code that never trips these specific rules in the first place.

## ⭐ UPDATE 2026-07-13: a Sonar MCP is now configured — PREFER it over the manual scan

The user added a Sonar MCP server. From now on, **query the Sonar MCP directly for real SonarCloud findings** instead of relying on the blind manual grep + GitHub-annotations method below. At the START of a session, run `ToolSearch("sonar")` (or `sonarqube`/`sonarcloud`) to load its tool schemas, then use them to pull actual issues/hotspots/quality-gate status for the PR or new code. The MCP registers only after a Claude Code **restart** — if `ToolSearch("sonar")` returns nothing, the server isn't live in this session yet; fall back to the manual scan below for that session. The manual grep/rules content below remains the FALLBACK (and is still useful for writing clean code up front), but the MCP is the source of truth for whether the gate will pass.

**Why:** PR #185 failed the gate twice — once for a security hotspot (`Math.random` in `pickRandomColor`), once with five code-smell warnings. All were trivially avoidable in the original commit.

## ⭐ FIRST STEP 2026-07-31 (PR #972): read the GATE CONDITIONS before fixing anything

The MCP works and is the fastest triage. Project key `GrooveHQ_axis`; the `pullRequest` param is just the GitHub PR number.

```
mcp__sonarqube__get_project_quality_gate_status({projectKey: 'GrooveHQ_axis', pullRequest: '972'})
mcp__sonarqube__search_sonar_issues_in_projects({projects: ['GrooveHQ_axis'], pullRequest: '972', issueStatuses: ['OPEN','CONFIRMED']})
```

**Do the gate-status call first, and let it set the scope.** The issue list is much longer than the blocking set. #972 had 11 open issues but failed on `new_reliability_rating` (4, needs 1) ALONE, from a single S2871 — `new_maintainability_rating` was already 1. So the "clear the whole smell category in files you touch" advice below (correct for #929) would have been pure wasted risk here: it would have meant refactoring three 8-and-9-parameter methods in a 1300-line importer this PR barely touched.

Rule: fix what the failing conditions actually demand, plus any finding your own diff introduced. Leave pre-existing smells in untouched code when their rating already passes, and say so in the commit. Check with `git diff master...HEAD -- <file>` whether a finding is even yours; Sonar reports every open issue in a changed FILE, not just your lines.

**Also: I shipped an S2871 despite this very note telling me to grep every `.sort()`.** It fires on `.toSorted()` too, on `string[]`, and inside a template literal where it is easy to miss. Grep the diff for `sort(` with no argument, every time.

## CRITICAL: the gate fails on RATINGS — and **Maintainability is one of them**

The "Sonar way" new-code gate fails on **Reliability Rating (Bugs)**, **Security Rating (Vulnerabilities)**, **Maintainability Rating (Code Smells)**, **Security Hotspots reviewed**, **Coverage**, and **Duplication**. A manual self-check that only greps for smells can still miss a gating Bug (PR #721: gate failed solely on "Reliability Rating on New Code = D" from one Bug), so bug rules stay the first sweep.

**CORRECTION 2026-07-28 (PR #929): smells DO gate.** An earlier version of this note claimed Maintainability "usually stays rating A and does not fail the gate". That is wrong. #929 failed on **"C Maintainability Rating on New Code (required ≥ A)"** with zero bugs and zero vulns — driven almost entirely by **S6759 (props not Readonly)**: 21 of 40 findings.

### The non-obvious part: touching a component pulls its file's whole smell backlog onto "new code"

None of the 40 findings were on lines the diff *added* — verified by intersecting the annotations against `git diff -U0` hunks. They were all pre-existing. But **S6759 anchors on the component declaration**, so editing a component's props block or body is enough for its long-standing issue to count as new code and drag the rating down. Contrast PR #928, same module, same session: it touched a plain util + two specs (no React components) and got **0 new issues / gate passed**.

Consequence: any PR that edits component signatures in a file with a smell backlog inherits that backlog. The reliable fix is to clear the whole category in the files you touch (e.g. wrap **every** component's inline props in `Readonly<>`, not just the ones flagged), which is type-only and provably output-neutral. Do NOT "fix" flagged a11y items in untouched code that carry deliberate `biome-ignore` justifications — that changes served markup for no gain.

### Fetching the real findings with NO Sonar token and NO MCP

The Sonar MCP is often not connected, and `sonarcloud.io/api/...` returns `{"errors":[{"msg":"Project doesn't exist"}]}` unauthenticated because `GrooveHQ_axis` is private. There is no `sonar-project.properties` and no `SONAR_*` in the workflows — it runs as the SonarCloud **GitHub App** (automatic analysis). So read it off the GitHub check run instead:

```bash
# failed gate conditions
gh api "repos/GrooveHQ/axis/commits/$(git rev-parse HEAD)/check-runs" \
  --jq '.check_runs[] | select(.name|test("Sonar")) | {conclusion, title:.output.title, summary:.output.summary, annotations:.output.annotations_count}'
# every finding with file:line + rule message (PAGINATE — the first page caps at 30)
RUN=$(gh api "repos/GrooveHQ/axis/commits/$(git rev-parse HEAD)/check-runs" --jq '.check_runs[]|select(.name|test("Sonar"))|.id')
gh api --paginate "repos/GrooveHQ/axis/check-runs/$RUN/annotations" --jq '.[] | [.path,.start_line,(.title//"-")] | @tsv'
```

A passing gate's summary carries a `0 New issues` line; a failing one lists only the failed conditions.

**How to apply:** a manual Sonar pass MUST scan for **Bug/Vulnerability (reliability/security) rules first** — those are what gate — then the smells. Reliability rating maps to bug severity: C = major bug, **D = critical bug**, E = blocker bug. One critical bug ⇒ gate fails.

### Bug rules to grep for (these gate — check these FIRST)

- **`typescript:S2871` — `Array.prototype.sort()` / `.toSorted()` with NO compare function** is a **reliability Bug** (not a smell), even on `string[]`. Fixes the gate: `.sort((a, b) => a.localeCompare(b))` for strings, `(a, b) => a - b` for numbers. Grep every `.sort()` / `.toSorted()` in the diff. (Avoid `(a,b) => a<b?-1:a>b?1:0` — that's a nested ternary → S3358.)
- Also sweep for other common reliability bugs in a diff: identical sub-expressions on both sides of `&&`/`||`/`===`, `Number`/`parseInt` NaN mishandling, unresolved promises, `useState` setter never used, array index as React `key`.

**How to apply:** Before finalizing any PR touching JS/TS, scan for these patterns and rewrite. They mostly map to easy alternatives.

## Code-smell rules we've hit (Maintainability — usually non-gating, but the user still wants them pre-empted)

- **`typescript:S2245` — `Math.random()`** is treated as a security hotspot regardless of context (color picker, demo data, anything). Use `randomInt` from `node:crypto` on the backend (`import { randomInt } from 'node:crypto'`). On the frontend, prefer `crypto.getRandomValues(new Uint32Array(1))[0] / 2**32` or accept the hotspot if the value is purely cosmetic and mark it "Safe" in the SonarCloud UI.
- **`S6772` — children-as-prop on JSX**. `<Comp children={…} />` fails. Always nest: `<Comp>…</Comp>`. Especially common with `@tanstack/react-form`'s `<form.Field name="x">{(field) => …}</form.Field>` pattern.
- **`S6759` — props not marked Readonly**. Inline component prop types like `({ x }: { x: T })` need to be `Readonly<{ x: T }>`. Field-level `readonly` modifiers on a separate `interface` may or may not satisfy the rule depending on Sonar's analyzer version — wrap in `Readonly<>` to be safe.
- **`S3358` — nested ternary**. Any ternary inside another ternary fires. Extract to a named helper function, an early-return, or an `if/else` block.
- **`S4624` — nested template literals**. Inner backticks inside an outer template (`` `/path${cond ? `?${q}` : ''}` ``) fire. Hoist into a `const` first: ``const path = cond ? `/x?${q}` : '/x';``.

## Process to avoid these proactively

1. **Install SonarLint Connected Mode** (VS Code/JetBrains plugin). Connect it to `sonarcloud.io` with a project-scoped token + bind to project key `GrooveHQ_axis`. Issues then surface as IDE squigglies as you type, identical ruleset to CI.
2. **Run a self-review pass before commit** specifically scanning for the patterns above. They show up in roughly half the React diffs.
3. **Use `gh pr checks <num>` + `gh run view <id> --log-failed`** to fetch failing check details (already configured). For SonarCloud specifically, the GitHub annotations panel (visible via the saved-page method when the API is auth-gated) lists each rule with line numbers — that's the fastest way to triage when issues do slip through.

The biome rules in `biome.jsonc` overlap partially with Sonar's set but don't cover all of these (e.g. `noChildrenProp` exists in biome but `noNestedTernary` would need explicit enablement). A future task could mirror the rules in biome to catch them at lint time.
