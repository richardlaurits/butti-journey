#!/bin/bash
# Hourly Investment Alert - Run during market hours
# Checks for unusual price movements every hour

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

# Only run on weekdays (Mon-Fri)
dow=$(date +%u)
if [ "$dow" -gt 5 ]; then
    exit 0
fi

# Only run during market hours: 09:00-17:30
hour=$(date +%H)
if [ "$hour" -lt 9 ] || [ "$hour" -ge 18 ]; then
    exit 0
fi

# Run the alert checker
OUTPUT=$(python3 agents/investment-agent/hourly_alert.py 2>/dev/null)

# If there's output (alerts detected), send to Telegram
if [ -n "$OUTPUT" ]; then
    # Check if it's an actual alert (starts with 🚨 or ⚠️)
    if echo "$OUTPUT" | grep -qE "^(🚨|⚠️)"; then
        # Send via Telegram
        echo "$OUTPUT" | python3 agents/investment-agent/telegram_sender.py 2>/dev/null
        # Also log it
        echo "[$(date '+%Y-%m-%d %H:%M')] Alert sent" >> logs/investment_alerts.log
    fi
fi
