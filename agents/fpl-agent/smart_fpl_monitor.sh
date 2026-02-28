#!/bin/bash
# Smart FPL Monitor - Runs Sundays to schedule next GW analysis
# Checks FPL API once per week, schedules analysis 24h before deadline

cd ~/.openclaw/workspace
source venv/bin/activate

# Fetch next GW deadline from FPL API
python3 << 'PYTHON_EOF'
import requests
import json
from datetime import datetime, timedelta
import subprocess
import os

try:
    resp = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/', timeout=15)
    data = resp.json()
    
    # Find next gameweek
    for event in data.get('events', []):
        if event.get('is_next'):
            deadline_str = event.get('deadline_time')
            gw_name = event.get('name', 'Unknown GW')
            break
    else:
        print("ERROR: Could not find next gameweek")
        exit(1)
    
    deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
    now = datetime.now(deadline.tzinfo)
    
    # Calculate when to run analysis (24h before deadline)
    analysis_time = deadline - timedelta(hours=24)
    
    hours_until_analysis = (analysis_time - now).total_seconds() / 3600
    
    print(f"Next GW: {gw_name}")
    print(f"Deadline: {deadline_str}")
    print(f"Analysis scheduled at: {analysis_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"Hours until analysis: {hours_until_analysis:.1f}")
    
    # If analysis is within 7 days, schedule it
    if hours_until_analysis > 0 and hours_until_analysis <= 168:  # 168h = 7 days
        # Create at job for the analysis (more flexible than cron)
        at_time = analysis_time.strftime('%H:%M %Y-%m-%d')
        
        # Remove any existing FPL analysis jobs
        os.system('atq | grep fpl-analysis | cut -f1 | xargs -r atrm 2>/dev/null')
        
        # Schedule new analysis
        cmd = f'echo "export OPENCLAW_API_KEY=unused; cd ~/.openclaw/workspace && ~/.openclaw/workspace/agents/fpl-agent/fpl_full_analysis.sh" | at {at_time} 2>&1'
        result = os.popen(cmd).read()
        
        print(f"Scheduled with at: {result}")
        
        # Also save to file for reference
        with open('agents/fpl-agent/next_gw_schedule.txt', 'w') as f:
            f.write(f"GW: {gw_name}\n")
            f.write(f"Deadline: {deadline_str}\n")
            f.write(f"Analysis at: {analysis_time.isoformat()}\n")
            f.write(f"Hours away: {hours_until_analysis:.1f}\n")
    else:
        print(f"Analysis time too far in future ({hours_until_analysis:.1f}h), will reschedule next Sunday")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
PYTHON_EOF

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S'): FPL monitoring updated for next GW" >> agents/fpl-agent/smart_monitor.log
else
    echo "$(date '+%Y-%m-%d %H:%M:%S'): ERROR - Failed to update FPL monitoring" >> agents/fpl-agent/smart_monitor.log
fi
