# Health Agent 💪

**Mission:** Track health metrics, optimize performance, achieve best shape goal

## Goal
**Best shape of life in 4 months** (Feb 14 → June 14, 2026)
- Current: 85 kg, ~20% body fat
- Target: Lose 5% body fat while maintaining/building strength
- Daily: 2,400-2,600 kcal consumed, 2,600-3,000 kcal burned

## Data Sources

### ✅ Ready Now
1. **Apple Watch Ultra 3**
   - Workouts (strength, running)
   - Heart rate, steps, calories burned
   - Sleep data
   - Method: HealthKit export (XML)

2. **Manual Input**
   - Daily weight (from Temu smart scale)
   - Body fat % (scale reading)
   - Workout logs (if needed)

3. **Omnipod DASH AID**
   - Carb logs (sporadic, in app)
   - Insulin deliveries

### ⏳ Integration Ready
1. **Dexcom G7 API** (Free tier available)
   - Real-time glucose
   - TIR tracking
   - Trends
   - Setup: OAuth registration

## Structure

```
agents/health-agent/
├── IDENTITY.md              # Agent identity
├── MEMORY.md                # Richard's health profile + goals
├── README.md                # This file
│
├── health-tracker.py        # Main health tracking system
├── dexcom-sync.py          # Dexcom API integration
├── healthkit-parser.py     # Apple HealthKit data parser
│
├── config/
│   └── dexcom-tokens.json  # OAuth tokens (auto-created)
│
├── data/
│   ├── weekly-YYYY-MM-DD.json    # Weekly summaries
│   └── healthkit-YYYY-MM-DD.json # Parsed watch data
│
└── templates/
    └── weekly-brief.md     # Template for Telegram brief
```

## Usage

### Phase 1: Manual Data (Now Active)
```bash
python3 agents/health-agent/health-tracker.py
```
Add daily data:
- Weight (from scale)
- Calories (consumed + burned)
- Workouts (type, duration)
- Blood sugar (Dexcom export)

### Phase 2: Apple Watch Integration
```bash
# Export from Health app → apple_health_export/export.xml
python3 agents/health-agent/healthkit-parser.py
```
Auto-extracts:
- Workouts
- Heart rate
- Steps
- Sleep

### Phase 3: Dexcom Real-Time
```bash
python3 agents/health-agent/dexcom-sync.py
```
One-time OAuth setup:
1. Register Dexcom developer account (free)
2. Create OAuth app
3. Run script for interactive auth
4. Tokens saved automatically

## Weekly Summary

**Sent to Telegram every Sunday**

```
📊 Weekly Health Brief

Weight & Body:
- Start/End weight
- Weight change
- Trend analysis

Calories:
- Avg consumed/burned
- Deficit summary

Diabetes (TIR):
- Avg TIR %
- Glucose trends

Training:
- Workout count
- Type breakdown
- Intensity summary

Progress:
- On track toward goal?
- Timeline projection
- Recommendations
```

## Metrics Tracked

| Metric | Source | Frequency |
|--------|--------|-----------|
| Weight | Temu scale | Daily |
| Body Fat % | Temu scale | Daily |
| Calories In | Manual/AID | Daily |
| Calories Out | Apple Watch | Daily |
| TIR | Dexcom | Real-time |
| Avg Glucose | Dexcom | Daily |
| Workouts | Apple Watch | Per session |
| Heart Rate | Apple Watch | Real-time |
| Steps | Apple Watch | Daily |
| Sleep | Apple Watch | Daily |

## Goals & Targets

**Primary Goal:** 5% body fat loss in 4 months
- Pace: ~1.25% per month
- Method: Caloric deficit + strength training

**Secondary:** Maintain 95% TIR while cutting
- Currently: 95% (excellent!)
- Target: ≥92% while losing weight

**Tertiary:** Increase strength
- Minimize muscle loss during cut
- 4-5 days/week strength training
- High protein diet

## Smart Features

### Correlation Analysis
- "TIR drops after high-carb days"
- "Weight increases on low sleep nights"
- "Calorie deficit impacts recovery"

### Anomaly Alerts
- TIR drops below 90%
- Unexpected weight gain
- Missed workouts

### Progress Projections
- "At current pace, goal achieved by May 28"
- "Need +500 kcal deficit/week for June 14 target"
- "Strength up 8% — muscle preservation on track"

## Setup Steps

### Right Now
1. ✅ MEMORY.md created with your profile
2. ✅ health-tracker.py ready for manual data
3. Add your first daily entry (weight, workouts)

### This Week
1. Export Apple HealthKit (Health app → Export Health Data)
2. Run HealthKit parser
3. Auto-extract workouts + metrics

### Next Week
1. Register Dexcom developer account (free)
2. Set up OAuth
3. Live TIR tracking begins

## Commands

```bash
# Add daily data (manual)
python3 agents/health-agent/health-tracker.py

# Parse Apple Watch data
python3 agents/health-agent/healthkit-parser.py

# Set up Dexcom
python3 agents/health-agent/dexcom-sync.py

# View this week's summary
cat agents/health-agent/data/weekly-latest.json | jq .summary
```

## Dexcom API Setup (Free Tier)

1. Go to: https://developer.dexcom.com/
2. Sign up (free)
3. Create new OAuth app
4. Get Client ID + Secret
5. Run: `python3 agents/health-agent/dexcom-sync.py`
6. Approve OAuth consent

Takes ~5 minutes. No cost.

---

**Status:** Phase 1 active (manual tracking)
**Next:** Apple HealthKit integration (this week)
**Target:** Dexcom live integration (next week)
