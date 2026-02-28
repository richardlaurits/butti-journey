# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Communication

### Telegram
- Bot username: **@MrLaurits_Bot**
- Bot token: `8581242714:AAFjjOK2G4bf3SGi9FAGkdCJWsiznsLW8Vw`
- Richard's chat ID: `7733823361`
- Status: ✅ Fully paired and operational

### Gmail
**Dual-account setup (2026-02-18):**
1. **butti.nightrider@gmail.com** (Bot account)
   - App password: `skills/gmail/app_password.txt`
   - IMAP: ✅ Read, SMTP: ✅ Send
   - Status: ✅ Working

2. **richardlaurits@gmail.com** (Richard's personal)
   - App password: `skills/gmail/richard_personal_app_password.txt`
   - IMAP: ✅ Read only, SMTP: ❌ BLOCKED (security)
   - Status: ✅ Working
   - Can read 138K+ emails

**Monitor:** `gmail_monitor.py` checks both accounts
- ⭐ Pernilla, 💰 Invoices, 🏦 Banks, 📅 Calendar, ❗ Urgent
- Runs via heartbeat every 30 minutes
- **Status:** ✅ Live (tested 2026-02-18 19:43)

### GitHub
- Username: **@richardlaurits**
- Personal Access Token (PAT): Stored in `~/.bashrc` as `$GITHUB_TOKEN`
- Token created: 2026-02-17 (original), 2026-02-18 (full-access updated)
- Permissions: **Full access** (all scopes)
- Skill: `skills/github/` (Manage repos, issues, PRs, create gists, delete repos)
- Status: ✅ Fully configured with elevated permissions
- Can now: Create, delete, modify repos without asking

### Fantasy Football
**[2026-02-14 12:10]** THREE specialized agents (one per league)

**Premier League (FPL):**
- Team ID: **17490** (FC MACCHIATO)
- League position: 4th (1,466 pts, GW26)
- Agent: `agents/fpl-agent/`
- Platform: Official FPL
- Rules: 2025/26 documented ✅

**Bundesliga:**
- League: Sandhems Bundesliga (5th, 60,621 pts, MD22)
- Agent: `agents/bundesliga-agent/`
- Platform: Official Bundesliga Fantasy Manager (EA Sports)
- Rules: 2025/26 documented ✅

**Serie A:**
- Agent: `agents/seriea-agent/`
- Platform: World Fantasy Soccer
- Rules: ⚠️ NEEDS CONFIRMATION
- Squad: ⚠️ NEEDS FULL DETAILS

**Auto-scraping:** Planned (not yet active)
**Master Guide:** `agents/FANTASY-AGENTS-README.md`

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
