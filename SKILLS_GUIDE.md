# Skills Reference Guide

Complete reference for OpenClaw skills installed and available.

---

## 🔐 Authentication Skills

### GitHub
**What it does:** Manage repositories, issues, PRs, commits, create gists.

**Config:**
- OAuth via Personal Access Token
- Revocable anytime

**Common tasks:**
```
"Create a new private repo"
"Push these files to GitHub"
"Find all open issues in my repos"
"Create a PR with these changes"
```

**Use cases:**
- Version control for code and data
- Research archives
- Documentation
- Data backup with history

---

### Gmail
**What it does:** Monitor inbox, read emails, extract information.

**Config:**
- OAuth token-based access
- Read/write permissions

**Common tasks:**
```
"Check for new emails"
"Find emails from a specific sender"
"Extract email attachments"
```

---

### ClawHub
**What it does:** Search, install, update, publish OpenClaw skills.

**Config:**
- API token for registry access
- Publish permissions for own skills

**Common tasks:**
```
"Search for a specific skill"
"Install the latest version of a skill"
"Update all installed skills"
"Publish a custom skill"
```

---

## 🌐 Web & Data Skills

### Playwright Scraper Skill
**What it does:** Browser automation with JavaScript rendering, form filling, screenshot capture.

**Best for:**
- Complex dynamic websites
- JavaScript-heavy applications
- Form submissions and interactions
- Visual verification (screenshots)

**Common tasks:**
```
"Scrape this website for data"
"Fill out this form and submit"
"Take a screenshot of this page"
"Extract data that loads dynamically"
```

---

### Web Scraper as a Service
**What it does:** Convert webpages into structured data (JSON, tables, metadata).

**Best for:**
- Static website content
- Quick data extraction
- Table parsing
- Structured data conversion

**Common tasks:**
```
"Extract all data from this table"
"Convert this webpage to JSON"
"Get metadata from this page"
```

---

### Tavily Search
**What it does:** Real-time web search with source attribution and recency filtering.

**Best for:**
- Latest news and trends
- Research and fact-finding
- Market data discovery
- Breaking news

**Common tasks:**
```
"Find recent news about this topic"
"Search for information from the past week"
"Find data across multiple sources"
```

---

## 🛠️ Development & Configuration Skills

### Coding Agent
**What it does:** Write, debug, test code; generate scripts and reports.

**Best for:**
- Python/JavaScript development
- Data analysis and transformation
- Script generation
- Algorithm implementation

**Common tasks:**
```
"Write a Python script to [do something]"
"Debug this code"
"Generate a report from this data"
"Transform this data format"
```

---

### Skill Creator
**What it does:** Design and package custom OpenClaw skills.

**Best for:**
- Building reusable automation tools
- Creating domain-specific capabilities
- Packaging workflows

---

### MCporter
**What it does:** Connect and run MCP (Model Context Protocol) servers.

**Best for:**
- Integrating external APIs
- Custom tool creation
- Advanced integrations

---

### Healthcheck
**What it does:** System security audits, dependency updates, version checks.

**Best for:**
- System maintenance
- Security hardening
- Compliance checks

**Common tasks:**
```
"Run a security audit on my system"
"Check for available updates"
"Verify system health"
```

---

## 📊 Analysis & Information Skills

### Weather
**What it does:** Current weather and forecasts.

**Best for:**
- Planning
- Decision-making based on conditions
- Integration into daily briefings

---

### Obsidian
**What it does:** Query personal knowledge base, search notes, manage tags.

**Best for:**
- Knowledge management
- Research archive integration
- Information retrieval

---

### Token Memory Optimizer
**What it does:** Manage context length, prevent token bloat, summarize history.

**Best for:**
- Long-running sessions
- Memory efficiency
- Context management

---

## Recommended Workflows

### Data Collection Pipeline
- Playwright Scraper → Extract data
- Web Scraper → Parse structure
- Coding Agent → Transform/analyze
- GitHub → Store results

### Research Workflow
- Tavily Search → Find sources
- Web Scraper → Extract content
- Coding Agent → Summarize
- GitHub → Archive results

### Automation Workflow
- Playwright Scraper → Collect data
- Cron → Schedule execution
- GitHub → Version control
- Notifications → Alert on changes

---

**Last Updated:** 2026-02-18 07:45 CET
