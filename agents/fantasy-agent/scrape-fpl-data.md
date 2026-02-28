# FPL Data Scraping Plan

**[2026-02-14 12:02]** Automated data collection strategy

## Sources to Scrape

### 1. Official FPL API (Real-time)
**URL:** `https://fantasy.premierleague.com/api/entry/17490/`

**What to fetch:**
```bash
# Current squad
curl -s 'https://fantasy.premierleague.com/api/entry/17490/' | jq '.current_event_points, .summary_overall_points'

# Gameweek history
curl -s 'https://fantasy.premierleague.com/api/entry/17490/history/' | jq '.current[-1]'

# Mini-league standings
curl -s 'https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/' 
```

**Update frequency:** Hourly during gameweeks, daily otherwise

---

### 2. FPL FantasyScout
**URL:** https://www.fantasyfootballscout.co.uk/

**Pages to scrape:**
- `/team-news/` - Injury updates
- `/transfer-tips/` - Expert recommendations  
- `/captain-picks/` - Captain analysis
- `/price-tips/` - Price change predictions

**Method:** `web_fetch` + parse key sections

**Update frequency:** 2x daily (morning + evening)

---

### 3. FPL Football Hub
**URL:** https://www.fantasyfootballhub.co.uk/

**Pages to scrape:**
- `/fixture-ticker/` - Upcoming matches analysis
- `/statistics/` - Player stats comparison
- `/transfer-planner/` - Optimal transfer suggestions

**Method:** `web_fetch` + extract tables/stats

**Update frequency:** Daily

---

### 4. Twitter Monitoring
**Accounts to track:**
- @OfficialFPL - Breaking news
- @BenCrellin - Rotation predictions
- @FPLRockstar - Price changes
- @FantasyScout - Expert picks

**Method:** `web_search` with recency filter

**Update frequency:** Every 4 hours during active periods

---

## Data Storage

**Structure:**
```
agents/fantasy-agent/data/
├── latest-squad.json          # From FPL API
├── injuries-YYYY-MM-DD.json   # Daily injury snapshot
├── prices-YYYY-MM-DD.json     # Price change tracking
├── scout-tips-YYYY-MM-DD.md   # FantasyScout recommendations
└── twitter-feed-YYYY-MM-DD.md # Compiled Twitter updates
```

**Retention:** Keep last 7 days, archive older

---

## Cron Job Setup

**Morning Brief Enhancement (07:00):**
```yaml
job:
  name: "FPL Data Scrape - Morning"
  schedule:
    kind: cron
    expr: "0 7 * * *"
    tz: "Europe/Zurich"
  payload:
    kind: agentTurn
    message: |
      Scrape FPL data sources:
      1. Fetch team 17490 current status from API
      2. Check FPL FantasyScout for overnight news
      3. Scan Twitter for injury updates
      4. Check price changes from last night
      
      Save to data/ folder and update MEMORY.md if anything significant.
      Only notify Richard if urgent action needed.
  sessionTarget: isolated
  delivery:
    mode: announce
    channel: telegram
    to: "7733823361"
    bestEffort: true
```

**Evening Deadline Prep (20:00):**
```yaml
job:
  name: "FPL Data Scrape - Evening"  
  schedule:
    kind: cron
    expr: "0 20 * * *"
    tz: "Europe/Zurich"
  payload:
    kind: agentTurn
    message: |
      Pre-deadline FPL check:
      1. FPL Football Hub fixture ticker
      2. Price predictions for tonight
      3. Lineup rumors from Twitter
      4. Last-minute injury news
      
      If deadline tomorrow: Generate quick brief with key decisions.
      Save data, notify only if time-sensitive.
  sessionTarget: isolated
  delivery:
    mode: announce
    channel: telegram
    to: "7733823361"
    bestEffort: true
```

---

## Usage Examples

**Manual scrape (test):**
```
Ask ButtiBot: "Scrape latest FPL data for my team"
→ Spawns FPL Scout agent
→ Fetches from all sources
→ Updates MEMORY.md
→ Reports findings
```

**Automated flow:**
```
07:00 → Cron triggers morning scrape
     → FPL Scout agent activates
     → Scrapes priority sources
     → Finds: "Salah injury doubt for Sunday"
     → Sends Telegram alert to Richard
     → Updates MEMORY.md injury tracker
```

---

## Next Steps

**[2026-02-14]** To activate:

1. **Test manual scrape** - Verify sources work
2. **Create cron jobs** - Add to OpenClaw via `cron add`
3. **Monitor first week** - Tune frequency/sources
4. **Expand to Bundesliga/Serie A** - Once FPL stable

---

**Status:** ✅ Plan ready, awaiting activation
**Maintained by:** ButtiBot + FPL Scout Agent
