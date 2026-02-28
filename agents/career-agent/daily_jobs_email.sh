#!/bin/bash
# Daily Jobs Email - Career Agent
# Sends top 10 jobs every morning at 08:00

cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting daily jobs email" >> agents/career-agent/daily_email.log

# Run the Python script
python3 agents/career-agent/send_daily_jobs_email.py >> agents/career-agent/daily_email.log 2>&1

# Check for "applied" replies from previous emails
python3 agents/career-agent/process_applied_jobs.py check >> agents/career-agent/daily_email.log 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S'): Daily jobs email completed" >> agents/career-agent/daily_email.log
