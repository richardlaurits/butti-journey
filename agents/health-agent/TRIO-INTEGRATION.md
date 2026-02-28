# Trio DIY AID Integration Guide

**Richard's Setup:** Trio + Omnipod DASH + Dexcom G7 + Fiasp

## Data Export Options (in order of preference)

### Option 1: Nightscout (Recommended) ✅
**Status:** Trio supports direct integration
**Setup Time:** 20-30 minutes
**Cost:** Free (self-hosted or cloud)
**Data includes:** Glucose, insulin, carbs, predictions, settings

**How it works:**
1. Create Nightscout server (free options: Heroku/Railway/Fly.io)
2. Get your Nightscout URL + API_SECRET
3. In Trio app → Settings → Nightscout
4. Enter URL + API_SECRET
5. Enable "Allow Uploading to Nightscout"

**Integration path:**
```
Trio (iPhone)
    ↓
Nightscout API
    ↓
ButtiBot health-agent
    ↓
Weekly Telegram brief
```

**API endpoint:** `https://YOUR-NIGHTSCOUT-URL/api/v1/entries`

**What we can access:**
- CGM readings (glucose, trend)
- Insulin delivered
- Carbs entered
- Time in range calculations
- Loop predictions
- Settings

---

### Option 2: Apple Health ✅
**Status:** Trio supports direct write
**Setup Time:** 5 minutes
**Cost:** Free
**Data includes:** Glucose, insulin, carbs

**How it works:**
1. In Trio app → Settings → Apple Health
2. Toggle ON "Write to Apple Health"
3. Grant permissions in iPhone Settings → Health
4. Trio auto-syncs to HealthKit

**Integration path:**
```
Trio (iPhone)
    ↓
Apple HealthKit
    ↓
HealthKit export (XML/CSV)
    ↓
ButtiBot health-agent
    ↓
Weekly brief
```

**What we can access:**
- Blood glucose readings
- Insulin delivered (amount)
- Carbs entered
- Heart rate (from watch)
- Workouts
- Sleep

**Limitation:** Can only export via Health app (manual), not programmatic

---

### Option 3: Tidepool (Optional) 🔗
**Status:** Tidepool Mobile can upload from Apple Health
**Setup Time:** 10 minutes
**Cost:** Free (Tidepool account)
**Data includes:** Everything from Apple Health

**How it works:**
1. Trio → Apple Health (as above)
2. Tidepool Mobile app → reads Apple Health
3. Tidepool Mobile → uploads to Tidepool cloud
4. We access via Tidepool API

**Integration path:**
```
Trio → Apple Health → Tidepool Mobile → Tidepool API
```

---

## Recommended Setup (For Your Health Agent)

### Best Path: Nightscout + Apple Health

**Step 1: Set up Nightscout (One-time, 20 min)**
- Free hosting options:
  - Heroku (free tier)
  - Railway.app (free tier)
  - Fly.io (free tier)
  - PythonAnywhere
- Docs: https://nightscout.github.io/

**Step 2: Connect Trio to Nightscout**
- Trio Settings → Services → Nightscout
- Paste your Nightscout URL + API_SECRET
- Test connection
- Enable upload

**Step 3: Enable Trio → Apple Health** (parallel setup)
- Trio Settings → Apple Health
- Toggle ON "Write to Apple Health"
- Allows manual HealthKit export as backup

**Step 4: Tell me:**
1. Your Nightscout URL
2. Your Nightscout API_SECRET (keep private!)
3. Whether you want backup Apple Health export too

---

## What Your Data Looks Like

### Nightscout API Response
```json
{
  "entries": [
    {
      "type": "sgv",
      "sgv": 125,
      "trend": "Flat",
      "date": 1708027200000,
      "dateString": "2026-02-15T12:00:00Z"
    }
  ],
  "devicestatus": [
    {
      "pump": {
        "battery": 95,
        "iob": 2.5,
        "cob": 8
      },
      "uploader": {
        "battery": 72
      }
    }
  ]
}
```

### What Health Agent Will Calculate
- **TIR %** from glucose readings
- **Avg glucose** (daily/weekly)
- **Insulin delivered** totals
- **Carbs entered** patterns
- **Correlations** (TIR vs carbs, weight vs calories, etc)
- **Trends** (improving/declining)

---

## Implementation Timeline

**This week:**
1. Set up Nightscout (20 min)
2. Connect Trio → Nightscout
3. Give me URL + API_SECRET
4. I integrate Nightscout API into health-agent

**Next week:**
1. Add Apple Health export parser (backup)
2. Add Tidepool if interested
3. Deploy weekly Telegram briefs

---

## Security Notes

- Nightscout API_SECRET = like a password → keep private
- Don't share your full URL publicly
- Consider private Nightscout instance (not shared with followers)
- API key can be read-only or read-write

---

## Documentation Links

- **TrioDocs:** https://triodocs.org/
- **Trio Nightscout Setup:** https://triodocs.org/configuration/settings/services/nightscout/
- **Trio Apple Health:** https://triodocs.org/0.2.x/settings/services/applehealth/
- **Nightscout Project:** https://nightscout.info/
- **Tidepool Mobile:** https://www.tidepool.org/

---

## Quick Decision

**Choose one:**

Option A: **Nightscout only** (recommended, most data)
→ Setup time: 20 min → Full automation possible

Option B: **Apple Health + Tidepool** (backup option)
→ Setup time: 15 min → Manual export needed

Option C: **Apple Health only** (simplest)
→ Setup time: 5 min → Manual export weekly

**Let me know which you prefer and I'll guide you through setup!**
