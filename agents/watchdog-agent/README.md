# Watchdog Agent - System Health Monitor

Autonomous monitoring for the OpenClaw agent ecosystem.

## What It Does

1. **Agent Health Checks** — Monitors all agents for recent activity
2. **Cron Job Validation** — Ensures scheduled tasks are running
3. **Environment Verification** — Detects Node/NVM issues
4. **Auto-Remediation** — Fixes simple issues, alerts on complex ones
5. **Status Dashboard** — Maintains real-time `status.json`

## Usage

### Manual Check
```bash
cd ~/.openclaw/workspace && python3 agents/watchdog-agent/watchdog.py
```

### View Status Dashboard
```bash
cat agents/watchdog-agent/status.json | jq .
```

### View Logs
```bash
tail -f agents/watchdog-agent/watchdog.log
```

## Integration

The watchdog is designed to run via heartbeat — add to `HEARTBEAT.md`:
```bash
cd ~/.openclaw/workspace && python3 agents/watchdog-agent/watchdog.py
```

## Status File Structure

```json
{
  "last_check": "2026-02-28T22:50:00",
  "agents": {
    "fpl-agent": {
      "status": "healthy|stale|no_logs",
      "last_activity": "2026-02-28T10:00:00",
      "path": "agents/fpl-agent"
    }
  },
  "cron_jobs": {
    "morning_brief": {
      "status": "healthy|stale|no_data",
      "last_run": "2026-02-28T07:00:00",
      "schedule": "0 7 * * *"
    }
  },
  "environment": {
    "node_available": true,
    "node_version": "v22.22.0",
    "nvm_available": true,
    "nvm_current": "v22.22.0",
    "npm_healthy": true,
    "npm_prefix": "/home/.../.nvm/versions/..."
  },
  "alerts": [],
  "auto_fixed": []
}
```

## Alert Severity Levels

- **CRITICAL**: Node completely unavailable — immediate action required
- **HIGH**: Critical cron jobs (morning brief) failing
- **MEDIUM**: NVM/npm misconfiguration — manual fix needed
- **LOW**: Stale agents — informational, may be expected

## Rollback

To disable: Remove the heartbeat entry or delete `agents/watchdog-agent/`.
Zero impact on existing functionality.
