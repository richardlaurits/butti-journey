# Enhanced Job Crawler - Complete Guide

## What It Does

Your new career crawler script (`enhanced-job-crawler.py`) automatically:

1. ✅ **Accepts cookies** - Clicks "Accept All" buttons automatically
2. ✅ **Waits for pages** - Ensures JavaScript fully loads before scraping
3. ✅ **Filters locations** - Searches Switzerland, Denmark, Sweden only
4. ✅ **Filters roles** - Director, VP, Business Dev, General Manager, etc.
5. ✅ **Takes screenshots** - Saves PNG of each matching job card
6. ✅ **Scores & ranks** - Prioritizes best matches (0-10 scale)
7. ✅ **Sends Telegram** - Auto-reports results to your chat

## Quick Start

### 1. One-Time Setup (Already Done!)
```bash
cd ~/.openclaw/workspace
source venv/bin/activate
pip install playwright
playwright install chromium
```

### 2. Run the Crawler
```bash
cd agents/career-agent
python3 enhanced-job-crawler.py
```

### 3. Get Telegram Notification
```bash
python3 run-and-report.py
```

## What You'll See

### Terminal Output
```
======================================================================
🚀 CAREER AGENT - ENHANCED JOB CRAWLER
======================================================================
📅 Started: 2026-02-17 15:30:45
🎯 Scanning: 8 companies
🗺 Countries: Switzerland, Denmark, Sweden
💼 Roles: Director, VP, Business Dev, General Manager, etc.
======================================================================

📄 Novo Nordisk
   URL: https://careers.novonordisk.com/
   ⏳ Loading... ✓
   🍪 Checking cookies... ✓ Cookies accepted
   ⏱ Waiting for page... ✓
   🗺 Filtering location... (no location filters found)
   🔍 Finding jobs... (18 found)
   📋 Processing jobs...
      ✓ [8/10] Director, Global Business Development (Denmark)
      ✓ [7/10] Senior Manager, Marketing Strategy (Switzerland)

📄 Roche
   URL: https://careers.roche.com/global/en
   ⏳ Loading... ✓
   ...

======================================================================
📊 SUMMARY
======================================================================
⏱ Scan took: 42s
📍 Jobs found (score ≥5): 12
📸 Screenshots saved: 12
💾 Results saved: ./job_results/jobs_20260217_153045.json

🏆 TOP MATCHES:
   [8/10] Director, Global Business Development
           Novo Nordisk - Copenhagen, Denmark
           🔗 https://careers.novonordisk.com/job/...
   
   [7/10] VP, EMEA Commercial Strategy
           Roche - Zurich, Switzerland
           🔗 https://careers.roche.com/job/...

======================================================================
✅ Done! Results and screenshots ready in ./job_results/ and ./job_screenshots/
======================================================================
```

### Files Created

**Results JSON** (auto-analyzed, spreadsheet-friendly)
```
./job_results/jobs_20260217_153045.json
```

**Example Entry:**
```json
{
  "company": "Novo Nordisk",
  "title": "Director, Global Business Development",
  "location": "Copenhagen, Denmark",
  "description": "Lead our strategic expansion in diabetes care...",
  "link": "https://careers.novonordisk.com/job/...",
  "score": 8,
  "screenshot": "./job_screenshots/Novo_Nordisk_5_8.png"
}
```

**Screenshots** (PNG of each job card)
```
./job_screenshots/
├── Novo_Nordisk_0_8.png     ← Score 8/10
├── Novo_Nordisk_1_7.png     ← Score 7/10
├── Roche_3_6.png            ← Score 6/10
└── ...
```

### Telegram Report

You'll receive a message like:

```
🎯 Career Agent - Job Scan Complete

📅 2026-02-17 15:30:45
⏱ Duration: 42s
📍 Companies: 8
💼 Jobs found (score ≥5): 12
📸 Screenshots: 12

🏆 TOP MATCHES:

• [8/10] Director, Global Business Development
  Novo Nordisk • Copenhagen, Denmark
  🔗 https://careers.novonordisk.com/job/...

• [7/10] VP, EMEA Commercial Strategy
  Roche • Zurich, Switzerland
  🔗 https://careers.roche.com/job/...

📁 Results: jobs_20260217_153045.json
```

## Customization

### Add More Companies

Edit `enhanced-job-crawler.py`, find `COMPANIES` dict:

```python
COMPANIES = {
    "Novo Nordisk": "https://careers.novonordisk.com/",
    "IQVIA": "https://www.iqvia.com/careers",
    "Your Company": "https://yourcompany.com/careers",  # Add here
}
```

### Change Search Keywords

Edit `TARGET_KEYWORDS`:

```python
TARGET_KEYWORDS = {
    "roles": [
        "director", "vp", "chief",
        "product manager",  # Add
        "engineer",         # Add
    ],
    "industries": [
        "medtech", "biotech",
        "ai", "software",   # Add
    ],
}
```

### Adjust Scoring

The `score_job()` function ranks 0-10:
- 0-3: No match (filtered out)
- 4-6: Borderline (screenshot saved)
- 7-10: Strong match (highlighted in report)

Only jobs scoring **≥5** are saved.

To be stricter, change:
```python
if score >= 7:  # Only 7+ instead of 5+
```

## Automate with Cron

Want it to run every weekday at 8 AM?

```bash
crontab -e
```

Add this line:
```cron
0 8 * * 1-5 cd /home/richard-laurits/.openclaw/workspace/agents/career-agent && source ../../venv/bin/activate && python3 run-and-report.py
```

(Adjust paths if needed)

## Troubleshooting

### "ModuleNotFoundError: playwright"
```bash
source ~/.openclaw/workspace/venv/bin/activate
pip install playwright
```

### "No jobs found"
Try:
1. Increase timeout: `page.set_default_timeout(30000)`
2. Check the URLs are still valid
3. Reduce keyword filters (too strict?)

### "Screenshots not saving"
Make sure this dir exists:
```bash
mkdir -p ~/.openclaw/workspace/agents/career-agent/job_screenshots
chmod 755 job_screenshots
```

### "Telegram not sending"
Check OpenClaw Telegram is configured:
```bash
openclaw status
```

Should show Telegram channel active.

## Performance

- **8 companies**: ~30-50 seconds
- **Per company**: 4-7 seconds (depends on page size)
- **Storage**: Screenshots ~2-5 MB per run

## Next Steps

1. ✅ Run the crawler: `python3 enhanced-job-crawler.py`
2. ✅ Check results in `./job_results/`
3. ✅ Review screenshots in `./job_screenshots/`
4. ✅ Send report: `python3 run-and-report.py`
5. ✅ Set up cron for automated daily/weekly scans

Any questions? I'm here to help!
