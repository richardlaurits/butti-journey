#!/usr/bin/env python3
"""Test calendar access"""

import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

token_file = Path(__file__).parent / "calendar_token.pickle"

if not token_file.exists():
    print("❌ Token not found")
    exit(1)

# Load credentials
with open(token_file, 'rb') as f:
    creds = pickle.load(f)

if creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Build service
service = build('calendar', 'v3', credentials=creds)

try:
    # Get calendar list
    calendars = service.calendarList().list().execute()
    
    print("📅 DIN KALENDER:")
    print()
    
    for cal in calendars.get('items', []):
        print(f"✅ {cal['summary']}")
        print(f"   ID: {cal['id']}")
        print(f"   Primary: {cal.get('primary', False)}")
        print()
    
    # Get upcoming events (next 7 days)
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
    
    primary_calendar = calendars['items'][0]['id']
    
    events = service.events().list(
        calendarId=primary_calendar,
        timeMin=now,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    print("📍 KOMMANDE EVENTS (nästa 7 dagar):")
    print()
    
    for event in events.get('items', []):
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"📌 {event['summary']}")
        print(f"   Tid: {start}")
        if 'description' in event:
            print(f"   Desc: {event['description'][:50]}...")
        print()
    
    print("✅ KALENDER-ÅTKOMST FUNGERAR! 🎯")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
