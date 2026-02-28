# Career Scout Agent 🎯

**Mission:** Find perfect job matches for Richard + optimize applications

## What It Does

✅ Monitors job boards 24/7 (Monster, Indeed, LinkedIn, Swedish/Danish boards)
✅ Sends Telegram alerts when good matches appear
✅ Manages resume versions + optimizes for each role
✅ Generates personalized cover letters
✅ Tracks applications + interviews

## Structure

```
career-agent/
├── IDENTITY.md                     # Agent identity
├── MEMORY.md                       # Career profile, preferences, tracking
├── job-monitor.py                  # Main job monitoring script
├── job-monitor-config.json         # Job boards + search config
├── generate-cover-letter.py        # Cover letter generator
├── resume/
│   ├── current-resume.pdf          # [PENDING: Richard's latest]
│   ├── current-resume-parsed.md    # Parsed version
│   └── archive/
├── templates/
│   ├── cover-letter-template.md    # [PENDING: Richard's example]
│   └── cover-letters/              # Generated drafts
├── applications.json               # Track all applications
└── job-monitor-state.json          # Last check times, seen jobs
```

## Setup Status

### Ready ✅
- [ ] Job board configuration
- [ ] Resume management structure
- [ ] Cover letter template system
- [ ] Application tracking

### Awaiting Richard 📋
- [ ] Current resume (PDF)
- [ ] Previous cover letter (as template)

## Next Steps

1. **Richard uploads:**
   - Latest resume (PDF)
   - Previous cover letter (as template)

2. **I will then:**
   - Parse resume → extract keywords, skills, experience
   - Learn cover letter style from example
   - Set up automated job board monitoring
   - Deploy cron job for 24/7 monitoring

3. **You'll receive:**
   - Telegram alerts for matching jobs
   - Pre-drafted cover letters + resume variants
   - Application tracking dashboard

## Usage

### Manual Job Check
```bash
cd agents/career-agent
python3 job-monitor.py
```

### Generate Cover Letter
```bash
python3 generate-cover-letter.py
```

### View Applications
```bash
cat applications.json
```

---

**Status:** In preparation 🚀
**Ready for:** Richard's resume + cover letter template
