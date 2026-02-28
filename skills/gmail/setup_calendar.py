#!/usr/bin/env python3
"""
Setup Google Calendar OAuth using existing Gmail credentials
Combines Gmail + Calendar scopes in one login
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Paths
CREDENTIALS_FILE = Path(__file__).parent / "gmail_credentials.json"
CALENDAR_TOKEN_FILE = Path(__file__).parent / "calendar_token.pickle"

# Scopes - BOTH Gmail and Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar',
]

def setup_calendar():
    """Setup Calendar OAuth using Gmail credentials."""
    
    if not CREDENTIALS_FILE.exists():
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        exit(1)
    
    print("🔐 Setting up Google Calendar OAuth...")
    print(f"📁 Using credentials: {CREDENTIALS_FILE}")
    print(f"📋 Scopes: Gmail + Calendar")
    print()
    
    try:
        # Create flow from credentials
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES
        )
        
        print("🌐 Opening browser for authentication...")
        print("   (If it doesn't open, visit the URL in the terminal)")
        print()
        
        # Run OAuth flow
        creds = flow.run_local_server(port=0)
        
        # Save token
        with open(CALENDAR_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        print()
        print("✅ SUCCESS!")
        print(f"📁 Token saved to: {CALENDAR_TOKEN_FILE}")
        print()
        print("✨ You can now use:")
        print("   - Gmail (already working)")
        print("   - Google Calendar (new!)")
        print()
        print("Ready to go! 🚀")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    setup_calendar()
