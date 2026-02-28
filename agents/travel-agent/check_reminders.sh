#!/bin/bash
# Travel Agent - Daily check for check-in reminders
# Runs every hour during daytime

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

# Check for reminders
OUTPUT=$(python3 agents/travel-agent/travel_agent.py reminders 2>/dev/null)

# If there are reminders, send to Telegram
if [ -n "$OUTPUT" ] && [ "$OUTPUT" != "✅ Inga påminnelser just nu." ]; then
    echo "$OUTPUT" | python3 agents/travel-agent/telegram_sender.py 2>/dev/null
    echo "[$(date '+%Y-%m-%d %H:%M')] Check-in reminder sent" >> logs/travel_agent.log
fi
