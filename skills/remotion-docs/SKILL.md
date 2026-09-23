---
name: remotion-docs
description: |
  Fetch authoritative Remotion documentation instead of guessing at its APIs,
  CLI flags, limits and defaults. Use when working with Remotion, @remotion/lambda,
  @remotion/renderer, @remotion/player, @remotion/media-parser, OffthreadVideo,
  compositions, or when deploying/sizing Remotion Lambda functions and sites.
---

# Remotion docs

Remotion's docs are fetchable as plain markdown. Prefer them over recalled knowledge:
the API moves fast and version defaults change between majors.

## Orientation

`https://www.remotion.dev/llms.txt` is a ~11 KB cheatsheet written for LLMs: project
structure, core components, the rules Remotion enforces (no `<video>`, use `<OffthreadVideo>`;
no CSS animations, drive everything from `useCurrentFrame()`). Read it first when starting
Remotion work or when unsure which primitive applies.

## Any specific page

Append `.md` to a docs URL to get markdown rather than rendered HTML:

```
https://www.remotion.dev/docs/lambda/disk-size      -> HTML
https://www.remotion.dev/docs/lambda/disk-size.md   -> text/markdown
```

Fetch the `.md` form. The HTML form loses code blocks and renders defaults through React
components, so numbers show up as component names instead of values.

## Finding the page

`https://www.remotion.dev/sitemap.xml` lists every URL. Grep it:

```bash
curl -sS https://www.remotion.dev/sitemap.xml | grep -o '<loc>[^<]*</loc>' | grep lambda
```

## Version matters

Check the installed version before trusting any default:

```bash
pnpm exec remotion versions
```

Defaults change across majors (Lambda disk defaulted to 2048 MB below 5.0.0, 10240 MB from
5.0.0). A doc page states the current default, which may not be the one a 4.x install used.
`remotion versions` also reports package-version mismatches, a common cause of unexplained
render failures.

## Reading Lambda render failures

Errors surfaced to the caller are often downstream of the real one. Get the function's own
CloudWatch log and read it in timestamp order:

```bash
aws logs tail /aws/lambda/<function-name> --follow --region <region>
```

Remotion appends a generic "disk space is low" hint to asset-fetch failures regardless of
cause, so treat it as boilerplate rather than a diagnosis. A `Could not extract frame from
compositor` with `ECONNRESET`/`ECANCELED` means the compositor process died; check whether it
precedes or follows the proxy error to tell cause from consequence.
