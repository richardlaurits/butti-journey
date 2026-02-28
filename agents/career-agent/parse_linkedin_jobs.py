#!/usr/bin/env python3
"""
Career Agent - LinkedIn Job Parser with Links
Extracts job links from LinkedIn and Indeed emails
"""

import sys
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

import imaplib
import email
from datetime import datetime, timedelta
import re
from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    """Extract links from HTML"""
    def __init__(self):
        super().__init__()
        self.links = []
        self.current_data = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            if 'href' in attrs_dict:
                self.links.append({
                    'url': attrs_dict['href'],
                    'text': ''
                })
                self.current_data = ''
                
    def handle_data(self, data):
        if self.links:
            self.links[-1]['text'] += data.strip()

def extract_links_from_html(html_content):
    """Extract all links from HTML"""
    parser = LinkExtractor()
    try:
        parser.feed(html_content)
    except:
        pass
    return parser.links

def parse_job_emails():
    """Main function to parse job emails"""
    
    EMAIL = 'richardlaurits@gmail.com'
    
    with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/richard_personal_app_password.txt', 'r') as f:
        PASSWORD = f.read().strip()
    
    # Keywords
    ROLES = ['marketing', 'director', 'manager', 'strategy', 'commercial', 
             'business development', 'medical', 'healthcare', 'medtech']
    LOCATIONS = ['switzerland', 'denmark', 'sweden', 'schweiz', 'danmark', 
                 'sverige', 'geneva', 'zurich', 'copenhagen', 'stockholm']
    COMPANIES = ['novo nordisk', 'roche', 'iqvia', 'glooko', 'ypsomed', 
                 'bd', 'medtronic', 'insulet']
    
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(EMAIL, PASSWORD)
    imap.select('INBOX')
    
    # Last 24 hours
    since_date = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')
    
    # Search LinkedIn
    status, messages = imap.search(None, f'(FROM "jobs@linkedin.com" SINCE {since_date})')
    linkedin_ids = messages[0].split()
    
    # Search Indeed
    status, messages = imap.search(None, f'(FROM "indeed.com" SINCE {since_date})')
    indeed_ids = messages[0].split()
    
    jobs = []
    
    # Parse LinkedIn with links
    for email_id in linkedin_ids[-20:]:
        try:
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get('Subject', '')
            subject_lower = subject.lower()
            
            # Score
            role_match = sum(1 for r in ROLES if r in subject_lower)
            location_match = sum(1 for l in LOCATIONS if l in subject_lower)
            company_match = sum(1 for c in COMPANIES if c in subject_lower)
            score = role_match + location_match + (company_match * 2)
            
            if score >= 2:
                # Extract body
                body_html = ''
                body_text = ''
                
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == 'text/html':
                            try:
                                body_html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            except:
                                pass
                        elif content_type == 'text/plain':
                            try:
                                body_text = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            except:
                                pass
                else:
                    try:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            body_text = payload.decode('utf-8', errors='ignore')
                    except:
                        pass
                
                # Extract links from HTML
                links = []
                if body_html:
                    extracted = extract_links_from_html(body_html)
                    # Filter for job links only
                    for link in extracted:
                        url = link['url']
                        text = link['text'].lower()
                        # LinkedIn job links typically contain /jobs/ or /view/
                        if '/jobs/' in url or '/view/' in url or 'linkedin.com/jobs' in url:
                            if any(keyword in text or keyword in url.lower() for keyword in ['job', 'apply', 'position', 'view']):
                                links.append({
                                    'url': url,
                                    'text': link['text'][:50] if link['text'] else 'Job Link'
                                })
                
                # Also look for plain URLs in text
                if not links and body_text:
                    url_pattern = r'https?://[^\s<>"\']+(?:jobs?|careers?|apply)[^\s<>"\']*'
                    found_urls = re.findall(url_pattern, body_text, re.IGNORECASE)
                    links = [{'url': url, 'text': 'Job Link'} for url in found_urls[:3]]
                
                jobs.append({
                    'source': 'LinkedIn',
                    'subject': subject[:100],
                    'score': score,
                    'links': links[:3],  # Max 3 links
                    'matches': {
                        'roles': [r for r in ROLES if r in subject_lower][:2],
                        'locations': [l for l in LOCATIONS if l in subject_lower][:2],
                        'companies': [c for c in COMPANIES if c in subject_lower][:2]
                    }
                })
        except Exception as e:
            continue
    
    # Parse Indeed
    for email_id in indeed_ids[-15:]:
        try:
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            subject = msg.get('Subject', '')
            subject_lower = subject.lower()
            
            role_match = sum(1 for r in ROLES if r in subject_lower)
            location_match = sum(1 for l in LOCATIONS if l in subject_lower)
            
            if role_match >= 1 and location_match >= 1:
                # Extract HTML for links
                body_html = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/html':
                            try:
                                body_html = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            except:
                                pass
                
                links = []
                if body_html:
                    extracted = extract_links_from_html(body_html)
                    for link in extracted:
                        url = link['url']
                        if 'indeed.com' in url and ('job' in url or 'apply' in url.lower()):
                            links.append({
                                'url': url,
                                'text': link['text'][:50] if link['text'] else 'Indeed Job'
                            })
                
                jobs.append({
                    'source': 'Indeed',
                    'subject': subject[:100],
                    'score': role_match + location_match,
                    'links': links[:3],
                    'matches': {
                        'roles': [r for r in ROLES if r in subject_lower][:2],
                        'locations': [l for l in LOCATIONS if l in subject_lower][:2]
                    }
                })
        except Exception as e:
            continue
    
    imap.close()
    imap.logout()
    
    # Sort by score
    jobs.sort(key=lambda x: x['score'], reverse=True)
    
    return jobs

if __name__ == "__main__":
    jobs = parse_job_emails()
    
    if jobs:
        print(f"✅ Found {len(jobs)} relevant jobs with links\n")
        for i, job in enumerate(jobs[:10], 1):
            print(f"{i}. [{job['source']}] {job['subject']}")
            if job['matches'].get('companies'):
                print(f"   🏢 Company: {', '.join(job['matches']['companies'])}")
            if job['matches'].get('locations'):
                print(f"   📍 Location: {', '.join(job['matches']['locations'])}")
            if job['matches'].get('roles'):
                print(f"   💼 Role: {', '.join(job['matches']['roles'])}")
            
            if job['links']:
                print(f"   🔗 Links:")
                for link in job['links']:
                    print(f"      • {link['text']}: {link['url'][:80]}...")
            else:
                print(f"   ⚠️  No direct links extracted")
            print()
    else:
        print("⚠️  No relevant job emails in last 24h")
    
    # Save count for shell script
    with open('/tmp/linkedin_jobs_today.txt', 'w') as f:
        f.write(str(len(jobs)))
    
    # Save full results
    import json
    with open('/tmp/career_jobs_with_links.json', 'w') as f:
        json.dump(jobs, f, indent=2)
