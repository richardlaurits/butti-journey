#!/bin/bash
# Fantasy Football Brief - Fridays 07:05 CET
# Separate fantasy update for Richard Laurits

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S'): Starting fantasy brief" >> logs/fantasy_brief.log

# Generate fantasy brief using a sub-agent
openclaw sessions_spawn \
    --task "Generate a Fantasy Football brief for Richard Laurits. Today is Friday.

STRUCTURE:

⚽ **FANTASY FOOTBALL BRIEF - Fredag**
📅 $(date '+%A %d %B %Y')

───

🏴󠁧󠁢󠁥󠁮󠁧󠁿 **FPL (Premier League)**
- Check GW status (is there a deadline this weekend?)
- Check injuries, suspensions for key players in Richard's team
- Check price changes (risers/fallers)
- Suggest transfer targets based on fixtures
- Deadline info

───

🇩🇪 **Bundesliga**
- Current standings (Richard's position)
- Check injuries for his players
- MD upcoming this weekend
- Suggest transfers

───

🇮🇹 **Serie A (World Fantasy)**
- Current world rank
- Any important news
- Upcoming matchday info

───

💡 **Veckans Tips**
- Key fixtures this weekend
- Differential picks
- Captain suggestions

Keep it concise but comprehensive. Focus on actionable advice." \
    --label fantasy-brief-generator \
    --mode run \
    --timeout 120 >> logs/fantasy_brief.log 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S'): Fantasy brief completed" >> logs/fantasy_brief.log
