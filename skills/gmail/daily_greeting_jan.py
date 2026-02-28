#!/usr/bin/env python3
"""
Daily greeting email to Jan Laurits (Richard's father)
Personalized with weather, day info, emoji art, and creative messages
Runs every day at 10:00 CET
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
import random
import requests

password_file = os.path.dirname(os.path.abspath(__file__)) + '/app_password.txt'
with open(password_file, 'r') as f:
    password = f.read().strip()

JAN_EMAIL = 'janlaurits@icloud.com'

# Fun emoji art for variety
EMOJI_ART = [
    "☕ 🌅 ☕",
    "🎉 😊 🎉",
    "☀️ 🌤️ ☀️",
    "💪 🏃 💪",
    "🧠 💻 🧠",
    "🎯 🚀 🎯",
    "🌟 ⭐ 🌟",
    "👍 😄 👍",
    "🎊 🤖 🎊",
]

def get_goteborg_weather():
    """Fetch weather for Göteborg"""
    try:
        resp = requests.get('https://wttr.in/Göteborg?format=j1', timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            current = data['current_condition'][0]
            temp = int(current['temp_C'])
            desc = current['weatherDesc'][0]['value'].lower()
            return temp, desc
    except:
        pass
    return None, None

def get_day_info():
    """Get info about today"""
    today = datetime.now()
    day_name = today.strftime('%A')
    
    days_sv = {
        'Monday': 'Måndag',
        'Tuesday': 'Tisdag',
        'Wednesday': 'Onsdag',
        'Thursday': 'Torsdag',
        'Friday': 'Fredag',
        'Saturday': 'Lördag',
        'Sunday': 'Söndag',
    }
    
    return days_sv.get(day_name, day_name)

def generate_greeting():
    """Generate a personalized greeting for Jan"""
    
    day_sv = get_day_info()
    temp, weather = get_goteborg_weather()
    
    # Motivation + Movement reminders
    movement_messages = [
        "En påminnelse: Röra på sig är viktigt! En promenad kanske?",
        "Dags att komma igång med dagen! Lite rörelse gör gott.",
        "Hoppas du tar en trevlig promenad idag - bra för kropp och själ!",
        "Kom igång med dagen! En kort gång är bättre än ingen.",
        "Påminnelse från Richard: Röra på sig är viktigt! Vad säger du?",
    ]
    
    # Computer learning encouragement
    computer_messages = [
        "Hur går det med den nya datorn? Dags att utforska lite mer?",
        "Har du testat något nytt på datorn idag? Små steg, stora framsteg!",
        "Påminnelse: Den nya datorn är en möjlighet! Vad vill du lära dig idag?",
        "Richard säger att du ska peppas med datorn! Det är inte så svårt - bara ett steg i taget.",
        "Dags att testa något nytt på datorn? Du klarar det!",
        "Hur många minuter på datorn idag? Gradvis framåt är allt!",
    ]
    
    # Weather snippets (always included)
    weather_snippets = []
    if temp is not None:
        if temp < 0:
            weather_snippets = [
                f"Kallt i Göteborg ({temp}°C) - varmt kaffe rekommenderas! ☕",
                f"Minusgrader hemma ({temp}°C). Perfekt väder för att träna inomhus.",
            ]
        elif temp < 5:
            weather_snippets = [
                f"Kyligt men fint i Göteborg ({temp}°C).",
                f"Några plusgrader hemma ({temp}°C). Perfekt för en promenad!",
            ]
        elif temp < 10:
            weather_snippets = [
                f"Ganska trevligt väder i Göteborg ({temp}°C).",
                f"Milt väder hemma ({temp}°C). Dags att vara ute!",
            ]
        else:
            weather_snippets = [
                f"Fint väder i Göteborg ({temp}°C)! 🌞",
                f"Värmt och trevligt hemma ({temp}°C) - njut av det!",
            ]
        
        if 'rain' in weather or 'drizzle' in weather:
            weather_snippets.append(f"Lite regn hemma ({temp}°C). Perfekt träningväder inomhus!")
        elif 'cloud' in weather or 'overcast' in weather:
            weather_snippets.append(f"Mulet i Göteborg ({temp}°C), men ändå inte så dåligt.")
        elif 'sun' in weather or 'clear' in weather:
            weather_snippets.append(f"Solsken i Göteborg ({temp}°C)! Gå ut och ta lite sol! ☀️")
    
    # Build main greeting
    main_greetings = [
        f"Godmorgon Jan! En ny {day_sv} börjar!",
        f"Hej Jan! Trevlig {day_sv} för dig!",
        f"Godmorgon från Schweiz! Richard och jag säger hej!",
        f"Hej Jan! Hur mår du denna {day_sv}?",
        f"Godmorgon! Hoppas du har en bra dag före dig.",
        f"Hej Jan! {day_sv} är här - dags att komma igång!",
    ]
    
    # Combine everything
    greeting = random.choice(main_greetings)
    
    # Add weather (always)
    if weather_snippets:
        greeting += " " + random.choice(weather_snippets)
    
    # Add motivation/reminder (50/50 movement or computer)
    if random.random() > 0.5:
        greeting += "\n\n" + random.choice(movement_messages)
    else:
        greeting += "\n\n" + random.choice(computer_messages)
    
    return greeting

def send_greeting(to_email=None):
    """Send daily greeting with emoji art and signature"""
    try:
        if to_email is None:
            to_email = JAN_EMAIL
        
        greeting = generate_greeting()
        emoji_art = random.choice(EMOJI_ART)
        
        # Create multipart email with HTML
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🤖 Godmorgon från ButtiBot"
        msg['From'] = 'butti.nightrider@gmail.com'
        msg['To'] = to_email
        
        # HTML content with emoji art and signature
        html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.8; color: #333; background-color: #f9f9f9; padding: 20px;">
    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
      
      <p style="font-size: 16px; margin: 0 0 20px 0;">{greeting}</p>
      
      <div style="text-align: center; margin: 30px 0; font-size: 40px;">
        {emoji_art}
      </div>
      
      <hr style="border: none; border-top: 2px solid #ddd; margin: 30px 0;">
      
      <div style="text-align: left; font-size: 12px; color: #666; margin-top: 30px;">
        <p style="margin: 0;">
          <strong style="font-size: 14px;">🤖 ButtiBot</strong><br>
          24/7 Digital Assistant for Richard Laurits<br>
          <em style="font-size: 11px; color: #999;">Powered by OpenClaw</em><br>
          <br>
          <span style="font-size: 10px; color: #aaa;">
            Automatisk daglig hälsning från ButtiBot - Richards digitala assistans
          </span>
        </p>
      </div>
      
    </div>
  </body>
</html>
"""
        
        # Attach HTML
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('butti.nightrider@gmail.com', password)
            server.send_message(msg)
        
        target = "Jan" if to_email == JAN_EMAIL else "Richard"
        print(f"✅ Greeting with emoji sent to {target}")
        
        # Log it
        log_file = os.path.dirname(password_file) + '/jan_greeting_log.json'
        logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'greeting': greeting[:100],
            'recipient': to_email,
            'emoji': emoji_art,
            'status': 'sent'
        })
        
        # Keep last 100 entries
        logs = logs[-100:]
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Test mode - send to Richard
        send_greeting('richardlaurits@gmail.com')
    else:
        # Normal mode - send to Jan
        send_greeting()
