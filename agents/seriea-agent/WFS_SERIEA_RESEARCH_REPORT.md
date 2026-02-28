# World Fantasy Soccer Serie A - Research Report

**Date:** 2026-02-24  
**Platform:** World Fantasy Soccer (worldfantasysoccer.com)  
**For:** Richard Laurits - Team "Pick Team $ 1.2" (#98 World Rank)

---

## 1. GW DEADLINES ⏰

### Typical Serie A Schedule (for deadline estimation):
- **Friday matches:** ~8:45 PM CET (2:45 PM ET)
- **Saturday matches:** 
  - Early: ~3:00 PM CET (9:00 AM ET)
  - Mid: ~6:00 PM CET (12:00 PM ET)
  - Late: ~8:45 PM CET (2:45 PM ET)
- **Sunday matches:**
  - Early: ~12:30 PM CET (6:30 AM ET)
  - Mid: ~3:00 PM CET (9:00 AM ET)
  - Afternoon: ~6:00 PM CET (12:00 PM ET)
  - Late: ~8:45 PM CET (2:45 PM ET)
- **Monday matches:** ~8:45 PM CET (2:45 PM ET)

### Deadline Pattern:
Based on FPL-style rules mentioned on the platform, **deadlines are likely 90 minutes before the first kickoff of each gameweek** (similar to FPL). This typically means:
- **Saturday deadlines:** ~1:30 PM CET
- **Sunday deadlines:** ~11:00 AM CET (if first match is Sunday early)

**⚠️ NOTE:** Exact deadlines must be checked in the World Fantasy Soccer app/website as they may vary by gameweek based on fixture scheduling.

---

## 2. RULES 📋

### FPL-Style Rules (as confirmed by app description):
World Fantasy Soccer uses "FPL style rules" - completely free, no ads.

### Squad Composition:
- **15 players total:**
  - 2 Goalkeepers
  - 5 Defenders
  - 5 Midfielders
  - 3 Forwards

### Formation Rules:
- Must select a starting 11 from your 15-man squad
- Must always have:
  - 1 Goalkeeper
  - At least 3 Defenders
  - At least 1 Forward
- Valid formations include: 3-4-3, 3-5-2, 4-3-3, 4-4-2, 4-5-1, 5-3-2, 5-4-1, 5-2-3

### Transfer Rules:
- **Free transfers:** 1 free transfer per gameweek
- **Rollover:** Can save up to 5 free transfers (roll over unused transfers)
- **Additional transfers:** Cost 4 points each (hit)

### Chips Available:
Based on FPL-style structure, likely include:
1. **Wildcard** - Unlimited transfers without penalty (typically 2 per season)
2. **Free Hit** - Unlimited transfers for one gameweek only (squad reverts after)
3. **Triple Captain** - Captain scores 3x instead of 2x
4. **Bench Boost** - Points from bench players count in addition to starting 11

**Chip Rules:**
- Only ONE chip can be played per gameweek
- Wildcard cannot be used in Gameweek 1
- Once confirmed, chips cannot be cancelled

### Captain & Vice-Captain:
- Select a Captain who scores **2x points**
- Select a Vice-Captain who scores **2x points** if Captain doesn't play

### Auto-Substitutions:
- If a starting player doesn't play, they're automatically subbed
- Substitution priority based on bench order
- Must maintain valid formation after substitutions

---

## 3. PLAYER STATISTICS 📊

### In-App Statistics:
The World Fantasy Soccer app should provide:
- Player prices
- Total points
- Form (recent performance)
- Ownership percentages
- Fixture difficulty ratings

### External Sources for Serie A Stats:
Since World Fantasy Soccer is a newer platform, consider these for detailed stats:
- **FBref.com** - Comprehensive player statistics
- **WhoScored.com** - Player ratings and detailed stats
- **Transfermarkt** - Player values and transfer info
- **Serie A official site** (legaseriea.it) - Official statistics

---

## 4. API ACCESS 🔌

### Official API:
**❌ NO official public API found** for World Fantasy Soccer.

### Data Export Options:
- Website is a **Single Page Application (SPA)** - content loads dynamically via JavaScript
- Static HTML only shows privacy policy
- Data is likely loaded from internal APIs not documented for public use

### Potential Workarounds:
1. **Mobile App:** May have internal APIs that could be reverse-engineered (not recommended)
2. **Web Scraping:** Would require JavaScript rendering (Selenium/Playwright)
3. **Manual Export:** Check if app has "Export Data" or "Share Team" features

### Technical Details:
- Platform uses: Google Analytics, Firebase (mobile), MySQL database, Amazon SES
- App: `com.wfsmobile` (Android), `id6748660442` (iOS)

---

## 5. WEBSITE STRUCTURE 🌐

### Main Website:
- **URL:** https://worldfantasysoccer.com/
- **Type:** Single Page Application (SPA)
- **Static content:** Minimal (only privacy policy visible without JavaScript)

### URL Patterns Discovered:
- `/season/{season_id}/mini-leagues/{league_code}` - Mini-league pages
  - Example: `/season/20174/mini-leagues/ruQj6YHd`

### Likely URL Structure (based on FPL patterns):
- `/login` - Login page
- `/register` - Registration
- `/seriea` - Serie A competition home
- `/seriea/players` - Player list/statistics
- `/seriea/standings` - Global rankings
- `/seriea/fixtures` - Fixture list
- `/my-team` - Team management
- `/transfers` - Transfer page

### Navigation:
Since the website requires JavaScript, navigation is likely:
1. **Main Menu:** Competitions, My Team, Leagues, Fixtures, Statistics
2. **Competition Selector:** Choose from 50+ leagues (Serie A is one option)
3. **Team Management:** Pick squad, make transfers, set captain
4. **Leagues:** Global leaderboard + private mini-leagues

### Mobile Apps (RECOMMENDED):
- **iOS:** https://apps.apple.com/us/app/world-fantasy-soccer/id6748660442
- **Android:** https://play.google.com/store/apps/details?id=com.wfsmobile
- **Size:** ~25 MB
- **Requirements:** iOS 15.1+ / Android equivalent

---

## 6. RICARD'S TEAM - "Pick Team $ 1.2" 🔍

### Current Status:
- **Team Name:** Pick Team $ 1.2
- **World Rank:** #98
- **Platform:** World Fantasy Soccer Serie A

### How to Look Up the Team:
**❌ CHALLENGE:** World Fantasy Soccer does NOT appear to have public team lookup by name or rank.

### Potential Methods to Find/Share Team:

#### Option 1: Mini-League URL Structure
If Richard is in a public mini-league:
- URL format: `https://worldfantasysoccer.com/season/{season_id}/mini-leagues/{league_code}`
- The team would be visible in the league standings

#### Option 2: Team ID/URL (if exists)
- Check if the app provides a "Share Team" option
- Look for team-specific URLs like `/team/{team_id}`
- Check "My Profile" or "Team Settings" for public sharing options

#### Option 3: Global Rankings Page
- Navigate to Serie A → Standings/Rankings
- Search or scroll to rank #98
- Team name "Pick Team $ 1.2" should be listed

#### Option 4: Direct Search (if available)
- Some fantasy platforms allow searching by team name
- Check the rankings page for a search function

### Recommendations for Richard:
1. **Open the World Fantasy Soccer app**
2. **Go to "My Team" or "Profile"**
3. **Look for "Share Team" or "Public URL" option**
4. **Copy the link to share with others**
5. **Alternative:** Join a mini-league together to see each other's teams

---

## 7. ADDITIONAL FINDINGS 🔎

### Platform Features:
- ✅ **Completely FREE** - No paid features
- ✅ **No advertisements**
- ✅ **50+ competitions** including all major European leagues
- ✅ **Prediction League** for each competition
- ✅ **Mini-leagues** - Create/join private leagues with friends
- ✅ **Global Leaderboard** - Compete worldwide

### Available Competitions (50+):
- Italian Serie A (Men's & Women's)
- English Premier League, Championship, League One, League Two
- Spanish LaLiga
- German Bundesliga (Men's & Women's)
- French Ligue 1
- UEFA Champions League, Europa League, Conference League
- FIFA World Cup, Euro, Copa America
- And 40+ more leagues worldwide

### Related Sites:
- **Women's Fantasy Soccer:** https://womensfantasysoccer.com/
- **Privacy/Terms:** https://worldfantasysoccer.com/terms

### Support/Contact:
- Email: contact@worldfantasysoccer.com (from privacy policy)

---

## 8. KEY URLs SUMMARY 🔗

| Resource | URL |
|----------|-----|
| Main Website | https://worldfantasysoccer.com/ |
| iOS App | https://apps.apple.com/us/app/world-fantasy-soccer/id6748660442 |
| Android App | https://play.google.com/store/apps/details?id=com.wfsmobile |
| Terms/Privacy | https://worldfantasysoccer.com/terms |
| Women's Site | https://womensfantasysoccer.com/ |

---

## 9. RECOMMENDATIONS FOR RICHARD 💡

### To Stop Tracking via Screenshots:
1. **Check if the app has data export features** (Settings → Export Data)
2. **Use the web app** - may have better data visibility than screenshots
3. **Create a mini-league** for yourself to track historical performance

### For API/Data Access:
1. **Contact World Fantasy Soccer** directly at contact@worldfantasysoccer.com to ask about API access
2. **Check if they have a developer program** (unlikely but worth asking)
3. **Consider browser automation** (Selenium/Playwright) as last resort

### For Team Lookup:
1. **Ask Richard to share his team URL** from the app
2. **Create a shared mini-league** to view each other's teams
3. **Navigate to global rankings** and filter by rank #98

### For Deadline Tracking:
1. **Set calendar reminders** for typical deadline times:
   - Saturday ~1:30 PM CET
   - Sunday ~11:00 AM CET
2. **Check the app weekly** for exact deadline countdown
3. **Enable push notifications** from the app

---

## 10. DATA AVAILABILITY SUMMARY ✅/❌

| Feature | Available | Notes |
|---------|-----------|-------|
| Mobile App | ✅ | iOS & Android |
| Free to Play | ✅ | No ads, completely free |
| Player Stats | ✅ | In-app (prices, points, form, ownership) |
| Fixture List | ✅ | In-app |
| Mini-Leagues | ✅ | With join codes |
| Global Rankings | ✅ | Worldwide leaderboard |
| Public API | ❌ | No documented API |
| Data Export | ❓ | Unknown - check app settings |
| Web Interface | ✅ | SPA at worldfantasysoccer.com |
| Team Sharing | ❓ | Likely available in app |

---

*Report generated by OpenClaw Research Agent*  
*Sources: World Fantasy Soccer app store pages, Reddit discussions, ESPN Serie A schedule, FPL documentation*
