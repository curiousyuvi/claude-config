---
name: project-gap-legacy-cleanup-pr
description: "Cleanup PR GrooveHQ/axis#2245 MERGED 2026-11-23 IST (31be39fc4); next is prod testing of GitHub + gaps flows on the Groove workspace"
metadata:
  node_type: memory
  type: project
  originSessionId: 4cfbb9d1-da3f-43ed-8568-7f1b64dc2708
  modified: 2026-11-22T19:00:45.069Z
---

State 2026-11-23 IST:
- #2181 merged (cf2d7fb18), deployed, prod backfill applied (75 written).
- #2245 MERGED as 31be39fc4: drops legacy gap columns; migration locks both tables then a DO-block guard raises if unconverted old fixes remain. Staging never ran the backfill, so the staging pre-deploy may fail until the backfill runs there from cf2d7fb18 (command in the PR body).
- Prod GitHub Apps are all PRIVATE ("Only on this account"): prod `helply-github-integration`, staging `helply-github-integration-staging`, dev `helply-development`. Installs can only go to GrooveHQ, which blocks every customer. User drafted a Slack ask to Jared to make prod public.
- User connected GitHub for the Groove prod workspace and wants to test verify, screenshot hints, PR gaps and the drafter fixes on real data. Advice given: do NOT clear gaps; sample instead (editor verify, `knowledge-gaps:run` with small caps via railway ssh, Redraft 5-10 gaps, turn off auto-publish). Missing piece: a bin script to replay past merged PRs (`publishPullRequestMerged` {orgId, repositoryId, number}) and queue CODE_WEEKLY_ORG once; offered as a small PR, user has not answered.

See [[project-gap-article-edits-redesign]] and [[project-github-integration-plan]].
