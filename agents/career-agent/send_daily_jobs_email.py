#!/usr/bin/env python3
"""
Career Agent - Daily Job Email
Sends top 10 jobs to Richard every morning with full details
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

def load_applied_jobs():
    """Load list of already applied jobs"""
    try:
        with open('/home/richard-laurits/.openclaw/workspace/agents/career-agent/applied_jobs.json', 'r') as f:
            data = json.load(f)
            return data.get('jobs', [])
    except:
        return []

def is_job_applied(job_id, applied_jobs):
    """Check if job has already been applied"""
    for job in applied_jobs:
        if job.get('id') == job_id or job.get('subject') == job_id:
            return True
    return False

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
        'title': subject,
        'company': '',
        'location': '',
        'description': '',
        'link': '',
        'salary': ''
    }
    
    # Extract company
    company_patterns = [
        r'(?:at|@)\s+([A-Z][A-Za-z\s]+?)(?:\s+-|\s+\(|\s+in\s|$)',
        r'^([A-Z][A-Za-z\s]+?)\s+-',
    ]
    
    full_text = subject + ' ' + body
    
    for pattern in company_patterns:
        match = re.search(pattern, full_text)
        if match:
            details['company'] = match.group(1).strip()
            break
    
    # Extract location
    location_patterns = [
        r'\b(Geneva|Zurich|Basel|Copenhagen|Stockholm|Gothenburg|Malmö)\b',
        r'\b(Switzerland|Denmark|Sweden)\b',
        r'\bin\s+([A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+)?)\b'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            details['location'] = match.group(1).strip()
            break
    
    # Extract description (first 200 chars of body)
    if body:
        # Clean up text
        desc = re.sub(r'\s+', ' ', body).strip()
        details['description'] = desc[:300] if len(desc) > 300 else desc
    
    # Extract link from HTML
    if html_body:
        links = extract_links(html_body)
        for link in links:
            url = link['url']
            # Look for direct job links
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
    
    # Search various job sources
    search_queries = [
        f'FROM "jobs@linkedin.com" SINCE {since_date}',
        f'FROM "jobalerts-noreply@linkedin.com" SINCE {since_date}',
        f'FROM "indeed.com" SINCE {since_date}',
        f'SUBJECT "career" SINCE {since_date}',
        f'SUBJECT "job alert" SINCE {since_date}'
    ]
    
    all_jobs = []
    applied_jobs = load_applied_jobs()
    
    for query in search_queries:
        try:
            status, messages = imap.search(None, query)
            email_ids = messages[0].split()
            
            for email_id in email_ids[-20:]:  # Last 20 per category
                try:
                    status, msg_data = imap.fetch(email_id, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    subject = msg.get('Subject', '')
                    
                    # Skip if already applied
                    if is_job_applied(subject, applied_jobs):
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
                    
                    # Extract details
                    details = extract_job_details(subject, body_text, body_html)
                    rating = calculate_rating(subject, body_text, details['company'], details['location'])
                    
                    # Only include if rating >= 6
                    if rating >= 6:
                        all_jobs.append({
                            'id': f"{subject}_{msg.get('Date', '')}",
                            'subject': subject,
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
    
    # Sort by rating and remove duplicates
    seen = set()
    unique_jobs = []
    for job in sorted(all_jobs, key=lambda x: x['rating'], reverse=True):
        key = job['subject'][:50]
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    return unique_jobs[:10]  # Return top 10

def generate_email_content(jobs):
    """Generate HTML email content"""
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
        .job {{ border: 1px solid #ddd; margin: 20px 0; padding: 20px; border-radius: 8px; background: #f9f9f9; }}
        .job-header {{ border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-bottom: 15px; }}
        .title {{ font-size: 20px; font-weight: bold; color: #667eea; margin: 0; }}
        .company {{ font-size: 16px; color: #555; margin: 5px 0; }}
        .location {{ font-size: 14px; color: #777; margin: 5px 0; }}
        .rating {{ display: inline-block; background: #ffd700; color: #333; padding: 5px 10px; border-radius: 15px; font-weight: bold; }}
        .description {{ margin: 15px 0; padding: 10px; background: white; border-left: 4px solid #667eea; }}
        .apply-btn {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; margin-top: 10px; }}
        .apply-btn:hover {{ background: #764ba2; }}
        .footer {{ margin-top: 30px; padding: 20px; background: #f0f0f0; text-align: center; font-size: 12px; color: #666; }}
        .instructions {{ background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>💼 Dagliga Jobbmöjligheter</h1>
        <p>{datetime.now().strftime('%A %d %B %Y')}</p>
        <p>De 10 mest relevanta jobben för dig</p>
    </div>
    
    <div class="instructions">
        <strong>📧 Så här använder du detta:</strong><br>
        1. Klicka på "Ansök nu" för att gå till jobbannonsen<br>
        2. Om du söker jobbet, svara på detta mail med: "SÖKT: [Jobbnummer]"<br>
        3. Jag kommer då ta bort det från framtida listor<br>
        4. Varje söndag får du en sammanställning av alla jobb du sökt den veckan
    </div>
"""
    
    for i, job in enumerate(jobs, 1):
        stars = '⭐' * (job['rating'] // 2)
        
        # Clean up description
        desc = job['description'][:250] if job['description'] else 'Se länk för fullständig beskrivning'
        desc = desc.replace('<', '&lt;').replace('>', '&gt;')  # Escape HTML
        
        # Format location
        location = job['location'] if job['location'] else 'Se annons för plats'
        
        # Format company
        company = job['company'] if job['company'] else 'Se annons för företag'
        
        html += f"""
    <div class="job">
        <div class="job-header">
            <span class="rating">{stars} {job['rating']}/10</span>
            <h2 class="title">#{i}: {job['subject'][:70]}</h2>
            <div class="company">🏢 {company}</div>
            <div class="location">📍 {location}</div>
            <div style="margin-top: 5px; font-size: 12px; color: #999;">Källa: {job['source']}</div>
        </div>
        
        <div class="description">
            <strong>Beskrivning:</strong><br>
            {desc}...
        </div>
        
        {f'<a href="{job["link"]}" class="apply-btn" target="_blank">🔗 Ansök nu / Läs mer</a>' if job["link"] else '<p style="color: #999;">⚠️ Ingen direktlänk tillgänglig - se originalmail</p>'}
    </div>
"""
    
    html += f"""
    <div class="footer">
        <p>Detta mail skickades automatiskt av din Career Agent 🤖</p>
        <p>Datum: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
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
        # Load sender credentials
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
    print("📧 DAGLIGT JOBBMAIL - Genererar och skickar")
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
    
    # Generate email
    print("📄 Genererar HTML-email...")
    email_content = generate_email_content(jobs)
    
    # Save to file for review
    with open('/tmp/daily_jobs_email.html', 'w', encoding='utf-8') as f:
        f.write(email_content)
    
    print("💾 Sparade preview till: /tmp/daily_jobs_email.html")
    
    # Send email
    print("📨 Skickar email till richardlaurits@gmail.com...")
    subject = f"💼 Dagliga Jobbmöjligheter - {datetime.now().strftime('%A %d %b')} - {len(jobs)} jobb"
    
    if send_email('richardlaurits@gmail.com', subject, email_content):
        print("✅ Email skickat!")
    else:
        print("❌ Kunde inte skicka email")
    
    # Also send Telegram summary
    print("📱 Skickar sammanfattning till Telegram...")
    telegram_msg = f"""💼 Dagliga Jobbmöjligheter - {datetime.now().strftime('%A %d %b')}

Hittade {len(jobs)} relevanta jobb:

"""
    for i, job in enumerate(jobs[:5], 1):
        telegram_msg += f"{i}. {job['subject'][:50]}... ({job['rating']}/10)\n"
    
    telegram_msg += f"\n📧 Fullständig lista skickad till din email!"
    
    # Save for Telegram sender
    with open('/tmp/telegram_career_msg.txt', 'w') as f:
        f.write(telegram_msg)
    
    print(telegram_msg)
    
    # Save jobs for tracking
    with open('/tmp/todays_jobs.json', 'w') as f:
        json.dump(jobs, f, indent=2)
    
    print()
    print("=" * 80)
    print("✅ KLART!")
    print("=" * 80)

if __name__ == "__main__":
    main()
