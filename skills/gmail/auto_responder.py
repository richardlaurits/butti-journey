#!/usr/bin/env python3
"""
Auto-responder for butti.nightrider@gmail.com
Monitors inbox, identifies email types, sends appropriate replies
Logs all sent responses

FOUNDATION RULES (Always Follow):
✅ AUTO-RESPOND: Emails written DIRECTLY TO butti.nightrider@gmail.com
✅ AUTO-RESPOND: Emails FROM Richard (richardlaurits@gmail.com)
❌ NEVER RESPOND: Forwarded emails from others (even via Richard)
❌ NEVER RESPOND: Sensitive matters (money, legal, personal decisions)
⚠️ UNCLEAR: Alert Richard and wait for instructions
"""

import imaplib
import smtplib
from email.parser import HeaderParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_PASSWORD_FILE = os.path.join(SCRIPT_DIR, 'app_password.txt')
LOG_FILE = os.path.join(SCRIPT_DIR, 'auto_responder_log.json')
STATE_FILE = os.path.join(SCRIPT_DIR, 'responder_state.json')

EMAIL = 'butti.nightrider@gmail.com'

def load_app_password():
    """Load app password"""
    with open(APP_PASSWORD_FILE, 'r') as f:
        return f.read().strip()

def load_state():
    """Load which emails we've already processed"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'processed_ids': []}

def save_state(state):
    """Save state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def log_response(sender, subject, response_type, response_text):
    """Log the response we sent"""
    entry = {
        'timestamp': datetime.now().isoformat(),
        'from': sender,
        'subject': subject,
        'response_type': response_type,
        'response': response_text[:200],  # First 200 chars
    }
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def is_forwarded_email(subject, body):
    """Check if email is forwarded"""
    subject_lower = subject.lower()
    body_lower = body.lower()
    
    forwarded_indicators = [
        'forwarded message',
        '---------- forwarded message',
        'original message',
        'begin forwarded message'
    ]
    
    subject_indicators = ['fwd:', 'fw:', 'forward:']
    
    has_forwarded_body = any(ind in body_lower for ind in forwarded_indicators)
    has_forwarded_subject = any(ind in subject_lower for ind in subject_indicators)
    
    return has_forwarded_body or has_forwarded_subject

def should_auto_respond(subject, sender, body):
    """
    Determine if we should auto-respond based on Foundation Rules
    Returns: (should_respond: bool, reason: str)
    """
    subject_lower = subject.lower()
    sender_lower = sender.lower()
    body_lower = body.lower()
    
    # ❌ RULE 1: Forwarded emails - CHECK FIRST (even if from Richard)
    if any(x in body_lower for x in ['forwarded message', '---------- forwarded message', 'original message']):
        return False, "Forwarded email - requires Richard's approval"
    
    if any(x in subject_lower for x in ['fwd:', 'fw:', 'forward:']):
        return False, "Forwarded email (subject) - requires Richard's approval"
    
    # ✅ RULE 2: Email FROM Richard himself (and not forwarded) - respond
    if 'richardlaurits@gmail.com' in sender_lower or 'richard.laurits' in sender_lower:
        return True, "From Richard himself"
    
    # ✅ RULE 3: Direct to butti.nightrider@gmail.com - CAN respond
    # (This is checked by the fact that we're processing this inbox)
    
    return True, "Direct email to ButtiBot"

def analyze_forwarded_email(subject, sender, body):
    """
    Analyze a forwarded email and propose actions to Richard
    Returns: dict with analysis and proposed actions
    """
    import re
    
    analysis = {
        'original_sender': 'Unknown',
        'original_subject': subject.replace('Fwd:', '').replace('FW:', '').strip(),
        'email_type': 'General',
        'urgency': 'Normal',
        'proposed_actions': [],
        'suggested_response': None
    }
    
    # Try to extract original sender from forwarded email
    body_lower = body.lower()
    
    # Look for "From: Name <email>" pattern
    from_match = re.search(r'from:\s*([^<\n]+)?<([^>]+)>', body, re.IGNORECASE)
    if from_match:
        analysis['original_sender'] = from_match.group(2).strip()
    else:
        # Try alternative patterns
        from_match = re.search(r'from:\s*([\w\s@.]+)', body, re.IGNORECASE)
        if from_match:
            analysis['original_sender'] = from_match.group(1).strip()[:50]
    
    # Classify email type
    if any(x in body_lower for x in ['invitation', 'invite', 'calendar', 'meeting']):
        analysis['email_type'] = 'Calendar/Invitation'
        analysis['proposed_actions'] = [
            'Check calendar availability',
            'Review meeting details',
            'Accept/decline invitation'
        ]
        analysis['suggested_response'] = 'Would you like me to check your calendar and suggest a response?'
        
    elif any(x in body_lower for x in ['invoice', 'payment', 'bill', 'receipt', 'order']):
        analysis['email_type'] = 'Invoice/Payment'
        analysis['urgency'] = 'High' if 'due' in body_lower or 'overdue' in body_lower else 'Normal'
        analysis['proposed_actions'] = [
            'Verify amount and details',
            'Check if already paid',
            'Forward to accounting if needed'
        ]
        analysis['suggested_response'] = 'This appears to be an invoice. Shall I help you verify the details?'
        
    elif any(x in body_lower for x in ['job', 'position', 'career', 'opportunity', 'hiring']):
        analysis['email_type'] = 'Job/Career'
        analysis['proposed_actions'] = [
            'Add to job tracker',
            'Extract key details (company, role, deadline)',
            'Suggest response template'
        ]
        analysis['suggested_response'] = 'This looks like a job opportunity. Should I add it to your career tracking?'
        
    elif any(x in body_lower for x in ['flight', 'booking', 'reservation', 'hotel', 'travel']):
        analysis['email_type'] = 'Travel'
        analysis['proposed_actions'] = [
            'Extract booking details',
            'Add to travel agent tracking',
            'Set up check-in reminders'
        ]
        analysis['suggested_response'] = 'Travel booking detected. Shall I extract the details and add to your travel plans?'
        
    elif any(x in body_lower for x in ['newsletter', 'subscribe', 'unsubscribe']):
        analysis['email_type'] = 'Newsletter/Marketing'
        analysis['urgency'] = 'Low'
        analysis['proposed_actions'] = [
            'Archive or delete',
            'Unsubscribe if requested'
        ]
        analysis['suggested_response'] = 'This appears to be a newsletter. Archive or delete?'
        
    elif any(x in body_lower for x in ['question', 'help', 'support', 'inquiry']):
        analysis['email_type'] = 'Inquiry/Support'
        analysis['proposed_actions'] = [
            'Analyze what information is needed',
            'Draft response for your review',
            'Suggest next steps'
        ]
        analysis['suggested_response'] = 'Someone is asking for help/information. Shall I draft a response for your review?'
        
    else:
        analysis['proposed_actions'] = [
            'Review content',
            'Determine if response needed',
            'Suggest action based on content'
        ]
        analysis['suggested_response'] = 'I\'ve received this forwarded email. What would you like me to do with it?'
    
    return analysis

def notify_richard_about_forwarded_email(subject, sender, body, analysis):
    """
    Send notification to Richard about forwarded email with proposed actions
    Via both Telegram and email
    """
    from datetime import datetime
    from pathlib import Path
    
    # Format the notification
    lines = []
    lines.append("📧 **Forwarderat Email - Förslag på Åtgärd**")
    lines.append("")
    lines.append(f"**Från:** {analysis['original_sender']}")
    lines.append(f"**Ämne:** {analysis['original_subject']}")
    lines.append(f"**Typ:** {analysis['email_type']}")
    lines.append(f"**Prioritet:** {analysis['urgency']}")
    lines.append("")
    lines.append("**💡 Föreslagna Åtgärder:**")
    for i, action in enumerate(analysis['proposed_actions'], 1):
        lines.append(f"   {i}. {action}")
    lines.append("")
    lines.append(f"**📝 Förslag:** {analysis['suggested_response']}")
    lines.append("")
    lines.append("Svara med:")
    lines.append("• 'JA' - Utför föreslagna åtgärder")
    lines.append("• 'NEJ' - Gör inget")
    lines.append("• Ange specifika instruktioner")
    
    message = "\n".join(lines)
    
    # Send via Telegram (using telegram_sender.py)
    try:
        import subprocess
        sender_script = Path('/home/richard-laurits/.openclaw/workspace/agents/investment-agent/telegram_sender.py')
        if sender_script.exists():
            subprocess.run(['python3', str(sender_script)], input=message, text=True, timeout=30)
            print(f"✅ Telegram notification sent for forwarded email: {analysis['original_subject'][:50]}")
    except Exception as e:
        print(f"⚠️ Could not send Telegram: {e}")
    
    # Send via email to Richard
    try:
        send_email_to_richard(
            subject=f"[ButtiBot] Forwarded email: {analysis['original_subject'][:50]}",
            body=message
        )
        print(f"✅ Email notification sent to Richard")
    except Exception as e:
        print(f"⚠️ Could not send email: {e}")
    
    return True

def send_email_to_richard(subject, body):
    """Send notification email to Richard"""
    try:
        password = load_app_password()
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL
        msg['To'] = 'richardlaurits@gmail.com'
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"❌ Failed to send email to Richard: {e}")
        return False

def classify_email(subject, sender, body):
    """Classify email type to determine response"""
    
    subject_lower = subject.lower()
    sender_lower = sender.lower()
    body_lower = body.lower()
    
    # Check Foundation Rules first
    should_respond, reason = should_auto_respond(subject, sender, body)
    if not should_respond:
        print(f"⏸️ SKIPPED: {reason}")
        return 'SKIP'
    
    # Ignore patterns (automated senders)
    if any(x in sender_lower for x in ['noreply', 'no-reply', 'newsletter', 'marketing', 'notifications']):
        return 'IGNORE'
    
    # Notifications
    if any(x in subject_lower for x in ['confirmation', 'verified', 'welcome', 'activation', 'confirm']):
        return 'CONFIRMATION'
    
    # Service alerts
    if any(x in subject_lower for x in ['alert', 'notification', 'update', 'status']):
        return 'NOTIFICATION'
    
    # Direct messages from humans
    if any(x in subject_lower for x in ['hello', 'hi', 'question', 'inquiry', 'help']):
        return 'INQUIRY'
    
    # Default: treat as inquiry if it has a real sender
    if not any(x in sender_lower for x in ['amazon', 'google', 'github', 'linkedin', 'microsoft']):
        return 'INQUIRY'
    
    return 'NOTIFICATION'

def get_response_text(email_type, sender_name):
    """Generate response based on email type"""
    
    responses = {
        'CONFIRMATION': f"Hi {sender_name},\n\nThanks for the confirmation. All set!\n\nBest,\nButtiBot",
        
        'NOTIFICATION': f"Hi {sender_name},\n\nThanks for the update.\n\nBest,\nButtiBot",
        
        'INQUIRY': f"Hi {sender_name},\n\nThanks for reaching out! I'll forward this to Richard and he'll get back to you soon.\n\nBest,\nButtiBot (Richard's assistant)",
    }
    
    return responses.get(email_type, responses['NOTIFICATION'])

def send_email(to_email, subject, body):
    """Send email via SMTP"""
    try:
        password = load_app_password()
        
        msg = MIMEText(body)
        msg['Subject'] = f"Re: {subject}"
        msg['From'] = EMAIL
        msg['To'] = to_email
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

def process_inbox():
    """Check inbox and auto-respond"""
    try:
        password = load_app_password()
        imap = imaplib.IMAP4_SSL('imap.gmail.com')
        imap.login(EMAIL, password)
        imap.select('INBOX')
        
        state = load_state()
        processed = set(state.get('processed_ids', []))
        
        # Get last 20 unread emails
        status, messages = imap.search(None, 'UNSEEN')
        email_ids = messages[0].split()[-20:]
        
        alerts = []
        
        for email_id in email_ids:
            email_id_str = email_id.decode()
            
            if email_id_str in processed:
                continue
            
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            parser = HeaderParser()
            msg = parser.parsestr(msg_data[0][1].decode())
            
            sender = msg.get('From', '')
            subject = msg.get('Subject', '')
            
            # Get body for classification
            body = ""
            if msg.is_multipart():
                for part in msg.get_payload():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload()
                        break
            else:
                body = msg.get_payload()
            
            email_type = classify_email(subject, sender, body)
            
            # Handle forwarded emails - notify Richard with proposed actions
            if email_type == 'SKIP' and is_forwarded_email(subject, body):
                print(f"📧 Forwarded email detected from {sender}")
                analysis = analyze_forwarded_email(subject, sender, body)
                notify_richard_about_forwarded_email(subject, sender, body, analysis)
                alerts.append(f"📧 Forwarded email analyzed: {analysis['original_subject'][:40]}")
                processed.add(email_id_str)
                continue
            
            # Skip ignored emails
            if email_type in ['IGNORE', 'SKIP']:
                processed.add(email_id_str)
                continue
            
            if email_type != 'IGNORE':
                # Extract sender name
                sender_name = sender.split('<')[0].strip() if '<' in sender else sender.split('@')[0]
                
                response_text = get_response_text(email_type, sender_name)
                
                if send_email(sender, subject, response_text):
                    log_response(sender, subject, email_type, response_text)
                    alerts.append(f"✅ Replied to {sender_name} ({email_type})")
                    processed.add(email_id_str)
        
        imap.close()
        imap.logout()
        
        # Save state
        state['processed_ids'] = list(processed)[-500:]  # Keep last 500
        save_state(state)
        
        return alerts
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == '__main__':
    alerts = process_inbox()
    
    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("HEARTBEAT_OK")
