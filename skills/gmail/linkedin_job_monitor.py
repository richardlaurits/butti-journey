#!/usr/bin/env python3
"""
LinkedIn Job Monitor - Checks for LinkedIn job recommendation emails
Scans Richard's Gmail for LinkedIn job alerts and scores them
"""

import imaplib
import email
import json
import os
import re
from datetime import datetime, timedelta
from email.parser import HeaderParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, 'linkedin_state.json')
APP_PASSWORD_FILE = os.path.join(SCRIPT_DIR, 'richard_personal_app_password.txt')

# Richard's profile criteria (from career-agent config)
TARGET_ROLES = [
    'director', 'senior manager', 'vp', 'vice president', 'chief', 'head of',
    'business development', 'corporate development', 'product strategy',
    'go-to-market', 'commercial', 'strategic partnerships',
    'global marketing', 'emea marketing', 'general manager', 'managing director'
]

TARGET_INDUSTRIES = [
    'medical', 'medtech', 'healthcare', 'diabetes', 'device', 
    'biotech', 'pharma', 'life sciences'
]

TARGET_LOCATIONS = [
    'switzerland', 'zurich', 'geneva', 'basel', 'zug',
    'denmark', 'copenhagen', 'sweden', 'stockholm', 'gothenburg'
]

def score_job_match(subject, body_preview):
    """Score a job posting 0-10 based on Richard's criteria"""
    text = (subject + ' ' + body_preview).lower()
    score = 0
    
    # Role matching (0-4 points)
    role_matches = sum(1 for role in TARGET_ROLES if any(word in text for word in role.split()))
    score += min(4, role_matches * 2)
    
    # Industry matching (0-3 points)
    industry_matches = sum(1 for ind in TARGET_INDUSTRIES if ind in text)
    score += min(3, industry_matches * 1.5)
    
    # Location matching (0-3 points)
    location_matches = sum(1 for loc in TARGET_LOCATIONS if loc in text)
    score += min(3, location_matches * 1.5)
    
    return min(10, score)

def is_quiet_hours():
    """Check if it's quiet hours (22:00-07:00)"""
    now = datetime.now()
    hour = now.hour
    # Quiet hours: 22:00 - 07:00
    return hour >= 22 or hour < 7

def check_linkedin_jobs():
    """Check Gmail for LinkedIn job recommendation emails"""
    try:
        with open(APP_PASSWORD_FILE, 'r') as f:
            app_password = f.read().strip()
        
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('richardlaurits@gmail.com', app_password)
        mail.select('inbox')
        
        # Search for unread LinkedIn emails from last 24h
        date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        _, messages = mail.search(None, f'(UNSEEN FROM "linkedin.com" SINCE {date})')
        
        job_matches = []
        
        for msg_num in messages[0].split():
            _, msg_data = mail.fetch(msg_num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject = msg['subject'] or ''
            
            # Check if it's a job-related email
            job_keywords = ['job', 'position', 'role', 'hiring', 'opportunity', 'career']
            if any(kw in subject.lower() for kw in job_keywords):
                # Get body preview (first 500 chars)
                body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')[:500]
                            break
                
                score = score_job_match(subject, body)
                
                # Only alert for good matches (6+)
                if score >= 6:
                    job_matches.append({
                        'subject': subject[:100],
                        'score': score,
                        'preview': body[:200] if body else 'No preview'
                    })
        
        mail.logout()
        
        # Sort by score
        job_matches.sort(key=lambda x: x['score'], reverse=True)
        
        return job_matches[:3]  # Top 3
        
    except Exception as e:
        return f"Error: {str(e)[:50]}"

if __name__ == '__main__':
    jobs = check_linkedin_jobs()
    
    if isinstance(jobs, list) and jobs:
        print("🔗 LINKEDIN JOBS FOUND:")
        for job in jobs:
            print(f"\n📊 Score: {job['score']}/10")
            print(f"📧 {job['subject']}")
    elif isinstance(jobs, list) and not jobs:
        print("NO_LINKEDIN_JOBS")
    else:
        print(f"ERROR: {jobs}")
