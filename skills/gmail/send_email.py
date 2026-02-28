#!/usr/bin/env python3
"""
Send email from ButtiBot's Gmail account
Uses SMTP with app password
"""

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail credentials for butti.nightrider@gmail.com
GMAIL_USER = "butti.nightrider@gmail.com"
APP_PASSWORD = "jlcylboroggobdhj"  # From app_password.txt

def send_email(to_email, subject, body, html_body=None):
    """Send email via Gmail SMTP"""
    
    msg = MIMEMultipart('alternative')
    msg['From'] = GMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Plain text version
    msg.attach(MIMEText(body, 'plain'))
    
    # HTML version if provided
    if html_body:
        msg.attach(MIMEText(html_body, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, APP_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_email.py <to> <subject> <body_file>")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body_file = sys.argv[3]
    
    with open(body_file, 'r') as f:
        body = f.read()
    
    send_email(to_email, subject, body)
