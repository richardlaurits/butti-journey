# Architecture Overview

## System Design

ButtiBot is a locally-running AI assistant built on OpenClaw. It operates in a multi-agent architecture where specialized agents handle different domains.

### Core Components

#### 1. Main Agent (ButtiBot)
- **Runtime:** Node.js + Anthropic Claude API
- **Memory:** SOUL.md, USER.md, MEMORY.md, daily logs
- **Skills:** 13+ installed
- **Responsibilities:** General assistance, orchestration, user interaction

#### 2. Specialized Sub-Agents
- **Health Agent** — Track diabetes, fitness, nutrition, weight trends
- **FPL Agent** — Premier League Fantasy Football analysis
- **Bundesliga Agent** — Bundesliga Fantasy analysis
- **Serie A Agent** — Serie A Fantasy analysis
- **Career Agent** — Job market research & scraping

#### 3. Automation Layer
- **Heartbeat:** 30-min polling (email, weather, calendar checks)
- **Cron Jobs:** Scheduled tasks (morning brief 07:00 CET)
- **GitHub Actions:** Future webhook triggers

#### 4. Data Layer

**Local Storage:**
- `~/.openclaw/workspace/` — Main workspace (all configs, skills, agents)
- `MEMORY.md` — Long-term memories
- `memory/YYYY-MM-DD.md` — Daily session logs
- `agents/*/` — Agent configs & data

**External Services:**
- Gmail (OAuth) — Email monitoring
- GitHub (PAT) — Repo management
- ClawHub API — Skill registry
- Telegram API — Messaging
- Anthropic API — LLM inference

### Data Flow

```
User Input (Telegram/Web)
    ↓
ButtiBot Main Agent
    ├→ Email check (Gmail)
    ├→ Health data analysis (Health Agent)
    ├→ Fantasy updates (FPL/Bundesliga/Serie A agents)
    ├→ Web scraping (Playwright/Tavily)
    ├→ GitHub operations (Repos/Issues/PRs)
    └→ Job market research (Career Agent)
    ↓
Output (Telegram/GitHub/Local Files)
```

### Skill Integration

Each skill is modular and can be chained:

```
Job Hunt Workflow:
1. Playwright Scraper → Extract job listings from career sites
2. Web Scraper → Parse job details into JSON
3. Tavily Search → Find salary/company data
4. Coding Agent → Analyze data + generate report
5. GitHub → Commit results to job-crawler repo
6. Telegram → Alert Richard with findings
```

### Security Model

**Local Execution:**
- All code runs on Richard's machine (no cloud processing)
- Skills have sandboxed access to filesystem
- Secrets in `~/.bashrc` (not in git)

**API Authentication:**
- GitHub PAT (90-day rotation)
- Gmail OAuth token (auto-refresh)
- ClawHub API token (if publishing)
- Telegram bot token (restricted to @MrLaurits_Bot)

**Data Privacy:**
- Private GitHub repos for sensitive data
- No telemetry/analytics collection
- All personal health data encrypted at rest

---

## Deployment

**Hardware Requirements:**
- Linux VM (Ubuntu 22.04+)
- 4GB RAM minimum
- 2 CPU cores
- 20GB storage

**Installation:**
```bash
# Already done ✅
npm install -g openclaw clawhub
openclaw config init
clawhub install github playwright-scraper-skill tavily-search
```

**Secrets Setup:**
```bash
# In ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="ghp_..."
export CLAWHUB_TOKEN="clh_..."
export TELEGRAM_BOT_TOKEN="..."
```

---

## Performance & Costs

**Token Usage (per day):**
- Heartbeat checks: ~500 tokens
- Morning brief: ~1,500 tokens
- Job scraping: ~2,000 tokens (depends on site complexity)
- Casual requests: ~500-1,000 tokens
- **Total:** ~4,500 tokens/day (varies)

**API Costs (monthly):**
- Anthropic Claude API: $5-15 (depending on token usage)
- GitHub API: Free (public repos)
- Gmail API: Free
- Telegram API: Free
- **Total:** ~$5-15/month

---

## Scalability

**Current Bottlenecks:**
- Anthropic API rate limits (solved via authentication)
- Job site anti-bot protection (solved via Playwright)
- Memory context (solved via Token Optimizer skill)

**Optimization Strategies:**
1. Batch similar requests (email → calendar → weather in one heartbeat)
2. Use Cron for long-running tasks (keeps main session light)
3. Cache results (GitHub repos as cache layer)
4. Sub-agent isolation (keeps main session clean)

---

**Last Updated:** 2026-02-17 23:50 CET
