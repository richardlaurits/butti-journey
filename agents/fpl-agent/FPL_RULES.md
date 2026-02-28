# FPL RULES - ButtiBot Learning Document

**Purpose:** Store FPL knowledge so I improve over time and never make the same mistakes twice.

---

## CRITICAL RULES (NEVER BREAK THESE)

### 1. NEVER GUESS - ALWAYS VERIFY WITH DATA
- ❌ NEVER guess player prices, form, or stats
- ❌ NEVER assume data when search returns 0 results
- ✅ If API search fails → search again with different keywords
- ✅ If data uncertain → ask Richard or say "data unavailable"
- ✅ Always verify exact player names (e.g., "J.Timber" not "Timber")
- **Example:** I guessed Timber was £5.0 (wrong!), should have been £6.4 — cost Richard correct analysis
- **Lesson:** Verified via screenshot = £6.4 correct, my guess = £5.0 WRONG

### 2. Verify Gameweek Status BEFORE Analysis
- ❌ NEVER assume GW is finished
- ✅ Check if all fixtures are complete
- ✅ Check Arsenal vs Tottenham status (high-profile game)
- ✅ Only analyze AFTER all fixtures complete
- Example: GW27 (2026-02-18) has Arsenal vs Tottenham tonight — CANNOT finalize analysis yet

### 2. Player Positions (Element Types)
- 1 = GK (Goalkeeper)
- 2 = DEF (Defender)
- 3 = MID (Midfielder)
- 4 = FWD (Forward) ← **HAALAND IS FWD, NOT GK**

### 3. Points Calculation
- Base points: Player event_points from API
- Captain multiplier: x2
- Vice-captain multiplier: x1 (only if captain doesn't play)
- Example: Haaland (FWD) scored 5 pts, captain = 5 x 2 = **10 pts total**

### 4. Rank System
- Top 100K = ranks 1 to 100,000
- 138K = 138,000 = OUTSIDE top 100K ← Richard pointed this out
- Richard's goal: <100,000 overall rank

### 5. Transfer Rules (CRITICAL)
- **Max 1 free transfer per GW** (additional transfers = -4 pts cost each)
- **Max 5 free transfers can be saved** (useful for strategic GWs)
- Example: If you use 1 transfer GW28, you have 1 free for GW29. If you use 0 in GW29, you have 2 free for GW30.
- Check bank balance before suggesting transfers
- Prices change overnight → ALWAYS verify current price before finalizing
- With 11 GWs remaining: You have 11 free transfers total available (1/GW, max 5 saved)

---

## RICHARD'S TEAM INFO (HARDCODED)

- **Team ID:** 17490
- **Team Name:** FC MACCHIATO
- **Captain:** Haaland (FWD, Man City)
- **Vice-Captain:** João Pedro (FWD, Chelsea)

---

## FUNA-LIGAN (Mini-League)

- **League ID:** 94030
- **Name:** Funas Fantasy Premier League

### Current Standings (GW27):
1. BK Långburk (Fredrik Ankarås) - 1,651 pts
2. Timmerhuggarna (Micael Gustafsson) - 1,592 pts ← **TARGET: +22 pts gap**
3. FC MACCHIATO (Richard) - 1,570 pts
4. The Doodles (Emmanuel Nylander) - 1,555 pts
5. Tractor Boys (Fredrik Hellsberg) - 1,554 pts

### Strategy:
- Need +2 pts/GW average vs #2 over 11 remaining GWs
- Current form too weak (25 pts GW27 vs needed 50-60)

---

## GW27 STATUS (AS OF 2026-02-18 20:01 CET)

### STILL ONGOING:
- ❌ Arsenal vs Tottenham (tonight)
- These teams affect: Timber (DEF), Gabriel (DEF), Rice (MID), Son, Maddison, etc.

### COMPLETE:
- Man City, Chelsea, Liverpool, etc.

### RULE:
**DO NOT FINALIZE GW27 ANALYSIS UNTIL ALL FIXTURES COMPLETE**

---

## API ENDPOINTS (FOR REFERENCE)

```
https://fantasy.premierleague.com/api/entry/{TEAM_ID}/
https://fantasy.premierleague.com/api/entry/{TEAM_ID}/event/{GW}/picks/
https://fantasy.premierleague.com/api/bootstrap-static/
https://fantasy.premierleague.com/api/fixtures/?event={GW}
https://fantasy.premierleague.com/api/leagues-classic/{LEAGUE_ID}/standings/
```

---

## COMMON MISTAKES TO AVOID

1. ❌ Guessing player positions (always check element_type)
2. ❌ Forgetting captain x2 multiplier
3. ❌ Analyzing incomplete GWs
4. ❌ Using outdated player data
5. ❌ Not checking injury risk (chance_of_playing_this_round)
6. ❌ Ignoring bench management (bench can score points you don't get)

---

## SOURCES FOR NEWS & RUMORS

**When analyzing transfers, MUST fetch:**
1. FPL injury updates (from API: chance_of_playing)
2. **News & rumors** (need Brave Search or similar)
   - Injuries, transfers, form
   - Expert tips from FPL blogs
   - Fixture difficulty ratings

**Providers:**
- FPL Hints (Twitter/X)
- Fantasy Football Hub
- Official FPL injury reports
- Match previews & analysis

---

## NEXT STEPS FOR RICHARD

1. ✅ Get Brave Search API key (for news & rumors)
2. ✅ Set up automated weekly brief (GW analysis + fixtures + injuries)
3. ✅ Track gap to #2 in Funa-ligan daily
4. ✅ Monitor Arsenal status (currently weak form)

---

**Last Updated:** 2026-02-18 20:01 CET
**Author:** ButtiBot (Learning)
