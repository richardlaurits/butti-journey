# DATA_SOURCES.md - Where to Get Fresh Data

**[2026-02-14 11:55]** Official data sources for FPL Scout

## Premier League (FPL)

### Official FPL API
**Base URL:** `https://fantasy.premierleague.com/api/`

**Key Endpoints:**
```
/bootstrap-static/
→ All players, teams, gameweeks, fixtures
→ Updated live during matches

/entry/{team_id}/
→ Specific manager's team
→ Richard's team ID: [TBD - need from Richard]

/entry/{team_id}/history/
→ Historical performance, chips used

/fixtures/
→ All fixtures with difficulty ratings

/element-summary/{player_id}/
→ Player detailed stats, fixtures, history

/dream-team/{gw}/
→ Team of the week
```

**How to use:**
```bash
curl -s 'https://fantasy.premierleague.com/api/bootstrap-static/' | jq '.elements[] | select(.web_name=="Haaland")'
```

### Injury & Rotation Intel
- **Ben Crellin Twitter:** @BenCrellin (fixture expert)
- **FPL Rockstar:** @FPLRockstar (price predictions)
- **Official club sites:** Presser summaries

### Price Change Predictors
- **FPL Statistics:** http://www.fplstatistics.co.uk/
- **Fantasy Football Fix:** https://www.fantasyfootballfix.com/price/

### Richard's Priority Sources (Scrape 1-2x daily)
**[2026-02-14 12:02]** Top resources to monitor:

1. **FPL FantasyScout** - https://www.fantasyfootballscout.co.uk/
   - Use team ID 17490 for personalized analysis
   - Check: Team tips, Transfer picks, Captain picks
   
2. **FPL Football Hub** - https://www.fantasyfootballhub.co.uk/
   - Use team ID 17490 where applicable
   - Check: Fixture ticker, Price predictors, Stats center

3. **Official FPL Stats** - https://fantasy.premierleague.com/
   - Team page: https://fantasy.premierleague.com/entry/17490/
   - Use for: Current squad, points, transfers, mini-league standings

4. **X (Twitter) Feeds:**
   - @OfficialFPL - Official news
   - @FantasyScout - Expert analysis  
   - @FPL_Hub - Stats & tools
   - @BenCrellin - Rotation/fixtures
   - @FPLRockstar - Price changes

---

## Bundesliga

### Official Stats
**URL:** https://www.bundesliga.com/en/bundesliga/stats

**Key Sections:**
- Top scorers
- Assists leaders
- Form tables
- Fixture list

### Fantasy Platform
**[TBD]** - Richard, which Bundesliga fantasy platform do you use?
- Kickbase?
- Official Bundesliga Fantasy?
- Community league?

### Injury News
- **Transfermarkt:** https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1
- **Kicker.de:** https://www.kicker.de/bundesliga/spieltag (German)

---

## Serie A

### Official Site
**URL:** https://www.legaseriea.it/en

### Fantasy Platforms
**[TBD]** - Richard, which Serie A fantasy do you use?
- Fantrax?
- Official Serie A fantasy?

### Stats & News
- **Football Italia:** https://www.football-italia.net/
- **ESPN Serie A:** https://www.espn.com/soccer/league/_/name/ita.1

---

## General Football Data

### Fixture Difficulty & Form
- **Understat:** https://understat.com/ (xG, xA stats)
- **FBref:** https://fbref.com/ (detailed analytics)

### Twitter Accounts to Monitor
- @OfficialFPL - FPL official news
- @BenCrellin - Rotation & doubles
- @FPLRockstar - Price changes
- @{Bundesliga fantasy account} - TBD
- @SerieA_EN - Serie A official

### Backup Search Queries
If APIs fail, use web_search:
```
"[player name] injury latest news"
"[team] press conference [date]"
"FPL [player] price change"
"Bundesliga [team] lineup news"
```

---

## Data Freshness Rules

**Real-time (use API):**
- Player prices
- Injury flags
- Ownership %
- Live match scores

**Hourly refresh OK:**
- Form stats (last 5 games)
- Fixture difficulty
- Press conference summaries

**Daily refresh OK:**
- Season stats (goals, assists)
- League tables
- Long-term injury lists

**Manual check needed:**
- Transfer rumors
- Manager comments (tone/context)
- Unusual tactical changes

---

## How to Verify Data

1. **Check timestamp:** Is it current?
2. **Cross-reference:** 2+ sources agree?
3. **Official > Community:** Club site > Reddit
4. **Recent > Historical:** Last 5 games > season average

---

---

## Automated Scraping Schedule

**[2026-02-14 12:02]** Setup plan:

### Daily Morning Scrape (08:00 CET)
```bash
# Fetch latest from priority sources
1. Official FPL team data (ID 17490)
2. FPL FantasyScout - overnight news
3. Twitter feeds - injury updates
4. Price change results
```

### Daily Evening Scrape (20:00 CET)
```bash
# Pre-deadline prep
1. FPL Football Hub - fixture ticker
2. FPL Statistics - price predictions
3. Press conference summaries
4. Lineup rumors
```

### Implementation:
- Use `web_fetch` for structured pages
- Use `web_search` for Twitter/news
- Cache results in `agents/fantasy-agent/data/` folder
- Update MEMORY.md with latest intel

---

**Note:** Always mention data source + timestamp in reports!
Example: "*Per FPL API 2026-02-14 12:00: Haaland ownership 82%*"
