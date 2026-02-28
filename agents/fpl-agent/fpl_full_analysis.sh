#!/bin/bash
# Full FPL Analysis - Runs 24h before deadline
# Comprehensive analysis of Richard's squad

cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting full FPL analysis" >> agents/fpl-agent/analysis.log

openclaw sessions_spawn \
    --task "You are the FPL Agent for Richard Laurits. It's 24 hours before the Gameweek deadline. Run a COMPREHENSIVE analysis:

1. FPL API DATA:
   - Fetch current squad from entry 17490
   - Check player form, fixtures, ownership
   - Identify rotation risks

2. INJURY/SUSPENSION CHECK (All 11 players):
   - Haaland, Gabriel, Rice, Timber, Saka, Son, Salah, Guéhi, Solanke, Hill, Thiago
   - Use web_search with queries like '[player] injury FPL', '[player] suspension'
   - Check FPL official status

3. TRANSFER RUMOURS:
   - Search for transfer rumours affecting your players
   - Use web_search freshness=pw (past week)
   - Sources: BBC Sport, Sky Sports, official club sites

4. FIXTURE ANALYSIS:
   - Check difficulty of upcoming fixtures
   - Identify captaincy options
   - Note any DGW (Double Gameweek) or BGW (Blank Gameweek) risks

5. RECOMMENDATIONS:
   - Suggest transfers if needed (max 2 free transfers)
   - Captain recommendation
   - Bench order advice
   - Any urgent actions needed

6. DATA SOURCES TO USE:
   - FPL API (bootstrap-static, entry data)
   - web_search for news
   - Fantasy Football Scout (if accessible)
   - Fantasy Football Hub (if accessible)
   - X/Twitter FPL community
   - Google News

OUTPUT: Send comprehensive Telegram report with:
- 🏆 Squad Status Overview
- ⚠️ Injury/Suspension Alerts (if any)
- 📊 Key Stats (form, fixtures)
- 🎯 Transfer Recommendations (if needed)
- ©️ Captain Pick suggestion
- ✅ Final checklist before deadline

Be thorough. This is the main pre-deadline briefing." \
    --label fpl-full-analysis \
    --mode run \
    --timeout 300 >> agents/fpl-agent/analysis.log 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S'): Analysis completed" >> agents/fpl-agent/analysis.log
