#!/bin/bash
# Process Apple Health JSON export
# Usage: ./process_health_export.sh <path_to_export.json>

EXPORT_FILE="$1"

if [ -z "$EXPORT_FILE" ]; then
    echo "Usage: $0 <path_to_export.json>"
    exit 1
fi

echo "🩺 Processing Apple Health export..."
echo "📁 File: $EXPORT_FILE"

# Move to data directory
mkdir -p ~/.openclaw/workspace/agents/health-agent/data/apple-health
cp "$EXPORT_FILE" ~/.openclaw/workspace/agents/health-agent/data/apple-health/export_latest.json

# Parse and generate report
cd ~/.openclaw/workspace/agents/health-agent
source ../../venv/bin/activate

python3 apple_health_parser.py data/apple-health/export_latest.json > /tmp/health_report.txt

# Send to Telegram
cat /tmp/health_report.txt | python3 telegram_sender.py

echo "✅ Health report sent to Telegram!"
