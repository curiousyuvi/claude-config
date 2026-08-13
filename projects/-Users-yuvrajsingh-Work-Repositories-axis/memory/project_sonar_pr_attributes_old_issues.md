---
name: project-sonar-pr-attributes-old-issues
description: SonarCloud PR gates fail on pre-existing issues in changed files — likely a shallow clone denying it blame data
metadata: 
  node_type: memory
  type: project
  originSessionId: 7cc61853-fad8-4679-9603-21f16494f649
  modified: 2026-08-09T10:07:55.677Z
---

A PR can fail `new_maintainability_rating` on issues it did not introduce. Seen on #1090: gate ERROR with rating 3, six issues — and `git blame` put five on an earlier merged commit and one months older, while master's own gate was OK.

**The tell:** every reported issue sat in a file the PR modified, and none anywhere else. Without git blame data SonarCloud cannot separate old lines from new, so it treats all issues in changed files as new code. Usually caused by a shallow clone (`fetch-depth: 1`) in the Sonar CI step; the workflow files are not in the repo checkout, so this has to be fixed wherever CI is configured.

**Before fixing anything, check whether it is yours:**
```
mcp__sonarqube__get_project_quality_gate_status(projectKey: "GrooveHQ_axis")              # master
mcp__sonarqube__get_project_quality_gate_status(projectKey: "GrooveHQ_axis", pullRequest: "<n>")
mcp__sonarqube__search_sonar_issues_in_projects(projects: ["GrooveHQ_axis"], pullRequest: "<n>")
git blame -L <line>,<line> --porcelain <file> | head -1
```

Master green + PR red + all issues confined to changed files ⇒ not a regression. Fixing them still unblocks the merge and is usually cheap, but say plainly in the PR that they are pre-existing, or the diff reads as unrelated scope creep.

Related: [[feedback_sonar_rules]]
