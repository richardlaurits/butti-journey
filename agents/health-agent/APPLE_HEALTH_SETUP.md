# Apple Health Auto Export - Setup Guide for Richard

## Del 1: Installera Appen (Du gör detta på iPhone)

### Steg 1: Ladda ner
1. Öppna **App Store** på din iPhone
2. Sök efter **"Health Auto Export"**
3. Installera appen (utvecklare: HealthyApps)
4. Öppna appen

### Steg 2: Ge Åtkomst till Apple Health
1. Appen kommer fråga om åtkomst till Apple Health
2. Tryck **"Turn All Categories On"** eller välj specifikt:
   - ✅ Activity (Steg, kalorier, träning)
   - ✅ Heart (Hjärtfrekvens, HRV)
   - ✅ Sleep (Sömntider, stadier)
   - ✅ Body Measurements (Vikt om du har det)
   - ✅ Other Data (Blodsocker om Dexcom delar till Health)

### Steg 3: Konfigurera Automatisering
1. I appen, gå till fliken **"Automations"** (nederst)
2. Tryck **"+ Add Automation"**
3. Välj **"REST API"** som typ

### Steg 4: Fyll i Server-Information

**URL:**
```
http://192.168.1.X:8080/api/health/apple
```
(Ersätt 192.168.1.X med din servers lokala IP - jag meddelar dig denna)

**Method:** POST

**Headers:**
```
Content-Type: application/json
Authorization: Bearer RICHARD_API_KEY_2026
```

**Body Template (lämna som default):**
```json
{
  "timestamp": "{{timestamp}}",
  "data": {{data}}
}
```

### Steg 5: Välj Data och Frekvens

**Välj vad som ska skickas:**
- ✅ Steps
- ✅ Heart Rate
- ✅ Sleep Analysis
- ✅ Workouts
- ✅ Active Energy
- ✅ Blood Glucose (om tillgängligt)

**Frekvens:**
- **Rekommendation:** "Every 6 hours" eller "Daily at 08:00"
- Du kan också välja "After Workout" för träningsdata

### Steg 6: Testa
1. Tryck **"Test Now"** i appen
2. Om det fungerar ser du "Success!"
3. Om fel - kontrollera URL och att servern är igång

---

## Del 2: Vanliga Problem

### "Connection failed"
- Kontrollera att iPhone och server är på samma WiFi
- Kontrollera att du använder rätt IP-adress
- Testa med http:// (inte https://) först

### "Unauthorized"
- Kontrollera att Authorization-header är exakt: `Bearer RICHARD_API_KEY_2026`
- Inga extra mellanslag eller tecken

### Data kommer inte fram
- Kontrollera att automation är "Enabled" (grön toggle)
- Testa manuellt först innan du väntar på automation

---

## Del 3: Server-Status

**Status:** ⏳ Väntar på att Richard startar servern
**URL:** Kommer att meddelas
**Port:** 8080

När servern är igång:
1. Data sparas i: `~/.openclaw/workspace/health-data/apple-health/`
2. Health Agent analyserar automatiskt
3. Rapporter skickas till din Telegram

---

## Nästa Steg

1. Installera appen på din iPhone nu
2. Meddela mig när du gjort det
3. Jag startar servern och ger dig rätt IP-adress
4. Vi testar tillsammans!

Frågor? Skicka skärmdump om något ser konstigt ut! 📱
