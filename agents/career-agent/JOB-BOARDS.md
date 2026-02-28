# Job Boards Reference

## International

### Monster.com
- **Coverage:** CH, SE, DK
- **API:** Yes (requires registration)
- **Update Frequency:** Real-time
- **Search:** Advanced filters available
- **Scraping:** Allowed with User-Agent

### Indeed.com
- **Coverage:** CH, SE, DK
- **API:** Yes (limited free tier)
- **Update Frequency:** Real-time
- **Search:** Advanced filters available
- **Scraping:** Robots.txt compliant

## Sweden

### Arbetsförmedlingen.se
- **Coverage:** All Swedish jobs
- **API:** Yes (free, official)
- **Update Frequency:** Real-time
- **Search:** Comprehensive

### Placera.nu
- **Coverage:** Executive/professional roles
- **API:** Scraping (respectful)
- **Update Frequency:** Daily

### Blocket Jobb (blocket.se/jobb)
- **Coverage:** General Swedish jobs
- **Scraping:** Allowed
- **Update Frequency:** Real-time

## Denmark

### Findjob.dk
- **Coverage:** Danish jobs
- **Scraping:** Respectful scraping OK
- **Update Frequency:** Daily

### Jobindex.dk
- **Coverage:** Comprehensive Danish market
- **Scraping:** Respectful scraping OK
- **Update Frequency:** Real-time

## Switzerland

### Jobs.ch
- **Coverage:** Swiss jobs (trilingual)
- **Scraping:** Respectful scraping OK
- **Update Frequency:** Real-time

### Jobscout24.ch
- **Coverage:** Professional roles
- **Scraping:** Respectful scraping OK
- **Update Frequency:** Daily

### LinkedIn (Switzerland)
- **Coverage:** All roles
- **Method:** Email notifications + parsing
- **Update Frequency:** Real-time

## LinkedIn Job Alerts

**Strategy:** Use LinkedIn's built-in email notifications
1. Set up job alerts on LinkedIn (Richard's account)
2. Parse incoming emails from LinkedIn
3. Filter by criteria + score matching
4. Forward good matches to Richard

**Pros:**
- No API risk
- Respects LinkedIn ToS
- Real-time alerts
- LinkedIn's own ranking/quality

---

## Monitoring Strategy

**Priority Order:**
1. LinkedIn (email notifications)
2. Monster.com + Indeed.com (APIs)
3. Swedish boards (Arbetsförmedlingen + Placera)
4. Danish boards (Findjob + Jobindex)
5. Swiss boards (Jobs.ch + Jobscout24)

**Check Intervals:**
- LinkedIn alerts: Real-time (email parsed as received)
- Monster/Indeed: Every 1-2 hours
- Swedish boards: Every 2 hours
- Danish boards: Every 2 hours
- Swiss boards: Every 2 hours

---

## Matching Algorithm

1. **Must-haves:** Marketing, Manager, Leadership
2. **Location check:** CH, SE, or DK
3. **Keyword scoring:** Count relevant terms (product, global, digital, etc)
4. **Salary filter:** Min 120k
5. **Company screening:** Exclude known bad actors
6. **Final score:** 0-10 → Alert if >= 7

---

Created: 2026-02-14
Ready for: Automation setup
