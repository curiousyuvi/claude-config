---
name: feedback-no-kb-redirect-feature
description: The KB has no article-to-article redirect and I must not propose or build one; retire/merge just unpublish
metadata:
  type: feedback
---
The KB has no redirect from one article to another (only legacy slug/segment redirects). Do not propose building one, do not put it in a design, do not ask about it. Retire and merge simply unpublish the old article; links to it break, which is why the judge proposes them only for solid reasons.

**Why:** The user has said this many times ("for the 100th time") and got angry when a design added a redirect PR.
**How to apply:** In gap change designs (retire_article, merge_article) never add redirect columns, reader changes or edge work. See [[project-post-eval-pr-backlog]].
