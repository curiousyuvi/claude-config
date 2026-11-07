---
name: local-prod-snapshot-workflow
description: "Helply + InstantDocs prod workspaces copied into the local DB (2026-11-06) so the screenshot agent and gaps are tested locally, then shipped in one PR"
metadata:
  node_type: memory
  type: project
  originSessionId: f52b7cfa-40e4-4905-aaed-8f32ce04ad40
  modified: 2026-11-07T01:08:01.255Z
---

User decided (2026-11-06): stop testing the gaps and screenshot agent in prod with PR after PR. Test locally on a prod copy, then ship one PR once satisfied. #1980 is the branch under test. It has origin/master merged locally, not pushed.

How the copy was made, with no PR and no deploy:
- Export: user runs a read-only psql file in their own terminal: `cd apps/backend && op run --env-file=.env.production -- sh -c 'PGPASSWORD="$DB_PASSWORD" psql "host=$DB_HOST port=$DB_PORT user=$DB_USER dbname=$DB_NAME sslmode=prefer" -X -q -f <export.sql>'`. It picks the orgs that have an app_capture_connections row (prod: exactly InstantDocs + Helply; the names don't match exactly by `name in (...)`). One repeatable-read read-only transaction. Every table with org_id, plus organizations, ba_organizations, ba_members and ba_users, written to CSV. Skips scheduled_messages, slack_workspace_settings, %backup% tables and all credential tables.
- Import: a bash script stages each CSV as text in schema `snap`, fakes emails and phones (@snapshot.test), deletes those orgs' local rows, inserts only the columns the local table has (`on conflict do nothing`) under session_replication_role=replica, and prints staged/inserted counts. outbox_events fails on partitions, which is wanted (don't replay old events).
- Then: local migrations via `MIKRO_ORM_MIGRATIONS_SNAPSHOT=false node --env-file=.env.local --import @swc-node/register/esm-register ./node_modules/@mikro-orm/cli/cli.js migration:up` (the pnpm scripts use op). db-objects and `bin/search-reindex.ts --org-id=<id>` run the same way.
- The scripts lived in session f52b7cfa's scratchpad (snapshot-export.sql, snapshot-import.sh, hash-password.mjs). Re-create them if that's gone.

Local ids: InstantDocs 019f84ef-f398-7939-88ba-63d1c28cd07a, Helply 019f84f0-1be2-70fb-8ce4-d7951d764b93. Login: yuvraj@snapshot.test / password (the imported Yuvraj user, admin in both; hash made with better-auth/crypto hashPassword).

Helply sign-in: legacy Helply has invisible reCAPTCHA v3 (score-based), so live sign-in from a Firecrawl browser fails at random ("Verification failed"). Cindy will exempt yuvraj+screenshotagent@groovehq.com on Mon 2026-11-09. Customers with reCAPTCHA will hit this too, so look into Firecrawl stealth/proxy options. The local Helply connection is on profile generation 9 after the user's successful local sign-in.

A Mac restart (2026-11-06 ~19:19 IST) wiped /private/tmp: the scratchpad scripts, the snapshot CSVs and dev.log were lost. The DB, Redis and Qdrant (Docker volumes) survived. Eval scripts now live in ~/Work/kg-eval/ (eval-round.sh), and the server log goes to ~/Work/kg-eval/dev.log. Eval harness: eval-round.sh <label> [title regex] saves, clears and re-queues the gaps. It also clears finished kg-survey-* jobs (same job id or the re-ask is dropped) and the per-day cap key app_capture:runs:day:<org>:<date>. The server must run as `pnpm dev 2>&1 | tee <scratchpad>/dev.log` so the logs can be read. Finished picture = img.url (already cropped and framed); edit.sourceUrl plus crop/elements (percent of source height, origin = centre) are only for re-editing.

Round 2 (2026-11-06, 18:16 IST) findings, not fixed yet: (1) the access block misses tRPC/REST JSON bodies, and the agent saved a password on the live test KB acme.instantdocsbase.com (kb/updateKBWebSharing) plus SEO; user told to turn it off; (2) reversible allows writes to other sites (Stripe checkout init seen); (3) the app's own background writes count as agent changes, 8 of 29 mark_screen refused; (4) an empty editor line is unnamed, so the agent can't type into a new doc (numbered list); (5) a drifting screen fingerprint defeats the repeat guard (20 alternating clicks); (6) cross-origin iframes (support widgets) aren't listed; (7) the "Send" label block conflicts with the playground-chat prompt; (8) shots taken before async content renders (blank Chats list, blank sidebar); (9) planner pictures "absence" statements and disabled Save buttons. Firecrawl 429 (100 concurrent jobs, account-wide) also seen.

2026-11-06 evening, uncommitted on #1980's branch (origin/master merged locally): user rejected word lists for safety ("strings that in many contexts are harmless"), so (1)(2)(3)(7) were replaced by a write judge. `decideRequest` keeps a floor: reads, sign-in, prefixes, no DELETE, no other site; else CHECK, then `WriteGate` (application/browser/write-gate.ts). Idle writes (>5 s after an action) are housekeeping. Writes an action caused go to a model judge (domain/write-check.prompt.ts, subfeature `guard`), cached per write shape plus onSample; bookkeeping verdicts are learned. Only label check left: `endsSession` (sign-out GET). Still to do: (4) (5) (6) (8) (9). Other word-matching found but NOT changed: `pressedStepKey` parses "press X" from step text (capture-recipe.ts); app-sign-in.ts finds sign-in buttons, paths and fields by English words.

STATE 2026-11-06 ~22:40 IST (resume here). On ys/fix/capture-survey-followups, ALL uncommitted, with origin/master merged locally (two merge commits, not pushed). Done and green locally (306 app-capture + telemetry tests, typecheck, lint):
- Write judge: capture-safety.ts floor returns CHECK; application/browser/write-gate.ts holds the verdicts and refusals; domain/write-check.prompt.ts; subfeature `guard`; deps.checkWrite in capture-model.service agentDeps.
- `endsSession` sign-out check is the only label check left.
- Fixes for items 4-7 and 9:
  - 'empty text area' fallback label in page-elements labelOf;
  - repeat guard keys on path plus role/name of each control, element by name (`repeated(tool, args)`);
  - `CaptureSession.networkQuiet` before shots, plus `networkMoved` listeners in open();
  - child frames listed after the page's (`PageElement.frame`, `ReadPageOptions.firstIndex`, `elementLocator` by frame url, first frame per url);
  - planner prompt skips absence statements and contact-support steps, and never targets Save on review steps.
- Wiki updated. A thermo-nuclear review was done and its fixes applied.

PENDING: (a) the user restarts the server with `pnpm dev 2>&1 | tee ~/Work/kg-eval/dev.log` (after `op` sign-in); (b) run `~/Work/kg-eval/eval-round.sh r3` (lean-ctx allow may be needed); (c) deep-analyse round 3: logs, actions, hints, screenshots viewed (render via a Pillow script like the old render_shots.py: download img.url into a raw folder, then view the PNGs); (d) then commit and push to #1980 when the user is satisfied. Also pending: the user's answer on replacing pressedStepKey with the validator. Separately: PR #1994 (kb natural size not an edit) MERGED; after deploy, run `kb:recompute-unpublished-changes -- --apply` on prod; the user must turn off the password protection the agent set on acme.instantdocsbase.com.

ROUND 3 (2026-11-06 22:52-23:47 IST, all 17 gaps): 23 pictures added (r2 22, prod 25). Safety held: the only write was one playground chat; no access writes. Chats 1 to 5 pictures. Editor gaps (numbered list, HTML blocks) still 0. Overnight probes r3b..r3l (user asleep, said keep going) on those two gaps found and fixed, uncommitted:
- the judge prompt blocked untitled new items (now: creating a new item is allowed) and editing-lock housekeeping on customer pages (now allowed on any page);
- SampleEdits rewritten: Firecrawl's remote browser gives NO response body for guarded requests (`Network.getResponseBody: No data found`), so a sample = a page the app moved to within 30 s of a POST change sent from another page (or whose id the request carried) that no earlier listing link or app memory pointed to; `CaptureSession.sentFrom` keeps {page, at};
- CUSTOMER_TEXT now tells the agent to create a new sample; an ON_SAMPLE line is appended to the page description on a sample;
- logs: `was refused N writes: reasons`, `blocked N requests: kinds`, and an action outcome of `+blocked`;
- pointerTip puts the ring at the start of an empty editor line.
Later that night (to 06:10 IST 2026-11-07), also uncommitted:
- trailChanged ignores saves sent from a sample;
- runs remember the samples they made (CaptureRun.samples becomes known screens with sample:true, named "Sample <title> made for an article"), and the known-screens list marks "(sample)";
- validator prompt: fail a menu left open, and fail a box on the step's result ("Select Export. The wizard opens").
Round r4 (all 17, 03:45-04:42): 23 pictures (HTML blocks 3, export 4, downloads 1; numbered list 0 that run, 2 in r3l/r4b). r5 was queued 05:08, but OrbStack hung about 05:42 (docker ps hangs, Redis not answering), so r5 never ran. Unit tests hang while Docker is down; the last edit (the "(sample)" marker) passed typecheck and lint but not tests. Next: the user restarts OrbStack, then rerun tests and `eval-round.sh r5`.
Other round 3 findings, not fixed: a stale dropdown left open in a picture (4-10, 3-4), the downloads toast is transient, and the export wizard needs OAuth (should skip sooner). Analysis tooling: ~/Work/kg-eval/shots.mjs (needs NODE_EXTRA_CA_CERTS=$HOME/.portless/ca.pem), trace.mjs and subfeatures.mjs (local Jaeger :16686). eval-round.sh labels r3b..r3l are saved in kg_eval_runs.

**Why:** prod fix-forward loops cost the user several PRs a day. Local copy, fix, eval, then one PR.

**How to apply:** local app connections use profile_generation +1000, so they never share prod's Firecrawl browser profile. Their saved password and TOTP were cleared, so sign-in is redone in the local UI. The target apps are test workspaces, per the user, so writes there are accepted. Related: [[capture-agent-smarter-plan]], [[project-knowledge-gaps-feature]].
