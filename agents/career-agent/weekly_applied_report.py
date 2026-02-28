#!/usr/bin/env python3
"""
Career Agent - Weekly Applied Jobs Report
Sends Sunday summary of all jobs applied during the week
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

def load_applied_jobs():
    """Load applied jobs database"""
    try:
        with open('/home/richard-laurits/.openclaw/workspace/agents/career-agent/applied_jobs.json', 'r') as f:
            data = json.load(f)
            return data.get('jobs', [])
    except:
        return []

def generate_weekly_report():
    """Generate weekly report of applied jobs"""
    
    jobs = load_applied_jobs()
    
    # Filter for last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    recent_jobs = []
    
    for job in jobs:
        applied_date = job.get('applied_date', '')
        if applied_date:
            try:
                date = datetime.fromisoformat(applied_date)
                if date >= week_ago:
                    recent_jobs.append(job)
            except:
                pass
    
    if not recent_jobs:
        return None
    
    # Group by company
    by_company = {}
    for job in recent_jobs:
        company = job.get('company', 'Unknown')
        if company not in by_company:
            by_company[company] = []
        by_company[company].append(job)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; }}
        .summary {{ background: #f0f0f0; padding: 15px; margin: 20px 0; border-radius: 8px; }}
        .company {{ margin: 30px 0; }}
        .company-name {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 5px; }}
        .job {{ margin: 15px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #667eea; }}
        .footer {{ margin-top: 30px; padding: 20px; background: #f0f0f0; text-align: center; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Veckorapport - Sökta Jobb</h1>
        <p>Vecka {datetime.now().isocalendar()[1]}, {datetime.now().year}</p>
        <p>{(datetime.now() - timedelta(days=7)).strftime('%d %b')} - {datetime.now().strftime('%d %b %Y')}</p>
    </div>
    
    <div class="summary">
        <h2>📈 Sammanfattning</h2>
        <p><strong>Totalt sökta jobb denna vecka:</strong> {len(recent_jobs)}</p>
        <p><strong>Antal företag:</strong> {len(by_company)}</p>
        <p><strong>Totalt sökta sedan start:</strong> {len(jobs)}</p>
    </div>
"""
    
    for company, company_jobs in by_company.items():
        html += f"""
    <div class="company">
        <h2 class="company-name">🏢 {company}</h2>
"""
        for job in company_jobs:
            html += f"""
        <div class="job">
            <strong>{job.get('title', 'Unknown Position')}</strong><br>
            📍 {job.get('location', 'Location not specified')}<br>
            📅 Sökt: {job.get('applied_date', 'Unknown date')[:10]}
        </div>
"""
        html += "    </div>"
    
    html += f"""
    <div class="footer">
        <p>Rapport genererad: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <p>Career Agent 🤖</p>
    </div>
</body>
</html>
"""
    
    return html

def send_weekly_report():
    """Send weekly report email"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    html_content = generate_weekly_report()
    
    if not html_content:
        print("⚠️  Inga jobb sökta denna vecka - ingen rapport skickas")
        return
    
    try:
        with open('/home/richard-laurits/.openclaw/workspace/skills/gmail/app_password.txt', 'r') as f:
            sender_password = f.read().strip()
        
        sender_email = 'butti.nightrider@gmail.com'
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"📊 Veckorapport - Sökta Jobb - Vecka {datetime.now().isocalendar()[1]}"
        msg['From'] = sender_email
        msg['To'] = 'richardlaurits@gmail.com'
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, 'richardlaurits@gmail.com', msg.as_string())
        
        print("✅ Veckorapport skickad!")
        
    except Exception as e:
        print(f"❌ Fel vid skickande: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("📊 VECKORAPPORT - Sökta Jobb")
    print("=" * 80)
    print()
    
    send_weekly_report()
