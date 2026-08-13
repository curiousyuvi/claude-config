---
name: reference-axis-ci-gates
description: "Axis PR CI gotchas — SonarCloud S2068 on password-named props; React Doctor 49/100 is informational, not the gate"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f77596b0-3faf-495c-b304-f5fb513ff117
---

Two Axis PR CI gates that mislead:

**SonarCloud (MQR mode).** The quality gate condition that bites is **"Security Rating on New Code ≥ A"**. A Security *Rating* is driven by **vulnerabilities** (a Major one = C → gate fails); security *hotspots* (e.g. S5852 super-linear regex, S1313 hardcoded IP) only affect the separate *Security Review* rating and do NOT fail this condition. **S2068 ("Review this potentially hard-coded password") fires on any `password:`/`secret:`/`token:`/`pwd:` property assigned a string literal — even when the literal is an env-var NAME, not a secret.** It caught `password: 'REDIS_PASSWORD'` in `redis.module.ts` (PR #589). Fix: never write `password: '<literal>'`; build config keys from a prefix (`config.get(\`${prefix}_PASSWORD\`)`) so the password value is a function call, not a literal. Enumerate PR findings via the GitHub check annotations (`gh api repos/GrooveHQ/axis/check-runs/<id>/annotations`, capped at 50) — the unauthenticated SonarCloud API returns 0 for PR-scoped queries.

**React Doctor.** The posted PR comment score (e.g. "49/100") is an **informational whole-repo health scan** (`react-doctor --score`, no diff scope, all projects) — one PR can't move it. The actual GATE is the green/red check: `--diff master` (changed files) + `fail-on error`; it passes as long as the changed files have 0 error-level findings (warnings are fine). Don't chase the 49.

**More gates hit on PR #636 (KB editor, [[project-kb-editor-blocks]], 2026-07-03):**
- **Web Build (`pnpm --filter web build`) OOMs on CI's ~2GB node heap** — the KB editor bundle pulls shiki grammars + mermaid + hls + katex → a 4MB+ chunk; passes locally (more RAM). Fix: `NODE_OPTIONS: --max-old-space-size=4096` on the ci.yml "Build web" step env (NOT the shared web `build` script — Yuvraj rejected mutating that; it hits every platform/context). Done in commit 11f9265c.
- **Unused Dependencies (knip):** `pnpm exec knip`; flagged `@radix-ui/react-popover` as unused — its only importer was the dead, unimported vendored scaffold `components/ui/emoji-toolbar-button.tsx` (the app's Popover uses the `radix-ui` meta-package). Fix: delete the scaffold + drop the dep + `pnpm install --lockfile-only --ignore-scripts` (the `safe-chain` preinstall hook blocks a normal `pnpm install` without `mise install`). Done.
- **SonarCloud gate here = "Reliability Rating on New Code ≥ A"** (not Security). The Sonar issues export (parse the downloaded HTML — strip `<style>`/`<script>`, then regex `file.tsx  message  <CleanCodeAttr>  Reliability|Security`) showed exactly **3 Reliability** issues (rest are Maintainability = don't affect this gate): `media-audio-node`/`media-video-node` (S6905 "media must have a `<track>` for captions" → add `<track kind="captions" />` as a child) + `table-toolbar-button.tsx` ("`role='button'` must be tabbable" → add `tabIndex={0}` **and** an `onKeyDown` for Enter/Space, else the keyboard-listener rule fires). FIXED commit d48abac4.
- **Lint & Format (`pnpm check` → `check:react-doctor` = repo-pinned react-doctor v0.1.2, whole `--project web`, `--fail-on error`) and the React Doctor workflow (npx react-doctor@latest v0.6.2, `--diff master --blocking error`) are REAL gates, NOT pre-existing noise** — my earlier note here was wrong. Both failed on 2 **error-level** findings in the NEW file `code-block-node.tsx`: `jsx-a11y/role-has-required-aria-props` (a `role="combobox"` needs `aria-controls` → add `React.useId()` id on the `CommandList` listbox + `aria-controls={id}` on the trigger) and `react-doctor/effect-needs-cleanup` (a `setTimeout` in `useEffect` with no cleanup → guard on the state + `return () => clearTimeout(id)`). Reproduce locally: `pnpm exec react-doctor . --project web --offline --fail-on error` (only `✗` = error-level blocks; `⚠` warnings don't). The posted "62/100" comment is still the informational whole-repo score — don't chase it. FIXED commit d48abac4.
- **My polish work itself is clean** (tsgo typecheck web+backend, biome, 1037 web tests, backend rendering+golden all pass). PR #636 commits pushed through d48abac4.

Related: [[project-kb-native-in-axis]], [[feedback-axis-verify-commands]].
