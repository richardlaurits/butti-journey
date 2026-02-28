# Gmail Reader Skill

Read-only access to Richard's Gmail inbox via Google API.

## Files

- **`gmail_skill.py`** - Manual Gmail search/check
- **`gmail_monitor.py`** - Smart automated monitor (HEARTBEAT)
- **`gmail_credentials.json`** - OAuth client credentials
- **`token.pickle`** - Authenticated token (read-only scope)
- **`monitor_state.json`** - State tracking (auto-created)

## Usage

### Automated Monitor (Heartbeat - PREFERRED)

Run every 30 minutes via HEARTBEAT.md:
```bash
source venv/bin/activate && python3 skills/gmail/gmail_monitor.py
```

**Smart filtering:**
- ⭐ Emails from Pernilla Laurits (always important)
- 💰 Invoices/payments (keywords: faktura, invoice, betalning, payment due, etc)
- 🏦 Bank notifications (Nordea, SEB, Handelsbanken, UBS, etc)
- 📅 Calendar invitations
- ❗ Gmail Important-labeled emails

**Ignores:**
- Newsletters (LinkedIn, Forbes, etc)
- Marketing and ads
- Automatic app notifications

**Output:**
- If important emails found → displays them
- If nothing important → returns `HEARTBEAT_OK` (silent)

**State tracking:**
- Remembers seen email IDs to avoid duplicates
- Tracks last check timestamp
- Keeps max 200 recent IDs

### Manual Search

Search for specific emails:
```bash
source venv/bin/activate && python3 skills/gmail/gmail_skill.py <search-query>
```

Examples:
```bash
python3 skills/gmail/gmail_skill.py Fourmiliare
python3 skills/gmail/gmail_skill.py "invoice after:2026/01/01"
python3 skills/gmail/gmail_skill.py from:pernilla
```

## Setup

Already configured with:
- Virtual environment (`venv/` in workspace root)
- Read-only Gmail API scope
- OAuth credentials and token

## Notes

- Monitor runs via heartbeat every ~30 minutes
- Manual search available for ad-hoc queries
- All output in Swedish unless specified otherwise
