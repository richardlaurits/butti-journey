#!/usr/bin/env python3
"""
Test email with embedded GIF
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

password_file = os.path.dirname(os.path.abspath(__file__)) + '/app_password.txt'
with open(password_file, 'r') as f:
    password = f.read().strip()

def send_gif_email():
    """Send test email with embedded GIF"""
    try:
        msg = MIMEMultipart('related')
        msg['Subject'] = "🤖 Test: ButtiBot Morning Greeting with GIF"
        msg['From'] = 'butti.nightrider@gmail.com'
        msg['To'] = 'richardlaurits@gmail.com'
        
        # HTML content with embedded image
        html_content = """
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.8; color: #333; background-color: #f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
      
      <h2 style="color: #2c3e50; margin-top: 0;">Godmorgon Jan! En ny Måndag börjar!</h2>
      
      <p style="font-size: 16px;">Kallt i Göteborg just nu (2°C) - varmt kaffe rekommenderas! ☕</p>
      
      <p style="font-size: 14px;">En påminnelse: Röra på sig är viktigt! En promenad kanske?</p>
      
      <div style="text-align: center; margin: 30px 0;">
        <img src="cid:morning_coffee" alt="Morning Coffee" style="max-width: 400px; border-radius: 8px;">
      </div>
      
      <hr style="border: none; border-top: 2px solid #ddd; margin: 30px 0;">
      
      <div style="text-align: left; font-size: 12px; color: #666; margin-top: 30px;">
        <p style="margin: 0;">
          <strong style="font-size: 14px;">🤖 ButtiBot</strong><br>
          24/7 Digital Assistant for Richard Laurits<br>
          <em style="font-size: 11px; color: #999;">Powered by OpenClaw</em>
        </p>
      </div>
      
    </div>
  </body>
</html>
"""
        
        # Attach HTML
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        msg_alternative.attach(MIMEText(html_content, 'html'))
        
        # Attach GIF
        gif_path = os.path.dirname(os.path.abspath(__file__)) + '/morning_coffee.gif'
        
        if os.path.exists(gif_path):
            with open(gif_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'inline', filename='morning_coffee.gif')
            part.add_header('Content-ID', '<morning_coffee>')
            part.add_header('Content-Transfer-Encoding', 'base64')
            msg.attach(part)
            
            print(f"✅ Attached GIF: {gif_path}")
        else:
            print(f"⚠️ GIF not found: {gif_path}")
        
        # Send
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('butti.nightrider@gmail.com', password)
            server.send_message(msg)
        
        print("✅ Test email sent to Richard with embedded GIF")
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    send_gif_email()
