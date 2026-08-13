---
name: Freelancing goals and tooling
description: Freelance automation project at freelance-autopilot, partially configured, evaluating FreelanceMCP as alternative
type: user
---

- New to freelance platforms (as of 2026-04-06), but 3yr experienced SaaS developer + ex-CTO
- Target platforms: Upwork (primary), Freelancer.com (secondary)

## freelance-autopilot (custom-built 2026-04-06)
- Location: `/Work/Repositories/freelance-autopilot/`
- Python pipeline: scans platforms → scores with Claude Haiku → drafts proposals → Telegram notifications
- Pause/resume/reset CLI, SQLite state, configurable profile.yaml

### What's configured (as of 2026-04-07):
- Anthropic API key (scoring + drafting)
- Telegram bot + chat_id (notifications tested and working)

### Still needed to activate:
- **Google Custom Search API** (GOOGLE_API_KEY + GOOGLE_CSE_ID) — for scanning without platform APIs
- Upwork API credentials (apply at developer.upwork.com, may take days)
- Freelancer.com API token (optional, secondary)

### Key constraint:
- Upwork blocks direct scraping (403) and discontinued RSS feeds (Aug 2024)
- Must use official API or Google Custom Search as workaround

## FreelanceMCP (discovered 2026-04-07)
- GitHub: N1KH1LT0X1N/FreelanceMCP — MCP server for Claude Desktop
- More mature than custom autopilot: v2.1.0, 3000+ lines, Upwork + Freelancer APIs, Groq-based AI scoring, auto-bidding, email/Slack/Discord notifications, Docker support
- User was evaluating whether to switch to this as of 2026-04-07
- Would need Telegram notification added (has email/Slack/Discord already)
