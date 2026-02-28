# Career Agent - Enhanced Crawler Setup

## Requirements

The enhanced job crawler uses **Playwright** to handle JavaScript-heavy career pages.

## Installation

### 1. Install Python Dependencies

```bash
cd ~/.openclaw/workspace
source venv/bin/activate
pip install playwright
playwright install chromium
```

(First run takes ~1-2 min to download browser, then you're good)

### 2. Test the Crawler

```bash
cd agents/career-agent
python3 enhanced-job-crawler.py
```

## Features

✅ **Cookie Acceptance** - Automatically clicks "Accept All" cookies
✅ **Full Page Load Wait** - Waits for network idle + 2s buffer
✅ **Smart Filtering** - Location filter (CH/DK/SE) + role keywords
✅ **Screenshot Capture** - Saves PNG of each matching job
✅ **Scoring System** - Ranks jobs 0-10 based on match quality
✅ **Telegram Report** - Auto-sends summary to your chat

## Usage

### Option A: Run Crawler Only
```bash
python3 enhanced-job-crawler.py
```

Results saved to:
- `./job_results/jobs_YYYYMMDD_HHMMSS.json`
- `./job_screenshots/*.png`

### Option B: Run + Send Telegram Report
```bash
python3 run-and-report.py
```

Or set up as a cron job (Mon-Fri 8 AM):
```bash
0 8 * * 1-5 cd ~/.openclaw/workspace/agents/career-agent && python3 run-and-report.py
```

## Customization

Edit `enhanced-job-crawler.py`:

- **COMPANIES** - Add/remove career URLs
- **TARGET_KEYWORDS** - Change job titles/industries
- **TARGET_LOCATIONS** - Add/remove countries
- **score_job()** - Adjust scoring formula

## Output

### Job Scoring

- **0-3**: Poor match (ignored)
- **4-6**: Potential match (saved)
- **7-8**: Good match (screenshot taken)
- **9-10**: Excellent match

### Summary Report

```
🏆 TOP MATCHES:
   [8/10] Director, Global Business Development
   Novo Nordisk • Switzerland

   [7/10] VP, Commercial Strategy  
   Roche • Denmark
```

## Troubleshooting

**Playwright fails to load pages?**
- Try increasing `page.set_default_timeout(30000)` in the script

**Screenshots not being saved?**
- Check `./job_screenshots/` directory permissions
- Make sure `job_elem.screenshot()` has write access

**Telegram not sending?**
- Verify OpenClaw is configured with Telegram bot
- Check `run-and-report.py` has correct chat ID (7733823361)

**Need Selenium instead?**
- Use `job-search-playwright.py` as alternative
- Or let me know, happy to create Selenium version
