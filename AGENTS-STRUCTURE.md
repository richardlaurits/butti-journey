# Agent Structure - Richard's Workspace

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RICHARD'S AGENT ECOSYSTEM                       │
└─────────────────────────────────────────────────────────────────────────┘

                              MAIN SESSION
                             (ButtiBot in
                            Telegram/Web)
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
         ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
         │ FANTASY AGENTS │ │ CAREER AGENT │ │ HEALTH AGENT   │
         │    (Sports)    │ │   (Work)     │ │  (Fitness)     │
         └────────────────┘ └──────────────┘ └────────────────┘
              │                  │                   │
      ┌───────┼───────┐          │                   │
      │       │       │          │                   │
      ▼       ▼       ▼          ▼                   ▼
    ┌───┐  ┌───┐  ┌───┐      ┌─────────┐        ┌────────────┐
    │FPL│  │BUN│  │SER│      │CAREER   │        │HEALTH      │
    │   │  │   │  │   │      │SCOUT    │        │DASHBOARD   │
    └───┘  └───┘  └───┘      │         │        │            │
     PL    BL    SA          │API:     │        │API:        │
   17490               │ Indeed │        │Dexcom │
                        │LinkedIn│        │ Apple  │
                        │AF.se   │        │ Health │
                        └─────────┘        │MFP     │
                                          └────────────┘

```

---

## Current Agents (✅ LIVE)

### 1. **FPL Agent** ⚽ (Fantasy Football - Premier League)
- **ID:** `agents/fpl-agent/`
- **Team:** FC MACCHIATO (17490)
- **Function:** Analyze team, mini-leagues, GW picks, next-GW recommendations
- **Model:** Haiku (fast + cheap)
- **Update Freq:** On-demand (spawn)
- **Data:** Official FPL API (bootstrap-static, entry, fixtures)
- **Output:** Telegram alerts + detailed analysis

### 2. **Bundesliga Agent** ⚽ (Fantasy Football - German)
- **ID:** `agents/bundesliga-agent/`
- **League:** Sandhems Bundesliga (5th place)
- **Function:** BL Fantasy analysis (same as FPL)
- **Model:** Haiku
- **Data:** Official Bundesliga Fantasy API
- **Status:** ✅ Ready, needs more game data

### 3. **Serie A Agent** ⚽ (Fantasy Football - Italian)
- **ID:** `agents/seriea-agent/`
- **Team:** Pick Team $ 1.2 (#98 world rank!)
- **Platform:** World Fantasy Soccer (https://worldfantasysoccer.com/season/20153)
- **Function:** Serie A fantasy analysis (same as FPL/Bundesliga)
- **Model:** Haiku
- **Update Freq:** On-demand (spawn)
- **Status:** ✅ READY TO USE

### 4. **Career Agent** 💼 (NEW - In Progress)
- **ID:** `agents/career-agent/`
- **Purpose:** Find ideal jobs + optimize applications
- **Functions:**
  - Monitor 10+ job boards (Indeed, Monster, Jobs.ch, Arbetsförmedlingen, etc)
  - Score jobs against your criteria (0-10)
  - Generate personalized cover letters
  - Manage resume versions
  - Track applications
- **Model:** Haiku
- **APIs:** 
  - ✅ Indeed (awaiting your key)
  - ✅ Arbetsförmedlingen (Swedish)
  - ✅ LinkedIn email parsing (awaiting alerts setup)
- **Output:** Telegram job alerts, draft cover letters
- **Status:** 🔧 Framework ready, awaiting: resume + cover letter template

---

## Active Agents (🔧 IN-PROGRESS)

### 5. **Health Agent** 💪 (NEW - Phase 1)
- **ID:** `agents/health-agent/`
- **Purpose:** Track fitness, nutrition, diabetes management
- **Metrics:**
  - TIR tracking (Dexcom G7)
  - Workout logging (type, volume, intensity)
  - Nutrition tracking (calories, macros, quality)
  - Body composition (weight, body fat %)
  - Strength progression
  - Recovery metrics
- **APIs:** 
  - Dexcom (blood sugar)
  - Apple HealthKit (workouts, HR, steps)
  - MyFitnessPal (nutrition, if used)
  - Whoop/Oura (optional)
- **Analysis:**
  - Weekly brief
  - TIR trends + correlations
  - Calorie deficit analysis
  - Strength progression
  - Body composition trajectory
  - Personalized recommendations
- **Output:** Weekly health brief to Telegram + alerts for anomalies
- **Status:** 🔧 Phase 1 ready (manual tracking), phases 2-3 next week

---

## Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    EXTERNAL DATA SOURCES                     │
└──────────────────────────────────────────────────────────────┘
        │                │                │                │
        ▼                ▼                ▼                ▼
    ┌────────┐       ┌────────┐      ┌────────┐       ┌─────────┐
    │  FPL   │       │ Career │      │Dexcom  │       │ Apple   │
    │  API   │       │  APIs  │      │  API   │       │ Health  │
    └────────┘       └────────┘      └────────┘       └─────────┘
        │                │                │                │
        └────────────────┼────────────────┼────────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │  AGENT PROCESSORS          │
            │  (spawn sub-agents)        │
            └────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │  DATA STORAGE              │
            │  (JSON + memory files)     │
            └────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────────┐
            │  TELEGRAM OUTPUT           │
            │  (alerts + briefs)         │
            └────────────────────────────┘
```

---

## File Organization

```
~/.openclaw/workspace/
├── agents/
│   ├── fpl-agent/
│   │   ├── IDENTITY.md
│   │   ├── MEMORY.md
│   │   ├── RULES-2025-26.md
│   │   └── data/
│   │
│   ├── bundesliga-agent/
│   │   ├── IDENTITY.md
│   │   ├── MEMORY.md
│   │   └── RULES-2025-26.md
│   │
│   ├── seriea-agent/
│   │   ├── IDENTITY.md
│   │   ├── MEMORY.md
│   │   └── RULES-2025-26.md
│   │
│   ├── career-agent/
│   │   ├── IDENTITY.md
│   │   ├── MEMORY.md
│   │   ├── fetch-jobs-api.py
│   │   ├── generate-cover-letter.py
│   │   ├── job-monitor.py
│   │   ├── resume/
│   │   ├── templates/
│   │   ├── data/
│   │   └── job-monitor-config.json
│   │
│   ├── health-agent/  (PLANNED)
│   │   ├── IDENTITY.md
│   │   ├── MEMORY.md
│   │   ├── health-tracker.py
│   │   ├── dexcom-sync.py
│   │   ├── healthkit-parser.py
│   │   └── data/
│   │
│   └── FANTASY-AGENTS-README.md
│
├── MEMORY.md
├── SOUL.md
├── IDENTITY.md
├── USER.md
├── HEARTBEAT.md
└── skills/
    └── gmail/
```

---

## Agent Communication Pattern

```
┌─────────────┐
│ Richard (YOU)
└──────┬──────┘
       │ 
       │ "Run FPL analysis"
       │
       ▼
┌──────────────────────────┐
│  Main Session (ButtiBot)  │
│  Command: sessions_spawn  │
└──────────────────────────┘
       │
       │ spawn → fpl-agent
       │
       ▼
┌──────────────────────────┐
│ FPL Agent (subprocess)    │
│ - Fetch API data          │
│ - Analyze GW              │
│ - Generate insights       │
└──────────────────────────┘
       │
       │ Return results
       │
       ▼
┌──────────────────────────┐
│ Main Session → Telegram   │
│ "Here's your FPL brief"   │
└──────────────────────────┘
```

---

## What's Missing / Next Steps

| Agent | Status | Blocker |
|-------|--------|---------|
| FPL | ✅ LIVE | None |
| Bundesliga | ✅ READY | More game data |
| Serie A | ✅ READY | Complete! (#98 world rank) |
| Career | 🔧 IN-PROGRESS | Resume + cover letter template + Indeed key |
| Health | 📋 PROPOSED | Your health tracking preferences |

---

## Suggested Additional Agents (Future)

1. **Email Agent** 📧
   - Smart inbox management
   - Auto-categorize + prioritize

2. **Calendar Agent** 📅
   - Meeting prep
   - Time blocking
   - Conflict detection

3. **Investment Agent** 💰
   - Stock/crypto tracking
   - Portfolio analysis

4. **News Agent** 📰
   - AI/Tech curated
   - Relevant to your interests

5. **Smart Home Agent** 🏠
   - Camera monitoring
   - Temperature/lights

---

**Ready to build the health agent next?** Just tell me your answers to those 6 questions! 💪
