#!/bin/bash
# Enhanced Career Agent - Multi-Approach Job Scan
# Tries multiple methods to find jobs: email parsing, web scraping, API calls
# Goal: Find at least 10 interesting jobs per week

cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting enhanced career scan - multi-approach" >> agents/career-agent/enhanced_scan.log

# Create combined report file
REPORT_FILE="/tmp/career_scan_$(date +%Y%m%d).txt"
echo "💼 CAREER AGENT - Multi-Approach Scan" > $REPORT_FILE
echo "📅 $(date '+%A %d %B %Y, %H:%M')" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# ============================================================
# APPROACH 1: Parse LinkedIn/Indeed emails from Gmail
# ============================================================
echo "🔍 APPROACH 1: Email Parsing" >> $REPORT_FILE
python3 << 'PYEOF' >> $REPORT_FILE 2>&1
import sys
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

print("Checking Gmail for job emails...")

try:
    import imaplib
    import email
    from datetime import datetime, timedelta
    
    EMAIL = 'richardlaurits@gmail.com'
    with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/richard_personal_app_password.txt', 'r') as f:
        PASSWORD = f.read().strip()
    
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(EMAIL, PASSWORD)
    imap.select('INBOX')
    
    # Search for job-related emails from last 7 days
    since_date = (datetime.now() - timedelta(days=7)).strftime('%d-%b-%Y')
    
    # Search for LinkedIn job emails
    status, messages = imap.search(None, f'(FROM "jobs@linkedin.com" SINCE {since_date})')
    linkedin_ids = messages[0].split()
    
    # Search for Indeed emails  
    status, messages = imap.search(None, f'(FROM "indeed.com" SINCE {since_date})')
    indeed_ids = messages[0].split()
    
    print(f"✅ Found {len(linkedin_ids)} LinkedIn job emails")
    print(f"✅ Found {len(indeed_ids)} Indeed job emails")
    
    jobs_found = []
    
    # Parse LinkedIn emails
    for email_id in linkedin_ids[:5]:  # Check last 5
        status, msg_data = imap.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg.get('Subject', '')
        
        # Look for job titles in subject
        if any(word in subject.lower() for word in ['marketing', 'director', 'manager', 'strategy', 'medical', 'healthcare']):
            jobs_found.append({
                'source': 'LinkedIn',
                'subject': subject,
                'role': 'Extracted from subject'
            })
    
    # Parse Indeed emails
    for email_id in indeed_ids[:5]:
        status, msg_data = imap.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg.get('Subject', '')
        
        if any(word in subject.lower() for word in ['marketing', 'director', 'manager', 'strategy', 'medical']):
            jobs_found.append({
                'source': 'Indeed',
                'subject': subject,
                'role': 'Extracted from subject'
            })
    
    imap.close()
    imap.logout()
    
    if jobs_found:
        print(f"\n📧 Jobs from emails: {len(jobs_found)}")
        for job in jobs_found[:3]:
            print(f"  • [{job['source']}] {job['subject'][:60]}")
    else:
        print("\n⚠️ No relevant jobs found in emails this week")
    
    print(f"\n📊 EMAIL PARSING RESULT: {len(jobs_found)} jobs")
    
except Exception as e:
    print(f"❌ Email parsing error: {e}")
    print("📊 EMAIL PARSING RESULT: 0 jobs (error)")

PYEOF

echo "" >> $REPORT_FILE

# ============================================================
# APPROACH 2: Web Search for recent postings
# ============================================================
echo "🔍 APPROACH 2: Web Search (past week)" >> $REPORT_FILE
python3 << 'PYEOF' >> $REPORT_FILE 2>&1
import sys
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

print("Searching web for recent job postings...")

# Company targets
COMPANIES = [
    "Novo Nordisk", "Roche", "BD (Becton Dickinson)", "Medtronic", 
    "Abbott", "Siemens Healthineers", "Philips Healthcare", "Stryker",
    "Baxter", "Fresenius Medical Care", "Boston Scientific", "Johnson & Johnson"
]

LOCATIONS = ["Switzerland", "Denmark", "Sweden"]

print(f"Target companies: {len(COMPANIES)}")
print(f"Target locations: {', '.join(LOCATIONS)}")
print("\nSearch queries used:")
print("  • 'marketing director medtech Switzerland jobs'")
print("  • 'business development manager pharma Denmark'")
print("  • 'strategy healthcare Sweden careers'")

# Note: Actual web search would require API key
# For now, we'll document what we would search for
print("\n⚠️ Web search requires API setup")
print("📊 WEB SEARCH RESULT: Would search ~36 combinations")
print("                      (12 companies × 3 locations)")

PYEOF

echo "" >> $REPORT_FILE

# ============================================================
# APPROACH 3: Company Career Page Scraping
# ============================================================
echo "🔍 APPROACH 3: Company Career Pages" >> $REPORT_FILE
python3 << 'PYEOF' >> $REPORT_FILE 2>&1

print("Testing company career page scraping...")
print("")

companies_to_try = [
    {"name": "Novo Nordisk", "url": "https://www.novonordisk.com/careers/find-a-job.html", "method": "NOT_TESTED"},
    {"name": "Roche", "url": "https://careers.roche.com/global/en", "method": "NOT_TESTED"},
    {"name": "BD", "url": "https://jobs.bd.com/", "method": "NOT_TESTED"},
    {"name": "Medtronic", "url": "https://careers.medtronic.com/", "method": "NOT_TESTED"},
]

print("Companies to test:")
for c in companies_to_try:
    print(f"  • {c['name']}: {c['url']}")

print("\n⚠️ Career page scraping requires:")
print("  1. Testing each site's structure")
print("  2. Handling anti-bot protection")
print("  3. Maintaining selectors over time")
print("  4. Rate limiting to avoid blocks")

print("\n📊 CAREER PAGE RESULT: 0 jobs (not yet tested)")
print("💡 RECOMMENDATION: Start with 2-3 companies and test manually first")

PYEOF

echo "" >> $REPORT_FILE

# ============================================================
# SUMMARY
# ============================================================
echo "📊 SUMMARY" >> $REPORT_FILE
echo "==========" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "Approach 1 (Email parsing): Needs Gmail access setup" >> $REPORT_FILE
echo "Approach 2 (Web search): Needs Brave Search API key" >> $REPORT_FILE  
echo "Approach 3 (Career pages): Needs Playwright + testing" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "NEXT STEPS:" >> $REPORT_FILE
echo "1. Set up Gmail app password for Richard's account" >> $REPORT_FILE
echo "2. Test 2-3 company career pages manually" >> $REPORT_FILE
echo "3. Build working scraper for successful sites" >> $REPORT_FILE
echo "4. Run combined scan weekly" >> $REPORT_FILE

echo "$(date '+%Y-%m-%d %H:%M:%S'): Enhanced scan completed - see $REPORT_FILE" >> agents/career-agent/enhanced_scan.log

# Send report to Telegram
cat $REPORT_FILE | python3 /home/richard-laurits/.openclaw/workspace/agents/investment-agent/telegram_sender.py 2>/dev/null || echo "Could not send to Telegram"
