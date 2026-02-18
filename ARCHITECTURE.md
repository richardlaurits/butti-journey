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
- **Domain-specific agents** for different use cases
- **Isolated execution** to keep main session clean
- **Specialized knowledge** tailored to specific tasks
- **Independent memory** with main session visibility

#### 3. Automation Layer
- **Heartbeat:** Periodic polling for routine checks
- **Cron Jobs:** Scheduled tasks at specific times
- **GitHub Actions:** Webhook-based triggers (future)
- **Async Processing:** Long-running tasks in background

#### 4. Data Layer

**Local Storage:**
- `~/.openclaw/workspace/` — Main workspace
- `MEMORY.md` — Long-term memories
- `memory/YYYY-MM-DD.md` — Daily session logs
- `agents/*/` — Agent configs & data

**External Services:**
- Gmail (OAuth) — Email management
- GitHub (PAT) — Repository management
- Telegram API — Messaging & notifications
- Anthropic API — LLM inference

### Data Flow

```
User Input (Telegram/Web)
    ↓
ButtiBot Main Agent
    ├→ Email checks (Gmail)
    ├→ Data analysis (Sub-agents)
    ├→ Web scraping (Playwright/Tavily)
    ├→ GitHub operations (Repos/Issues)
    └→ Notifications (Telegram)
    ↓
Output (Telegram/GitHub/Local Files)
```

### Skill Integration

Skills are modular and can be chained:

```
Example Workflow:
1. Web Scraper → Extract data from websites
2. Data Parser → Parse/structure data
3. Analyzer → Generate insights
4. GitHub → Store results with history
5. Notification → Alert via Telegram
```

### Security Model

**Local Execution:**
- All code runs on user's machine
- Skills have sandboxed access
- External APIs accessed via tokens only

**API Authentication:**
- Token-based access (revocable anytime)
- Secrets stored locally, not in git
- Regular token rotation
- No password storage

**Data Privacy:**
- Private repositories for sensitive data
- No external logging or telemetry
- User retains full data control

---

## Deployment

**Hardware Requirements:**
- Linux VM (Ubuntu 22.04+) or equivalent
- 4GB RAM minimum
- 2 CPU cores
- 20GB storage

**Installation:**
```bash
npm install -g openclaw
openclaw config init
# Install desired skills via clawhub
```

**Secrets Setup:**
```bash
# In ~/.bashrc or ~/.zshrc
export GITHUB_TOKEN="your-token"
export CLAWHUB_TOKEN="your-token"
```

---

## Performance & Costs

**Token Usage (per day):**
- Routine checks: ~500 tokens
- Scheduled tasks: ~2,000 tokens
- Research/analysis: ~1,500 tokens
- **Total:** ~4,000 tokens/day (varies)

**API Costs (monthly):**
- Anthropic Claude API: $5-20 (depends on usage)
- GitHub API: Free (public repos)
- Gmail API: Free
- Telegram API: Free
- **Total:** ~$5-20/month

---

## Scalability

**Current Architecture Strengths:**
- Modular skill system
- Sub-agent isolation
- Async task processing
- Token optimization

**Optimization Strategies:**
1. Batch similar requests together
2. Use Cron for long-running tasks
3. Cache results in GitHub
4. Sub-agent isolation keeps memory light

---

**Last Updated:** 2026-02-18 07:45 CET
