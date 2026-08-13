---
name: project_claude_config_repo_symlinked_skills
description: "The claude-config repo backs up ~/.claude/skills symlinks, not the skill content, which lives in ~/.agents/skills"
metadata: 
  node_type: memory
  type: project
  originSessionId: b507c086-0f57-43dc-99d3-33f1a8c4e81c
  modified: 2026-08-13T05:47:00.670Z
---

`~/.claude` is a git repo pushed to `curiousyuvi/claude-config` (private, set up
2026-08-13). Most entries under `~/.claude/skills/` are **symlinks** into
`~/.agents/skills/` (brandkit, gpt-taste, design-taste-frontend,
full-output-enforcement, high-end-visual-design, image-to-code,
imagegen-frontend-{web,mobile}, industrial-brutalist-ui, minimalist-ui,
redesign-existing-projects, stitch-design-taste). Git stores the link, not the
target, so those skills are **not actually backed up** by that repo. Only the
real directories are: copywriting, lean-ctx, gitnexus-*,
thermo-nuclear-code-quality-review.

**Why:** `~/.agents/` is outside the repo root, so no gitignore whitelist can
reach it. A restore from `claude-config` alone would leave a dozen dangling
symlinks.

**How to apply:** If Yuvraj asks for a full config backup or a restore on a new
machine, flag this and either add `~/.agents` as a second repo/submodule or
replace the symlinks with real copies. Do not claim the skills are backed up.

Related: the auto-push Stop hook and the tracked-path whitelist are documented in
`~/.claude/CLAUDE.md`.
