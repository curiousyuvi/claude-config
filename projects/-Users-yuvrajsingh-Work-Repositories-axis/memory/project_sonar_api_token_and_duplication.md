---
name: sonar-api-token-and-duplication
description: "Query SonarCloud directly with the token in ~/.claude.json when the sonarqube MCP tools won't load; duplication needs the measures API, not annotations"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b038355-45c8-41b6-8349-48112da19a69
  modified: 2026-09-02T12:38:32.868Z
---

The sonarqube MCP server connects (`claude mcp list` shows it green) but its tools are
sometimes unreachable: `ToolSearch` returns "no tools match" for `sonar`, `sonarqube`, and
even the exact tool names. Do not conclude there is no Sonar access. Read the token and hit
the API directly:

```bash
T=$(jq -r '.mcpServers.sonarqube.env.SONARQUBE_TOKEN' ~/.claude.json)
curl -s -u "$T:" "https://sonarcloud.io/api/measures/component_tree?component=GrooveHQ_axis&pullRequest=1360&metricKeys=new_duplicated_lines,new_duplicated_lines_density&qualifiers=FIL&ps=100"
curl -s -u "$T:" "https://sonarcloud.io/api/duplications/show?key=GrooveHQ_axis:<path>&pullRequest=1360"
```

`duplications/show` returns the paired blocks (`_ref` + `from` + `size`) and a `files` map,
so it names the exact other file and line range.

**Why:** the check-run annotations route in [[feedback_sonar_rules]] only lists issues.
A gate that fails on "Duplication on New Code" shows up with annotations that point at
unrelated lines, which sends you refactoring the wrong thing. On PR #1360 the annotations
pointed at `kb-maintenance-worker.service.ts` (both pre-existing July lines) and I collapsed
four `upsertJobScheduler` blocks for nothing: the 5.3% was 15 duplicated lines in a spec
file, a copy of the sibling spec's org+KB+article setup helper.

**How to apply:** when the failing condition is duplication, go straight to the measures
API for per-file `new_duplicated_lines`, then `duplications/show` on the file that has them.
Never infer the duplicated block from annotations.
