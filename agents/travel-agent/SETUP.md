# Travel Agent - Setup Guide

## Overview
Helps with flight check-ins:
1. **Reminders** - Alerts when check-in opens (24h before flight)
2. **Booking parsing** - Extracts info from confirmation emails
3. **Semi-automated check-in** - Opens browser, fills everything except passport

## Security Note
- **NO passport data stored** - You fill that manually
- Only stores: flight numbers, dates, booking refs, routes
- All data in local JSON file (not Git)

## How to Use

### Add a new trip manually:
```bash
cd ~/.openclaw/workspace/agents/travel-agent
python3 travel_agent.py
# Then provide details interactively
```

### Forward booking email:
Forward your booking confirmation to butti.nightrider@gmail.com with subject "FLIGHT BOOKING"

### List upcoming trips:
```bash
python3 travel_agent.py list
```

### Get check-in reminder:
Automatic - runs every hour, sends Telegram when check-in opens

### Prepare check-in (opens browser):
```bash
python3 checkin_helper.py 1
```
(Replace "1" with your trip ID)

## Supported Airlines
- SAS (SK)
- Swiss (LX)
- Lufthansa (LH)
- KLM (KL)
- Air France (AF)
- British Airways (BA)
- EasyJet (U2)
- Ryanair (FR)

## Files
- `travel_agent.py` - Main logic
- `checkin_helper.py` - Browser automation
- `travel_db.json` - Trip storage (no passport data!)
- `check_reminders.sh` - Cron wrapper
