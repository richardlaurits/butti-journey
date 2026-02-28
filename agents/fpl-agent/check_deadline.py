#!/usr/bin/env python3
"""Check FPL deadline and trigger alerts at 24h and 3h before"""
import requests
import json
from datetime import datetime, timedelta
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), 'deadline_state.json')

def get_fpl_deadline():
    """Fetch current gameweek deadline from FPL API"""
    try:
        resp = requests.get('https://fantasy.premierleague.com/api/bootstrap-static/', timeout=10)
        data = resp.json()
        
        # Find next gameweek
        for event in data.get('events', []):
            if event.get('is_next'):
                return event.get('deadline_time')
        
        # Fallback: find current gameweek + 1
        for event in data.get('events', []):
            if event.get('is_current'):
                current_id = event.get('id')
                for next_event in data.get('events', []):
                    if next_event.get('id') == current_id + 1:
                        return next_event.get('deadline_time')
    except Exception as e:
        print(f"Error fetching deadline: {e}")
    return None

def should_alert(deadline_str):
    """Check if we should alert now (24h or 3h before deadline)"""
    if not deadline_str:
        return None
    
    deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
    now = datetime.now(deadline.tzinfo)
    time_until = deadline - now
    
    hours_until = time_until.total_seconds() / 3600
    
    # Load state
    alerted_windows = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            alerted_windows = state.get('alerted', [])
            last_deadline = state.get('last_deadline')
            
            # Reset if new gameweek
            if last_deadline != deadline_str:
                alerted_windows = []
    
    # Check 24h window (23-25 hours before)
    if 23 <= hours_until <= 25 and '24h' not in alerted_windows:
        return '24h'
    
    # Check 3h window (2.5-3.5 hours before)
    if 2.5 <= hours_until <= 3.5 and '3h' not in alerted_windows:
        return '3h'
    
    return None

def save_state(deadline_str, alert_type):
    """Save that we alerted for this window"""
    state = {'last_deadline': deadline_str, 'alerted': []}
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    
    if alert_type not in state['alerted']:
        state['alerted'].append(alert_type)
    state['last_deadline'] = deadline_str
    
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

if __name__ == '__main__':
    deadline = get_fpl_deadline()
    
    if deadline:
        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        now = datetime.now(deadline_dt.tzinfo)
        hours_left = (deadline_dt - now).total_seconds() / 3600
        
        print(f"Next FPL deadline: {deadline}")
        print(f"Hours until deadline: {hours_left:.1f}")
        
        alert = should_alert(deadline)
        
        if alert == '24h':
            print("ALERT_24H")
            save_state(deadline, '24h')
        elif alert == '3h':
            print("ALERT_3H")
            save_state(deadline, '3h')
        else:
            print("NO_ALERT")
    else:
        print("ERROR: Could not fetch deadline")
