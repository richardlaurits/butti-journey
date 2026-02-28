#!/usr/bin/env python3
"""
Smart Gmail Monitor - Filtrerar endast viktiga mejl
Kör var 30:e minut via heartbeat
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import json
import re
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, 'monitor_state.json')

# Viktiga avsändare
IMPORTANT_SENDERS = [
    'pernilla.laurits@gmail.com',
    'pernilla@',  # Catch-all för Pernilla
]

# Bank-domäner
BANK_DOMAINS = [
    'nordea',
    'seb.se',
    'handelsbanken',
    'ubs.com',
    'credit-suisse',
    'postfinance',
    'raiffeisen',
]

# Faktura/betalnings-nyckelord
INVOICE_KEYWORDS = [
    'faktura',
    'invoice',
    'facture',
    'betalning',
    'payment due',
    'payment reminder',
    'räkning',
    'rechnung',
    'paiement',
]

# Kalender-nyckelord
CALENDAR_KEYWORDS = [
    'calendar invitation',
    'meeting invitation',
    'inbjudan',
    'möte',
]

# Ignorera dessa avsändare (nyhetsbrev, marknadsföring)
IGNORE_SENDERS = [
    'linkedin.com',
    'forbes',
    'noreply',
    'no-reply',
    'newsletter',
    'notifications',
    'marketing',
]

def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    token_path = os.path.join(SCRIPT_DIR, 'token.pickle')
    credentials_path = os.path.join(SCRIPT_DIR, 'gmail_credentials.json')
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def load_state():
    """Ladda senaste check-timestamp och sedd mejl-lista"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'last_check': None, 'seen_ids': []}

def save_state(state):
    """Spara state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def is_important_sender(from_email):
    """Kolla om avsändaren är viktig"""
    from_lower = from_email.lower()
    
    # Kolla Pernilla först
    for sender in IMPORTANT_SENDERS:
        if sender.lower() in from_lower:
            return True, "Från Pernilla"
    
    # Kolla banker
    for bank in BANK_DOMAINS:
        if bank.lower() in from_lower:
            return True, "Från bank"
    
    return False, None

def is_invoice(subject):
    """Kolla om ämnesraden innehåller faktura/betalning"""
    subject_lower = subject.lower()
    for keyword in INVOICE_KEYWORDS:
        if keyword.lower() in subject_lower:
            return True
    return False

def is_calendar_invite(subject):
    """Kolla om det är en kalenderhändelse"""
    subject_lower = subject.lower()
    for keyword in CALENDAR_KEYWORDS:
        if keyword.lower() in subject_lower:
            return True
    return False

def should_ignore(from_email, subject):
    """Kolla om mejlet ska ignoreras"""
    from_lower = from_email.lower()
    subject_lower = subject.lower()
    
    # Ignorera nyhetsbrev och marknadsföring
    for ignore in IGNORE_SENDERS:
        if ignore.lower() in from_lower:
            return True
    
    # Ignorera om "unsubscribe" finns (oftast nyhetsbrev)
    if 'unsubscribe' in subject_lower:
        return True
    
    return False

def check_important_emails():
    """Kolla inbox för viktiga mejl sedan senaste check"""
    service = get_gmail_service()
    state = load_state()
    
    # Kolla mejl från senaste 2 timmar (säkerhetsmargin)
    cutoff_time = datetime.now() - timedelta(hours=2)
    cutoff_timestamp = int(cutoff_time.timestamp())
    
    # Sök olästa mejl + viktiga (Gmail important label)
    results = service.users().messages().list(
        userId='me',
        q=f'is:unread after:{cutoff_timestamp}',
        maxResults=50
    ).execute()
    
    messages = results.get('messages', [])
    
    if not messages:
        return None  # Inga nya mejl
    
    important_emails = []
    seen_ids = state.get('seen_ids', [])
    new_seen_ids = seen_ids.copy()
    
    for msg in messages:
        msg_id = msg['id']
        
        # Skippa om redan sedd
        if msg_id in seen_ids:
            continue
        
        # Hämta fullständig mejl-metadata
        message = service.users().messages().get(
            userId='me', 
            id=msg_id,
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()
        
        headers = message['payload']['headers']
        from_header = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No subject')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
        
        # Kolla om Gmail markerat som Important
        labels = message.get('labelIds', [])
        is_gmail_important = 'IMPORTANT' in labels
        
        # Filtrera bort ignorerade
        if should_ignore(from_header, subject):
            new_seen_ids.append(msg_id)
            continue
        
        # Kolla om viktigt
        is_important_person, reason = is_important_sender(from_header)
        is_inv = is_invoice(subject)
        is_cal = is_calendar_invite(subject)
        
        if is_important_person or is_inv or is_cal or is_gmail_important:
            priority = []
            if is_important_person:
                priority.append(f"⭐ {reason}")
            if is_inv:
                priority.append("💰 Faktura/Betalning")
            if is_cal:
                priority.append("📅 Kalender")
            if is_gmail_important:
                priority.append("❗ Gmail Important")
            
            important_emails.append({
                'from': from_header,
                'subject': subject,
                'date': date,
                'priority': ' | '.join(priority)
            })
            
            new_seen_ids.append(msg_id)
    
    # Spara uppdaterad state
    state['last_check'] = datetime.now().isoformat()
    state['seen_ids'] = new_seen_ids[-200:]  # Behåll max 200 senaste
    save_state(state)
    
    if not important_emails:
        return None  # Inga viktiga mejl
    
    # Formatera output
    output = ["📧 VIKTIGA NYA MEJL:\n"]
    for email in important_emails:
        output.append(f"{email['priority']}")
        output.append(f"Från: {email['from']}")
        output.append(f"Ämne: {email['subject']}")
        output.append(f"Datum: {email['date']}")
        output.append("")
    
    return "\n".join(output)

if __name__ == "__main__":
    result = check_important_emails()
    if result:
        print(result)
    else:
        print("HEARTBEAT_OK")  # Inga viktiga mejl
