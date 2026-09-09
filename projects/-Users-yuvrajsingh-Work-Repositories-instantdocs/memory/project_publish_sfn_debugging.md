---
name: project-publish-sfn-debugging
description: How to debug a broken/blank published article: check PublishedSnapshot rows, then the PublishVideoAndArticleTaskProd Step Functions execution history via aws cli
metadata:
  type: project
---

Published article with broken snapshot images usually means `publishedHTML` still holds `snapshot://<id>` tags but the `PublishedSnapshot` rows are missing, so `getHTMLWithSnapshotURLs` swaps in an empty src. The cause lives in the publish Step Function, not the KB renderer.

**Why:** `doOptimisticPublish` writes the placeholder HTML before the state machine runs; a failed run calls `finalize-failed-publish`, which only clears the rendering flags and leaves the placeholder HTML live (as of 2026-09-09).

**How to apply:** local `aws` CLI is authed to account 786844223641 (us-east-1). `aws stepfunctions list-executions --state-machine-arn ...:PublishVideoAndArticleTaskProd` then `get-execution-history` on the FAILED run. CLI timestamps print in local time (+05:30), so filter with python, not string compares. `TaskProgress` rows (type PUBLISH, `sfnName`) link a page to its execution name. As of 2026-09-09 every prod failure since June was `locale: null` input making `get-article-snapshots` 404. See [[project-voiceover-requeue-recovery]] for the sibling task-requeue pattern.
