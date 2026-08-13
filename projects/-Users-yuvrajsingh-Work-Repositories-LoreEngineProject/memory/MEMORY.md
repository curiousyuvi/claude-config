# LoreEngine memory index

- [Autonomous phases](feedback_autonomous_phases.md) — don't pause between phases for permission; keep going unless something breaks
- [Commit cadence](feedback_commit_cadence.md) — commits on medium-substantial changes, PRs on very-big-substantial changes
- [Design system + brand assets](reference_design_system.md) — pointers to docs/design-system.md, logo files, typed tokens. Read before any UI work.
- [Realtime + RLS setAuth](feedback_realtime_rls_setauth.md) — call `realtime.setAuth(token)` before subscribing to RLS-protected channels, or every event gets dropped silently.
- [Anthropic prompt caching](feedback_anthropic_prompt_caching.md) — cache_control fires in agents/base.py for all agents; don't re-add per-agent. Min cacheable prefix is 1024 tokens.
- [Salience layer](project_salience_layer.md) — significance model + fast-path disambiguation + validator loop shipped (PR #24/#68, unmerged pending live test); cascade gated OFF, calibrate on evals before enabling.
