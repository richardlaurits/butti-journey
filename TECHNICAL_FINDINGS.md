# Technical Findings: Job Crawler v3 Test Results

**Test Date:** 2026-02-17 23:53 CET
**Duration:** 252.8 seconds (4.2 minutes)
**Status:** ✅ Completed with insights

---

## Test Execution Summary

### Configuration
- Companies tested: 2 (Roche, Novo Nordisk)
- Search keywords per company: 4 (Marketing, Strategy, Director, Manager)
- Screenshots captured: 9
- Results file: `jobs_v3_20260217_235718.json`

### Results
- **Jobs extracted:** 1 (Roche)
- **Jobs from Novo Nordisk:** 0
- **Screenshots captured:** 9 (documenting each step)

---

## Key Findings

### Problem 1: Cookie Consent Overlay (CRITICAL)
**Symptom:** `<div class="onetrust-pc-dark-filter ot-fade-in"></div>` blocking clicks

**What happened:**
```
<div class="onetrust-consent-sdk">
  <div class="onetrust-pc-dark-filter ot-fade-in"></div>  ← This overlay blocks all interactions
</div>
```

**Impact:** OneTrust cookie consent banner is preventing interaction with search button
**Solution:** Close the consent dialog BEFORE attempting interactions

### Problem 2: Search Button Instability (CRITICAL)
**Error message:**
```
Locator.click: Timeout 30000ms exceeded
- element is visible, enabled and stable
- <div class="onetrust-pc-dark-filter ot-fade-in"></div> intercepts pointer events
```

**What's happening:**
1. Search button is visible ✓
2. Button is enabled ✓
3. Button is stable ✓
4. **BUT:** Consent overlay is on top, blocking clicks ✗

**Solution:** Must dismiss the consent modal first

### Problem 3: Location Input Not Found
**Error:**
```
Locator.fill: Timeout 30000ms exceeded
- waiting for locator("input[placeholder*="location"]")
- locator resolved to <input id="language-selector" placeholder="Enter location or Language">
```

**What's happening:**
- Our selector is matching the LANGUAGE selector, not the job location input
- The job location input is either:
  1. Not visible until we scroll
  2. Hidden behind the consent dialog
  3. Using a different selector

**Solution:** Use more specific selectors or wait for page to fully load

### Problem 4: Novo Nordisk Search Button Not Found
**Error:** `Search button not found`

**What's happening:**
- Novo Nordisk's search button might use a different selector
- Could be `<button class="search">`, `<button type="submit">`, or icon button
- Site might require pressing Enter instead of clicking a button

**Solution:** Manual inspection of Novo Nordisk HTML needed

---

## Detailed Error Log

### Roche Flow
1. ✅ Page loads
2. ❌ Consent banner appears → blocks all interactions
3. ❓ Location input found BUT it's the language selector
4. ✓ Keyword input works (typed into it successfully)
5. ❌ Search button blocked by consent overlay
6. ✅ Page still renders 1 job card (default results)

### Novo Nordisk Flow
1. ✅ Page loads
2. ✅ Consent banner dismissed
3. ✓ Location input found and filled
4. ✓ Keyword input found and filled
5. ❌ Search button not found (wrong selector)
6. ❌ No jobs extracted

---

## Screenshot Analysis

9 screenshots captured:
1. `roche_01_home.png` — Homepage with consent banner visible
2-5. `roche_02_[keyword].png` — Search attempts (banner visible)
6. `novo_nordisk_01_home.png` — Homepage
7-9. `novo_nordisk_02_[keyword].png` — Search attempts

**Insights from screenshots:**
- Roche has a large OneTrust cookie banner covering ~40% of viewport
- Novo Nordisk's search form is simpler but search button selector differs
- Both sites render defaults jobs/results (not search results)

---

## Solutions to Implement

### HIGHEST PRIORITY: Consent Banner Handling
```javascript
// Before any interactions, close the consent banner
try {
  // OneTrust close button
  await page.click('.onetrust-close-btn-handler, .onetrust-pc-close-button');
  await page.waitForSelector('.onetrust-consent-sdk', { state: 'hidden' });
} catch {
  // If no close button, wait for user to accept
  try {
    await page.click('button:has-text("Accept"), button:has-text("Agree")');
  } catch {}
}
```

### MEDIUM PRIORITY: Better Selector Strategy
```javascript
// More specific location selector
const locationSelectors = [
  'input[name="location"]',
  'input[aria-label*="location"]',
  'input[placeholder*="Enter location"]',
  '#location-input',
  '[data-testid="location-search"]'
];

// Try each selector until one works
for (const selector of locationSelectors) {
  const input = page.locator(selector);
  if (await input.count() > 0) {
    // Found it!
    break;
  }
}
```

### MEDIUM PRIORITY: Enter Key Fallback
```javascript
// If search button not clickable, try pressing Enter
await page.press(keywordInputSelector, 'Enter');
```

### LOW PRIORITY: Site-Specific Configs
```javascript
// Different sites need different handling
const siteConfigs = {
  "roche.com": {
    consentCloseButton: ".onetrust-close-btn-handler",
    locationInput: "[aria-label*='Location']",
  },
  "novonordisk.com": {
    consentCloseButton: ".ot-close-icon",
    searchMethod: "enter-key", // Not button click
  }
};
```

---

## Next Steps

### Immediate (This Week)
1. **Fix consent banner blocking** — Update v3 with proper banner dismissal
2. **Test on Roche only** — Get this working end-to-end
3. **Validate extracted jobs** — Confirm we're getting real job postings

### Short Term (Next Week)
1. Add site-specific configurations
2. Test on 3-5 additional companies
3. Build job de-duplication logic
4. Set up automatic alerts

### Long Term (Next Phase)
1. LinkedIn API integration
2. Salary data extraction
3. Application tracking
4. Interview prep notes

---

## Technical Debt

- [ ] Timeouts too aggressive (30s) — some sites are slow
- [ ] Selectors hardcoded per site — need more generic approach
- [ ] No retry logic if search fails
- [ ] Screenshots not associated with results
- [ ] No error logging to file
- [ ] Memory leaks possible with many job cards

---

## Recommended Test Plan

```
Test 1: Roche with consent fix
├─ Load page
├─ Dismiss consent banner
├─ Search "Switzerland" + "Marketing"
├─ Extract jobs
├─ Validate 5+ results
└─ Screenshot each step

Test 2: Novo Nordisk with selector fixes
├─ Load page
├─ Try multiple search button selectors
├─ Try Enter key fallback
├─ Extract jobs
└─ Validate results

Test 3: Other companies (if Tests 1 & 2 succeed)
├─ McKinsey
├─ BCG
├─ Bain
└─ Others
```

---

**Prepared by:** ButtiBot  
**Test Environment:** Linux VM, Playwright (headless)  
**Next Update:** After v3 fixes are implemented  
**Estimated Fix Time:** 30 minutes  

