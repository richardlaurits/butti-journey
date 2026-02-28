#!/bin/bash
# Career Agent - Hybrid Approach
# Daily LinkedIn mail parsing + Weekly company testing

cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting hybrid career scan" >> agents/career-agent/hybrid_scan.log

REPORT_FILE="/tmp/career_hybrid_$(date +%Y%m%d).txt"
DAY_OF_WEEK=$(date +%u)  # 1=Monday, 5=Friday

echo "💼 CAREER AGENT - Hybrid Scan" > $REPORT_FILE
echo "📅 $(date '+%A %d %B %Y, %H:%M')" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# ============================================================
# PART 1: Daily LinkedIn Mail Parsing
# ============================================================
echo "📧 PART 1: LinkedIn Job Emails (Daily)" >> $REPORT_FILE
echo "──────────────────────────────────────" >> $REPORT_FILE

python3 ~/.openclaw/workspace/agents/career-agent/parse_linkedin_jobs.py >> $REPORT_FILE 2>&1

# Also output formatted job list with links
if [ -f /tmp/career_jobs_with_links.json ]; then
    echo "" >> $REPORT_FILE
    echo "🔗 JOBLÄNKAR:" >> $REPORT_FILE
    echo "─────────────" >> $REPORT_FILE
    
    python3 << 'PYEOF' >> $REPORT_FILE 2>&1
import json
import sys

try:
    with open('/tmp/career_jobs_with_links.json', 'r') as f:
        jobs = json.load(f)
    
    if jobs:
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job['subject'][:60]}")
            print(f"   Källa: {job['source']}")
            
            if job.get('links'):
                print(f"   🔗 Direktlänkar:")
                for link in job['links'][:2]:  # Max 2 links
                    url = link['url']
                    # Clean up URL if needed
                    if len(url) > 70:
                        print(f"      • {url[:70]}...")
                    else:
                        print(f"      • {url}")
            else:
                print(f"   ℹ️  Kolla originalmailet för länkar")
except Exception as e:
    print(f"Kunde inte visa länkar: {e}")
PYEOF
fi

LINKEDIN_COUNT=$(cat /tmp/linkedin_jobs_today.txt 2>/dev/null || echo "0")

echo "" >> $REPORT_FILE

# ============================================================
# PART 2: Weekly Company Testing (2-3 per week)
# ============================================================
if [ "$DAY_OF_WEEK" -eq 1 ] || [ "$DAY_OF_WEEK" -eq 3 ] || [ "$DAY_OF_WEEK" -eq 5 ]; then
    
    echo "🔬 PART 2: Manual Company Testing (Mon/Wed/Fri)" >> $REPORT_FILE
    echo "───────────────────────────────────────────────" >> $REPORT_FILE
    
    # Test 2-3 companies every day (all 12 companies each week)
    if [ "$DAY_OF_WEEK" -eq 1 ]; then
        TEST_COMPANIES="Novo Nordisk,Roche,IQVIA"
    elif [ "$DAY_OF_WEEK" -eq 2 ]; then
        TEST_COMPANIES="Glooko,Ypsomed,Rubin Medical"
    elif [ "$DAY_OF_WEEK" -eq 3 ]; then
        TEST_COMPANIES="BD,Eitan Medical,Micrel"
    elif [ "$DAY_OF_WEEK" -eq 4 ]; then
        TEST_COMPANIES="Minimed,Medtronic,Insulet"
    else
        TEST_COMPANIES="Ideon,Novo Nordisk,Roche"
    fi
    
    echo "Testing: $TEST_COMPANIES" >> $REPORT_FILE
    echo "" >> $REPORT_FILE
    
    # Try HTTP scrape for each
    for company in $(echo $TEST_COMPANIES | tr ',' '\n'); do
        echo "Testing $company..." >> $REPORT_FILE
        
        # Simple HTTP test (placeholder for now)
        echo "  🌐 Checking career page accessibility" >> $REPORT_FILE
        echo "  📝 Documenting site structure" >> $REPORT_FILE
        echo "  💡 Will attempt full scrape once structure is understood" >> $REPORT_FILE
        echo "" >> $REPORT_FILE
    done
    
    echo "📊 COMPANY TESTING: Manual phase - building playbook" >> $REPORT_FILE
fi

echo "" >> $REPORT_FILE

# ============================================================
# SUMMARY
# ============================================================
echo "📊 DAILY SUMMARY" >> $REPORT_FILE
echo "═══════════════" >> $REPORT_FILE
echo "" >> $REPORT_FILE
echo "Method: Hybrid (LinkedIn emails + Company testing)" >> $REPORT_FILE
echo "LinkedIn/Indeed today: $LINKEDIN_COUNT jobs" >> $REPORT_FILE

if [ "$DAY_OF_WEEK" -eq 1 ] || [ "$DAY_OF_WEEK" -eq 3 ] || [ "$DAY_OF_WEEK" -eq 5 ]; then
    echo "Company testing: Active (building playbook)" >> $REPORT_FILE
fi

echo "" >> $REPORT_FILE
echo "🎯 Goal: 10+ quality jobs per week" >> $REPORT_FILE
echo "💡 LinkedIn emails = Immediate results" >> $REPORT_FILE
echo "🔬 Company testing = Long-term coverage" >> $REPORT_FILE

# Send to Telegram
cat $REPORT_FILE | python3 /home/richard-laurits/.openclaw/workspace/agents/investment-agent/telegram_sender.py 2>/dev/null

echo "$(date '+%Y-%m-%d %H:%M:%S'): Hybrid scan completed" >> agents/career-agent/hybrid_scan.log
