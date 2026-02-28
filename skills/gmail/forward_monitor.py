#!/usr/bin/env python3
"""
Forward Monitor - Automatically read and act on emails Richard forwards to ButtiBot
Monitors: butti.nightrider@gmail.com for emails from Richard
"""

import imaplib
import email
from email.header import decode_header
import json
import os
from datetime import datetime

EMAIL = "butti.nightrider@gmail.com"
APP_PASSWORD = "jlcylboroggobdhj"
STATE_FILE = "forward_state.json"

def load_state():
    """Load previously seen email IDs"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"processed_ids": []}

def save_state(state):
    """Save processed email IDs"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_forward_subject(msg):
    """Decode email subject"""
    subject = msg.get('Subject', '(no subject)')
    if isinstance(subject, str):
        return subject
    return str(subject)

def get_body(msg):
    """Extract email body"""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try:
                payload = part.get_payload(decode=True)
                return payload.decode('utf-8', errors='ignore')
            except:
                return part.get_payload()
    return ""

def check_forwards():
    """Check for new forwards from Richard"""
    state = load_state()
    
    try:
        imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        imap.login(EMAIL, APP_PASSWORD)
        imap.select('INBOX')
        
        # Search for emails from Richard
        status, messages = imap.search(None, 'FROM "richardlaurits@gmail.com"')
        email_ids = messages[0].split()
        
        new_forwards = []
        
        for email_id in email_ids:
            email_id_str = email_id.decode() if isinstance(email_id, bytes) else email_id
            
            # Skip already processed
            if email_id_str in state['processed_ids']:
                continue
            
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject = get_forward_subject(msg)
            
            # Only care about forwards
            if 'Fwd:' in subject or 'Forward' in subject:
                body = get_body(msg)
                new_forwards.append({
                    'id': email_id_str,
                    'subject': subject,
                    'date': msg.get('Date'),
                    'body_preview': body[:200]
                })
                
                # Mark as processed
                state['processed_ids'].append(email_id_str)
        
        imap.close()
        save_state(state)
        
        return new_forwards
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    forwards = check_forwards()
    
    if forwards:
        print(f"📧 Found {len(forwards)} new forward(s) from Richard:\n")
        for fwd in forwards:
            print(f"Subject: {fwd['subject']}")
            print(f"Date: {fwd['date']}")
            print(f"Preview: {fwd['body_preview'][:100]}...")
            print()
    else:
        print("✅ No new forwards")
