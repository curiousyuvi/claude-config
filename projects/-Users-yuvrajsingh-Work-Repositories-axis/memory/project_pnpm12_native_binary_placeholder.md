---
name: project-pnpm12-native-binary-placeholder
description: "Failed to switch pnpm to v12.15.0 ... ENOEXEC" = pnpm 12 tool install kept its text placeholder bin; fix by running its install.js
metadata:
  type: project
---
`pnpm` in axis (packageManager pnpm@12.15.0) fails with "Failed to switch pnpm to v12.15.0 ... spawnSync .../.tools/pnpm/12.15.0/bin/pnpm ENOEXEC" (seen 2026-11-14). Cause: the pnpm 10 that downloads 12.15.0 into ~/Library/pnpm/.tools/pnpm/12.15.0 skips its lifecycle script, so `node_modules/pnpm/pnpm` stays a text placeholder instead of the native binary. This breaks `pnpm check` and the lefthook pre-commit hooks.

**Why:** deleting the folder only makes pnpm re-download the same broken placeholder; deleting the `12.15.0_tmp_*` folder next to it also triggered a re-download.

**How to apply:** run `cd ~/Library/pnpm/.tools/pnpm/12.15.0/node_modules/pnpm && node install.js` (node 24), then check `file .../bin/pnpm` says Mach-O. Leave the `_tmp_*` folder alone. Workaround without the fix: `npm_config_manage_package_manager_versions=false` lets the outer pnpm 10 run, but scripts that call pnpm again still fail.
