---
name: recorder-app-macos-testing
description: "macOS local-testing traps for the Helply desktop recorder (TCC identity, deep-link registration, stale user data) and where the full recipe lives"
metadata: 
  node_type: memory
  type: project
  originSessionId: 887f294a-fcd7-4b6a-9b3a-6561b071b31d
  modified: 2026-09-18T07:42:15.024Z
---

The Helply desktop recorder (`~/Work/Repositories/helply-recorder-app`) has a committed
`AGENTS.md` (commit 30c78d1, 2026-09-18) with the full macOS local-testing recipe. Essentials:

- `npm run package:mac-unsigned` builds are linker-signed as generic "Electron", so macOS TCC
  grants never attach; after every build: `codesign --force --deep --sign - --identifier
  com.helply.recorder <app>`, then `tccutil reset ScreenCapture|Microphone|Accessibility
  com.helply.recorder`, then `lsregister -f <app>` (deep-link login needs the scheme registered).
- Dev mode (`npm start`) cannot log in: no `helply-recorder://` handler; prompts name "Electron".
- Keep exactly one app copy on the machine; Screen Recording applies on next launch.
- Stuck skeleton loaders = stale session token; clear `~/Library/Application Support/helply-recorder{,-app}`.
- `release/app/` is source (packaging manifest), never delete; build output is `release/build/` only.
- All obsolete once builds get the real Developer ID cert.
