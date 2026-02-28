#!/bin/bash
# Check FPL deadline and spawn agent if 24h or 3h before

cd ~/.openclaw/workspace
source venv/bin/activate

RESULT=$(python3 agents/fpl-agent/check_deadline.py)

if echo "$RESULT" | grep -q "ALERT_24H"; then
    echo "$(date): Triggering 24h alert" >> agents/fpl-agent/deadline_cron.log
    openclaw sessions_spawn \
        --task "FPL DEADLINE ALERT - 24 hours left! Check for injuries on Haaland, Salah, Saka, Son, Gabriel, Rice, Timber, Guéhi, Solanke, Hill, Thiago. Use web_search with freshness=pw. Alert Richard immediately of any issues via Telegram." \
        --label fpl-agent-24h \
        --mode run \
        --timeout 120 >> agents/fpl-agent/deadline_cron.log 2>&1
elif echo "$RESULT" | grep -q "ALERT_3H"; then
    echo "$(date): Triggering 3h alert" >> agents/fpl-agent/deadline_cron.log
    openclaw sessions_spawn \
        --task "FPL FINAL ALERT - 3 hours to deadline! URGENT check for last-minute injuries on all FC MACCHIATO players. Use web_search. Alert Richard immediately via Telegram if any issues." \
        --label fpl-agent-3h \
        --mode run \
        --timeout 120 >> agents/fpl-agent/deadline_cron.log 2>&1
fi
