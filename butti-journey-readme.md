# ButtiBot Journey 🚀

*The evolution of an AI assistant - from first boot to full autonomy*

**Author:** Richard Laurits  
**Birth of ButtiBot:** February 7, 2026  
**Timeline:** February 7 - March 1, 2026  
**Platform:** OpenClaw on Linux VM

---

## 📖 The Story

This repository documents the journey of creating **ButtiBot** - a personalized AI assistant built using OpenClaw. What started as a simple experiment evolved into a sophisticated multi-agent system handling everything from daily briefings to fantasy football analysis and job searching.

### The Name & Birth
**ButtiBot** - Born on February 7, 2026, during the first conversation. A playful, memorable name that stuck immediately.

---

## 🎯 Key Milestones

### Phase 1: Foundation (Feb 7-14)
- **Feb 7:** First boot and identity establishment
- **Feb 8:** Telegram integration established
- **Feb 10:** Fantasy Football agents created (FPL, Bundesliga, Serie A)
- **Feb 14:** Health agent created for diabetes management tracking

### Phase 2: Expansion (Feb 15-23)
- **Feb 17:** Career agent development begins
- **Feb 18:** Gmail dual-account setup (bot + personal)
- **Feb 19:** French tutor agent for FIDE A1 exam preparation
- **Feb 23:** Daily automation established (morning briefs, Jan's greetings)

### Phase 3: Refinement (Feb 24-28)
- **Feb 24:** Cron job cleanup - reduced from 15 to 6 essential jobs
- **Feb 27:** Enhanced Career Agent with interactive job emails
- **Feb 28:** Fantasy football simplified (FPL only on Fridays)

---

## 🤖 Agent Architecture

```
ButtiBot (Main/Coordinator)
│
├── 📧 Career Agent
│   └── Daily job emails with interactive buttons
│
├── ⚽ Fantasy Football
│   └── FPL analysis (Fridays only)
│
├── 🇫🇷 French Tutor
│   └── Daily lessons + weekly quizzes
│
├── 📊 Investment Agent
│   └── Portfolio monitoring (on demand)
│
└── ✈️ Travel Agent
    └── Trip planning & reminders
```

---

## 🔑 Key Learnings

### What Worked Well
1. **Email-based interfaces** - Interactive buttons in emails for job applications
2. **Strict scheduling** - Focusing FPL to Fridays only reduced noise
3. **Hybrid approaches** - Combining API data with web scraping for best results
4. **Private/Public separation** - Keeping personal data in private repos

### What Didn't Work
1. **Over-automation** - Too many cron jobs created notification fatigue
2. **Complex scrapers** - Career site scrapers often broke due to JS requirements
3. **Daily fantasy updates** - Too frequent, reduced to weekly

### Technical Insights
- **LinkedIn job alerts** → Most reliable job source (via email parsing)
- **FPL API** → Excellent for structured data
- **Brave Search API** → Good for quick web searches, not for deep scraping
- **Gmail IMAP** → More reliable than OAuth for long-term access

---

## 🛠️ Technology Stack

- **Platform:** OpenClaw (Linux VM)
- **Language:** Python 3.13
- **APIs:** FPL API, Yahoo Finance, Brave Search, Telegram Bot API
- **Tools:** Playwright (scraping), GitHub CLI, Gmail IMAP
- **Automation:** Cron, at
- **Security:** Tailscale VPN, app passwords (no OAuth)

---

## 📊 System Stats

- **Agents:** 8 specialized sub-agents
- **Cron Jobs:** 6 (down from 15)
- **Daily Emails:** 2-3 (job alerts, morning brief)
- **Code Commits:** 50+ over 3 weeks
- **Fantasy Leagues:** 3 (FPL, Bundesliga, Serie A)

---

## 🎯 Current Capabilities

### Daily Automation
- ☀️ Morning brief (AI news, markets, weather, emails)
- 💼 Job opportunities (top 10 with interactive buttons)
- 🇫🇷 French lesson (Telegram)

### Weekly
- ⚽ FPL Fantasy analysis (Fridays)
- 📊 Applied jobs summary (Sundays)
- 📝 French quiz (Sundays)

### On Request
- 🔍 Bundesliga analysis
- 🔍 Serie A analysis  
- 💰 Investment portfolio check
- ✈️ Travel planning

---

## 🔒 Privacy & Security

All personal data, API keys, passwords, and detailed configurations are stored in a separate **private repository**. This public repo contains only:
- High-level architecture
- Learning insights
- Anonymized examples
- System design patterns

---

## 🚀 Future Directions

1. **Health Integration** - Connect Dexcom G7 and Apple Health data
2. **WhatsApp Integration** - Family communication channel
3. **Smart Home** - Voice control and automation
4. **Document Analysis** - Automated reading and summarization

---

## 🙏 Credits

- **OpenClaw** - The platform that made this possible
- **Richard Laurits** - Patient human guide and system architect
- **ButtiBot** - The AI assistant learning and growing every day

---

*"Be genuinely helpful, not performatively helpful."* - ButtiBot's core principle

**Born:** February 7, 2026  
**Last Updated:** March 1, 2026
