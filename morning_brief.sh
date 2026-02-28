#!/bin/bash
# Morning Brief - Daily 07:00 CET
# Focus: AI news, markets/world economy, weather, important emails

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting morning brief" >> logs/morning_brief.log

# Get CHF/SEK exchange rate
CURRENCY_DATA=$(python3 << 'PYEOF'
import sys
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')
try:
    import yfinance as yf
    ticker = yf.Ticker("CHFSEK=X")
    hist = ticker.history(period="2d")
    if len(hist) >= 2:
        current = hist['Close'].iloc[-1]
        previous = hist['Close'].iloc[-2]
        change = ((current - previous) / previous) * 100
        print(f"1 CHF = {current:.2f} SEK ({change:+.2f}%)")
    else:
        print("1 CHF = ~12.00 SEK")
except:
    print("1 CHF = ~12.00 SEK")
PYEOF
)

# Generate the brief
openclaw sessions_spawn \
    --task "Generate a FOCUSED morning brief for Richard Laurits. Current time: $(date '+%Y-%m-%d %H:%M').

🎯 FOCUS AREAS (priority order):
1. 🤖 AI NEWS (last 24h) - Major developments, model releases, industry moves
2. 📈 MARKETS & WORLD ECONOMY (last 24h) - Stock markets, crypto, key economic indicators  
3. 🌤️ LOCAL WEATHER - Prangins/Eysins today + tomorrow
4. 📧 IMPORTANT EMAILS - Check richardlaurits@gmail.com for unread important emails (Pernilla, bank, calendar, urgent)
5. 💱 CURRENCY - CHF/SEK rate and brief context

❌ DO NOT INCLUDE:
- Agent status details
- Fantasy football (only on Fridays)
- French lessons
- General news unless AI/market related

STRUCTURE:
🌅 GOD MORGON RICHARD!
$(date '+%A %d %B %Y, %H:%M')

───

🤖 AI NYHETER (24h)
Search for: AI news last 24 hours, new model releases, OpenAI, Google, major AI companies
3-5 key bullet points with sources

───

📈 MARKNADER & VÄRLDSEKONOMI (24h)
Search for: Stock market today, world economy news, crypto, major indices
Key movements and why

───

🌤️ VÄDER Prangins/Eysins
Current + today forecast

───

💱 VALUTA
CHF/SEK: ${CURRENCY_DATA}
Brief context (if notable movement)

───

📧 VIKTIGA EMAILS
Check Gmail for unread from: Pernilla, banks, calendar invites, urgent matters
If none critical: 'Inga brådskande ärenden idag.'

Keep it concise. Focus on what's actionable or important for Richard's day." \
    --label morning-brief-generator \
    --mode run \
    --timeout 180 >> logs/morning_brief.log 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S'): Morning brief completed" >> logs/morning_brief.log
