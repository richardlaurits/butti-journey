#!/bin/bash
# Watchdog Agent Demonstration Script
# Shows before/after system observability

echo "========================================"
echo "  WATCHDOG AGENT DEMONSTRATION"
echo "========================================"
echo ""

echo "📊 BEFORE: No system visibility"
echo "   - Agents could fail silently"
echo "   - Cron jobs could break undetected"
echo "   - Environment issues only found manually"
echo "   - No centralized status view"
echo ""

echo "========================================"
echo "  LIVE SYSTEM STATUS (NOW)"
echo "========================================"
echo ""

# Show the status dashboard
if [ -f ~/.openclaw/workspace/agents/watchdog-agent/status.json ]; then
    echo "🗂️  Status Dashboard: agents/watchdog-agent/status.json"
    echo ""
    cat ~/.openclaw/workspace/agents/watchdog-agent/status.json | python3 -m json.tool 2>/dev/null || cat ~/.openclaw/workspace/agents/watchdog-agent/status.json
    echo ""
else
    echo "⚠️  Status file not found — run watchdog first"
fi

echo ""
echo "========================================"
echo "  AGENT HEALTH SUMMARY"
echo "========================================"
echo ""

# Parse and display agent status
python3 << 'EOF'
import json
from pathlib import Path

status_file = Path.home() / ".openclaw/workspace/agents/watchdog-agent/status.json"
if status_file.exists():
    with open(status_file) as f:
        data = json.load(f)
    
    print("📦 AGENTS:")
    for name, info in data.get("agents", {}).items():
        icon = "✅" if info["status"] == "healthy" else "⚪" if info["status"] == "no_logs" else "⚠️"
        print(f"   {icon} {name:20} → {info['status']}")
    
    print("")
    print("⏰ CRON JOBS:")
    for name, info in data.get("cron_jobs", {}).items():
        icon = "✅" if info["status"] == "healthy" else "⚠️" if info["status"] == "stale" else "❓"
        last = info.get("last_run", "never")[:10] if info.get("last_run") else "never"
        print(f"   {icon} {name:20} → {info['status']} (last: {last})")
    
    print("")
    print("🖥️  ENVIRONMENT:")
    env = data.get("environment", {})
    print(f"   ✅ Node: {env.get('node_version', 'N/A')}")
    print(f"   ✅ NVM: {env.get('nvm_current', 'N/A')}")
    print(f"   ✅ NPM prefix: {'healthy' if env.get('npm_healthy') else 'ISSUE'}")
    
    alerts = data.get("alerts", [])
    print("")
    if alerts:
        print(f"🚨 ALERTS: {len(alerts)} issue(s) detected")
        for alert in alerts:
            print(f"   [{alert['severity'].upper()}] {alert['component']}: {alert['issue']}")
    else:
        print("🎉 No alerts — all systems operational")
EOF

echo ""
echo "========================================"
echo "  RECENT WATCHDOG ACTIVITY"
echo "========================================"
echo ""

if [ -f ~/.openclaw/workspace/agents/watchdog-agent/watchdog.log ]; then
    echo "📜 Last 10 log entries:"
    tail -10 ~/.openclaw/workspace/agents/watchdog-agent/watchdog.log
else
    echo "No log file yet"
fi

echo ""
echo "========================================"
echo "  OPERATOR GUIDE"
echo "========================================"
echo ""
echo "🔧 Manual Health Check:"
echo "   python3 agents/watchdog-agent/watchdog.py"
echo ""
echo "📊 View Status Dashboard:"
echo "   cat agents/watchdog-agent/status.json | jq ."
echo ""
echo "📜 View Logs:"
echo "   tail -f agents/watchdog-agent/watchdog.log"
echo ""
echo "⚙️  Run via Heartbeat (every 4h):"
echo "   See HEARTBEAT.md for integration"
echo ""
echo "🔄 Rollback (if needed):"
echo "   rm -rf agents/watchdog-agent/"
echo "   (Zero impact on existing functionality)"
echo ""
echo "========================================"
echo "  AUTONOMY IMPACT"
echo "========================================"
echo ""
echo "✅ Self-monitoring: System detects its own failures"
echo "✅ Proactive alerts: Issues surfaced before they cascade"
echo "✅ Centralized visibility: Single source of truth for health"
echo "✅ Foundation layer: Enables predictive scheduling & self-healing"
echo ""
echo "========================================"
