#!/usr/bin/env python3
"""
Travel Agent - Flight Check-in Assistant
Helps with flight reminders and semi-automated check-in
Phase 1: Reminders + Booking parsing
Phase 2: Semi-automated check-in (user fills passport manually)
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

AGENT_DIR = Path('/home/richard-laurits/.openclaw/workspace/agents/travel-agent')
DATA_FILE = AGENT_DIR / 'travel_db.json'

def load_travels():
    """Load saved trips"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"trips": [], "last_check": None}

def save_travels(data):
    """Save trips to file"""
    AGENT_DIR.mkdir(exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def parse_booking_email(email_text):
    """Extract flight details from booking confirmation email"""
    
    # Common patterns in booking confirmations
    patterns = {
        'booking_ref': r'(?:Booking|Reservation|Confirmation) (?:Reference|Number|#)[:\s]*([A-Z0-9]{5,8})',
        'flight_number': r'(?:Flight|Vol)[:\s]*([A-Z]{2,3}\d{2,4})',
        'airline': r'(?:Airline|Compagnie|Operated by)[:\s]*([A-Za-z\s]+?)(?:\n|$)',
        'departure_date': r'(?:Departure|Date)[:\s]*(\d{1,2}[\s\-/\.][A-Za-z]{3,9}[\s\-/\.]\d{2,4})',
        'route': r'(?:Route|From|To)[:\s]*([A-Z]{3})\s*(?:to|→|->|-)\s*([A-Z]{3})',
        'passenger': r'(?:Passenger|Name)[:\s]*([A-Za-z\s\-]+)',
    }
    
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, email_text, re.IGNORECASE)
        if match:
            extracted[key] = match.group(1).strip()
    
    # Try to parse date
    if 'departure_date' in extracted:
        date_str = extracted['departure_date']
        # Common formats: 15 Mar 2026, 15/03/2026, 2026-03-15
        try:
            # Try various formats
            for fmt in ['%d %b %Y', '%d %B %Y', '%d/%m/%Y', '%Y-%m-%d', '%d.%m.%Y']:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    extracted['parsed_date'] = parsed.isoformat()
                    break
                except:
                    continue
        except:
            pass
    
    return extracted

def calculate_checkin_time(departure_date_str):
    """Calculate when check-in opens (usually 24-48h before)"""
    try:
        dep_date = datetime.fromisoformat(departure_date_str)
        # Most airlines open 24h before, some 48h
        checkin_opens = dep_date - timedelta(hours=24)
        return checkin_opens.isoformat()
    except:
        return None

def add_trip(booking_info):
    """Add new trip to database"""
    data = load_travels()
    
    trip = {
        "id": len(data['trips']) + 1,
        "added": datetime.now().isoformat(),
        **booking_info,
        "checkin_reminder_sent": False,
        "checkin_completed": False
    }
    
    if 'parsed_date' in booking_info:
        trip['checkin_opens'] = calculate_checkin_time(booking_info['parsed_date'])
    
    data['trips'].append(trip)
    save_travels(data)
    
    return trip

def get_upcoming_trips(days_ahead=7):
    """Get trips in the next X days"""
    data = load_travels()
    upcoming = []
    
    now = datetime.now()
    cutoff = now + timedelta(days=days_ahead)
    
    for trip in data['trips']:
        if 'parsed_date' in trip:
            trip_date = datetime.fromisoformat(trip['parsed_date'])
            if now <= trip_date <= cutoff:
                upcoming.append(trip)
    
    return upcoming

def check_checkin_reminders():
    """Check if any check-ins are opening soon"""
    data = load_travels()
    reminders = []
    now = datetime.now()
    
    for trip in data['trips']:
        if trip.get('checkin_completed'):
            continue
            
        if 'checkin_opens' in trip:
            checkin_time = datetime.fromisoformat(trip['checkin_opens'])
            
            # Reminder when check-in opens (within last hour)
            if checkin_time <= now <= checkin_time + timedelta(hours=1):
                if not trip.get('checkin_reminder_sent'):
                    reminders.append(trip)
                    trip['checkin_reminder_sent'] = True
    
    save_travels(data)
    return reminders

def format_trip_summary(trip):
    """Format trip info for display"""
    lines = []
    lines.append(f"✈️ **Resa #{trip['id']}**")
    
    if 'route' in trip:
        lines.append(f"🛫 {trip.get('from', '???')} → {trip.get('to', '???')}")
    
    if 'parsed_date' in trip:
        dep = datetime.fromisoformat(trip['parsed_date'])
        lines.append(f"📅 {dep.strftime('%A %d %B %Y, %H:%M')}")
    
    if 'flight_number' in trip:
        lines.append(f"✈️ Flight: {trip['flight_number']}")
    
    if 'airline' in trip:
        lines.append(f"🏢 Airline: {trip['airline']}")
    
    if 'booking_ref' in trip:
        lines.append(f"🎫 Bokningsnr: {trip['booking_ref']}")
    
    if 'checkin_opens' in trip:
        checkin = datetime.fromisoformat(trip['checkin_opens'])
        lines.append(f"⏰ Check-in öppnar: {checkin.strftime('%A %d %B, %H:%M')}")
    
    return "\n".join(lines)

def format_reminder(trip):
    """Format check-in reminder message"""
    lines = []
    lines.append("🔔 **Dags att checka in!**")
    lines.append("")
    lines.append(format_trip_summary(trip))
    lines.append("")
    lines.append("💡 **Så här checkar du in:**")
    lines.append(f"1. Gå till flygbolagets hemsida")
    lines.append(f"2. Ange bokningsreferens: {trip.get('booking_ref', '???')}")
    lines.append(f"3. Fyll i ditt efternamn")
    lines.append(f"4. Fyll i passnummer (jag har inte detta)")
    lines.append("")
    lines.append("Eller skicka bokningsbekräftelsen till mig så förbereder jag check-in!")
    
    return "\n".join(lines)

def main():
    """Main function for testing"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'reminders':
        # Check for reminders
        reminders = check_checkin_reminders()
        if reminders:
            for trip in reminders:
                print(format_reminder(trip))
                print("\n" + "="*50 + "\n")
        else:
            print("✅ Inga påminnelser just nu.")
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'list':
        # List upcoming trips
        trips = get_upcoming_trips(30)
        if trips:
            print("📅 **Kommande resor:**\n")
            for trip in trips:
                print(format_trip_summary(trip))
                print("")
        else:
            print("📭 Inga kommande resor hittades.")
    
    elif len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test parsing with sample email
        sample = """
        Booking Reference: ABC123
        Flight: SK1234
        Airline: SAS Scandinavian Airlines
        Departure Date: 15 Mar 2026
        Route: GVA-ARN
        Passenger: Richard Laurits
        """
        
        parsed = parse_booking_email(sample)
        print("🧪 Test parsing:")
        print(json.dumps(parsed, indent=2))
        
        # Add test trip
        trip = add_trip(parsed)
        print(f"\n✅ Testresa tillagd! ID: {trip['id']}")

if __name__ == "__main__":
    main()
