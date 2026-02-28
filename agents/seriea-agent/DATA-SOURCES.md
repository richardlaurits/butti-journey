# Serie A Fantasy Data Sources

**[2026-02-14]** Primary data source identified: World Fantasy Soccer

## World Fantasy Soccer Platform

**URL:** https://worldfantasysoccer.com/
**Richard's League:** Season 20153
**Full Rules & Stats:** https://worldfantasysoccer.com/season/20153

### What to Access

From World Fantasy Soccer, the agent should extract:

1. **Player Stats**
   - Player points
   - Player prices
   - Position (GK, DEF, MID, FWD)
   - Current form
   - Injury status

2. **Scoring System**
   - Points for goals, assists, clean sheets
   - Bonus points
   - Negative points (yellow/red cards)
   - Position-specific multipliers

3. **League Data**
   - Richard's current team composition
   - Current ranking
   - Points vs competition
   - Budget remaining

4. **Fixture Information**
   - Upcoming Serie A matches
   - Difficulty ratings (for planning transfers)
   - Team news & injuries

5. **Transfer Rules**
   - Transfer windows
   - Budget constraints
   - Squad size limits
   - Position requirements

### Data Fetching Strategy

1. **Direct browsing:** Can parse World Fantasy Soccer website
2. **API endpoint:** Check if WFS has public API (likely JSON)
3. **Web scraping:** Respectful scraping of stats pages
4. **Export:** See if user can export league data as CSV/JSON

### Agent Implementation

The agent should:
- ✅ Fetch Richard's team ID (from user input or settings)
- ✅ Pull current squad + points
- ✅ Get upcoming fixtures
- ✅ Analyze transfer opportunities
- ✅ Recommend next GW lineup
- ✅ Compare performance vs league standings

### Integration Steps

**Phase 1 (NOW):**
- Document WFS platform rules
- Identify API endpoints
- Test data access

**Phase 2:**
- Build data fetcher (scraper or API)
- Parse league standings
- Parse player stats

**Phase 3:**
- Weekly Serie A brief
- Transfer recommendations
- GW analysis (similar to FPL agent)

---

**Status:** Ready for Phase 1
**Next:** Agent implementation (awaiting rules confirmation from Richard)
