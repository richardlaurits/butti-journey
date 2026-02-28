#!/usr/bin/env python3
"""
Hourly Flashscore Live Alerts via Telegram
Runs once per hour, sends only significant matches (PL, Bundesliga, Serie A)
"""

import subprocess
import json
import re
from datetime import datetime
from pathlib import Path

TELEGRAM_CHAT_ID = "7733823361"
BOT_TOKEN = "8581242714:AAFjjOK2G4bf3SGi9FAGkdCJWsiznsLW8Vw"
STATE_FILE = "flashscore_state.json"

def load_state():
    """Load last known match state"""
    if Path(STATE_FILE).exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_matches": {}}

def save_state(state):
    """Save match state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def scrape_flashscore():
    """Scrape live matches from Flashscore"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            page.goto("https://www.flashscore.com/", timeout=20000)
            page.wait_for_timeout(2000)
            
            text = page.evaluate("() => document.body.innerText")
            browser.close()
            
            return extract_matches(text)
    except Exception as e:
        print(f"Scrape error: {e}")
        return {}

def extract_matches(text):
    """Extract live matches from page text"""
    matches = {}
    
    # Define league sections
    leagues = {
        "PL": ("Premier League", "ENGLAND"),
        "BL": ("Bundesliga", "GERMANY"),
        "SA": ("Serie A", "ITALY")
    }
    
    for league_key, (league_name, country) in leagues.items():
        if league_name in text:
            idx = text.find(league_name)
            section = text[idx:idx+1500]
            
            # Extract match patterns: "Team1 X-X Team2"
            match_pattern = r'(\w+[\s\w]*?)\s(\d+)\s-\s(\d+)\s(\w+[\s\w]*?)\n'
            found_matches = re.findall(match_pattern, section)
            
            if found_matches:
                matches[league_key] = found_matches[:3]  # Top 3 per league
    
    return matches

def format_telegram_message(matches, state):
    """Format message for Telegram"""
    message = "⚽ **FLASHSCORE HOURLY UPDATE**\n\n"
    
    time_str = datetime.now().strftime("%H:%M CET")
    message += f"🕐 *{time_str}*\n\n"
    
    league_names = {"PL": "🏴󐁧󐁢󐁥󐁮󐁧󐁿 Premier League", "BL": "🇩🇪 Bundesliga", "SA": "🇮🇹 Serie A"}
    
    if not matches:
        message += "ℹ️ No live matches at this hour\n"
        return message
    
    for league_key in ["PL", "BL", "SA"]:
        if league_key in matches and matches[league_key]:
            message += f"\n**{league_names[league_key]}**\n"
            
            for home, h_score, a_score, away in matches[league_key]:
                # Check if score changed
                match_key = f"{league_key}_{home}_vs_{away}"
                old_score = state.get("last_matches", {}).get(match_key, "0-0")
                
                status = "🔴 LIVE" if f"{h_score}-{a_score}" != old_score else "⚽"
                message += f"{status} {home} **{h_score}-{a_score}** {away}\n"
                
                # Update state
                state["last_matches"][match_key] = f"{h_score}-{a_score}"
    
    message += f"\n_Check again at {(int(time_str.split(':')[0])+1) % 24:02d}:00 CET_"
    return message

def send_telegram(message):
    """Send message to Telegram"""
    try:
        import requests
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=data, timeout=10)
        return response.ok
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def main():
    """Main execution"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting hourly check...")
    
    # Load state
    state = load_state()
    
    # Scrape matches
    matches = scrape_flashscore()
    
    # Format message
    message = format_telegram_message(matches, state)
    
    # Send if there are live matches
    if matches:
        send_telegram(message)
        print(f"✅ Sent {len(matches)} league updates")
    else:
        print("ℹ️ No live matches - quiet period")
    
    # Save state
    save_state(state)

if __name__ == "__main__":
    main()
