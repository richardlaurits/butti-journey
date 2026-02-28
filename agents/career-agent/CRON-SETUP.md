# Career Agent: Daily Company Crawler Cron Job

**[2026-02-16 11:17]** Setup instructions

## Cron Job Configuration

**Schedule:** Mon-Fri, 8:00 AM CET
**Task:** Check all 14 target companies for new job postings
**Action:** Alert Richard on Telegram if high-scoring matches found

```
0 8 * * 1-5 cd ~/.openclaw/workspace && source venv/bin/activate && python3 agents/career-agent/company-crawler.py >> agents/career-agent/logs/crawler.log 2>&1
```

## How It Works

1. **Daily at 8 AM** (Mon-Fri only)
2. **Crawls 14 company careers pages:**
   - Denmark: Novo Nordisk, Dawn Health, IQVIA, CapGemini
   - Sweden: Glooko, Medicon Village, Minc, Lund Innovation
   - Switzerland: Tandem, BD, Haleon, Roche, MyLife, embecta

3. **Scores jobs** against Richard's criteria:
   - Director/VP/Senior Manager level
   - Business Development, Corporate Development, Product Strategy
   - Medical Tech, Diabetes, Healthcare focus
   - Switzerland, Denmark, Sweden locations

4. **Saves matches** to `data/jobs-YYYY-MM-DD.json`
5. **Sends Telegram alert** if score ≥ 7/10 found

## Files Created

- `company-crawler.py` — Main crawler script
- `TARGET-COMPANIES.md` — Company list + URLs
- `logs/` — Daily crawler logs (auto-created)
- `data/jobs-*.json` — Results

## Setup Steps

1. **Make crawler executable:**
   ```bash
   chmod +x agents/career-agent/company-crawler.py
   ```

2. **Create logs directory:**
   ```bash
   mkdir -p agents/career-agent/logs
   ```

3. **Add cron job** (from main gateway):
   ```bash
   crontab -e
   # Add the cron line above
   ```

4. **Test manually:**
   ```bash
   cd ~/.openclaw/workspace && python3 agents/career-agent/company-crawler.py
   ```

## Next Steps

1. ✅ Refine company URLs (some may need adjustment)
2. ✅ Add Telegram notification on high scores
3. ✅ Upload resume + cover letter template
4. ✅ Start automated daily monitoring

---

**Status:** Ready to deploy! 🚀
