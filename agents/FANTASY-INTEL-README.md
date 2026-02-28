# Fantasy Football Intel System

## Overview

Replaced daily standings-based scraping with **targeted player intel only**.

No league positions, no mini-league tracking — just squad news & rumours for YOUR players.

## Schedule

### FPL (Nightly - 11 PM CET)
```bash
openclaw cron 23:00 --task "cd ~/.openclaw/workspace && python3 agents/fpl-agent/nightly-scraper.py"
```

**What it does:**
- Fetches current injury/suspension list from FPL official sources
- Checks your FC MACCHIATO squad (Haaland, Gabriel, Rice, Timber, Saka, Son, Salah, etc.)
- Alerts if ANY of your players are injured, suspended, or have breaking news
- Ignores: standings, points, league tables

**Sources:**
- FPL official API (injuries)
- FPL Hints (Twitter @fplhints)
- Team news pages
- X/Twitter injury reporters

### Bundesliga (Friday 08:00 CET)
```bash
openclaw cron 08:00:friday --task "cd ~/.openclaw/workspace && python3 agents/bundesliga-agent/friday-scraper.py"
```

**What it does:**
- Scrapes current week injury/suspension news (max 7 days old)
- Checks your squad (Kane, Díaz, Baumgartner, Grimaldo, etc.)
- Alerts if any are unavailable or suspended
- Ignores: standings, points, league tables

**Sources:**
- bulinews.com/fantasy (PRIMARY — Richard's preference)
- Official Bundesliga Fantasy Manager
- Team news pages (Bayern, Leverkusen, Leipzig, Hoffenheim, Köln, Freiburg)
- X/Twitter injury news

### Serie A (Manual Weekly)
- You send updated screenshot
- I compare to last week's squad
- Alert if roster changes detected

## What Was Killed

- ❌ Daily FPL standings scraper
- ❌ Daily Bundesliga standings scraper
- ❌ Morning cron briefing (replaced with voice greeting only)
- ❌ Mini-league tracking (Funa-ligan, etc.)
- ❌ League position alerts

## Alert Rules

Alert only if:
- ✅ Player is injured/suspended
- ✅ Player has breaking news (transfer rumour, form crisis)
- ✅ Player's status changed from last check

Don't alert:
- ❌ Standings/points changes
- ❌ Other teams' news
- ❌ General market news
- ❌ Price changes alone (unless player-specific)

## Files

- `fpl-agent/nightly-scraper.py` — FPL intel (11 PM CET)
- `bundesliga-agent/friday-scraper.py` — Bundesliga intel (Friday 8 AM CET)
- `seriea-screenshots/` — Store weekly Serie A snapshots for comparison

## Next Steps

1. ✅ Scripts created with YOUR player lists
2. ⏳ Set up web scraping (need Brave API for full functionality)
3. ⏳ Configure cron jobs
4. ⏳ Start alerts

For now, scripts are placeholders. Once web_search is configured (Brave API key), they'll fetch real data.
