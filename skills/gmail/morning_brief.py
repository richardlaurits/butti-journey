#!/usr/bin/env python3
"""
Morning Brief Generator - Daily 07:00 CET
Comprehensive daily briefing for Richard Laurits
"""

import imaplib
import email
import json
import os
from datetime import datetime, timedelta
from email.parser import HeaderParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, 'brief_state.json')

def check_important_emails():
    """Check Richard's Gmail for important unread emails"""
    try:
        with open(os.path.join(SCRIPT_DIR, 'richard_personal_app_password.txt'), 'r') as f:
            app_password = f.read().strip()
        
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('richardlaurits@gmail.com', app_password)
        mail.select('inbox')
        
        # Search for unread emails from last 24h
        date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        _, messages = mail.search(None, f'(UNSEEN SINCE {date})')
        
        important_emails = []
        
        for msg_num in messages[0].split()[:5]:  # Check first 5 unread
            _, msg_data = mail.fetch(msg_num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            subject = msg['subject'] or '(No Subject)'
            sender = msg['from'] or '(Unknown)'
            
            # Check if important
            is_important = False
            
            # From Pernilla
            if 'pernilla' in sender.lower():
                is_important = True
            
            # Calendar invites
            if 'calendar' in subject.lower() or 'invitation' in subject.lower():
                is_important = True
            
            # Bank/payment related
            bank_keywords = ['invoice', 'faktura', 'payment', 'betalning', 'nordea', 'seb', 'ubs']
            if any(kw in subject.lower() for kw in bank_keywords):
                is_important = True
            
            if is_important:
                important_emails.append(f"📧 {sender.split('<')[0].strip()}: {subject[:60]}")
        
        mail.logout()
        
        if important_emails:
            return "\n".join(important_emails[:3])  # Top 3
        return "✅ Inga viktiga olästa mejl"
        
    except Exception as e:
        return f"⚠️ Kunde inte läsa Gmail: {str(e)[:50]}"

def get_last_night_activity():
    """Check what happened during the night (6h cron runs)"""
    # Check FPL deadline log
    fpl_log = os.path.join(SCRIPT_DIR, '..', '..', 'agents', 'fpl-agent', 'deadline_cron.log')
    activities = []
    
    if os.path.exists(fpl_log):
        with open(fpl_log, 'r') as f:
            lines = f.readlines()
            recent = [l for l in lines if 'Triggering' in l]
            if recent:
                activities.append("🏆 FPL deadline check: Alert sent")
    
    if not activities:
        return "🌙 Lugn natt - inga kritiskt tidskänsliga händelser"
    
    return "\n".join(activities)

def get_today_plan():
    """What agents are scheduled today"""
    weekday = datetime.now().strftime('%A')
    plans = []
    
    # Check cron schedule
    plans.append("📋 Automatiska schemalagda uppgifter:")
    plans.append("  • Gmail monitor (var 30:e minut)")
    plans.append("  • FPL deadline-tracking (var 6:e timme)")
    
    if weekday == 'Friday':
        plans.append("  • 🏢 Career Agent kl 09:00 (veckans jobbscan)")
        plans.append("  • ⚽ Bundesliga Agent kl 10:00 (skador inför helgen)")
    
    return "\n".join(plans)

def generate_suggestions():
    """Generate 3 suggestions based on current context"""
    suggestions = [
        "🤖 Vill du att jag undersöker nya AI-verktyg eller uppdateringar inom ditt område?",
        "📊 Ska vi gå igenom din FPL-strategi inför nästa omgång?",
        "💼 Vill du att jag gör en extra jobbsökning utanför det schemalagda?",
        "🏃‍♂️ Vill du ha en uppdatering om dina hälsomål och framsteg?",
        "📰 Ska jag djupdyka i något specifikt ämne som intresserar dig?",
        "🔧 Vill du att jag optimerar eller förbättrar någon av dina automatiska agenter?",
        "📚 Ska jag sammanfatta en artikel eller rapport du inte hunnit läsa?",
        "💡 Vill du brainstorma idéer för ett nytt projekt eller intresseområde?"
    ]
    
    # Rotate based on day of month
    day = datetime.now().day
    start_idx = day % len(suggestions)
    
    selected = []
    for i in range(3):
        idx = (start_idx + i) % len(suggestions)
        selected.append(suggestions[idx])
    
    return "\n".join(selected)

if __name__ == '__main__':
    print("=== MORNING BRIEF DATA ===")
    print("\n📧 IMPORTANT EMAILS:")
    print(check_important_emails())
    print("\n🌙 LAST NIGHT:")
    print(get_last_night_activity())
    print("\n📅 TODAY'S PLAN:")
    print(get_today_plan())
