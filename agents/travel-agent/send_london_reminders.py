#!/usr/bin/env python3
"""
London Trip Reminders
Sends reminders for Richard's London business trip
"""

import json
from datetime import datetime
from pathlib import Path

REMINDER_FILE = Path('/home/richard-laurits/.openclaw/workspace/agents/travel-agent/london_trip_reminders.json')

def load_reminders():
    if REMINDER_FILE.exists():
        with open(REMINDER_FILE, 'r') as f:
            return json.load(f)
    return {}

def send_telegram(message):
    """Send message via telegram_sender.py"""
    import subprocess
    sender_script = Path('/home/richard-laurits/.openclaw/workspace/agents/travel-agent/telegram_sender.py')
    
    try:
        subprocess.run(['python3', str(sender_script)], input=message, text=True, timeout=30)
        return True
    except Exception as e:
        print(f"Failed to send: {e}")
        return False

def check_and_send():
    """Check which reminder to send based on date/time"""
    data = load_reminders()
    now = datetime.now()
    
    # Check if today is one of the trip days
    today_str = now.strftime('%Y-%m-%d')
    current_hour = now.hour
    current_minute = now.minute
    
    # Map dates to reminder keys
    date_map = {
        data.get('dates', {}).get('wednesday'): 'wednesday',
        data.get('dates', {}).get('thursday'): 'thursday',
        data.get('dates', {}).get('friday'): 'friday'
    }
    
    today_key = date_map.get(today_str)
    if not today_key:
        return  # Not a trip day
    
    reminders = data.get('reminders', {})
    
    # Wednesday
    if today_key == 'wednesday':
        if current_hour == 8 and current_minute < 15:
            send_telegram(reminders.get('wednesday_morning', {}).get('message', ''))
        elif current_hour == 12 and current_minute < 15:
            send_telegram(reminders.get('wednesday_afternoon', {}).get('message', ''))
    
    # Thursday
    elif today_key == 'thursday':
        if current_hour == 8 and current_minute < 30:
            send_telegram(reminders.get('thursday_morning', {}).get('message', ''))
    
    # Friday
    elif today_key == 'friday':
        if current_hour == 8 and current_minute < 30:
            send_telegram(reminders.get('friday_morning', {}).get('message', ''))
        elif current_hour == 9 and current_minute < 15:
            send_telegram(reminders.get('friday_departure', {}).get('message', ''))

if __name__ == "__main__":
    check_and_send()
