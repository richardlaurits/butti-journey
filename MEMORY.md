# MEMORY.md - Long-Term Memory

## First Contact
**2026-02-07** - Första konversationen. Richard introducerade sig själv och gav mig namnet ButtiBot.

## Key Facts
**[2026-02-14]** Arthur fyllde 7 år den 11 februari 2026
**[2026-02-07]** Richard cyklar till jobbet måndag-torsdag, 3,8 km varje väg
**[2026-02-07]** Familjen har bott i Schweiz i 6 år men är svenskar
**[2026-02-07]** Richards diabetes är mycket välkontrollerad (95% TIR)

## Family
**[2026-02-23]** Jan Laurits (Richards pappa)
- Born: 1954 (71 år)
- Email: janlaurits@icloud.com
- Location: Rosengatan 2a, 41310 Göteborg, Sverige
- Contact: Responsive, friendly, asks about weather, Olympics, investments
- Daily greeting: ✅ 10:00 CET every morning (via system crontab)
- Script: `skills/gmail/daily_greeting_jan.py`
- Log: `skills/gmail/jan_greeting_log.json`
- Status: ✅ LIVE (set up 2026-02-23 19:44 CET)
- Features:
  - Random funny GIF each email
  - Weather snippet (always included)
  - Alternating motivation: Movement/exercise OR learning new computer
  - Professional signature: "🤖 ButtiBot - 24/7 Digital Assistant for Richard Laurits"

## Current Date Reference
**[Updated 2026-02-14 11:49 CET]** Idag är lördag 14 februari 2026
- Arthur's 7th birthday: 11 februari 2026 (3 dagar sedan)

## Gmail Access
**[2026-02-18 19:43 CET]** Dual-account Gmail setup LIVE

**Account 1: butti.nightrider@gmail.com**
- App Password: `jlcylboroggobdhj` (stored in `skills/gmail/app_password.txt`)
- IMAP: ✅ Read emails
- SMTP: ✅ Send emails (from this account)
- Status: ✅ Live

**Account 2: richardlaurits@gmail.com**
- App Password: `skills/gmail/richard_personal_app_password.txt`
- IMAP: ✅ Read all Richard's emails (138K+ in inbox)
- SMTP: ❌ BLOCKED (security - cannot send from Richard's account)
- Status: ✅ Live

**[2026-02-23 19:35 CET]** OAuth replaced with IMAP + App Passwords
- Old method: OAuth (token expired 2026-02-19)
- New method: IMAP + app passwords (no token expiration)
- Script: `skills/gmail/gmail_monitor_imap.py` (rebuilt)
- Status: ✅ Tested working, heartbeat updated

**Security Rules:**
- ❌ Cannot modify Richard's account, send from it, or spam
- ✅ Can only read Richard's emails
- ✅ Sends responses ONLY from butti.nightrider@gmail.com

**Monitor Scripts:**
1. `gmail_monitor_imap.py` — checks YOUR inbox (richardlaurits@gmail.com)
   - Filters: ⭐ Pernilla, 💰 Invoices, 🏦 Banks, 📅 Calendar, ❗ Urgent
   - Runs via heartbeat (every 30 min)
   - Returns: Alert list or `HEARTBEAT_OK`

2. `auto_responder.py` — manages MY inbox (butti.nightrider@gmail.com)
   - Auto-responds to unread emails
   - Classifies: Confirmations, notifications, inquiries
   - Ignores: Newsletters, marketing, automated notifications
   - Logs: All sent responses to `auto_responder_log.json`
   - Runs via heartbeat (every 30 min)

**📧 EMAIL RESPONSE RULES (Foundation - Always Follow):**

**✅ AUTO-RESPOND (No approval needed):**
- Emails written DIRECTLY TO butti.nightrider@gmail.com
- Emails FROM Richard himself (richardlaurits@gmail.com)
- Standard responses: confirmations, thank-yous, information requests

**❌ NEVER RESPOND (Always ask Richard first):**
- Forwarded emails from other people (even if sent by Richard)
- Emails involving sensitive decisions, money, legal matters
- Emails requiring Richard's personal input/opinion
- Any email where sender might think Richard (not ButtiBot) is responding

**📝 Process:**
1. Check if email is DIRECT to me or FROM Richard
2. If YES → Auto-respond appropriately
3. If FORWARDED or UNCLEAR → Alert Richard, wait for instructions

**Rule updated:** 2026-02-24 10:45 CET

## Morning Brief (Automated) **[UPDATED 2026-02-24]**

**[2026-02-24 00:00 CET]** Complete redesign - comprehensive daily briefing

- **Tid:** 07:00 CET dagligen
- **Kanal:** Telegram
- **Trigger:** Cron (`0 7 * * *`)

**Sektioner:**
1. 🤖 **Agent Status** - Hälsa på FPL, Bundesliga, Career, Health agenter
2. 🌤️ **Väder** - Prangins + Eysins (Vaud) för dagen
3. 📍 **Lokalt** - Relevanta nyheter Prangins/Nyon/Vaud
4. 🤖 **AI Nyheter** - 3-5 bullets senaste 24h
5. 🌍 **Världsnyheter** - 3-5 bullets senaste 24h
6. 📧 **Viktiga Email** - Olästa viktiga mejl (Pernilla, kalender, bank)
7. 🌙 **Inatt** - Vad som hände under natten
8. 📋 **Idag** - Planerade uppgifter
9. 💡 **3 Förslag** - Roterande förslag på vad jag kan göra

**FPL inom Morning Brief:**
- Agent status (när nästa analys körs)
- Inte full analys (den körs separat 24h innan deadline)

## Health Agent
**[2026-02-14 19:29]** Health agent created and configured
**[2026-02-14 19:37]** Trio DIY AID setup documented

**Richard's Health Profile:**
- Height: 190 cm | Weight: 85 kg
- Goal: -5% body fat in 4 months (by June 14, 2026)
- TIR: 95% (maintaining during fat loss)
- Training: 4-5x/week strength + 1-2x running
- Diet: Low-carb, high-protein, high-quality fats
- Daily: 2,400-2,600 kcal consumed, 2,600-3,000 kcal burned

**Diabetes Management (Type 1 since 1994):**
- **AID System:** Trio (open-source DIY AID)
  - Pump: Omnipod DASH
  - CGM: Dexcom G7
  - Insulin: Fiasp (fast-acting, ~10 min onset)
- **Control:** Excellent (95% TIR)
- **Data:** Trio exports data (can integrate Nightscout/APIs)

**Data Sources:**
- ✅ Apple Watch Ultra 3 (workouts, HR, steps, sleep)
- ✅ Temu smart scale (weight, body fat %)
- ✅ Trio AID app (carbs, insulin, blood sugar)
- ✅ Dexcom G7 data (via Trio)

**Integration Phases:**
1. **Phase 1 (NOW):** Manual data input + weekly summary generation ✅
2. **Phase 2 (This week):** Nightscout API integration (Richard sets up server, 20 min)
3. **Phase 3 (Next week):** Apple Health export parser + correlations
4. **Phase 4:** Automated weekly Telegram briefs + anomaly alerts

**Trio Data Export Options:**
- ✅ **Nightscout** (Recommended): Full API, 20 min setup, free hosting
- ✅ **Apple Health**: 5 min setup, manual export weekly
- ✅ **Tidepool**: Optional, uses Apple Health as bridge

**Agent Status:** 🔧 Phase 1 ready, awaiting first data entry
**Location:** `agents/health-agent/`

## Agent Architecture **[NEW 2026-02-24]**

**System Maturity:** 55% (upgraded from 38%)

**Architecture:** Coordinator (main) + Specialized Sub-Agents

**Active Automation:**
- **Morning Brief:** Dagligen 07:00 (komplett briefing)
- **FPL Analysis:** 24h innan varje GW deadline (smart scheduling via Söndags-koll)
- **Bundesliga Check:** Fredagar 10:00 (inför helgens omgång)
- **Career Scan:** Fredagar 09:00 (veckans jobb)
- **Jan's Greeting:** Dagligen 10:00

**Manual/On-Demand:**
- Health Agent (väntar på data)
- Serie A Agent (screenshot-baserad)

**Supervisor:** Jag agerar koordinator, inte dedikerad supervisor agent (efficient for current scale)

## Fantasy Football Intel System

**[2026-02-23 19:36 CET]** SETUP COMPLETE - Squad-focused alerts

**FPL (Nightly 11 PM CET)**
- Team: FC MACCHIATO (ID 17490)
- Players tracked: Haaland, Gabriel, Rice, Timber, Saka, Son, Salah, Guéhi, Solanke, Hill, Thiago
- Alert on: Injuries, suspensions, breaking news
- Script: `agents/fpl-agent/nightly-scraper.py`

**Bundesliga (Friday 8 AM CET)**
- Players tracked: Kane, Díaz, Baumgartner, García, Burger, Olise, Kabak, Grimaldo, Coufal, Schlotterbeck, Schwäbe
- Alert on: Current week injuries/suspensions (max 7 days old)
- Sources: bulinews.com/fantasy (primary), Bundesliga official, team news
- Script: `agents/bundesliga-agent/friday-scraper.py`

**Serie A (Manual Weekly)**
- Players tracked: L Martínez, Dimarco, Yildiz, Paz, Leão, Modrić, Mandragora, etc.
- You upload: Weekly screenshot
- I check: Roster changes, injuries, transfers
- Store: `agents/seriea-screenshots/`

**KILLED:** Daily standings, league positions, mini-league tracking, cron briefs (voice greeting only now)

## Fantasy Football Ligor & Ställningar

### Bundesliga (Sandhems Bundesliga)
- **Lag:** Mitt lag (namn?)
- **Position:** 5:e plats (60,621 poäng)
- **Mål:** Top 3
- **Gap till #1:** +4,562 pts, till #4: -77 pts
- **Omgångar kvar:** 13-15
- **Konkurrenter:** Baxus (#1), Fysio FC (#2), Marsalito4 (#3), FantasyStatsAndStrategy (#4)

### Premier League (FPL Mini-League - "Funa-ligan")
**[2026-02-18 20:30 CET] GW28 TRANSFERS CONFIRMED:**
- OUT: J.Timber (Arsenal) → IN: Hill (Bournemouth) ✅
- OUT: Calvert-Lewin (Leeds) → IN: Thiago (Brentford) ✅
- Free transfers: 2/4 used
- Bank: £1.0m remaining
- Deadline: Fri 27 Feb, 19:30 CET

**[2026-02-18 19:46 CET] Current GW27 Status:**
- **Team:** FC MACCHIATO (ID: 17490)
- **Position:** 3:e plats (1,570 totalt)
- **Mål 1:** Reach #2 (Timmerhuggarna)
  - Gap: 22 pts
  - GWs remaining: 11
  - Needed: +2 pts/GW avg (achievable)
- **Mål 2:** Reach top 100K overall rank
  - Current: 140,593 (NOT top 100K)
  - ⚠️ 138K = 138,000 = OUTSIDE top 100K
  - Need: <100,000 rank
  - Challenge: Need 50-60+ pts/GW minimum
- **Konkurrenter:**
  - #1: BK Långburk (1,651) - +81 gap
  - #2: Timmerhuggarna (1,592) - +22 gap ← TARGET
  - #3: FC MACCHIATO (1,570)
- **Recent form:**
  - GW25: 77 pts (rank 138K)
  - GW26: 68 pts (rank 133K)
  - GW27: 25 pts (rank 140K) ❌ FELL OUT

### Serie A
- Ej analyserat än

## GW26/MD22 CRITICAL (10 FEB 16:25)

### FPL GW26 (DEADLINE TODAY ~18:45)
- Rogers (AVA) - bevaka Emery skador
- Arsenal triple (Timber, Gabriel, Rice) okej
- Guéhi status före 15:00 idag
- Gabriel som captain (7.5 ppg avg)

### Bundesliga MD22 (14-15 FEB)
**OUT (URGENT):** Manzambi (-27p), Wimmer (0p), Olise, Schlotterbeck, Raum
**EASY FIXTURES:** Bayern-Bremen, Leverkusen-Pauli, Dortmund-Mainz, Stuttgart-Köln
**KEEP:** Kane, Diaz (Bayern 2/3 max), Baumgartner, Musiala (back from injury)
**CONSIDER:** Undav (11 goals, strong despite last match miss)

## Night Research (2026-02-14)
**While Richard slept:** Researched 60+ OpenClaw use-cases från community
- **Fil:** `openclaw-use-cases-research.md`
- **Källor:** ForwardFuture.ai (41-page PDF), Skywork.ai, MyClaw.ai, DigitalOcean
- **Fokus:** Linux VM-friendly use-cases (ej Mac-specifikt)
- **Top picks för Richard:**
  1. WhatsApp integration (prio #1)
  2. Smart shopping list (enkel start, immediate family value)
  3. Calendar triage (stor tidsbesparing)
  4. Health data integration (Dexcom G7 + träning)
  5. Dev-from-phone (Telegram → Git)
- **Säkerhet:** Approval gates för high-risk actions, Docker sandbox rekommenderad

## Career Agent - Enhanced Job Crawler
**[2026-02-17 13:52]** Richard requested job crawler with:
- ✅ Accept cookies automatically
- ✅ Wait for full page load
- ✅ Filter locations (CH/DK/SE)
- ✅ Filter roles (marketing, management, strategy)
- ✅ Save screenshots of matches
- ✅ Report via Telegram

**V1 - Initial Version** ✅ Built & Tested
- 320-line Playwright script
- 8 company targets
- Smart job scoring (0-10)
- Cookie + page load handling
- Screenshot capture
- JSON results export
- **Result:** Found 0 jobs (selectors didn't match actual page structure)

**V2 - Improved Version** ✅ Built & Tested
- More flexible selectors with fallbacks
- Better HTML parsing
- Shows ALL job elements (not just matches)
- Saves page HTML for inspection
- Generic element detection
- **Result:** Found 19 elements on Roche, 1 screenshot captured
- **Key Finding:** Career sites are multi-step (click category → jobs load)

**Files Created:**
1. `enhanced-job-crawler.py` - V1 production script
2. `enhanced-job-crawler-v2.py` - V2 diagnostic script (better debugging)
3. `run-and-report.py` - Telegram wrapper
4. `SETUP.md` - Installation guide
5. `CRAWLER-GUIDE.md` - Usage documentation

**Test Results:**
- Novo Nordisk: 0 jobs found (page saved: `Novo_Nordisk_page.html`)
- Roche: 19 elements found, 1 screenshot (`Roche_7_5.png`)
- Runtime: V1 (119s / 8 companies), V2 (35s / 2 companies)

**Technical Insights:**
- ✅ Cookie acceptance works perfectly
- ✅ Page loading works
- ✅ Element detection works
- ⚠️ Issue: Career sites are dynamic/multi-step
  - Roche: Click category → jobs load
  - Novo Nordisk: Unknown structure (need inspection)
  - Most modern job sites load jobs via JavaScript after clicking filters

**Next Options:**
1. **Option A (Recommended):** Auto-click job categories, then scrape
2. **Option B:** Find and use company API endpoints
3. **Option C:** Advanced browser mocking with pagination handling

**Status:** ✅ MVP working, awaiting Richard's direction on approach for actual job extraction

## GitHub Integration
**[2026-02-17 23:42]** Richard created GitHub account
- Username: **@richardlaurits**
- Original PAT: 90-day expiration (created 2026-02-17)
- Status: ✅ Upgraded

**[2026-02-18 07:43]** Richard provided new PAT with **FULL ACCESS**
- Token: <REDACTED>
- Permissions: Full access (all scopes)
- Can now: Create/delete/modify repos, manage career-agent-private, etc.
- Skills: github skill fully integrated with elevated permissions

**[2026-02-18 07:45]** Cleaned up public repo (butti-journey)
- Removed: Personal/family details, career-specific information
- Kept: Generic system architecture, skills guide, technical reference
- Result: Professional, reusable documentation safe for public sharing
- Private data: Remains in private repos (job-market-tracker, health-metrics, etc.)

**[2026-02-17 23:49]** Created "butti-journey" repo
- URL: https://github.com/richardlaurits/butti-journey
- Purpose: Public log of ButtiBot's creation and evolution
- Content: Detailed timeline, milestones, architecture, capabilities
- Status: ✅ Live on GitHub

## Private Repos (2026-02-18 00:00)
Created 6 private repos for sensitive tracking:
1. **job-market-tracker** - Job search, company tracking, applications
2. **fpl-tracker** - Premier League Fantasy (deprecated, see #6)
3. **health-metrics** - Diabetes TIR, weight, fitness tracking
4. **investment-research** - Stocks, portfolio, DCA strategy
5. **personal-notes** - Ideas, learnings, reflections
6. **fantasy-football-tracker** (NEW) - FPL + Bundesliga + Serie A
   - Contains current standings, league positions, analysis
   - FPL: 4th place, 1,466 pts (GW26)
   - Bundesliga: 5th place, 60,621 pts (MD22)
   - Serie A: Pending full data collection
   - URL: https://github.com/richardlaurits/fantasy-football-tracker

## Fantasy Football Automation
**[2026-02-18 00:02]** Set up automated daily scraping:
- **Schedule:** 12:00 CET (noon) + 00:00 CET (midnight)
- **Data updated:** FPL, Bundesliga, Serie A
- **Auto-push:** GitHub commit with timestamp
- **Alerts:** Telegram summary
- **Source filtering:** Max 12 hours old only

**Bundes Liga Sources:**
- ✅ Bundesliga Official (official-fantasy.bundesliga.de)
- ✅ bulinews.com/fantasy ← PRIMARY (Richard's preference)
- ✅ X/Twitter injury news
- ✅ FPL Hints (for cross-league news)

**FPL Sources:**
- ✅ FPL Official API (fpl.com)
- ✅ X/Twitter injury reporters
- ✅ FPL Hints

**Serie A Sources:**
- ✅ World Fantasy Soccer (serieafantasy.com or official)
- ✅ Italian sports news (max 12h old)

## Session Notes (2026-02-23)

**[2026-02-23 19:36 CET] Richard's Requests:**
1. Kill all daily Fantasy scrape cron jobs ✅
2. Set up nightly FPL scraper (11 PM CET) — squad news & rumours only ✅
3. Set up Friday Bundesliga scraper (8 AM) — current week injury news only ✅
4. Keep Serie A as manual screenshot comparison weekly ✅
5. No league standings, just player intel ✅

**[2026-02-23 19:35 CET] Gmail Monitor Fix:**
- OAuth token expired on 2026-02-19
- Replaced with IMAP + app password method
- New script: `gmail_monitor_imap.py`
- Tested: Working ✅

## Investment Portfolio
**[2026-02-24 08:36 CET]** Nordic Dividend Portfolio tracked
**[2026-02-24 08:45 CET]** API integration completed

**Total holdings:** 14 stocks across SE/NO/FI/DK

**Core positions:**
• 🇸🇪 **Nordea Bank** - 15.11% (largest holding)
• 🇸🇪 **Handelsbanken A** - 13.35%
• 🇸🇪 **Swedbank A** - 11.79%
• 🇸🇪 **Tele2 B** - 11.63%
• 🇳🇴 **Equinor** - 7.11%
• 🇫🇮 **Sampo A** - 6.70%
• 🇳🇴 **Orkla** - 6.25%
• 🇩🇰 **Novo Nordisk B** - 4.86%
• 🇫🇮 **UPM-Kymmene** - 4.84%
• 🇸🇪 **Volvo B** - 4.73%
• 🇸🇪 **Essity B** - 3.89%
• 🇸🇪 **Sandvik** - 3.88%
• 🇸🇪 **Investor B** - 3.11%
• 🇸🇪 **ABB** - 2.76%

**Strategy:** Dividend-focused, Nordic large-caps, heavy bank exposure (~40%)

**Agent:** `agents/investment-agent/`
- **Primary API:** Yahoo Finance (yfinance) - 100% success rate
- **Backup:** Web scraping from Avanza/DI
- **Features:**
  - Daily winners/losers (top 3)
  - Weighted portfolio performance
  - Per-market breakdown (SE/NO/FI/DK)
  - Notable moves (>3%) alerts
  - Historical data storage
- **Hourly Alerts (NEW):**
  - Runs: Every hour during market hours (09:00-17:00 CET, Mon-Fri)
  - Triggers: >3% for banks, >4% for NO/FI, >5% for Novo Nordisk
  - Duplicate prevention: Same stock not alerted within 60 min
  - Severity: LOW (3-5%), MEDIUM (5-10%), HIGH (>10%)
  - Delivery: Telegram instant message
  - Cron: `0 9-17 * * 1-5`
- **Integration:** Morning brief daily 07:00
- **Files:**
  - `get_portfolio.py` - Main script
  - `hourly_alert.py` - Hourly monitoring
  - `run_hourly_alert.sh` - Cron wrapper
  - `telegram_sender.py` - Message delivery
  - `data/portfolio_YYYY-MM-DD.json` - Daily snapshots
  - `data/alerts.json` - Alert history
  - `api_test_results.json` - API validation
- **Status:** ✅ Active from 2026-02-24

## French Tutor Agent
**[2026-02-24 09:00 CET]** Created for FIDE A1 exam preparation
**[2026-02-24 09:30 CET]** Added adaptive quiz system

**Student:** Richard Laurits
**Goal:** Pass FIDE A1 → Secure Permit C (Swiss residence)
**Approach:** Very basic grammar + useful vocabulary

**Curriculum:** 12-week progressive program
- **Week 1-2:** Basics, greetings, être/avoir
- **Week 3-4:** Daily life, ER/IR/RE verbs
- **Week 5-6:** Food, shopping, partitive
- **Week 7-8:** Transport, city, prepositions
- **Week 9-10:** People, hobbies, adjectives
- **Week 11-12:** Past (passé composé), future

**Daily Lesson (08:00 CET):**
- 🇫🇷 Grammar point with conjugations
- 📝 Example sentences (FR + SV)
- 🗣️ 10 new vocabulary words
- 💬 Usage in context sentences
- 💡 5-minute practice tips

**Weekly Quiz (Adaptive):**
- **When:** Sundays (or type "QUIZ" anytime)
- **Duration:** 5-10 minutes
- **Format:** Mixed (Multiple Choice + Written)
- **Questions:** 8-10 based on week's learning
- **Adaptive learning:** Agent tracks performance
  - If MC works better → more MC questions
  - If written works better → more written
  - Balanced if equal performance
- **Grading:** Instant feedback via "QUIZ SVAR:"
- **Progress tracking:** Quiz results stored per format type

**Adaptive Features:**
- Tracks MC vs Written performance
- Adjusts quiz format based on history
- Learns what works best for Richard
- Quiz reminders on Wednesdays

**Agent tracks:**
- Progress per week/day
- Words learned (total count)
- Grammar points covered
- Quiz performance (MC vs written rates)
- Preferred learning format
- Lesson & quiz history

**Files:**
- `french_tutor.py` - Main lesson generator + quiz
- `quiz_grader.py` - Grades quiz responses
- `send_daily_lesson.sh` - Cron wrapper
- `progress.json` - Student progress + performance data
- `lessons.json` - Lesson history
- `quiz_results.json` - Quiz history
- `telegram_sender.py` - Message delivery

**Commands:**
- Daily lesson: Automatic at 07:00
- Weekly quiz: Sundays at 08:00
- Request quiz anytime: Type "QUIZ"
- Submit answers: "QUIZ SVAR: 1-A, 2-je suis, ..."

**Schedule:**
- 🇫🇷 **Lektion:** 07:00 dagligen (mån-sön)
- 🎓 **Quiz:** 08:00 söndagar
- ⏰ **Cron:** `0 7 * * *` + `0 8 * * 0`

**Status:** ✅ Active from 2026-02-24

## Travel Agent
**[2026-02-24 10:00 CET]** Created - Phase 1 & 2 (Reminders + Semi-automation)

**Purpose:** Help with flight check-ins without storing passport data

**Phase 1 - Reminders (ACTIVE):**
- Monitors calendar for upcoming flights
- Sends reminder 24h before check-in opens
- Telegram notification with flight details

**Phase 2 - Semi-automated Check-in (ACTIVE):**
- Parse booking confirmations from email
- Store: flight number, date, booking ref, route
- **NO passport data stored** (user fills manually)
- Opens browser with airline check-in page
- Fills booking reference automatically
- User fills: last name + passport number manually
- Supports: SAS, Swiss, Lufthansa, KLM, Air France, BA, EasyJet, Ryanair

**How to use:**
1. Forward booking email to butti.nightrider@gmail.com
2. Get reminder when check-in opens
3. Run: `python3 checkin_helper.py <trip_id>`
4. Browser opens - fill in passport manually

**Security:**
- No passport numbers stored anywhere
- Only flight metadata in local JSON
- Browser automation stops before passport field

**Files:**
- `travel_agent.py` - Main logic, booking parser
- `checkin_helper.py` - Browser automation
- `travel_db.json` - Trip storage (no sensitive data)
- `check_reminders.sh` - Cron wrapper

**Schedule:** Reminder check every hour 08:00-22:00
**Status:** ✅ Active from 2026-02-24

## To Remember
**[2026-02-14 11:49]** Richard reminded me: ALWAYS timestamp core memories. I made an error about Arthur's birthday (said "in 4 days" when it was 3 days AGO). Fixed.
**[2026-02-14 07:00]** Morning brief working ✅ (cron 07:00 CET daily, med röst)
**[2026-02-18 19:46]** FPL Ranking clarification: 138K = 138,000 = OUTSIDE top 100K (top 100K = ranks 1-100,000). Richard wants <100,000 rank overall.
**[2026-02-18 20:01]** CRITICAL: Always verify GW status before analysis. GW27 is ONGOING (Arsenal vs Tottenham tonight). Never guess player points - always check before finalizing analysis.

## FPL Learning Rules
**[2026-02-18 20:30]** CRITICAL RULE #1: NEVER GUESS
- I guessed Timber price = £5.0 (was £6.4)
- This broke budget analysis completely
- Richard corrected me with screenshot proof
- **Rule now:** ALWAYS verify with data, NEVER guess prices/stats
- If search fails → try different keywords, don't assume

**[2026-02-18 20:01]** Created FPL_RULES.md in agents/fpl-agent/ with:
- ✅ Critical rules (verify GW status, positions, points calculation)
- ✅ Rank system (138K = 138,000 = OUTSIDE top 100K)
- ✅ Richard's team info (ID 17490, FC MACCHIATO)
- ✅ Funa-ligan standings & strategy
- ✅ Common mistakes to avoid
- ✅ Plan: Need Brave Search API for news/rumors/injury tracking
- **Haaland is FWD (forward), not GK** - with captain = 5 pts x2 = 10 total

## Web Search API
**[2026-02-23 20:48 CET]** Brave Search API Key configured
- API Key: `BSAI8QbrhfyRgz5CgfX-SKgV4a5j8T8`
- Stored: `.env.brave` (local, secure)
- Status: ✅ Ready for web scraping
- Use cases:
  - FPL injury/suspension news (nightly)
  - Bundesliga current week injuries (Friday)
  - Morgonbrief (if resumed)

## Model Testing
**[2026-02-23 20:53 CET]** Kimi 2 API configured for testing
- API Key: `sk-QXjQ5ODoOX3tcg2z7GczdBmE5G5ITEVd6FESbXtorqwxGirf`
- Stored: `.env.kimi` (local, secure)
- Status: ✅ Ready for testing

**[2026-02-23 20:54 CET]** SWITCHED TO KIMI 2 FOR ALL TASKS
- Previous model: Claude Haiku
- New model: Kimi 2 (full switch)
- Test mode: Live - all responses now use Kimi 2
- Monitoring: Richard observing performance

## Token Optimization
**[2026-02-18 16:35 CET]** Implemented hard caps to reduce token burn:
- **Call caps:** 40-50 max per run (agent-specific in OPTIMIZATION.md)
- **Output caps:** 300-500 micro, 1,500-2,500 final
- **Reflections:** Only every 5-10 steps or end (no per-step)
- **Loop detector:** Abort if same error 3x
- **Memory archival:** Old daily logs moved to `memory/archive/`
- **Status:** ✅ Documented, live


## Pernilla Communication Guidelines
**[2026-02-24 16:45 CET]** Established VIP communication rules

**Email Style:**
- Always make emails beautiful, personal, and engaging
- Use HTML formatting with colors, emojis, nice design
- Include follow-up questions when more info needed
- Be proactive and helpful

**Examples of good emails:**
- Weekly menu with complete shopping list
- Weather reports with emojis and nice formatting
- Personal touches and warmth

**Technical:**
- Check inbox every 10 minutes for her emails
- Respond directly without asking Richard first
- VIP status: help immediately and thoroughly


## French Tutor Update
**[2026-02-25 07:15 CET]** Updated curriculum based on Richard feedback

**Changes:**
- **Vocabulary:** Increased difficulty level - more useful, practical words (not just basics)
- **Grammar:** Kept basic/simple grammar focus
- **New focus:** Question formation (Comment, Pourquoi, Où, Quand, Combien)
- **New categories:**
  - advanced_greetings (Enchanté, Bonne chance, etc.)
  - question_words (all question words with examples)
  - asking_directions (how to ask for directions)
  - useful_phrases (practical everyday phrases)
  - food_advanced (restaurant situations)
  - transport_advanced (travel booking)

**New Grammar Lessons:**
- Week 2: Questions avec "Est-ce que" (simple question form)
- Week 3: Questions med frågeord (Comment, Pourquoi, Où...)
- Continued: Basic être/avoir, ER/IR/RE verbs

**Status:** ✅ Active from 2026-02-25


## Schedule Updates
**[2026-02-25]** Updated cron schedule based on Richard preferences:

**Daily 07:00:** Morgonbrief (weather, email, portfolio, news)
**Fridays 07:05:** Separate Fantasy Football brief (FPL, Bundesliga, Serie A)
**Daily 08:00:** French lesson
**Daily 10:00:** Jan greeting (to janlaurits@icloud.com)

Fantasy brief only runs on Fridays (and special mid-week deadlines when applicable).
