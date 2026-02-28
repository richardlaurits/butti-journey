#!/usr/bin/env python3
"""
Smart Agent Scheduler - Proactive Activation Engine
Activates dormant agents based on contextual schedules
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

# Cost optimization: Track last activation to prevent duplicates
ACTIVATION_TRACKER = Path(__file__).parent / ".activation_tracker.json"
MIN_HOURS_BETWEEN_ACTIVATIONS = 6

def was_recently_activated(agent_name):
    """Check if agent was activated recently."""
    if not ACTIVATION_TRACKER.exists():
        return False
    try:
        with open(ACTIVATION_TRACKER) as f:
            tracker = json.load(f)
        last_str = tracker.get(agent_name)
        if last_str:
            last = datetime.fromisoformat(last_str)
            hours_ago = (datetime.now() - last).total_seconds() / 3600
            if hours_ago < MIN_HOURS_BETWEEN_ACTIVATIONS:
                return True
    except:
        pass
    return False

def record_activation(agent_name):
    """Record agent activation time."""
    tracker = {}
    if ACTIVATION_TRACKER.exists():
        try:
            with open(ACTIVATION_TRACKER) as f:
                tracker = json.load(f)
        except:
            pass
    tracker[agent_name] = datetime.now().isoformat()
    with open(ACTIVATION_TRACKER, "w") as f:
        json.dump(tracker, f)

AGENTS_DIR = Path(__file__).parent.parent
SCHEDULE_FILE = Path(__file__).parent / "agent_schedules.json"
ACTIVATION_LOG = Path(__file__).parent / "activation_log.json"


def load_schedules():
    """Load or initialize agent schedules."""
    if SCHEDULE_FILE.exists():
        with open(SCHEDULE_FILE) as f:
            return json.load(f)
    return {}


def log_activation(agent_name, reason, command=None, success=True):
    """Log activation attempt."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "reason": reason,
        "command": command,
        "success": success
    }
    
    logs = []
    if ACTIVATION_LOG.exists():
        with open(ACTIVATION_LOG) as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    logs = logs[-100:]  # Keep last 100
    
    with open(ACTIVATION_LOG, "w") as f:
        json.dump(logs, f, indent=2, default=str)


def get_agent_last_activity(agent_path):
    """Get hours since last agent activity."""
    logs = list(agent_path.glob("*.log"))
    if logs:
        newest = max(logs, key=lambda p: p.stat().st_mtime)
        hours_ago = (datetime.now() - datetime.fromtimestamp(newest.stat().st_mtime)).total_seconds() / 3600
        return hours_ago
    return float('inf')


def should_activate(agent_name, schedule):
    """Determine if agent should be activated."""
    if not schedule.get("auto_activate"):
        return False, "Auto-activation disabled"
    
    now = datetime.now()
    day_name = now.strftime("%A").lower()
    hour = now.hour
    
    # Check day
    if day_name not in schedule.get("active_days", []):
        return False, f"Not an active day ({day_name})"
    
    # Check hour
    if hour not in schedule.get("active_hours", []):
        return False, f"Not an active hour ({hour})"
    
    # Check idle time
    agent_path = AGENTS_DIR / agent_name
    idle_hours = get_agent_last_activity(agent_path)
    max_idle = schedule.get("max_idle_hours", 24)
    
    if idle_hours < max_idle:
        return False, f"Recently active ({idle_hours:.1f}h < {max_idle}h)"
    
    return True, f"Idle {idle_hours:.1f}h, within active window"


def activate_agent(agent_name, schedule):
    """Activate an agent with deduplication."""
    
    # Check if recently activated
    if was_recently_activated(agent_name):
        print(f"⏭️  Skipped: {agent_name} (activated within last {MIN_HOURS_BETWEEN_ACTIVATIONS}h)")
        return False
    
    agent_path = AGENTS_DIR / agent_name
    command_template = schedule.get("command", "")
    
    if not command_template:
        log_activation(agent_name, "No command configured", success=False)
        return False
    
    command = command_template.format(path=str(agent_path))
    
    try:
        # Execute
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=AGENTS_DIR.parent,
            timeout=30
        )
        success = result.returncode == 0
        log_activation(agent_name, "Activated", command, success)
        return success
    except Exception as e:
        log_activation(agent_name, f"Failed: {e}", command, False)
        return False


def main():
    """Run smart scheduler."""
    schedules = load_schedules()
    activated = 0
    skipped = 0
    
    print(f"Smart Scheduler - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("-" * 50)
    
    for agent_name, schedule in schedules.items():
        should_run, reason = should_activate(agent_name, schedule)
        
        if should_run:
            if activate_agent(agent_name, schedule):
                activated += 1
                print(f"✅ Activated: {agent_name}")
            else:
                print(f"❌ Failed: {agent_name}")
        else:
            skipped += 1
            print(f"⏭️  Skipped: {agent_name} ({reason})")
    
    print(f"\nSummary: {activated} activated, {skipped} skipped")
    return activated


if __name__ == "__main__":
    exit(main())
