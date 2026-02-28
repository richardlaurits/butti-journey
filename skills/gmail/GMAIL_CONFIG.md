# Gmail Configuration - ButtiBot

## Accounts

### 1. butti.nightrider@gmail.com (ButtiBot Account)
- **Email:** butti.nightrider@gmail.com
- **App Password:** Stored in `app_password.txt`
- **IMAP (Read):** ✅ ENABLED
- **SMTP (Send):** ✅ ENABLED
- **Purpose:** Bot's own email, can send messages from here
- **Status:** Live and tested

### 2. richardlaurits@gmail.com (Richard's Personal Account)
- **Email:** richardlaurits@gmail.com
- **App Password:** Stored in `richard_personal_app_password.txt`
- **IMAP (Read):** ✅ ENABLED
- **SMTP (Send):** ❌ DISABLED (security - can't send from Richard's account)
- **Purpose:** Monitor Richard's email, read all messages
- **Status:** Live and tested

## Security Rules

**❌ ButtiBot CANNOT:**
- Send email FROM richardlaurits@gmail.com ← **ENFORCED IN CODE**
- Modify Richard's email rules or settings
- Spam or abuse Richard's personal account
- Use SMTP with richardlaurits@gmail.com (error raised if attempted)

**✅ ButtiBot CAN:**
- Read all emails in richardlaurits@gmail.com inbox (IMAP only)
- Monitor for important messages (Pernilla, payments, calendar)
- Forward important messages to butti.nightrider@gmail.com if needed
- Send responses FROM butti.nightrider@gmail.com only

## Code-Level Protection

File: `SECURITY_RULES.py`
- `check_smtp_permission()` → Blocks any SMTP attempts from richardlaurits@gmail.com
- `check_imap_permission()` → Allows all IMAP reads
- All send functions MUST call `check_smtp_permission()` before SMTP

**Testing:** See `SECURITY_RULES.py` for examples.

## Monitor Script

`gmail_monitor.py` checks both inboxes and alerts on:
- ⭐ Emails from Pernilla Laurits
- 💰 Invoices and payments
- 🏦 Bank messages
- 📅 Calendar events and invitations
- ❗ Urgent/important markers

---

**Last updated:** 2026-02-18 19:43 CET
