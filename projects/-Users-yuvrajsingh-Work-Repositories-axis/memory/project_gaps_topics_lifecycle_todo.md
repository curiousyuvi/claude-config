---
name: project-gaps-topics-lifecycle-todo
description: "Gaps work to do once JJ's Topics PRs #1845 (stop tracking events) and #1863 (move/merge/delete) merge: subscribe lifecycle events, fix merged()/deleted(), queue filter, adapter conflict. User will say when they merge."
metadata:
  node_type: memory
  type: project
  originSessionId: 5297b585-30e3-414e-8e5f-0ed29a5a3fce
  modified: 2026-10-28T13:20:49.154Z
---

Recorded 2026-10-28. The user asked me to remember this through compactions; they will tell me when JJ's PR merges. Fixes go on #1810 (ys/feat/screenshot-agent); the user wants no extra PRs.

Context: BUG-07 / eval case TOP-09 (archiving, deleting or merging a subtopic leaves its gaps open) is pending on these. `GapSubtopicLifecycleService` (knowledge-gaps/application/services/gap-subtopic-lifecycle.service.ts) has reconcile/merged/deleted, but nothing calls it yet.

To build when #1845 + #1863 are on master:
1. **Event subscriber:** add `KnowledgeGapsAutomationRegistrar` in knowledge-gaps/application/, modelled on modules/csat/application/csat-job-processor.registrar.ts. Register it in knowledge-gaps.module.ts; QueueModule is @Global, so inject AutomationSubscriberRegistry directly. Read `data.payload`, with `orgId = payload.orgId` (the outbox injects it). Subscriptions:
   - `topic.subtopic_archived` {v, subtopicId, topicId, via, reason, gapIds, archivedAt, actor}: call `reconcile(orgId, subtopicId, gapIds, new Date(archivedAt))`.
   - `topic.subtopic_restored` {v, subtopicId, topicId, via, actor}: call `reconcile(orgId, subtopicId)`.
   - `topic.subtopics_merged` {v, sourceSubtopicIds, targetSubtopicId, actor}: call `merged(orgId, sources, target)`. Merged sources do not also get a deleted event.
   - `topic.subtopic_deleted` {v, subtopicId, topicId, via, actor}: call `deleted(orgId, subtopicId)`. A topic delete emits one per child.
2. **Fix `merged()`:** delivery is unordered, so the target can be stopped or deleted before the job runs.
   - Target STOPPED: move the gaps, then archive them as SUBTOPIC_STOPPED, so a restore brings them back.
   - Target DELETED: archive the sources' gaps as SUBTOPIC_DELETED.
   - Today it returns early, so the gaps stay open forever on a DELETED subtopic.
3. **Fix `deleted()`:** gaps already archived as SUBTOPIC_STOPPED must flip to SUBTOPIC_DELETED. Also delete that subtopic's knowledge_gap_checks rows, the way merged() does.
4. **Decide:** `subtopicIdsForTopic` (TableGapTopicsAdapter) includes deleted and merged-away subtopics, so the topic-scoped gaps queue shows gaps left on them. Probably filter `deleted_at IS NULL`.
5. **Merge conflict in table-gap-topics.adapter.ts:** keep both sides, `state: stateOf(row)` from JJ's PR and `archivedAt: stoppedAt(row.archived_at, row.topic_archived_at)` from ours.
6. **SubtopicDeletedEvent:** I asked JJ in review to export it from the topic-insights barrel. If he hasn't, do it.
7. **Afterwards:** re-run eval case TOP-09 (harness ~/Downloads/gaps-e2e, output ~/Downloads/gaps-e2e-rerun), plus merge/delete variants. Mark BUG-07 fixed in ~/Downloads/gaps-e2e-rerun/SUMMARY.md.

**Why:** the user called all of these important.
**How to apply:** when the user says #1863 (or #1845) merged, merge master into #1810 and do steps 1-7. Related: [[project-gaps-stacked-branches]], [[project-knowledge-gaps-feature]].
