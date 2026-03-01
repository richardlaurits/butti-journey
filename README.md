# ButtiBot Journey 🚀

*The evolution of a personalized AI assistant architecture*

**Timeline:** February - March 2026  
**Platform:** OpenClaw on Linux VM

---

## 📖 Overview

This repository documents the technical journey of building a multi-agent AI assistant using OpenClaw. It focuses on the architecture, lessons learned, and design patterns — not the specific applications built on top of it.

The actual implementations (specific agents, configurations, and personal data) live in private repositories.

---

## 🎯 Key Milestones

### Phase 1: Foundation
- Core identity and behavioral principles established
- Communication channels configured (Telegram)
- Workspace architecture designed

### Phase 2: Multi-Agent System
- Coordinator + sub-agent pattern implemented
- Specialized agents for different domains
- Inter-agent communication protocols

### Phase 3: Automation & Refinement
- Cron-based scheduling implemented
- Notification fatigue addressed through ruthless prioritization
- Public/private repository separation

---

## 🤖 Agent Architecture

```
Coordinator (Main Session)
│
├── Specialized Sub-Agents
│   ├── Career Agent (job search automation)
│   ├── Learning Agent (language acquisition)
│   ├── Sports Agent (fantasy analysis)
│   ├── Health Agent (metrics tracking)
│   └── Investment Agent (portfolio monitoring)
│
└── Automation Layer
    ├── Cron scheduler
    ├── Heartbeat monitoring
    └── Event triggers
```

### Design Principles

1. **Single Coordinator** — Main session handles orchestration
2. **Specialized Sub-Agents** — Domain experts for specific tasks
3. **Fire-and-Forget** — Sub-agents report completion, don't stay resident
4. **Public/Private Separation** — Architecture public, implementation private

---

## 🔑 Key Learnings

### What Worked Well

1. **Email-based interfaces** — Interactive buttons via mailto links
2. **Strict scheduling** — Consolidating jobs reduced noise significantly
3. **Hybrid data approaches** — APIs + parsing for best coverage
4. **Repository separation** — Clean boundary between public and private

### What Didn't Work

1. **Over-automation** — Too many cron jobs created notification fatigue
2. **Complex scrapers** — JavaScript-heavy sites broke headless approaches
3. **OAuth for email** — Tokens expired; app passwords proved more reliable

### Technical Insights

| Approach | Result |
|----------|--------|
| Email parsing | Highly reliable for structured data |
| REST APIs | Excellent when available |
| Web scraping | Fragile, use as fallback only |
| IMAP + App Passwords | More stable than OAuth for long-term |

---

## 🛠️ Technology Stack

- **Platform:** OpenClaw (Linux VM)
- **Language:** Python 3.13
- **APIs:** REST APIs, Telegram Bot API, various data sources
- **Tools:** Playwright (when scraping needed), GitHub CLI
- **Automation:** Cron, `at` for delayed tasks
- **Security:** Tailscale VPN, app passwords

---

## 📊 System Evolution

| Metric | Initial | Current |
|--------|---------|---------|
| Cron jobs | 15+ | 6 |
| Sub-agents | 3 | 8 |
| Daily interruptions | 10+ | 2-3 |
| Repos | 1 | 7 (1 public, 6 private) |

---

## 🎯 Current Capabilities

### Daily Automation
- Morning brief (curated information digest)
- Daily learning session
- Priority monitoring (emails, calendar)

### Weekly
- Domain-specific analysis (on schedule)
- Applied tasks summary
- Learning assessment

### On Request
- Deep-dive analysis
- Trip planning
- Ad-hoc research

---

## 🔒 Privacy & Security Model

**Public Repository (this repo):**
- High-level architecture
- Design patterns and lessons
- Generic workflow examples
- System evolution narrative

**Private Repositories:**
- Agent implementations
- API keys and credentials
- Personal data and configurations
- Specific use-case details

---

## 🚀 Future Directions

1. **Health Integration** — Connecting wearables and medical devices
2. **Family Communication** — Additional channels beyond Telegram
3. **Smart Home** — Voice control and automation
4. **Document Intelligence** — Automated analysis and summarization

---

## 🙏 Credits

- **OpenClaw** — The platform enabling this architecture
- **Open-source community** — Skills, patterns, and inspiration

---

*"Be genuinely helpful, not performatively helpful."* — Core principle

**Started:** February 2026  
**Last Updated:** March 2026
