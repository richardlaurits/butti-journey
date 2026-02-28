#!/usr/bin/env python3
"""
Career Agent - Interactive Job Email with Clickable Buttons
Uses mailto links for automatic replies + tracking
"""

import sys
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

import imaplib
import email
from datetime import datetime, timedelta
import re
import json
from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict:
                self.links.append({'url': attrs_dict['href'], 'text': ''})
    def handle_data(self, data):
        if self.links:
            self.links[-1]['text'] += data.strip()

def extract_links(html_content):
    parser = LinkExtractor()
    try:
        parser.feed(html_content)
    except:
        pass
    return parser.links

def extract_job_title_from_subject(subject):
    """Extract clean job title from email subject"""
    # Clean up UTF-8 encoding artifacts
    title = subject
    
    # Remove common prefixes
    prefixes = [
        '=?UTF-8?Q?',
        '=?utf-8?Q?',
        '"',
        'New job:',
        'Job alert:',
    ]
    
    for prefix in prefixes:
        title = title.replace(prefix, '')
    
    # Remove everything after common separators
    separators = [' - ', ' at ', ' @ ', ' | ', ' (', ' -"', '" -']
    for sep in separators:
        if sep in title:
            title = title.split(sep)[0]
    
    # Remove any remaining special characters
    title = title.strip('"=: ')
    
    return title[:80] if title else 'Job Position'

def load_applied_jobs():
    """Load list of already applied jobs"""
    try:
        with open('/home/richard-laurits/.openclaw/workspace/agents/career-agent/applied_jobs.json', 'r') as f:
            data = json.load(f)
            return data.get('jobs', [])
    except:
        return []

def load_skipped_jobs():
    """Load list of skipped jobs"""
    try:
        with open('/home/richard-laurits/.openclaw/workspace/agents/career-agent/skipped_jobs.json', 'r') as f:
            data = json.load(f)
            return data.get('jobs', [])
    except:
        return []

def is_job_processed(job_id, applied_jobs, skipped_jobs):
    """Check if job has already been processed"""
    for job in applied_jobs:
        if job.get('id') == job_id:
            return 'applied'
    for job in skipped_jobs:
        if job.get('id') == job_id:
            return 'skipped'
    return None

def calculate_rating(subject, body, company, location):
    """Calculate relevance 1-10"""
    score = 5
    text = (subject + ' ' + body).lower()
    
    # Role scoring
    if 'marketing director' in text or 'director of marketing' in text:
        score += 3
    elif 'commercial director' in text or 'business development director' in text:
        score += 3
    elif 'strategy director' in text:
        score += 2.5
    elif 'marketing manager' in text:
        score += 1.5
    elif 'head of marketing' in text or 'head of commercial' in text:
        score += 2.5
    
    # Industry
    if any(x in text for x in ['medical device', 'medtech', 'pharma', 'healthcare']):
        score += 2
    
    # Company
    target_companies = ['novo nordisk', 'roche', 'iqvia', 'medtronic', 'sophia genetics']
    if any(comp in text for comp in target_companies):
        score += 2
    
    # Location
    if 'switzerland' in text:
        score += 2
    elif 'denmark' in text or 'copenhagen' in text:
        score += 1.5
    elif 'sweden' in text or 'stockholm' in text:
        score += 1
    
    # Negative
    if 'intern' in text or 'junior' in text or 'entry level' in text:
        score -= 3
    
    return max(1, min(10, int(score)))

def extract_job_details(subject, body, html_body):
    """Extract detailed job information"""
    details = {
        'title': extract_job_title_from_subject(subject),
        'company': '',
        'location': '',
        'description': '',
        'link': '',
        'salary': ''
    }
    
    # Extract company
    full_text = subject + ' ' + body
    
    # Look for company patterns
    if ' at ' in full_text:
        parts = full_text.split(' at ')
        if len(parts) > 1:
            company_part = parts[1].split(' - ')[0].split(' | ')[0]
            details['company'] = company_part.strip()[:50]
    
    # Extract location
    location_patterns = [
        r'\b(Geneva|Zurich|Basel|Copenhagen|Stockholm|Gothenburg|Malmö)\b',
        r'\b(Switzerland|Denmark|Sweden)\b',
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            details['location'] = match.group(1).strip()
            break
    
    # Extract description
    if body:
        desc = re.sub(r'\s+', ' ', body).strip()
        details['description'] = desc[:300] if len(desc) > 300 else desc
    
    # Extract link from HTML
    if html_body:
        links = extract_links(html_body)
        for link in links:
            url = link['url']
            if 'linkedin.com/jobs' in url and ('/view/' in url or 'keywords=' in url):
                details['link'] = url
                break
            elif 'indeed.com' in url and 'job' in url:
                details['link'] = url
                break
    
    return details

def parse_job_emails():
    """Parse all job emails from last 48 hours"""
    
    EMAIL = 'richardlaurits@gmail.com'
    
    with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/richard_personal_app_password.txt', 'r') as f:
        PASSWORD = f.read().strip()
    
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(EMAIL, PASSWORD)
    imap.select('INBOX')
    
    # Last 48 hours
    since_date = (datetime.now() - timedelta(days=2)).strftime('%d-%b-%Y')
    
    search_queries = [
        f'FROM "jobs@linkedin.com" SINCE {since_date}',
        f'FROM "jobalerts-noreply@linkedin.com" SINCE {since_date}',
        f'FROM "indeed.com" SINCE {since_date}',
        f'SUBJECT "career" SINCE {since_date}',
        f'SUBJECT "job alert" SINCE {since_date}'
    ]
    
    all_jobs = []
    applied_jobs = load_applied_jobs()
    skipped_jobs = load_skipped_jobs()
    
    for query in search_queries:
        try:
            status, messages = imap.search(None, query)
            email_ids = messages[0].split()
            
            for email_id in email_ids[-20:]:
                try:
                    status, msg_data = imap.fetch(email_id, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    subject = msg.get('Subject', '')
                    job_id = f"{subject}_{msg.get('Date', '')}"
                    
                    # Skip if already processed
                    status = is_job_processed(job_id, applied_jobs, skipped_jobs)
                    if status:
                        continue
                    
                    # Extract bodies
                    body_text = ''
                    body_html = ''
                    
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == 'text/plain':
                                try:
                                    body_text = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                except:
                                    pass
                            elif content_type == 'text/html':
                                try:
                                    body_html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                except:
                                    pass
                    else:
                        try:
                            payload = msg.get_payload(decode=True)
                            if payload:
                                body_text = payload.decode('utf-8', errors='ignore')
                        except:
                            pass
                    
                    details = extract_job_details(subject, body_text, body_html)
                    rating = calculate_rating(subject, body_text, details['company'], details['location'])
                    
                    if rating >= 6:
                        all_jobs.append({
                            'id': job_id,
                            'subject': subject,
                            'clean_title': details['title'],
                            'source': 'LinkedIn' if 'linkedin' in query else 'Indeed' if 'indeed' in query else 'Other',
                            'company': details['company'],
                            'location': details['location'],
                            'description': details['description'],
                            'link': details['link'],
                            'rating': rating,
                            'date': msg.get('Date', ''),
                            'added_date': datetime.now().isoformat()
                        })
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            continue
    
    imap.close()
    imap.logout()
    
    # Remove duplicates and sort
    seen = set()
    unique_jobs = []
    for job in sorted(all_jobs, key=lambda x: x['rating'], reverse=True):
        key = job['clean_title'][:50]
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    return unique_jobs[:10]

def generate_interactive_email(jobs):
    """Generate interactive HTML email with buttons"""
    
    # Create mailto links for each job
    sender_email = "butti.nightrider@gmail.com"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 0 0 20px 20px; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .instructions {{ background: #e8f4f8; padding: 20px; margin: 20px; border-radius: 10px; border-left: 4px solid #667eea; }}
        .job {{ border: 1px solid #e0e0e0; margin: 20px; padding: 25px; border-radius: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .job-header {{ margin-bottom: 15px; }}
        .rating {{ display: inline-block; background: linear-gradient(135deg, #ffd700, #ffed4e); color: #333; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }}
        .title {{ font-size: 22px; font-weight: bold; color: #2c3e50; margin: 10px 0 5px 0; }}
        .company {{ font-size: 16px; color: #667eea; font-weight: 600; margin: 5px 0; }}
        .location {{ font-size: 14px; color: #666; margin: 5px 0; }}
        .description {{ margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; font-size: 14px; color: #555; }}
        .actions {{ margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap; }}
        .btn {{ padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: 600; font-size: 14px; text-align: center; display: inline-block; border: none; cursor: pointer; }}
        .btn-apply {{ background: #667eea; color: white; }}
        .btn-applied {{ background: #28a745; color: white; }}
        .btn-skip {{ background: #6c757d; color: white; }}
        .footer {{ margin-top: 30px; padding: 20px; background: #f0f0f0; text-align: center; font-size: 12px; color: #666; border-radius: 10px; margin: 20px; }}
        .btn:hover {{ opacity: 0.9; transform: translateY(-1px); }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💼 Dagliga Jobbmöjligheter</h1>
        <p>{datetime.now().strftime('%A %d %B %Y')}</p>
        <p>Top {len(jobs)} jobb för dig</p>
    </div>
    
    <div class="instructions">
        <strong>📧 Så här fungerar det:</strong><br>
        • <strong>"Jag har sökt"</strong> - Klicka för att markera som sökt (försvinner från framtida listor)<br>
        • <strong>"Passar inte"</strong> - Klicka för att skippa (försvinner från framtida listor)<br>
        • <strong>"Ansök nu"</strong> - Går till jobbannonsen<br>
        Du kan också svara på detta mail med: <strong>"SÖKT: #[nummer]"</strong> eller <strong>"SKIPPA: #[nummer]"</strong>
    </div>
"""
    
    for i, job in enumerate(jobs, 1):
        stars = '⭐' * (job['rating'] // 2)
        
        # Clean up description
        desc = job['description'][:250] if job['description'] else 'Se länk för fullständig beskrivning'
        desc = desc.replace('<', '&lt;').replace('>', '&gt;')
        
        # Location
        location = job['location'] if job['location'] else 'Plats ej angiven'
        
        # Company
        company = job['company'] if job['company'] else 'Företag ej angivet'
        
        # Create mailto links for buttons
        applied_subject = f"RE: Job Applied - #{i}"
        applied_body = f"Jag har sökt jobb #{i}:\\n{job['clean_title']}\\n\\nID: {job['id'][:50]}"
        applied_mailto = f"mailto:{sender_email}?subject={applied_subject}&body={applied_body}"
        
        skip_subject = f"RE: Job Skipped - #{i}"
        skip_body = f"Jag skippar jobb #{i}:\\n{job['clean_title']}\\n\\nID: {job['id'][:50]}"
        skip_mailto = f"mailto:{sender_email}?subject={skip_subject}&body={skip_body}"
        
        html += f"""
    <div class="job">
        <div class="job-header">
            <span class="rating">{stars} {job['rating']}/10</span>
            <div class="title">#{i}: {job['clean_title']}</div>
            <div class="company">🏢 {company}</div>
            <div class="location">📍 {location}</div>
            <div style="margin-top: 5px; font-size: 12px; color: #999;">Källa: {job['source']}</div>
        </div>
        
        <div class="description">
            {desc}...
        </div>
        
        <div class="actions">
            <a href="{applied_mailto}" class="btn btn-applied">✅ Jag har sökt</a>
            <a href="{skip_mailto}" class="btn btn-skip">❌ Passar inte</a>
            {f'<a href="{job["link"]}" class="btn btn-apply" target="_blank">🔗 Ansök nu</a>' if job["link"] else ''}
        </div>
    </div>
"""
    
    html += f"""
    <div class="footer">
        <p>Detta mail skickades automatiskt av din Career Agent 🤖</p>
        <p>{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p>För att sluta få dessa mail, kontakta Richard</p>
    </div>
</body>
</html>
"""
    
    return html

def send_email(to_email, subject, html_content):
    """Send email using Gmail SMTP"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    try:
        with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/app_password.txt', 'r') as f:
            sender_password = f.read().strip()
        
        sender_email = 'butti.nightrider@gmail.com'
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def main():
    """Main function"""
    print("=" * 80)
    print("📧 INTERAKTIVT JOBBMAIL - Med knappar")
    print("=" * 80)
    print()
    
    # Parse jobs
    print("🔍 Söker efter jobb...")
    jobs = parse_job_emails()
    
    if not jobs:
        print("⚠️  Inga nya relevanta jobb hittades idag")
        print("Skickar inget mail (spammar inte när det är tomt)")
        return
    
    print(f"✅ Hittade {len(jobs)} relevanta jobb")
    
    # Generate interactive email
    print("📄 Genererar interaktivt HTML-email med knappar...")
    email_content = generate_interactive_email(jobs)
    
    # Save to file
    with open('/tmp/interactive_jobs_email.html', 'w', encoding='utf-8') as f:
        f.write(email_content)
    
    print("💾 Sparade preview till: /tmp/interactive_jobs_email.html")
    
    # Send email
    print("📨 Skickar email till richardlaurits@gmail.com...")
    subject = f"💼 Dagliga Jobbmöjligheter - {datetime.now().strftime('%A %d %b')} - {len(jobs)} jobb"
    
    if send_email('richardlaurits@gmail.com', subject, email_content):
        print("✅ Interaktivt email skickat!")
    else:
        print("❌ Kunde inte skicka email")
    
    # Telegram summary
    telegram_msg = f"""💼 Dagliga Jobbmöjligheter - {datetime.now().strftime('%A %d %b')}

Hittade {len(jobs)} relevanta jobb med interaktiva knappar:

"""
    for i, job in enumerate(jobs[:5], 1):
        telegram_msg += f"{i}. {job['clean_title'][:50]}... ({job['rating']}/10)\n"
    
    telegram_msg += f"\n📧 Interaktivt mail skickat med 'SÖKT' och 'SKIPPA' knappar!"
    
    with open('/tmp/telegram_interactive_career.txt', 'w') as f:
        f.write(telegram_msg)
    
    print(telegram_msg)
    
    # Save jobs
    with open('/tmp/todays_interactive_jobs.json', 'w') as f:
        json.dump(jobs, f, indent=2)
    
    print()
    print("=" * 80)
    print("✅ KLART! Interaktivt jobbmail skickat")
    print("=" * 80)

if __name__ == "__main__":
    main()
