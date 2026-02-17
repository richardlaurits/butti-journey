# Job Crawler Analysis Report

**Date:** 2026-02-17 23:50 CET
**Status:** ✅ Operational, Results Analyzed

---

## Executive Summary

The job crawler successfully accessed career sites and extracted page elements, but modern job platforms use **dynamic JavaScript loading** to display actual job postings. Our current crawler captures the page structure but not the actual job listings.

**Solution:** Switch from generic CSS selectors to:
1. **Playwright with JavaScript wait events** (implemented)
2. **Job search API endpoints** (for supported sites)
3. **Manual search + capture workflow** (for complex sites)

---

## Test Run Results

### Companies Tested
- ✅ Novo Nordisk (careers.novonordisk.com)
- ✅ Roche (careers.roche.com)

### Data Extracted
- **Elements found:** 54 (Roche), navigation elements (Novo Nordisk)
- **High-scoring matches:** 1 (Roche "See More" button)
- **Screenshots captured:** 1 (Roche homepage)
- **Page HTML saved:** 1 (Novo Nordisk, for analysis)

### Analysis

**What works:**
✅ Cookie acceptance
✅ Page loading
✅ Element detection
✅ Screenshot capture
✅ HTML parsing

**What doesn't:**
❌ Actual job listings (they load after JavaScript execution)
❌ Filter-based search (need manual interaction)
❌ Location-specific job display (needs search trigger)

---

## Current Crawler Capabilities

| Feature | Status | Notes |
|---------|--------|-------|
| Cookies | ✅ | Auto-accepts site cookies |
| JavaScript | ✅ | Renders JS-heavy pages |
| Screenshots | ✅ | Captures page state |
| HTML export | ✅ | Saves for inspection |
| Job detection | ⚠️ | Finds elements, not listings |
| Location filtering | ⚠️ | Requires manual search |

---

## The Real Problem

Modern career sites (Roche, Novo Nordisk, Takeda) follow this pattern:

```
1. User visits site
2. Empty page loads with filters/search box
3. User enters: location + keyword → JavaScript triggers
4. Jobs load dynamically via AJAX/GraphQL
5. Results appear on page
```

**Our crawler stops at step 2.** It doesn't interact with the search/filter system.

---

## Solutions (in order of priority)

### Solution A: Click-and-Capture Workflow (EASIEST) ⭐
Instead of trying to parse the page, we:
1. Navigate to career site
2. Search for specific location (e.g., "Switzerland")
3. Filter by keyword (e.g., "marketing")
4. Let JavaScript load results
5. Scrape the job cards that appear
6. Take screenshots for manual review

**Example:**
```javascript
// Click "Switzerland" filter
await page.click('[aria-label="Switzerland"]');
// Wait for jobs to load
await page.waitForSelector('.job-card');
// Extract job data
const jobs = await page.$$eval('.job-card', cards => 
  cards.map(card => ({
    title: card.querySelector('.job-title')?.textContent,
    link: card.href,
  }))
);
```

### Solution B: API Reverse Engineering (MEDIUM)
Many job sites have hidden API endpoints. We can:
1. Inspect network traffic
2. Find the job listing API URL
3. Call it directly with filters
4. Get structured JSON response

**Example (if available):**
```bash
curl "https://careers.roche.com/api/jobs?location=Switzerland&keyword=marketing"
```

### Solution C: Dedicated Job Aggregators (HARDEST)
Use services like:
- LinkedIn API (requires authentication)
- Indeed API (requires paid subscription)
- Glassdoor scraper (no official API)

---

## Next Steps

### Phase 1: Immediate (This Week)
1. Enhance crawler with search interaction
2. Test on 2-3 companies
3. Validate job extraction accuracy
4. Set up automated alerts for matching jobs

### Phase 2: Optimization (Next Week)
1. Try API approach for major companies
2. Build a job aggregator (combine multiple sources)
3. Add salary scraping
4. Set up GitHub webhook for auto-alerts

### Phase 3: Advanced (Future)
1. Machine learning job matching (based on Richard's profile)
2. Automated LinkedIn/email outreach
3. Interview prep notes
4. Salary negotiation data

---

## Recommended Action Plan

**Right now:**
- I'll create **job-crawler-v3.py** with search interaction
- Test on Roche (simple search: "Switzerland" + "Marketing Manager")
- Validate if we can extract real jobs
- If successful, scale to other companies

**Configuration needed:**
```json
{
  "companies": [
    {
      "name": "Roche",
      "url": "https://careers.roche.com/global/en",
      "searchSteps": [
        {"click": ".location-filter"},
        {"type": "Switzerland"},
        {"click": ".keyword-filter"},
        {"type": "Marketing"},
        {"click": ".search-button"}
      ],
      "jobCardSelector": ".job-card"
    }
  ],
  "filterLocation": ["Switzerland", "Denmark", "Sweden"],
  "filterKeywords": ["Marketing", "Director", "Manager", "Strategy"],
  "outputFormat": "json"
}
```

---

## Technical Notes

**Why JavaScript loading is hard:**
- Different sites use different frameworks (React, Vue, Angular)
- Different selectors, APIs, timing
- Anti-scraping: delays, rate limits, IP blocks
- Dynamic content changes on each load

**Why Playwright is the right tool:**
- Handles all JavaScript frameworks
- Can wait for specific elements to appear
- Can interact with forms, buttons, filters
- Screenshots for verification
- Headless (no browser UI needed)

**Why this matters for Richard:**
- Need to find marketing/strategy jobs in Switzerland/Denmark/Sweden
- Need salary data
- Need to track applications
- Need to get alerts for new matching jobs
- Need to avoid manual checking every day

---

## Success Metrics

✅ **MVP Success:** Extract 10+ real jobs from 1 company within 1 minute
✅ **Beta Success:** Extract jobs from 3+ companies automatically
✅ **Production Ready:** 20+ new jobs/day with salary data, automatic GitHub commit

---

**Prepared by:** ButtiBot
**Last Updated:** 2026-02-17 23:50 CET
**Next Review:** 2026-02-18 10:00 CET
