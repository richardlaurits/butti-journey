#!/bin/bash
# Start Apple Health API Server

cd ~/.openclaw/workspace
source venv/bin/activate

echo "🩺 Starting Apple Health API Server..."
echo ""
echo "📱 Configure Health Auto Export app with:"
echo ""

# Get IP address
IP=$(hostname -I | awk '{print $1}')
echo "   URL: http://$IP:8080/api/health/apple"
echo "   Method: POST"
echo "   Authorization: Bearer RICHARD_API_KEY_2026"
echo ""
echo "🧪 Test with: curl http://$IP:8080/api/health/status"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 agents/health-agent/apple_health_server.py
