# Hourly Telegram Alerts - Cron Setup

## Quick Start

**Run this ONCE to set up hourly checks:**

```bash
# Create cron job
(crontab -l 2>/dev/null; echo "0 * * * * cd ~/.openclaw/workspace && source venv/bin/activate && python3 skills/flashscore/hourly_alert.py") | crontab -

# Verify it was added
crontab -l | grep hourly_alert
```

## What It Does

- ⏰ Runs **every hour** (at :00 minutes)
- 📱 Sends Telegram alert **ONLY if matches are live**
- 🟢 Filters: Premier League, Bundesliga, Serie A only
- 🔄 Tracks score changes (alerts only on updates)
- 💾 Maintains state (`flashscore_state.json`)

## Manual Test

```bash
cd ~/.openclaw/workspace/skills/flashscore
python3 hourly_alert.py
```

Expected output: Message sent to Telegram + state saved

## Stop Alerts

```bash
# Remove cron job
crontab -r

# Or edit to comment out:
crontab -e
# (Comment with # at start of line)
```

## Customize

Edit `hourly_alert.py` to:
- Change `TELEGRAM_CHAT_ID` (use your ID)
- Change leagues (add LaLiga, etc)
- Change match limit per league (currently 3)
- Add score change thresholds

## Logs

Cron output goes to `/var/mail/$USER` by default. To save logs:

```bash
0 * * * * cd ~/.openclaw/workspace && source venv/bin/activate && python3 skills/flashscore/hourly_alert.py >> skills/flashscore/hourly_alerts.log 2>&1
```

---

**Created:** 2026-02-18 21:48 CET
**Status:** Ready to deploy
