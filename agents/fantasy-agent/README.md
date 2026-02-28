# FPL Scout Agent - Usage Guide

**[2026-02-14 11:55]** Created by Richard & ButtiBot

## What Is This?

Your dedicated Fantasy Football research assistant. Runs in isolated sessions, doesn't clutter main chat, remembers everything about your squads.

---

## File Structure

```
agents/fantasy-agent/
├── README.md          ← You are here
├── IDENTITY.md        ← Agent personality & mission
├── AGENT.md           ← Behavior instructions
├── MEMORY.md          ← Current squads, injuries, prices
├── DATA_SOURCES.md    ← Where to get fresh data
└── reports/           ← Generated analysis (created automatically)
```

---

## How to Use

### Method 1: Ask ButtiBot to Spawn

In Telegram, just ask:
```
"Analyze my Bundesliga team for MD22"
"Check if Haaland will play this weekend"
"Find me a differential for FPL GW27"
```

ButtiBot will automatically spawn FPL Scout, run the research, and report back.

### Method 2: Manual Spawn (Advanced)

From main session:
```
sessions_spawn(
  agentId="fantasy-scout",
  task="Research FPL transfer targets under £8m",
  model="anthropic/claude-sonnet-4-5-20250929",
  label="FPL Research"
)
```

### Method 3: Scheduled Reports (via Cron)

Set up recurring analysis:
- Daily injury updates (07:00)
- Price change alerts (22:00)
- Weekly team review (Sunday 20:00)
- Pre-deadline reminders

---

## Example Tasks

**Quick Checks:**
- "Is Salah fit?"
- "Haaland or Kane captain?"
- "Check price changes tonight"

**Deep Analysis:**
- "Optimize my Bundesliga team for next 5 gameweeks"
- "Find differentials to catch Tractor Boys in FPL"
- "Analyze Bayern vs Leverkusen fixture from fantasy perspective"

**Recurring Monitoring:**
- "Alert me when any of my players get injured"
- "Track Musiala price - alert if rising"
- "Daily summary of Serie A team news"

---

## Data It Tracks

### Per League:
- ✅ Current squad + formation
- ✅ Budget remaining
- ✅ Transfers available
- ✅ Injuries & suspensions
- ✅ Price changes (rising/falling)
- ✅ Fixture difficulty (next 5)
- ✅ Rival team analysis
- ✅ Transfer targets shortlist

### Live Monitoring:
- Player prices
- Injury flags
- Press conference news
- Ownership %
- Form trends

---

## Updating Squad Data

After you make transfers, update MEMORY.md:

**Option 1: Tell ButtiBot**
```
"Update FPL squad: Out Saliba, In Dunk"
```

**Option 2: Manual edit**
Edit `agents/fantasy-agent/MEMORY.md` directly.

**Option 3: Agent auto-sync (future)**
Connect to FPL API with your credentials, auto-sync squad.

---

## Output Formats

### Short Updates (Telegram)
```
⚽ Haaland fit, 82% owned, rotation risk vs Brighton
💡 Hold but monitor lineups 2h before deadline
```

### Full Reports (File + Summary)
- Detailed analysis saved to `reports/YYYY-MM-DD-topic.md`
- Summary sent to Telegram with key actions
- You can read full report later if needed

---

## Configuration Options

Edit `IDENTITY.md` to customize:
- Output language (Swedish/English mix)
- Confidence thresholds
- Risk tolerance
- Differential ownership % cutoff
- Report verbosity

---

## Tips for Best Results

1. **Keep MEMORY.md updated** - Agent is only as good as its data
2. **Ask specific questions** - "FPL captain?" vs "Who should captain FPL GW26 with DGW context?"
3. **Set time constraints** - "Quick check" vs "Deep analysis" 
4. **Review reports** - Check `reports/` folder for detailed analysis
5. **Combine leagues** - "Compare Kane vs Haaland across all leagues"

---

## TODO / Future Enhancements

**[2026-02-14]** Planned improvements:

- [ ] FPL API integration (fetch Richard's team automatically)
- [ ] Bundesliga fantasy platform connection (need platform name)
- [ ] Serie A fantasy platform connection
- [ ] Price change cron job (nightly alerts)
- [ ] Injury news cron job (morning alerts)
- [ ] Rival tracking (monitor top competitors' transfers)
- [ ] Historical performance analysis (learn from past mistakes)
- [ ] Voice summaries (TTS reports for commute listening)

---

## Support

Questions? Improvements? Ask ButtiBot:
```
"How do I configure FPL Scout for X?"
"Update FPL Scout to do Y"
```

---

**Agent Status:** ✅ Active, ready to spawn
**Last Updated:** 2026-02-14 11:55 CET
**Maintained by:** ButtiBot
