#!/bin/bash
# Enhanced Career Agent - Daily Job Scan
# Runs Monday-Friday at 17:00
# Multi-approach: Email parsing + Company career pages

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting daily career scan" >> agents/career-agent/daily_scan.log

# Configuration
REPORT_FILE="/tmp/career_scan_$(date +%Y%m%d_%H%M).txt"
JOB_COUNT=0
MIN_JOBS_TARGET=10

echo "💼 CAREER AGENT - Daily Scan ($(date '+%A %d %B'))" > $REPORT_FILE
echo "🎯 Target: $MIN_JOBS_TARGET interesting jobs" >> $REPORT_FILE
echo "🏢 Companies: Roche, Novo Nordisk, Glooko, Ypsomed, Rubin Medical, BD, Eitan, Micrel, Minimed, Medtronic, Insulet, Ideon" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# ============================================================
# APPROACH 1: Parse LinkedIn Job Emails
# ============================================================
echo "🔍 APPROACH 1: LinkedIn Job Emails" >> $REPORT_FILE
echo "─────────────────────────────────" >> $REPORT_FILE

python3 << 'PYEOF' >> $REPORT_FILE 2>&1
import sys
sys.path.insert(0, '/home/richard-laurits/.openclaw/workspace')

try:
    import imaplib
    import email
    import re
    from datetime import datetime, timedelta
    import json
    
    EMAIL = 'richardlaurits@gmail.com'
    
    # Read app password
    try:
        with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/richard_personal_app_password.txt', 'r') as f:
            PASSWORD = f.read().strip()
    except:
        print("❌ Could not read app password")
        print("📊 LINKEDIN EMAILS: 0 jobs")
        exit(1)
    
    # Keywords for matching
    KEYWORDS = ['marketing', 'director', 'manager', 'strategy', 'medical', 'healthcare', 
                'medtech', 'commercial', 'business development', 'general manager', 
                'managing director', 'vp', 'vice president', 'head of', 'switzerland', 
                'denmark', 'sweden', 'copenhagen', 'geneva', 'zurich', 'stockholm']
    
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(EMAIL, PASSWORD)
    imap.select('INBOX')
    
    # Search LinkedIn job emails from last 24 hours
    since_date = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')
    status, messages = imap.search(None, f'(FROM "jobs@linkedin.com" SINCE {since_date})')
    email_ids = messages[0].split()
    
    linkedin_jobs = []
    
    for email_id in email_ids[-10:]:  # Check last 10 emails
        status, msg_data = imap.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg.get('Subject', '')
        
        # Check if subject matches keywords
        subject_lower = subject.lower()
        matches = [kw for kw in KEYWORDS if kw in subject_lower]
        
        if len(matches) >= 2:  # At least 2 keyword matches
            linkedin_jobs.append({
                'source': 'LinkedIn',
                'title': subject,
                'keywords': matches,
                'date': msg.get('Date', '')
            })
    
    imap.close()
    imap.logout()
    
    # Save to temp file for counting
    with open('/tmp/linkedin_jobs_count.txt', 'w') as f:
        f.write(str(len(linkedin_jobs)))
    
    if linkedin_jobs:
        print(f"✅ Found {len(linkedin_jobs)} relevant LinkedIn jobs\n")
        for i, job in enumerate(linkedin_jobs[:5], 1):
            print(f"{i}. {job['title'][:70]}")
            print(f"   Keywords: {', '.join(job['keywords'][:3])}")
    else:
        print("⚠️ No relevant LinkedIn jobs in last 24h\n")
    
    print(f"📊 LINKEDIN EMAILS: {len(linkedin_jobs)} jobs")
    
except Exception as e:
    print(f"❌ Error: {str(e)[:100]}")
    print("📊 LINKEDIN EMAILS: 0 jobs (error)")
    with open('/tmp/linkedin_jobs_count.txt', 'w') as f:
        f.write('0')

PYEOF

# Get count
LINKEDIN_COUNT=$(cat /tmp/linkedin_jobs_count.txt 2>/dev/null || echo "0")
JOB_COUNT=$((JOB_COUNT + LINKEDIN_COUNT))

echo "" >> $REPORT_FILE

# ============================================================
# APPROACH 2: Company Career Pages (Rotate 2-3 per day)
# ============================================================
echo "🔍 APPROACH 2: Company Career Pages" >> $REPORT_FILE
echo "──────────────────────────────────" >> $REPORT_FILE

# Rotate companies based on day of week
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 5=Friday

COMPANIES=(
    "Roche:https://careers.roche.com/global/en"
    "Novo Nordisk:https://www.novonordisk.com/careers/find-a-job.html"
    "Glooko:https://glooko.com/careers/"
    "Ypsomed:https://www.ypsomed.com/en/careers"
    "Rubin Medical:https://rubinmedical.com/careers"
    "BD:https://jobs.bd.com/"
    "Eitan Medical:https://www.eitanmedical.com/careers"
    "Micrel Medical:https://www.micrelmedical.com/careers"
    "Minimed:https://www.medtronic.com/us-en/careers.html"
    "Medtronic:https://www.medtronic.com/us-en/careers.html"
    "Insulet:https://www.insulet.com/careers"
    "Ideon:https://www.ideon.ai/careers"
)

# Select 2-3 companies based on day
if [ "$DAY_OF_WEEK" -eq 1 ]; then
    TODAY_COMPANIES="Roche,Novo Nordisk,Glooko"
    COMPANY_URLS=("${COMPANIES[0]}" "${COMPANIES[1]}" "${COMPANIES[2]}")
elif [ "$DAY_OF_WEEK" -eq 2 ]; then
    TODAY_COMPANIES="Ypsomed,Rubin Medical,BD"
    COMPANY_URLS=("${COMPANIES[3]}" "${COMPANIES[4]}" "${COMPANIES[5]}")
elif [ "$DAY_OF_WEEK" -eq 3 ]; then
    TODAY_COMPANIES="Eitan Medical,Micrel,Minimed"
    COMPANY_URLS=("${COMPANIES[6]}" "${COMPANIES[7]}" "${COMPANIES[8]}")
elif [ "$DAY_OF_WEEK" -eq 4 ]; then
    TODAY_COMPANIES="Medtronic,Insulet,Ideon"
    COMPANY_URLS=("${COMPANIES[9]}" "${COMPANIES[10]}" "${COMPANIES[11]}")
elif [ "$DAY_OF_WEEK" -eq 5 ]; then
    TODAY_COMPANIES="Roche,Novo Nordisk,Medtronic"
    COMPANY_URLS=("${COMPANIES[0]}" "${COMPANIES[1]}" "${COMPANIES[9]}")
fi

echo "Today's companies: $TODAY_COMPANIES" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Try to scrape each company (simplified HTTP request)
for company_info in "${COMPANY_URLS[@]}"; do
    IFS=':' read -r COMPANY_NAME COMPANY_URL <<< "$company_info"
    
    echo "Testing: $COMPANY_NAME" >> $REPORT_FILE
    
    # Try simple curl first
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$COMPANY_URL" 2>/dev/null || echo "000")
    
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "  ✅ Site accessible (HTTP 200)" >> $REPORT_FILE
        echo "  📝 URL: $COMPANY_URL" >> $REPORT_FILE
        echo "  ⚠️  Full scraping requires Playwright setup" >> $REPORT_FILE
    else
        echo "  ⚠️  Status: $HTTP_STATUS (may need JavaScript/cookies)" >> $REPORT_FILE
    fi
    echo "" >> $REPORT_FILE
done

echo "📊 COMPANY PAGES: Manual testing phase" >> $REPORT_FILE
echo "💡 Full scraping will be implemented after testing" >> $REPORT_FILE

# ============================================================
# SUMMARY & NEXT STEPS
# ============================================================
echo "" >> $REPORT_FILE
echo "📊 DAILY SUMMARY" >> $REPORT_FILE
echo "═══════════════" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "Jobs found today:" >> $REPORT_FILE
echo "  • LinkedIn emails: $LINKEDIN_COUNT" >> $REPORT_FILE
echo "  • Company pages: Testing phase" >> $REPORT_FILE
echo "  • Total so far: $JOB_COUNT" >> $REPORT_FILE
echo "" >> $REPORT_FILE

if [ "$JOB_COUNT" -ge "$MIN_JOBS_TARGET" ]; then
    echo "🎉 TARGET REACHED: $JOB_COUNT jobs (goal: $MIN_JOBS_TARGET)" >> $REPORT_FILE
else
    echo "📝 Progress: $JOB_COUNT/$MIN_JOBS_TARGET jobs" >> $REPORT_FILE
    echo "💡 Continue building scrapers to reach target" >> $REPORT_FILE
fi

echo "" >> $REPORT_FILE
echo "NEXT:" >> $REPORT_FILE
echo "• Tomorrow: Testing 3 more companies" >> $REPORT_FILE
echo "• Building working scrapers as we learn" >> $REPORT_FILE
echo "• Goal: Reach 10+ jobs per week consistently" >> $REPORT_FILE

# Send report
cat $REPORT_FILE | python3 /home/richard-laurits/.openclaw/workspace/agents/investment-agent/telegram_sender.py 2>/dev/null

# Log completion
echo "$(date '+%Y-%m-%d %H:%M:%S'): Daily scan completed - $JOB_COUNT jobs found" >> agents/career-agent/daily_scan.log
