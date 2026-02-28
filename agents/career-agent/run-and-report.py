#!/usr/bin/env python3
"""
Career Agent: Run Crawler + Send Telegram Report
Executes enhanced-job-crawler.py and sends summary to Richard
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

def get_latest_results():
    """Get most recent job results file"""
    results_dir = Path("./job_results")
    if not results_dir.exists():
        return None
    
    files = sorted(results_dir.glob("jobs_*.json"), reverse=True)
    return files[0] if files else None

def generate_telegram_message(results):
    """Generate formatted Telegram message"""
    message = "🎯 *Career Agent - Job Scan Complete*\n\n"
    message += f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"⏱ Duration: {results['scan_duration_seconds']}s\n"
    message += f"📍 Companies: {results['companies_scanned']}\n"
    message += f"💼 Jobs found (score ≥5): {results['total_jobs_found']}\n"
    message += f"📸 Screenshots: {results['screenshots_taken']}\n\n"
    
    if results['jobs']:
        message += "🏆 *TOP MATCHES:*\n"
        for job in sorted(results['jobs'], key=lambda x: x['score'], reverse=True)[:5]:
            message += f"\n• *[{job['score']}/10] {job['title']}*\n"
            message += f"  {job['company']} • {job['location']}\n"
            if job.get('link'):
                message += f"  🔗 {job['link']}\n"
    else:
        message += "⚠️ No high-scoring jobs found. Try expanding search criteria.\n"
    
    message += f"\n📁 Results: `{os.path.basename(str(get_latest_results()))}`"
    return message

def send_telegram_notification(results):
    """Send Telegram message via OpenClaw message tool"""
    try:
        # Import here to avoid dependency if Telegram not configured
        import sys
        sys.path.insert(0, '/home/richard-laurits/.openclaw')
        
        msg = generate_telegram_message(results)
        
        # Use OpenClaw's message function via subprocess
        cmd = [
            'openclaw',
            'message',
            '--action', 'send',
            '--channel', 'telegram',
            '--target', '7733823361',
            '--message', msg
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Telegram notification sent")
        else:
            print(f"⚠️ Failed to send Telegram: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Could not send Telegram: {str(e)}")

def main():
    """Run crawler and report"""
    print("\n🚀 Starting job crawler...")
    
    # Run the enhanced crawler
    try:
        result = subprocess.run(
            ["python3", "./enhanced-job-crawler.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False,
            text=True
        )
    except Exception as e:
        print(f"❌ Error running crawler: {e}")
        return
    
    # Get results and send notification
    results_file = get_latest_results()
    if results_file:
        with open(results_file) as f:
            results = json.load(f)
        
        print("\n📨 Sending Telegram report...")
        send_telegram_notification(results)
    else:
        print("❌ No results file found")

if __name__ == "__main__":
    main()
