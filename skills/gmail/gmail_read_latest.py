#!/usr/bin/env python3
"""
Read latest important email from Gmail
"""

import pickle
import base64
from pathlib import Path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Token path
token_file = Path(__file__).parent / "token.pickle"

if not token_file.exists():
    print("❌ Token file not found. Run gmail setup first.")
    exit(1)

# Load credentials
with open(token_file, 'rb') as f:
    creds = pickle.load(f)

# Refresh if needed
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Build service
service = build('gmail', 'v1', credentials=creds)

# Get latest important email
try:
    results = service.users().messages().list(
        userId='me',
        q='is:important',
        maxResults=1
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        print("Ingen nya viktiga mejl")
        exit(0)
    
    # Get full message
    msg = service.users().messages().get(
        userId='me',
        id=messages[0]['id'],
        format='full'
    ).execute()
    
    # Parse headers
    headers = {h['name']: h['value'] for h in msg['payload']['headers']}
    
    print(f"📧 FRÅN: {headers.get('From', 'Unknown')}")
    print(f"📌 ÄMNE: {headers.get('Subject', 'No subject')}")
    print(f"📅 DATUM: {headers.get('Date', 'Unknown')}")
    print("\n" + "="*70 + "\n")
    
    # Extract body
    body = ""
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                break
    else:
        if 'data' in msg['payload']['body']:
            body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
    
    print(body if body else "(Tom email)")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
