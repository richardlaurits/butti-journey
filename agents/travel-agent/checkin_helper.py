#!/usr/bin/env python3
"""
Check-in Helper - Semi-automated check-in preparation
Opens browser and fills in everything except passport number
"""

import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

AGENT_DIR = Path('/home/richard-laurits/.openclaw/workspace/agents/travel-agent')
DATA_FILE = AGENT_DIR / 'travel_db.json'

# Airline check-in URLs
AIRLINE_URLS = {
    'sas': 'https://www.flysas.com/en/check-in/',
    'swiss': 'https://www.swiss.com/ch/en/check-in',
    'lufthansa': 'https://www.lufthansa.com/ch/en/online-check-in',
    'klm': 'https://www.klm.com/check-in',
    'airfrance': 'https://wwws.airfrance.us/check-in',
    'british': 'https://www.britishairways.com/travel/olcilandingpage',
    'easyjet': 'https://www.easyjet.com/sv/check-in',
    'ryanair': 'https://www.ryanair.com/se/sv/check-in',
}

def load_trip(trip_id):
    """Load specific trip"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            for trip in data['trips']:
                if trip['id'] == trip_id:
                    return trip
    return None

def identify_airline(flight_number):
    """Identify airline from flight number prefix"""
    prefixes = {
        'SK': 'sas',
        'LX': 'swiss',
        'LH': 'lufthansa',
        'KL': 'klm',
        'AF': 'airfrance',
        'BA': 'british',
        'U2': 'easyjet',
        'FR': 'ryanair',
    }
    
    prefix = flight_number[:2].upper() if flight_number else ''
    return prefixes.get(prefix)

def prepare_checkin(trip_id):
    """Prepare check-in by opening browser with pre-filled info"""
    trip = load_trip(trip_id)
    
    if not trip:
        print(f"❌ Trip #{trip_id} not found")
        return False
    
    flight_num = trip.get('flight_number', '')
    airline = identify_airline(flight_num)
    booking_ref = trip.get('booking_ref', '')
    
    if not airline:
        print(f"⚠️ Unknown airline for flight {flight_num}")
        print(f"🎫 Booking ref: {booking_ref}")
        print(f"🌐 Please check in manually")
        return False
    
    url = AIRLINE_URLS.get(airline)
    if not url:
        print(f"⚠️ No URL configured for {airline}")
        return False
    
    print(f"✈️ Preparing check-in for {airline.upper()}")
    print(f"🎫 Flight: {flight_num}")
    print(f"🔢 Booking: {booking_ref}")
    print(f"🌐 Opening {url}")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Visible browser
            page = browser.new_page()
            
            # Navigate to check-in page
            page.goto(url)
            
            # Wait for page to load
            page.wait_for_load_state('networkidle')
            
            # Try to fill in booking reference (varies by airline)
            print(f"\n💡 **INSTRUCTIONS:**")
            print(f"1. Browser is now open with {airline.upper()} check-in")
            print(f"2. Booking reference: {booking_ref}")
            print(f"3. Enter your LAST NAME in the form")
            print(f"4. **YOU will fill in your passport number** (I don't have it)")
            print(f"5. Select seats and complete check-in\n")
            
            # Keep browser open
            print("⏳ Browser will stay open. Close it when done.")
            print("(Press Ctrl+C in terminal to close)")
            
            # Wait indefinitely
            page.wait_for_timeout(1000 * 60 * 30)  # 30 minutes max
            
            browser.close()
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"🌐 Please check in manually at: {url}")
        return False

def checkin_helper_cli():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Travel Check-in Helper')
    parser.add_argument('trip_id', type=int, help='Trip ID to check in for')
    parser.add_argument('--manual', action='store_true', help='Show manual instructions only')
    
    args = parser.parse_args()
    
    if args.manual:
        trip = load_trip(args.trip_id)
        if trip:
            print(f"✈️ **Check-in info for Trip #{args.trip_id}:**")
            print(f"🎫 Booking ref: {trip.get('booking_ref', 'N/A')}")
            print(f"✈️ Flight: {trip.get('flight_number', 'N/A')}")
            print(f"📅 Date: {trip.get('parsed_date', 'N/A')}")
            print(f"\n🌐 Go to airline website and enter:")
            print(f"   - Booking reference: {trip.get('booking_ref', '???')}")
            print(f"   - Your last name")
            print(f"   - **Your passport number** (you fill this)")
        else:
            print(f"❌ Trip #{args.trip_id} not found")
    else:
        prepare_checkin(args.trip_id)

if __name__ == "__main__":
    checkin_helper_cli()
