# FANTASY FOOTBALL AGENTS - Master Guide

**[2026-02-14 12:08]** Created by Richard & ButtiBot

## 🏆 Three Specialized Agents

You now have **three separate fantasy football agents**, each optimized for their specific league:

1. **FPL Scout** (`agents/fpl-agent/`) - Premier League
2. **Bundesliga Scout** (`agents/bundesliga-agent/`) - German Bundesliga
3. **Serie A Scout** (`agents/seriea-agent/`) - Italian Serie A

---

## 📁 Structure

```
agents/
├── FANTASY-AGENTS-README.md  ← You are here
│
├── fpl-agent/
│   ├── IDENTITY.md            ← Agent personality
│   ├── RULES-2025-26.md       ← FPL scoring system
│   ├── MEMORY.md              ← Current squad & data
│   ├── data/                  ← Scraped data cache
│   └── reports/               ← Generated analysis
│
├── bundesliga-agent/
│   ├── IDENTITY.md
│   ├── RULES-2025-26.md       ← Bundesliga Fantasy rules
│   ├── MEMORY.md
│   ├── data/
│   └── reports/
│
└── seriea-agent/
    ├── IDENTITY.md
    ├── RULES-2025-26.md       ← World Fantasy Soccer rules
    ├── MEMORY.md              ← ⚠️ NEEDS YOUR INPUT!
    ├── data/
    └── reports/
```

---

## 🚀 How to Use

### Method 1: Ask ButtiBot (Easiest)

Just ask naturally in Telegram or webchat:

```
"Analyze my FPL team for GW27"
"Who should I captain in Bundesliga MD23?"
"Check Lautaro's form in Serie A"
"Compare Kane vs Haaland across all leagues"
```

ButtiBot will automatically:
1. Identify which agent(s) to use
2. Spawn the agent(s)
3. Run the analysis
4. Report back with recommendations

### Method 2: Specific Agent Request

```
"FPL Scout: Find me a differential under £7m"
"Bundesliga Scout: Optimize my star players for MD22"
"Serie A Scout: Check Inter fixtures for next 5 GW"
```

### Method 3: All Leagues (Weekly Review)

```
"Review all my fantasy teams for this weekend"
→ Spawns all 3 agents
→ Each analyzes their league
→ Combined report with priorities
```

---

## 📋 What Each Agent Does

### FPL Scout (Premier League)

**Specialties:**
- 2025/26 double-chip strategy
- Defensive points optimization (CBIT system)
- Price change tracking
- Mini-league rival analysis
- Differential hunting (<10% owned)

**Data Sources:**
- Official FPL API (team 17490)
- FPL FantasyScout
- FPL Football Hub
- Twitter (@OfficialFPL, @BenCrellin, @FPLRockstar)

**Key Metrics:**
- Ownership %
- Fixture difficulty (FDR)
- Points per 90 minutes
- Effective ownership (EO)
- Bonus points system (BPS + CBIT)

---

### Bundesliga Scout (German Bundesliga)

**Specialties:**
- Star player optimization (1.5x multiplier!)
- 5 transfers/week flexibility
- Dynamic price tracking
- Daily Bonus reminders
- Best-11 auto-selection strategy

**Data Sources:**
- Official Bundesliga Fantasy API
- Bundesliga.com stats
- Transfermarkt
- Kicker.de (German press)

**Key Metrics:**
- Average points (last 4 matches)
- Star player value (1.5x impact)
- Price trends (dynamic market)
- Fixture difficulty (next 3 MD)
- European fixture congestion

---

### Serie A Scout (Italian Serie A)

**Specialties:**
- Defensive football analysis
- Clean sheet value optimization
- Derby awareness (big matches)
- Form-over-fixtures approach
- Tactical understanding (Italian football)

**Data Sources:**
- World Fantasy Soccer platform
- Serie A official stats
- Football Italia
- Sofascore

**Key Metrics:**
- Clean sheet potential
- xG/xA (expected goals/assists)
- Penalty takers
- Form (last 5 matches)
- Big 4 bias (Inter/Juve/Milan/Napoli)

⚠️ **STATUS:** Needs your input on rules/squad!

---

## ⚡ Quick Commands

### Daily Checks (via ButtiBot)
```
"Any fantasy news overnight?"
→ Checks injuries, price changes, news across all 3 leagues

"Price changes tonight?"
→ FPL: FPL Statistics predictions
→ Bundesliga: Dynamic market updates
→ Serie A: [If applicable]
```

### Pre-Deadline
```
"FPL deadline prep" (before FPL GW deadline)
"Bundesliga transfers for MD[X]" (before matchday)
"Serie A captain pick GW[X]" (before gameweek)
```

### Post-Matchday
```
"Review my FPL GW[X] performance"
"Bundesliga MD[X] analysis - what went wrong?"
"Serie A GW[X] lessons learned"
```

---

## 🔄 Automated Scraping

**Planned (not yet active):**

### FPL (2x daily)
- **08:00 CET:** Overnight news, price changes, injuries
- **20:00 CET:** Lineup rumors, deadline prep, price predictions

### Bundesliga (2x daily)
- **08:00 CET:** Press conferences, injury updates
- **19:00 CET:** Pre-matchday briefing

### Serie A (1x daily)
- **09:00 CET:** Overnight news, tactical updates

**To activate:** Tell ButtiBot "Set up fantasy scraping cron jobs"

---

## 📊 Reports & Data

### Where Reports Are Saved

Each agent saves detailed analysis to:
```
agents/[league]-agent/reports/YYYY-MM-DD-topic.md
```

Example:
```
agents/fpl-agent/reports/2026-02-14-gw26-transfers.md
agents/bundesliga-agent/reports/2026-02-14-md22-star-players.md
```

### Where Data Is Cached

Fresh scraped data stored in:
```
agents/[league]-agent/data/
├── latest-squad.json
├── injuries-YYYY-MM-DD.json
├── prices-YYYY-MM-DD.json
└── [source]-feed-YYYY-MM-DD.md
```

**Retention:** Last 7 days kept, older archived

---

## 🎯 Setup Checklist

### ✅ Done (FPL)
- [x] FPL ID saved (17490)
- [x] 2025/26 rules documented
- [x] Data sources identified
- [x] Agent identity configured

### ✅ Done (Bundesliga)
- [x] League identified (Sandhems Bundesliga)
- [x] 2025/26 rules documented
- [x] Star player system understood
- [x] Known squad players logged

### ⚠️ Todo (Serie A)
- [ ] **URGENT:** Confirm World Fantasy Soccer rules
- [ ] Provide full 15-player squad
- [ ] League details (name, code, rank)
- [ ] Budget & free transfers
- [ ] Chips available

### 🔜 Next Steps (All)
- [ ] Test spawn each agent with real task
- [ ] Set up automated scraping cron jobs
- [ ] Integrate FPL API for auto squad-sync
- [ ] Add Bundesliga Fantasy API connection
- [ ] Create weekly review automation (Sunday evenings)

---

## 💡 Pro Tips

**For FPL:**
- Use defensive points CBIT to find value (Tarkowski-style players)
- Double chips = aggressive plays OK (you get them twice!)
- Track mini-league rivals' teams (check their transfers)

**For Bundesliga:**
- Star players = 30-50% of your score - optimize ruthlessly!
- 5 transfers/week = Don't be afraid to pivot hard
- Daily Bonus = Log in EVERY day for free budget

**For Serie A:**
- Clean sheets >> goals in Serie A
- Big 4 dominate = Stack Inter/Juve/Milan/Napoli
- Derby matches = high-variance, captain carefully

---

## 🆘 Troubleshooting

**"Agent doesn't have my latest squad"**
→ Update MEMORY.md in that agent's folder
→ Or: "Update [league] agent with latest squad"

**"Agent made wrong recommendation"**
→ Check RULES-2025-26.md is correct
→ Provide feedback: "That's wrong because..."
→ Agent learns and updates notes

**"Need to change agent personality"**
→ Edit IDENTITY.md in agent folder
→ Restart doesn't needed, loads fresh each spawn

---

## 📞 Support

Questions? Improvements? Ask ButtiBot:
```
"How do I update FPL agent's squad?"
"Make Bundesliga agent more aggressive"
"Serie A agent needs X feature"
```

---

**Created:** 2026-02-14 12:08 CET
**Maintained by:** ButtiBot
**Status:** 
- FPL: ✅ Ready
- Bundesliga: ✅ Ready (needs squad details)
- Serie A: ⚠️ Needs Richard's input before operational
