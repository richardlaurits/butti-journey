# Target Companies for Career Agent Daily Crawler

**[2026-02-16 11:16]** Richard's target company list

## Denmark (8)
1. **Novo Nordisk** — https://www.novonordisk.com/careers
2. **Dawn Health** — https://www.dawnhealth.eu (digital health)
3. **IQVIA** — https://www.iqvia.com/careers
4. **Brain Capture** — https://braincapture.dk [NEW - 2026-02-16]
5. **Diabetes Pharma** — (research needed)
6. **Digital health startups** — (TBD - specific companies?)
7. **Medtech companies** — (TBD - specific companies?)
8. **CapGemini** — https://www.capgemini.com/careers (also in SE)

## Sweden (12)
1. **Novo Nordisk** — https://www.novonordisk.com/careers (also operates in SE)
2. **Glooko** — https://www.glooko.com/careers (diabetes management)
3. **Medicon Village** — https://mediconvillage.se (Lund/Malmö med-tech ecosystem)
4. **Minc Companies** — https://minc.se (startup network)
5. **Lund Innovation (LU Innovation)** — https://www.lunduniversity.lu.se/innovation
6. **CapGemini** — https://www.capgemini.com/careers [NEW - 2026-02-16]
7. **Microsoft** — https://careers.microsoft.com [NEW - 2026-02-16]
8. **Spotify** — https://www.spotifycareers.com [NEW - 2026-02-16]
9. **Klarna** — https://www.klarna.com/careers [NEW - 2026-02-16]
10. **Med-tech companies** — (TBD - specific companies?)
11. **Diabetes companies** — (TBD - specific companies?)
12. **Incubators** — (TBD - specific incubators?)

## Switzerland (13)
1. **Tandem Diabetes Care** — https://www.tandemdiabetes.com/careers
2. **Becton Dickinson (BD)** — https://www.bd.com/careers (YOUR CURRENT EMPLOYER)
3. **Haleon** — https://www.haleon.com/careers
4. **Roche** — https://www.roche.com/careers
5. **MyLife (ex Ypsomed)** — https://www.mylife.com/careers
6. **embecta** — https://www.embecta.com/careers
7. **Sophia Genetics** — https://www.sophiagenetics.com/careers [NEW - 2026-02-16]
8. **Medtronic** — https://www.medtronic.com/careers [NEW - 2026-02-16]
9. **Abbott** — https://www.abbott.com/careers [NEW - 2026-02-16]
10. **Dexcom** — https://www.dexcom.com/careers [NEW - 2026-02-16]
11. **Ypsomed** — https://www.ypsomed.com/careers [NEW - 2026-02-16]
12. **EPFL companies/spinouts** — (specific companies?)
13. **Diabetes startups** — (TBD - specific companies?)

---

## Crawler Setup Plan

**Frequency:** Mon-Fri, 8:00 AM CET
**Check:** Each company's careers page
**Filter for:**
- Director, VP, Senior Manager, Chief roles
- Business Development, Corporate Development, Product Strategy, Commercial
- Medical Tech, Diabetes, Medical Devices, Healthcare focus
- Switzerland, Denmark, Sweden locations (remote OK)

**Output:**
- Alert to Telegram if match found (score 7+/10)
- Save to `data/jobs-YYYY-MM-DD.json`
- Auto-draft cover letter

**Status:** Ready to build once you confirm:
1. Specific digital health startups (DK)?
2. Specific EPFL spinouts (CH)?
3. Any others to add?
