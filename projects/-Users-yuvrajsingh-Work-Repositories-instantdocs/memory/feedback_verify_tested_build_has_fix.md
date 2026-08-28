---
name: feedback-verify-tested-build-has-fix
description: "When a user reports a fix \"didn't work\", first prove the build they tested actually contained the fix"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3fb1e68f-618c-425c-afb4-299a6a3fcc7e
  modified: 2026-08-28T08:37:30.002Z
---

When the user says a fix didn't work, verify the tested bundle actually contains
the fix before hunting a new root cause. Compare build artifact identity, not
just intent: Next.js content hashes make this trivial (prod's
`webpack-*.js` runtime lists the chunk filenames it will load, so
`curl` the live runtime and diff the hash against the local patched build).

**Why:** In the iOS Safari 15 BlockNote lookbehind bug (PR #2661), the user
reported "not fixed, same error" and I spent a round trip looking for a third
cause. The crash log already named `…8bdc045bf978d000.js`, which was the
*pre-patch* chunk hash; prod had simply not been redeployed. The evidence was in
the log the whole time.

**How to apply:** Ask which build/URL was tested, and grep any provided stack
trace or console log for asset filenames first. An unchanged hash means the fix
was never exercised, so stop investigating and get it deployed. Cross-check
validity by confirming an *unrelated* chunk hash (e.g. react-dom) matches
between local and the tested deployment, which proves hashes are reproducible
across the two builds.

Related: [[feedback_ask_before_deciding]]
