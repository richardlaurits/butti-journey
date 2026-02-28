# MEMORY.md - Health Agent

## Richard's Health Profile
**[2026-02-14]** Setup complete

### Physical Stats
- **Height:** 190 cm
- **Current Weight:** 85 kg
- **Current BMI:** ~23.6 (healthy range)
- **Body Fat Target:** -5% from current
- **Timeline:** 4 months (goal: "Best shape of my life")
- **Estimated Goal Weight:** ~80-82 kg (depending on muscle gain)

### Diabetes Management
**[2026-02-14]** Trio DIY AID setup

- **Type:** Type 1 since 1994
- **AID System:** Trio (open-source DIY)
  - Controls: Omnipod DASH (pump)
  - Input: Dexcom G7 (CGM)
  - Insulin: Fiasp (fast-acting)
- **TIR (Time in Range):** 95% (excellent control!)
- **Carb Logging:** Trio app (sporadic)
- **Daily Calories:** 2,400-2,600 kcal consumed
- **Daily Burn:** 2,600-3,000 kcal expended
- **Diet:** Low-carb, high-protein, high-quality fats

**Trio AID Notes:**
- Open-source system (great for data access!)
- Likely exports data to local/cloud
- Can integrate with Nightscout (common)
- Fiasp onset: ~10 min (vs Humalog 15-20 min)

### Training
- **Frequency:** 4-5 days/week strength training + 1-2 runs/week
- **Primary Focus:** Strength training
- **Secondary:** Running (endurance/conditioning)
- **Goal:** Maintain muscle while losing 5% body fat

### Data Tracking
**Carb/Nutrition:**
- Primary source: Omnipod AID app (carb logging, sporadic)
- Fallback: Manual notes/memory
- Status: Inconsistent logging

**Fitness:**
- Apple Watch Ultra 3 (HR, workouts, steps, calories)
- Manual strength training logs (?)
- GPS for runs

**Body Metrics:**
- Smart scale from Temu (weight, body fat %, muscle %, water %)
- Updates: Regular (frequency TBD)

**Blood Sugar:**
- Dexcom G7 (continuous glucose monitoring)
- AID: Omnipod DASH

### API Access Available
**✅ Dexcom API:**
- Free tier available
- Endpoint: https://api.dexcom.com
- Data: Real-time glucose, trends, TIR
- Status: Ready to integrate

**✅ Apple HealthKit:**
- Local export (XML/CSV)
- Watch data: Workouts, HR, steps, calories
- Method: Export from Health app or sync to cloud service
- Status: Ready to parse

**✅ Omnipod/AID Data:**
- Tidepool API (Omnipod + Dexcom integrated)
- Open Humans (data sharing platform)
- Status: Can explore

### Goals
**Primary:** Best shape of life in 4 months
**Secondary:** Maintain 95% TIR while losing body fat
**Tertiary:** Increase strength while reducing weight
**Timeline:** 4 months (Feb 2026 → June 2026)

### Reporting
**Frequency:** Weekly summary
**Metrics to Track:**
- TIR trends + variability
- Daily calories (consumed vs burned)
- Workout volume + intensity
- Body weight + body fat %
- Strength progression (lifts)
- Recovery metrics (HR variability, sleep)
- Weekly recommendations

### Data Storage
- Weekly summaries saved to JSON
- Trends calculated month-over-month
- Alerts for anomalies (low TIR, unusual weight, etc)

---

## Integration Plan

**[2026-02-14]** Trio data export options researched & documented

**Available Options:**

**Option 1: Nightscout** (Recommended) ⭐
- Setup time: 20 minutes
- Cost: Free (self-hosted on Railway.app, Fly.io, Heroku)
- Data access: Full API to glucose, insulin, carbs, predictions, settings
- Automation: Full programmatic access
- Path: Trio app → Nightscout server → ButtiBot API integration
- Status: READY (awaiting Richard's Nightscout URL + API_SECRET)

**Option 2: Apple Health** (Parallel/Backup)
- Setup time: 5 minutes
- Cost: Free
- Data access: Glucose, insulin, carbs, HR, workouts, sleep
- Export method: Manual weekly via iPhone Health app
- Status: Ready (can enable in Trio settings anytime)

**Option 3: Tidepool** (Optional)
- Setup time: 10 minutes
- Uses Apple Health as data source
- Tidepool Mobile app bridges to cloud
- Status: Optional, can add later

### Week 1: MVP (Minimum Viable Product)
1. ✅ Manual data import (weight, workouts)
2. ✅ Calculate weekly trends
3. ✅ Generate first weekly summary

### Week 2: Nightscout Integration (Target)
1. Richard sets up Nightscout server (20 min)
2. Connects Trio → Nightscout (Settings → Services)
3. ButtiBot integrates Nightscout API
4. Automated glucose + insulin tracking begins

### Week 3: Apple Health Integration
1. Enable Trio → Apple Health (5 min in Trio settings)
2. Parse HealthKit export (manual or via HealthKit export)
3. Correlate with Nightscout data
4. Complete health picture (glucose + carbs + workouts + HR)

### Week 4+: Automation & Insights
1. Automated weekly brief to Telegram
2. Anomaly alerts (TIR drops, unusual weight, etc)
3. Correlation analysis (TIR vs carbs, weight vs calories, etc)
4. Smart recommendations ("5% BF loss on pace for May 28")
5. Trend projections

---

**Created:** 2026-02-14
**Status:** Phase 1 ready, awaiting Nightscout setup details
