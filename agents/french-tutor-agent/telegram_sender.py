#!/usr/bin/env python3
"""
Telegram Sender - Simple wrapper to send messages
Uses the bot token from TOOLS.md
"""

import os
import sys
import urllib.request
import urllib.parse
import json

# Bot configuration
BOT_TOKEN = "8581242714:AAFjjOK2G4bf3SGi9FAGkdCJWsiznsLW8Vw"
CHAT_ID = "7733823361"

def send_message(text, parse_mode="Markdown"):
    """Send message to Telegram"""
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": parse_mode
    }
    
    try:
        data_encoded = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(url, data=data_encoded, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            if result.get("ok"):
                print(f"✅ Message sent (ID: {result['result']['message_id']})")
                return True
            else:
                print(f"❌ Failed: {result.get('description')}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        send_message(message)
    else:
        # Read from stdin
        message = sys.stdin.read().strip()
        if message:
            send_message(message)
        else:
            print("No message provided")
