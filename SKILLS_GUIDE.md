# Skills Reference Guide

This is a complete guide to every skill ButtiBot has access to and how to use them.

## 🔐 Authentication Skills

### GitHub
**What it does:** Manage your GitHub repositories, issues, PRs, commits, and create gists.

**Config:**
- Username: `@richardlaurits`
- PAT: `$GITHUB_TOKEN` (90-day, expires 2026-05-17)

**Common tasks:**
```
"Create a new private repo called health-tracking"
"Add this data to my health-tracking repo as a CSV"
"Find all open issues in my repos"
"Create a PR to update the README"
"Push these job crawler results to GitHub"
```

**Use cases:**
- Version control for personal data
- Job search tracking
- Health metrics logging
- Investment research archive

---

### Gmail
**What it does:** Monitor inbox, read emails, extract key info.

**Config:**
- Read-only via OAuth
- Active: Heartbeat monitor (every 30 min)
- Filters: Pernilla, invoices, bank alerts, calendar, Gmail Important

**Common tasks:**
```
"Check for important emails"
"Get my latest invoice"
"Find emails from Pernilla"
```

**Use cases:**
- Inbox triage
- Bill tracking
- Important notifications
- Calendar event reminders

---

### ClawHub
**What it does:** Search, install, update, publish OpenClaw skills from the registry.

**Config:**
- API token: `$CLAWHUB_TOKEN`
- Registry: https://clawhub.com

**Common tasks:**
```
"Search for a database skill"
"Install the latest version of playwright-scraper"
"Update all my skills"
"Publish my custom health-tracking skill"
```

---

## 🌐 Web & Data Skills

### Playwright Scraper Skill
**What it does:** Browser automation with JavaScript rendering, anti-bot protection, form filling, screenshot capture.

**Best for:**
- Career sites with dynamic JavaScript
- Pagination handling
- Form submissions
- Taking screenshots of job listings

**Common tasks:**
```
"Scrape Roche's careers page for all marketing jobs"
"Extract job listings from LinkedIn (with filters)"
"Capture a screenshot of the target job page"
```

---

### Web Scraper as a Service
**What it does:** Convert any webpage into structured JSON, extract tables, lists, metadata.

**Best for:**
- Static website content
- Quick data extraction
- Table parsing
- Price comparison

**Common tasks:**
```
"Extract all job titles from this webpage"
"Convert this table into JSON"
"Get the metadata (title, description, author) from this page"
```

---

### Tavily Search
**What it does:** Real-time web search optimized for research, with source attribution and recency filtering.

**Best for:**
- Latest news & trends
- Company research
- Salary/market data
- Fantasy football breaking news

**Common tasks:**
```
"Find the latest AI breakthroughs from this week"
"Search for salary data for Marketing Manager in Switzerland"
"Find injury news for my fantasy football league"
```

---

## 🛠️ Development & Configuration Skills

### Coding Agent
**What it does:** Autonomous code writing, debugging, testing, version control, commit messages.

**Best for:**
- Writing Python scripts
- Debugging code
- Generating reports
- Data transformation

**Common tasks:**
```
"Write a Python script to parse job listing JSON"
"Debug my job crawler script"
"Generate a weekly health summary report"
```

---

### Skill Creator
**What it does:** Design and package custom OpenClaw skills with metadata, dependencies, documentation.

**Best for:**
- Building domain-specific tools
- Packaging reusable automation

**Common tasks:**
```
"Create a custom skill for tracking my TIR metrics"
"Package my job crawler as a reusable skill"
```

---

### MCporter
**What it does:** Connect and run MCP (Model Context Protocol) servers directly.

**Best for:**
- Integrating external APIs
- Custom tool bridges
- Advanced automation

---

### Healthcheck
**What it does:** Security audits of your Linux VM, firewall checks, update status, version verification.

**Best for:**
- System maintenance
- Security hardening
- Dependency updates

**Common tasks:**
```
"Run a security audit on my system"
"Check if my OpenClaw is up to date"
"List security vulnerabilities"
```

---

## 📊 Analysis & Information Skills

### Weather
**What it does:** Current weather and forecasts for your location.

**Best for:**
- Morning briefings
- Planning outdoor activities
- Deciding cycling commute viability

**Common tasks:**
```
"What's the weather tomorrow in Prangins?"
"Will it rain this week?"
"Is it a good day to cycle to the office?"
```

---

### Obsidian
**What it does:** Query your Obsidian vault, fuzzy search notes, traverse wikilinks, manage tags.

**Best for:**
- Knowledge base integration
- Personal research archive
- Project notes

**Requires:** Obsidian installed and configured

---

### Token Memory Optimizer
**What it does:** Prevent token context bloat, summarize old memories, reset & refresh.

**Best for:**
- Long-running sessions
- Token efficiency
- Memory maintenance

---

## 🎮 Entertainment & Specialized

### Not Yet Installed (But Available)

**Spotify Player** — Control music playback
**Discord** — Send messages to Discord servers
**Slack** — Integration with Slack workspace
**Notion** — Database and page management
**Trello** — Task board automation

---

## Skill Recommendations

### For Your Goals:

**Job Hunting:**
- Playwright Scraper (primary)
- Web Scraper (secondary)
- Tavily Search (salary research)
- GitHub (track results)
- Coding Agent (analyze data)

**Health Tracking:**
- GitHub (store daily data)
- Coding Agent (analyze trends)
- Healthcheck (system audits)
- Token Optimizer (manage memory)

**Fantasy Football:**
- Tavily Search (injury/news)
- Web Scraper (league standings)
- Coding Agent (analysis)
- GitHub (archive strategy)

---

**Last Updated:** 2026-02-17 23:50 CET
