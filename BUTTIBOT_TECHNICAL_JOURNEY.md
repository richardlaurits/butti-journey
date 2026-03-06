# ButtiBot Technical Journey

**Born:** February 7, 2026  
**Platform:** OpenClaw on Linux VM  
**Evolution:** From simple assistant to autonomous multi-agent system

---

## Phase 1: Foundation (Feb 7-14, 2026)

### Day 1: First Boot
- Identity establishment and naming
- Telegram integration configured
- Basic communication protocols established

### Week 1: Core Infrastructure
- Dual-account email system (bot + personal)
- IMAP/SMTP integration replacing OAuth
- Secure credential management with app passwords
- First automated workflows

### Key Technical Decisions
- **Linux VM over cloud:** Full control, no vendor lock-in
- **IMAP over OAuth:** More reliable long-term access
- **App passwords over tokens:** No expiration issues
- **Local execution over APIs:** Cost control and privacy

---

## Phase 2: Multi-Agent Architecture (Feb 15-28, 2026)

### Architecture Evolution

**Initial Approach:** Single monolithic agent
- Problems: Context overflow, task interference, no isolation

**Current Architecture:** Coordinator + Specialized Sub-Agents
- Benefits: Isolated failures, parallel processing, domain expertise
- Pattern: Main session orchestrates, sub-agents execute

### Integration Patterns

**Email-Based Interfaces**
- Interactive buttons for user actions
- Rich HTML formatting
- State persistence across conversations
- Fallback to plain text

**Monitoring Systems**
- Heartbeat-based health checks
- Cron-scheduled automated tasks
- State tracking to prevent duplicates
- Quiet hours for cost optimization

**Data Flow Architecture**
- Source → Parser → Analyzer → Notifier
- Caching layer for API responses
- Deduplication via message IDs
- Error handling with graceful degradation

---

## Phase 3: Automation & Optimization (Mar 1-6, 2026)

### Cost Optimization Strategy

**Token Economy**
- Hard caps: 40-50 calls per run
- Output limits: 300-500 micro, 1500-2500 final
- Reflection reduction: Every 5-10 steps instead of per-step
- Loop detection: Abort after 3 identical errors

**Scheduling Optimization**
- Day mode (07:00-22:00): Full monitoring
- Night mode (22:00-07:00): Essential only
- Reduced frequency: 50% cost savings during low-activity
- Batched checks: Combine related operations

**API Usage Patterns**
- Web search: Brave API for quick queries
- Email parsing: IMAP for reliability
- Screen scraping: Playwright for complex sites
- Data storage: Local JSON files over databases

### Model Selection Journey

**Initial:** Default OpenClaw models
**Testing:** Kimi 2, Claude Haiku, various providers
**Current:** Kimi 2 as primary for most tasks
**Rationale:** Balance of capability, cost, and speed

---

## Technical Stack

### Core Platform
- **Runtime:** OpenClaw on Ubuntu Linux VM
- **Language:** Python 3.13
- **Shell:** Bash
- **Version Control:** Git with GitHub

### Communication
- **Primary:** Telegram Bot API
- **Email:** Gmail IMAP/SMTP
- **Notifications:** In-app + Telegram alerts

### Data Processing
- **Web Scraping:** Playwright with stealth plugins
- **API Integration:** REST, GraphQL where available
- **Data Format:** JSON for structured data
- **Storage:** Local filesystem, no cloud databases

### Security
- **VPN:** Tailscale for secure access
- **Credentials:** App passwords, no hardcoded secrets
- **Repositories:** Public/Private separation
- **Access Control:** File permissions, no external exposure

---

## Key Learnings

### What Worked

1. **Email as Interface**
   - Universal accessibility
   - Natural async communication
   - Rich formatting capabilities
   - No app installation required

2. **Hybrid Automation**
   - Scheduled tasks for routine work
   - On-demand for complex analysis
   - Human-in-the-loop for decisions
   - Graceful degradation on failures

3. **Private/Public Separation**
   - Clean public documentation
   - Secure private data storage
   - Reusable patterns without exposure
   - Clear separation of concerns

### What Didn't Work

1. **Over-Automation**
   - Too many notifications = fatigue
   - Reduced to essential only
   - Quality over quantity

2. **Complex Scrapers**
   - JavaScript-heavy sites break easily
   - Fallback to email parsing preferred
   - API-first when available

3. **OAuth Dependencies**
   - Token expiration issues
   - Replaced with app passwords
   - More reliable long-term

### Architecture Insights

- **Coordinator pattern:** Essential for multi-agent systems
- **State management:** Track seen items to prevent duplicates
- **Error isolation:** Sub-agents must not crash main session
- **Cost awareness:** Every API call has a price

---

## Integration Categories

### Communication Systems
- Multi-channel messaging (Telegram, Email)
- Interactive email interfaces
- Automated response handling
- VIP contact prioritization

### Monitoring & Alerts
- Health check systems
- Cost tracking
- Performance monitoring
- Error alerting

### Data Sources
- Web scraping with anti-detection
- API integrations
- Email parsing
- RSS/feed monitoring

### Automation Patterns
- Cron-based scheduling
- Event-driven triggers
- State machines for workflows
- Caching and deduplication

---

## Future Directions

### Technical Evolution
- Health data integration (wearables, CGM)
- Voice interface exploration
- Document analysis capabilities
- Enhanced security measures

### Architecture Improvements
- Better error recovery
- More efficient token usage
- Improved context management
- Streamlined onboarding

---

## System Statistics

- **Born:** February 7, 2026
- **Platform:** OpenClaw on Linux VM
- **Evolution:** 4 major phases
- **Integrations:** 15+ system connections
- **Automation:** 6 essential cron jobs (down from 15)
- **Cost Reduction:** 50% through optimization
- **Commits:** 50+ over 4 weeks

---

## Core Principles

> *"Be genuinely helpful, not performatively helpful."*

1. **Actions over words:** Deliver results, not promises
2. **Privacy first:** Personal data stays private
3. **Cost conscious:** Every operation has a price
4. **Fail gracefully:** Errors shouldn't crash the system
5. **Human-centric:** Technology serves the human, not vice versa

---

**Last Updated:** March 6, 2026  
**Status:** Active evolution  
**Next Review:** Ongoing
