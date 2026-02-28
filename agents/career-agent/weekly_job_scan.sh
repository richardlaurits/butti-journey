#!/bin/bash
# Career Agent - Weekly Job Scan
# Runs every Friday at 09:00 CET
# Searches for jobs posted this week matching Richard's profile

cd ~/.openclaw/workspace
source venv/bin/activate

# Log start
echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting weekly job scan" >> agents/career-agent/weekly_scan.log

# Spawn the career agent with full task description
openclaw sessions_spawn \
    --task "You are the Career Agent for Richard Laurits. Today is Friday - scan for NEW jobs posted THIS WEEK (Monday-Friday) that match Richard's profile.

RICHARD'S PROFILE:
- Target roles: Director, Senior Manager, VP, Head of Marketing, Business Development, Corporate Strategy, Commercial, Strategic Partnerships, General Manager, Managing Director
- Industries: Medical devices, MedTech, Healthcare, Diabetes, Pharma, Biotech, Life Sciences
- Locations: Switzerland (Zurich, Geneva, Basel), Denmark (Copenhagen), Sweden (Stockholm, Gothenburg, Lund)
- Current: Global Marketing Manager at Becton Dickinson

SEARCH STRATEGY (use ALL methods):
1. web_search for 'marketing director medtech Switzerland' with freshness=pw (past week)
2. web_search for 'business development pharma Denmark' with freshness=pw
3. web_search for 'strategy healthcare Sweden' with freshness=pw
4. Check specific sites: LinkedIn Jobs, Indeed.com, Monster.com, Jobs.ch, StepStone.dk, AMS.se (Arbetsförmedlingen)
5. If Playwright crawler available at agents/career-agent/enhanced-job-crawler-v2.py, use it for Novo Nordisk and Roche career pages
6. Search for company-specific postings: Novo Nordisk, Roche, BD, Medtronic, Abbott, Siemens Healthineers, Philips Healthcare, Stryker

SELECTION CRITERIA (score 0-10):
- 8-10: Perfect match - senior role, target company, right location
- 6-7: Good match - senior role, right industry, acceptable location
- 4-5: Possible match - needs more evaluation
- <4: Ignore

OUTPUT REQUIRED:
For top 3-5 jobs (score 7+), provide:
- Company name
- Job title
- Location
- Posted date (must be this week)
- Brief description (2-3 bullet points)
- Why it matches Richard (1 sentence)
- Application link if available

DELIVERY:
Send a well-formatted summary to Richard via Telegram with title '🎯 Weekly Career Scan - [Date]'.

If NO high-quality jobs found, report 'No new high-match positions this week' and suggest 2-3 companies to monitor next week.

Be thorough but efficient. Focus on QUALITY over quantity." \
    --label career-agent-weekly \
    --mode run \
    --timeout 300 >> agents/career-agent/weekly_scan.log 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S'): Weekly scan completed" >> agents/career-agent/weekly_scan.log
