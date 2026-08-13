---
name: feedback-test-doc-prompts
description: "Don't bake test-doc-specific examples into LLM-facing prompts. Keep them generic so they don't bias real customer-app runs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bcef0bbe-dab8-4443-8005-65b8e65e1a84
---

When iterating on agent prompts during testing, never let names or
specifics from the test corpus accumulate inside any string the LLM
reads at runtime: gate prompts, planner prompts, picker prompts,
tool descriptions, action result memos. They drift in as "concrete
illustrative examples" while we're iterating on a single test
article, and stay in production where they bias the model against
real customer apps.

Specifically for the [[project-screenshot-agent]] codebase, the
LLM-facing surfaces are:
- `screenshot_agent/agents/prompts/*.md` (gate, planner, picker
  system prompts).
- Inline f-string prompts in `screenshot_agent/agents/annotator.py`
  — gate_prompt, pick_prompt, gate_section, action_section.
- Tool descriptions in `screenshot_agent/browser/hover_skill.py` —
  `hover_element_by_index`, `click_at_coordinates`,
  `click_revealed_child` (browser-use exposes the action's
  description string to the navigator LLM).
- ActionResult memory strings returned by the tools.

Code comments (`#` lines, docstrings used for developer
documentation) are NOT LLM-facing — they're safe places to record
why a fix landed, even when "why" references the specific InstantDocs
article that surfaced the bug.

**Why:** During the May 2026 InstantDocs spike, two test articles
(`/doc/add-doc`, `/doc/domains-and-redirects`) seeded the gate
prompt with examples like "the green check mark after domain
verification" / "the CNAME verification instructions" / "the
three-dots menu on a knowledge base card" / "the InstantDocs doc
editor". The picker's inline gate_section grew a "do NOT pick the
knowledge-base 'Test' title" example using the literal test KB
name. The Lucide icon library was treated as the default everywhere
in `hover_skill.py` because the test app uses it. The user
(Yuvraj) audited and asked me to strip them out — see the
"Strip test-doc-specific examples from LLM-facing prompts" commit.

**How to apply:** When you add or modify any LLM-facing prompt or
tool description in this codebase:

1. If you reach for a concrete example to illustrate a rule, ask
   "would this example make sense for a Stripe dashboard / e-commerce
   admin / CRM that isn't InstantDocs?" If no, either generalize it
   ("a verified-state indicator on a list item" beats "a green
   check mark on a verified domain") or drop the example and state
   the underlying rule.
2. Examples that use multiple unrelated SaaS patterns are good —
   they show the LLM the lesson generalizes ("e.g. configure SSO,
   open the project settings menu, connect a payment method").
3. Specific element class names from the test app (`lucide-plus`,
   `bn-button`, etc.) should appear in tool implementations (queries,
   matchers) freely — but in prompt text they should be framed as
   "one common pattern" alongside Heroicons, Material Symbols,
   in-house SVGs.
4. Periodically audit by grepping prompts for app-specific tokens:
   `grep -rn "instantdocs\|cname\|knowledge base card\|three-dots\|
   lucide-plus" screenshot_agent/agents/prompts/
   screenshot_agent/agents/annotator.py
   screenshot_agent/browser/hover_skill.py`.
