#!/usr/bin/env python3
"""
Gmail Monitor using IMAP + App Password (no OAuth needed)
Filtrerar endast viktiga mejl
"""

import imaplib
import json
import os
from datetime import datetime, timedelta
from email.parser import HeaderParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, 'monitor_state.json')
APP_PASSWORD_FILE = os.path.join(SCRIPT_DIR, 'app_password.txt')

# Viktiga avsändare
IMPORTANT_SENDERS = [
    'pernilla.laurits@gmail.com',
    'pernilla@',
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

def load_app_password():
    """Ladda app password från fil"""
    with open(APP_PASSWORD_FILE, 'r') as f:
        return f.read().strip()

def connect_imap():
    """Anslut till Gmail via IMAP"""
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    password = load_app_password()
    imap.login('butti.nightrider@gmail.com', password)
    return imap

def load_state():
    """Ladda senaste check-data"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'last_check': None, 'seen_ids': []}

def save_state(state):
    """Spara state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def is_important(sender, subject):
    """Avgör om mejl är viktigt"""
    sender_lower = sender.lower()
    subject_lower = subject.lower()
    
    # Viktiga avsändare
    for important in IMPORTANT_SENDERS:
        if important.lower() in sender_lower:
            return True, "⭐ Från Pernilla"
    
    # Bankmeddelanden
    for bank in BANK_DOMAINS:
        if bank.lower() in sender_lower:
            return True, "🏦 Bankmeddelande"
    
    # Fakturor/betalningar
    for keyword in INVOICE_KEYWORDS:
        if keyword.lower() in subject_lower:
            return True, "💰 Faktura/betalning"
    
    # Kalenderinbjudningar
    for keyword in CALENDAR_KEYWORDS:
        if keyword.lower() in subject_lower:
            return True, "📅 Kalenderhändelse"
    
    return False, None

def check_important_emails():
    """Hämta och filtrera viktiga mejl"""
    try:
        imap = connect_imap()
        imap.select('INBOX')
        
        # Hämta senaste 50 mejl
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()[-50:]  # Senaste 50
        
        state = load_state()
        seen_ids = set(state.get('seen_ids', []))
        important_emails = []
        
        for email_id in email_ids:
            email_id_str = email_id.decode()
            
            if email_id_str in seen_ids:
                continue
            
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            parser = HeaderParser()
            msg = parser.parsestr(msg_data[0][1].decode())
            
            sender = msg.get('From', '').lower()
            subject = msg.get('Subject', '')
            
            is_imp, label = is_important(sender, subject)
            
            if is_imp:
                important_emails.append({
                    'id': email_id_str,
                    'from': sender,
                    'subject': subject,
                    'label': label,
                })
                seen_ids.add(email_id_str)
        
        imap.close()
        imap.logout()
        
        # Spara state
        state['seen_ids'] = list(seen_ids)[-200:]  # Behåll senaste 200
        state['last_check'] = datetime.now().isoformat()
        save_state(state)
        
        return important_emails
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == '__main__':
    emails = check_important_emails()
    
    if emails:
        print("📧 Viktiga mejl hittade:\n")
        for email in emails:
            print(f"{email['label']} {email['subject']}")
            print(f"   Från: {email['from']}\n")
    else:
        print("HEARTBEAT_OK")
