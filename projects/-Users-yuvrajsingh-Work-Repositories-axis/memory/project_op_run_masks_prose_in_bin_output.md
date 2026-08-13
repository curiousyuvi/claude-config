---
name: project-op-run-masks-prose-in-bin-output
description: "op run redacts short vault secret values wherever they appear in stdout, including inside ordinary English words in bin script output"
metadata: 
  node_type: memory
  type: project
  originSessionId: cf4559da-6d1d-4711-9be5-10ce3c24b1ea
  modified: 2026-08-04T14:47:30.772Z
---

`op run` scans a wrapped process's stdout for known secret VALUES and replaces them with
`<concealed by 1Password>`. It matches raw substrings, not whole tokens, so a short/low-entropy secret in
the vault corrupts ordinary prose. Seen in production 2026-08-04 running `pnpm --filter backend
kb:move-org` in the Railway shell:

```
the search/AI steps be<concealed by 1Password> are what repairs them
```

("below" got partially masked.) Consequences worth remembering:

- Any `bin/` script run through `op run` can have its human-readable output AND its `--report=` JSON
  mangled. If a report file looks truncated or a message reads oddly in a deployed shell, suspect this
  before suspecting the script.
- It is also a security signal in its own right: a secret short enough to occur inside a common English
  word has almost no entropy. Something in the `Axis Production` vault matched ~3-5 characters of
  "below" and should be rotated or reclassified as non-secret.

Not reproducible locally when `op` isn't signed in (the script runs without `op run` at all — see
[[project-run-app-context-bin-without-op]]).
