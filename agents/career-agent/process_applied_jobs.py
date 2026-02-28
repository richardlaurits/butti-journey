#!/usr/bin/env python3
"""
Career Agent - Process Applied Jobs
Marks jobs as applied when Richard replies to the daily email
Run this manually or via cron to check for replies
"""

import imaplib
import email
import json
import re
from datetime import datetime

def load_applied_jobs():
    """Load current applied jobs database"""
    try:
        with open('/home/richard-laurits/.openclaw/workspace/agents/career-agent/applied_jobs.json', 'r') as f:
            return json.load(f)
    except:
        return {"version": "1.0", "jobs": []}

def save_applied_jobs(data):
    """Save applied jobs database"""
    with open('/home/richard-laurits/.openclaw/workspace/agents/career-agent/applied_jobs.json', 'w') as f:
        json.dump(data, f, indent=2)

def check_for_applied_replies():
    """Check Gmail for replies marking jobs as applied"""
    
    EMAIL = 'richardlaurits@gmail.com'
    
    with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/richard_personal_app_password.txt', 'r') as f:
        PASSWORD = f.read().strip()
    
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(EMAIL, PASSWORD)
    imap.select('INBOX')
    
    # Search for replies to our job emails
    # Look for subject containing "Re:" and sent to butti.nightrider@gmail.com
    status, messages = imap.search(None, 'SUBJECT "Re: 💼 Dagliga Jobbmöjligheter" UNSEEN')
    email_ids = messages[0].split()
    
    data = load_applied_jobs()
    new_applications = []
    
    for email_id in email_ids:
        try:
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Extract body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        try:
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                        except:
                            pass
            else:
                try:
                    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass
            
            # Look for "SÖKT: #X" or "APPLIED: #X" patterns
            patterns = [
                r'[Ss][Öö]KT[:\s#]+(\d+)',
                r'APPLIED[:\s#]+(\d+)',
                r'applied[:\s#]+(\d+)',
                r'sökt[:\s#]+(\d+)',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, body)
                for match in matches:
                    job_number = int(match)
                    
                    # Extract job info from the email body (look for the job details)
                    job_title = extract_job_title_from_body(body, job_number)
                    company = extract_company_from_body(body, job_number)
                    
                    application = {
                        "id": f"job_{datetime.now().strftime('%Y%m%d')}_{job_number}",
                        "job_number": job_number,
                        "title": job_title or f"Job #{job_number}",
                        "company": company or "Unknown",
                        "applied_date": datetime.now().isoformat(),
                        "source": "Daily Jobs Email",
                        "method": "Email reply"
                    }
                    
                    # Check if already exists
                    if not any(j.get('job_number') == job_number and 
                              j.get('applied_date', '').startswith(datetime.now().strftime('%Y-%m-%d')) 
                              for j in data['jobs']):
                        data['jobs'].append(application)
                        new_applications.append(application)
            
            # Mark email as read
            imap.store(email_id, '+FLAGS', '\\Seen')
            
        except Exception as e:
            print(f"Error processing email: {e}")
            continue
    
    imap.close()
    imap.logout()
    
    # Save updated database
    if new_applications:
        save_applied_jobs(data)
    
    return new_applications

def extract_job_title_from_body(body, job_number):
    """Extract job title from email body"""
    # Look for pattern like "#1: Job Title" or similar
    patterns = [
        rf'#{job_number}[:\s]+(.+?)(?:\n|$)',
        rf'{job_number}\.\s+(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, body, re.MULTILINE)
        if match:
            return match.group(1).strip()[:100]
    
    return None

def extract_company_from_body(body, job_number):
    """Extract company from email body"""
    # Look for company pattern near the job number
    patterns = [
        rf'#{job_number}[:\s]+.+?(?:🏢|Company:|at)\s+(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, body, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1).strip()[:50]
    
    return None

def manually_mark_applied(job_info):
    """Manually mark a job as applied"""
    data = load_applied_jobs()
    
    application = {
        "id": f"manual_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "title": job_info.get('title', 'Unknown'),
        "company": job_info.get('company', 'Unknown'),
        "location": job_info.get('location', ''),
        "applied_date": datetime.now().isoformat(),
        "source": "Manual entry",
        "notes": job_info.get('notes', '')
    }
    
    data['jobs'].append(application)
    save_applied_jobs(data)
    
    print(f"✅ Markerade '{application['title']}' hos {application['company']} som sökt")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        # Check for email replies
        print("=" * 80)
        print("🔍 Söker efter 'sökt'-svar i email...")
        print("=" * 80)
        
        new_apps = check_for_applied_replies()
        
        if new_apps:
            print(f"\n✅ Hittade {len(new_apps)} nya sökta jobb:")
            for app in new_apps:
                print(f"  • #{app['job_number']}: {app['title']} ({app['company']})")
        else:
            print("\n⚠️  Inga nya 'sökt'-svar hittades")
            
    elif len(sys.argv) > 1 and sys.argv[1] == 'add':
        # Manual add
        if len(sys.argv) < 4:
            print("Användning: python3 process_applied_jobs.py add 'Jobbtitel' 'Företag'")
            return
        
        job_info = {
            'title': sys.argv[2],
            'company': sys.argv[3],
            'notes': ' '.join(sys.argv[4:]) if len(sys.argv) > 4 else ''
        }
        manually_mark_applied(job_info)
        
    else:
        print("=" * 80)
        print("📋 Career Agent - Sökta Jobb")
        print("=" * 80)
        print()
        print("Kommandon:")
        print("  python3 process_applied_jobs.py check    # Sök efter svar i email")
        print("  python3 process_applied_jobs.py add 'Titel' 'Företag' [anteckningar]")
        print()
        
        # Show current status
        data = load_applied_jobs()
        print(f"📊 Totalt antal sökta jobb: {len(data.get('jobs', []))}")
        
        # Show last 5
        recent_jobs = sorted(data.get('jobs', []), 
                           key=lambda x: x.get('applied_date', ''), 
                           reverse=True)[:5]
        
        if recent_jobs:
            print("\nSenaste 5 sökta jobben:")
            for job in recent_jobs:
                date = job.get('applied_date', '')[:10]
                print(f"  • {date}: {job.get('title', 'Unknown')} @ {job.get('company', 'Unknown')}")

if __name__ == "__main__":
    main()
