---
name: user_timezone_ist
description: "The user is in IST (UTC+5:30); give times in IST, not UTC"
metadata:
  node_type: memory
  type: user
  originSessionId: 37833cef-2ea3-4a31-935a-0974e560e82c
  modified: 2026-09-30T09:47:40.862Z
---

The user works in IST, UTC+5:30 (machine `date` reports IST; commits carry +0530).

**Why:** asked "talk in my timezone" (2026-09-30) after I reported deploy times and a timer in UTC.

**How to apply:** state times in IST. Logs, Railway, GitHub and AWS all report UTC, so convert before reporting (add 5:30). When a UTC value matters for cross-referencing a log, give IST first and UTC in parentheses.
