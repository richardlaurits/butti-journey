#!/bin/bash
# FPL Friday Brief - Comprehensive Analysis
# Runs ONLY on Fridays at 07:05 with full API + Web Scraping

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting FPL Friday comprehensive analysis" >> logs/fpl_friday.log

# Run comprehensive FPL analysis with API + web scraping
openclaw sessions_spawn \
    --task "Generate COMPREHENSIVE FPL Friday Brief for Richard Laurits.

🎯 REQUIREMENTS:
1. Fetch FPL API data (bootstrap-static, player summaries, fixtures)
2. Web scrape for latest news, rumors, injuries from Fantasy Football Scout, BBC Sport, official FPL
3. Analyze trends (transfers in/out, price changes, form)
4. Check press conferences for injury updates
5. Analyze next GW fixtures and difficulty

📊 INCLUDE:
- Current GW deadline
- Injury/suspension updates with SOURCES
- Transfer recommendations (SELL/BUY/HOLD) with reasoning
- Captain recommendations with stats
- Differential picks (low ownership, high potential)
- Blank and Double GW warnings
- Team value and price change alerts

🚫 EXCLUDE:
- Bundesliga data
- Serie A data
- General fantasy tips not specific to Richard's team

STRUCTURE:
🏆 FPL FRIDAY BRIEF - GW[XX]
📅 Deadline: [Day] [Date] [Time] CET

⚠️ INJURIES & SUSPENSIONS (with sources)
✅ Confirmed available
❌ Confirmed out
🟡 Doubts

💡 TRANSFER RECOMMENDATIONS
[Specific players with stats]

🎯 CAPTAIN ANALYSIS
[Top 3 options with reasoning]

📈 TRENDS THIS WEEK
[Price changes, transfers, ownership]

🚨 BLANK/DOUBLE GW WARNINGS

Richard's team: FC MACCHIATO (#17490)" \
    --label fpl-friday-analysis \
    --mode run \
    --timeout 300 >> logs/fpl_friday.log 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S'): FPL Friday analysis completed" >> logs/fpl_friday.log
