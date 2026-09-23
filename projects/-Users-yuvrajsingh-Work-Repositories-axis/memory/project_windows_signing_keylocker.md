---
name: project_windows_signing_keylocker
description: "Windows recorder signing works only via `smctl sign --simple`, not the documented signtool/KSP path; cert expires 28 Jan 2027"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8740c10e-4dbf-4535-82ac-5dcbcef87f9b
  modified: 2026-09-20T15:48:16.293Z
---

Windows code signing for helply-recorder-app (DigiCert KeyLocker, EV cert,
Groove Networks Holdings Inc, account 1748137, keypair `key_1446942907`).

The working recipe on the Windows VM: install the **Windows Clients Installer**
from DigiCert ONE > KeyLocker > Resources > Client tools (the "DigiCert ONE
Clients" app alone gives `smctl` but NOT the KSP), run
`smctl windows certsync --keypair-alias=key_1446942907`, set `SM_HOST`,
`SM_API_KEY`, `SM_CLIENT_CERT_FILE`, `SM_CLIENT_CERT_PASSWORD` in the build
shell, then sign with `smctl sign --simple`.

**Why:** DigiCert's documented signtool+KSP path never works on this setup.
signtool always fails with "No private key is available" (with `/csp` + `/kc` +
`/f`) or "No certificates were found that met all the given criteria" (with
`/sha1` after certsync), even though `certutil -user -store My <hash>` reports
"Signature test passed" and `certutil -key -csp` lists the keypair. Two
competing KSP providers end up registered ("DigiCert Signing Manager KSP" and
"DigiCert Software Trust Manager KSP"); the cert binds to the second while the
docs and `smctl sign` (without `--simple`) pass the first. `--simple` bypasses
signtool entirely and timestamps itself. Not elevation-related: fails the same
in elevated and normal shells.

**How to apply:** `.erb/scripts/customSign.js` already uses `--simple`. Build
from the VM with `npm run package:publish:raw` after exporting the R2 keys, or
`npm run package:publish:win` if the 1Password CLI is signed in there. Never
`package:publish` on Windows: that env file carries the mac signing refs and
`op run` resolves every reference up front.

The VM is Windows on ARM, so `build.win.target` pins `arch: ["x64"]`; without
it electron-builder produces an arm64-only installer.

Certificate expires **28 Jan 2027** (Vikas's handover doc wrongly says Jan
2028). EV renewal needs business validation, so start around Dec 2026. The
signer on CertCentral order 1446942907 was Vikas until Sep 2026; only a user
with the **KeyLocker lead** role can reassign it, no reissue needed.

Related: [[project_helply_recorder_repos]]
