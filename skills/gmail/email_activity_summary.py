#!/usr/bin/env python3
"""
Email Activity Summary for Morning Brief
Summarizes emails received and sent in the last 24h
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

LOG_DIR = Path('/home/richard-laurits/.openclaw/workspace/skills/gmail')

def get_last_24h_emails():
    """Get email activity from last 24 hours"""
    
    # Load auto-responder log
    responder_log = LOG_DIR / 'auto_responder_log.json'
    received = []
    sent = []
    
    if responder_log.exists():
        with open(responder_log, 'r') as f:
            logs = json.load(f)
        
        cutoff = datetime.now() - timedelta(hours=24)
        
        for entry in logs:
            entry_time = datetime.fromisoformat(entry.get('timestamp', '2000-01-01'))
            if entry_time > cutoff:
                sent.append({
                    'to': entry.get('from', 'Unknown'),
                    'subject': entry.get('subject', 'No subject'),
                    'type': entry.get('response_type', 'Unknown'),
                    'time': entry_time.strftime('%H:%M')
                })
    
    # Check for received emails (from gmail monitor state)
    monitor_log = LOG_DIR / 'monitor_state.json'
    if monitor_log.exists():
        with open(monitor_log, 'r') as f:
            state = json.load(f)
        
        # Count emails checked in last 24h
        last_check = state.get('last_check')
        if last_check:
            last_check_time = datetime.fromisoformat(last_check)
            if datetime.now() - last_check_time < timedelta(hours=24):
                # Add recent emails from state if available
                pass  # Currently not storing received emails, only processed
    
    return received, sent

def format_summary():
    """Format email activity summary"""
    received, sent = get_last_24h_emails()
    
    lines = []
    lines.append("📧 **EMAIL-AKTIVITET (24h)**")
    lines.append("")
    
    if not sent:
        lines.append("📤 Skickat: Inga auto-svar igår")
    else:
        lines.append(f"📤 Skickat: {len(sent)} auto-svar")
        for email in sent[-3:]:  # Show last 3
            sender = email['to'].split('<')[0].strip()[:25]
            lines.append(f"   • Till {sender} ({email['type']})")
    
    lines.append("")
    lines.append("📥 Mottagna: Kontrolleras via Gmail-monitor")
    lines.append("   (Viktiga mejl listas ovan under 📧 VIKTIGA EMAIL)")
    
    return "\n".join(lines)

if __name__ == '__main__':
    print(format_summary())
