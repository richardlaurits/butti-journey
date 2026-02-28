#!/bin/bash
# French Tutor - Daily Lesson at 08:00
# FIDE A1 level preparation for Permit C

export PATH="/home/richard-laurits/.npm-global/bin:$PATH"
cd ~/.openclaw/workspace
source venv/bin/activate

# Generate lesson
OUTPUT=$(python3 agents/french-tutor-agent/french_tutor.py 2>/dev/null)

# Send to Telegram
if [ -n "$OUTPUT" ]; then
    echo "$OUTPUT" | python3 agents/french-tutor-agent/telegram_sender.py 2>/dev/null || echo "$OUTPUT" >> logs/french_lessons.log
fi

echo "[$(date '+%Y-%m-%d %H:%M')] French lesson sent" >> logs/french_tutor.log
