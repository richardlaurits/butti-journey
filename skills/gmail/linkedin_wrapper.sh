#!/bin/bash
# LinkedIn Job Monitor Wrapper
# Checks quiet hours before alerting

cd ~/.openclaw/workspace
source venv/bin/activate

# Check if it's quiet hours (22:00-07:00)
hour=$(date +%H)
if [ "$hour" -ge 22 ] || [ "$hour" -lt 7 ]; then
    # Quiet hours - only check, don't alert unless CRITICAL
    result=$(python3 skills/gmail/linkedin_job_monitor.py 2>&1)
    
    # Only log, don't send alerts during quiet hours
    if echo "$result" | grep -q "Score: 9\|Score: 10"; then
        # 9-10 score = CRITICAL match, alert anyway
        echo "$(date): LinkedIn CRITICAL job match found during quiet hours" >> skills/gmail/linkedin_monitor.log
        echo "$result"
    else
        # Lower scores = wait until morning
        echo "$(date): LinkedIn check during quiet hours - no critical matches" >> skills/gmail/linkedin_monitor.log
        echo "HEARTBEAT_OK"
    fi
else
    # Normal hours - full check with alerts
    python3 skills/gmail/linkedin_job_monitor.py
fi
