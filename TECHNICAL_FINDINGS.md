# Technical Architecture & Findings

**Document Type:** Technical Reference  
**Status:** Active Development

---

## System Architecture

### Multi-Agent Design
- **Main Agent:** Handles user interaction and orchestration
- **Sub-Agents:** Specialized tasks with isolated execution
- **Skill System:** Modular, composable capabilities
- **Automation Layer:** Scheduled tasks via cron and webhooks

### Integration Points

```
User Interface
    ↓
Main Agent (Orchestration)
    ├→ Sub-Agent 1 (Domain A)
    ├→ Sub-Agent 2 (Domain B)
    └→ Sub-Agent 3 (Domain C)
    ↓
External Services (GitHub, Gmail, APIs)
    ↓
Notifications (Telegram, Email, Local)
```

---

## Skill Integration Patterns

### Sequential Processing
1. Data collection (Scraper)
2. Data parsing (Parser)
3. Analysis (Analyzer)
4. Storage (GitHub)
5. Notification (Telegram)

### Parallel Processing
- Multiple sub-agents running simultaneously
- Isolated execution prevents conflicts
- Main session remains responsive

### Async Processing
- Cron jobs for scheduled tasks
- Background processing
- Push-based notifications

---

## Known Challenges & Solutions

### Challenge 1: Dynamic Content Loading
**Problem:** Modern websites load content via JavaScript after initial page load.

**Solution:**
```javascript
await page.waitForSelector('.content');
const data = await page.$$eval('.item', ...);
```

**Key Points:**
- Use Playwright for full JavaScript support
- Wait for specific elements before extraction
- Set appropriate timeouts

### Challenge 2: Consent & Security Dialogs
**Problem:** Cookie banners and security warnings block interactions.

**Solution:**
```javascript
await page.click('.close-btn');
await page.waitForSelector('.modal', { state: 'hidden' });
```

**Key Points:**
- Close dialogs before interaction
- Use generic close selectors (fallback strategy)
- Verify dialog is gone before proceeding

### Challenge 3: Rate Limiting
**Problem:** Repeated requests get blocked by servers.

**Solution:**
- Implement exponential backoff
- Space requests over time
- Use residential proxies if needed
- Respect robots.txt and rate limits

### Challenge 4: Context Management
**Problem:** Long-running sessions accumulate token usage.

**Solution:**
- Use Token Optimizer skill
- Summarize old messages
- Sub-agent isolation
- Regular memory cleanup

---

## Performance Metrics

### Typical Execution Times
- Email check: 2-5 seconds
- Single site scrape: 30-60 seconds
- Multi-site analysis: 2-5 minutes
- Data processing: 5-10 seconds

### Token Efficiency
- Routine checks: ~500 tokens
- Analysis tasks: ~1,500 tokens
- Research: ~2,000 tokens
- Daily total: ~4,000 tokens

---

## Recommendations

### Best Practices
1. ✅ Always wait for elements before interaction
2. ✅ Use multiple selector fallbacks
3. ✅ Implement comprehensive error handling
4. ✅ Log failures for debugging
5. ✅ Test selectors on multiple runs
6. ✅ Respect website rate limits
7. ✅ Use residential proxies for sensitive scraping

### Code Quality
- Write defensive code
- Handle timeouts gracefully
- Implement retry logic
- Document assumptions
- Test edge cases

---

## Future Improvements

- [ ] Machine learning for selector detection
- [ ] Automatic site fingerprinting
- [ ] Distributed execution for parallel tasks
- [ ] Advanced caching strategies
- [ ] Real-time performance monitoring
- [ ] Enhanced error diagnostics

---

**Last Updated:** 2026-02-18
**Visibility:** Public (technical reference)
