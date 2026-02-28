#!/usr/bin/env python3
"""
Watchdog Agent - Autonomous System Health Monitor with Tier-1 Recovery
Monitors: agents, cron jobs, environment health
Actions: auto-remediate (Tier-1) or escalate
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Cost optimization: Status caching to reduce redundant checks
CACHE_FILE = Path(__file__).parent / ".watchdog_cache.json"
CACHE_TTL_MINUTES = 30  # Don't re-check if checked within 30 min

def load_cached_status():
    """Load cached status if still valid."""
    if not CACHE_FILE.exists():
        return None
    try:
        with open(CACHE_FILE) as f:
            cache = json.load(f)
        cached_time = datetime.fromisoformat(cache.get("timestamp", "1970-01-01"))
        minutes_ago = (datetime.now() - cached_time).total_seconds() / 60
        
        if minutes_ago < CACHE_TTL_MINUTES:
            log(f"Using cached status ({int(minutes_ago)} min old)", "CACHE")
            return cache.get("status")
    except:
        pass
    return None

def save_cached_status(status):
    """Save status to cache."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "status": status
            }, f)
    except:
        pass

AGENTS_DIR = Path(__file__).parent.parent
WATCHDOG_DIR = Path(__file__).parent
STATUS_FILE = WATCHDOG_DIR / "status.json"
LOG_FILE = WATCHDOG_DIR / "watchdog.log"
RULES_FILE = WATCHDOG_DIR / "rules.json"
RECOVERY_LOG_FILE = WATCHDOG_DIR / "recovery_log.json"

# Health thresholds
AGENT_TIMEOUT_HOURS = 48
CRON_STALE_HOURS = 24  # Jan greeting considered stale after 24h


def log(message, level="INFO"):
    """Write to watchdog log with timestamp."""
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {level}: {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


def load_status():
    """Load current status or initialize."""
    if STATUS_FILE.exists():
        with open(STATUS_FILE) as f:
            return json.load(f)
    return {
        "last_check": None,
        "agents": {},
        "cron_jobs": {},
        "environment": {},
        "alerts": [],
        "auto_fixed": [],
        "remediation_taken": []
    }


def save_status(status):
    """Save status to JSON file."""
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2, default=str)


def load_recovery_log():
    """Load recovery history."""
    if RECOVERY_LOG_FILE.exists():
        with open(RECOVERY_LOG_FILE) as f:
            return json.load(f)
    return []


def append_recovery_entry(entry):
    """Append entry to recovery log (append-only)."""
    log_data = load_recovery_log()
    log_data.append(entry)
    with open(RECOVERY_LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2, default=str)


def get_recovery_history(action_id, hours=6):
    """Get recent recovery attempts for an action."""
    log_data = load_recovery_log()
    cutoff = datetime.now() - timedelta(hours=hours)
    return [
        entry for entry in log_data
        if entry.get("action_id") == action_id
        and datetime.fromisoformat(entry.get("timestamp", "1970-01-01")) > cutoff
    ]


def is_in_cooldown(action_id, cooldown_minutes):
    """Check if action is in cooldown period."""
    recent = get_recovery_history(action_id, hours=cooldown_minutes/60)
    return len(recent) > 0


def get_failed_count(action_id, hours=6):
    """Get count of failed recovery attempts."""
    log_data = load_recovery_log()
    cutoff = datetime.now() - timedelta(hours=hours)
    return sum(
        1 for entry in log_data
        if entry.get("action_id") == action_id
        and entry.get("result") == "failed"
        and datetime.fromisoformat(entry.get("timestamp", "1970-01-01")) > cutoff
    )


def check_agents():
    """Check all agent directories for recent activity."""
    agents = {}
    
    for agent_dir in AGENTS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        if agent_dir.name in ["watchdog-agent", "seriea-screenshots", "fantasy-screenshots"]:
            continue
            
        agent_name = agent_dir.name
        last_activity = None
        status = "unknown"
        
        # Check for recent log files
        log_files = list(agent_dir.glob("*.log")) + list(agent_dir.glob("*log*"))
        if log_files:
            newest = max(log_files, key=lambda p: p.stat().st_mtime)
            last_activity = datetime.fromtimestamp(newest.stat().st_mtime)
            hours_ago = (datetime.now() - last_activity).total_seconds() / 3600
            status = "healthy" if hours_ago < AGENT_TIMEOUT_HOURS else "stale"
        else:
            status = "no_logs"
            
        agents[agent_name] = {
            "status": status,
            "last_activity": last_activity.isoformat() if last_activity else None,
            "path": str(agent_dir)
        }
    
    return agents


def check_cron_jobs():
    """Check if cron jobs are running on schedule."""
    cron_jobs = {}
    
    expected_jobs = {
        "morning_brief": {
            "schedule": "0 7 * * *",
            "last_run_file": AGENTS_DIR.parent / ".last_morning_brief"
        },
        "fantasy_fpl": {
            "schedule": "0 11 * * 0",
            "last_run_file": AGENTS_DIR.parent / ".last_fpl_check"
        },
        "jan_greeting": {
            "schedule": "0 10 * * *",
            "log_file": AGENTS_DIR.parent / "skills" / "gmail" / "jan_greeting_log.json",
            "stale_threshold_hours": CRON_STALE_HOURS
        }
    }
    
    for job_name, config in expected_jobs.items():
        last_run = None
        status = "unknown"
        
        # Try to determine last run time from various sources
        if "log_file" in config and config["log_file"].exists():
            try:
                with open(config["log_file"]) as f:
                    log_data = json.load(f)
                    if isinstance(log_data, list) and log_data:
                        last_run_str = log_data[-1].get("timestamp") or log_data[-1].get("sent_at")
                        if last_run_str:
                            # Handle various timestamp formats
                            last_run_str = last_run_str.replace("Z", "+00:00").replace(" CET", "").replace(" CEST", "")
                            try:
                                last_run = datetime.fromisoformat(last_run_str)
                            except:
                                pass
            except Exception as e:
                log(f"Error reading log for {job_name}: {e}", "DEBUG")
        
        if "last_run_file" in config and config["last_run_file"].exists():
            last_run = datetime.fromtimestamp(config["last_run_file"].stat().st_mtime)
        
        if last_run:
            hours_ago = (datetime.now() - last_run).total_seconds() / 3600
            stale_threshold = config.get("stale_threshold_hours", 25)
            status = "healthy" if hours_ago < stale_threshold else "stale"
        else:
            status = "no_data"
            
        cron_jobs[job_name] = {
            "status": status,
            "last_run": last_run.isoformat() if last_run else None,
            "schedule": config["schedule"],
            "hours_ago": (datetime.now() - last_run).total_seconds() / 3600 if last_run else None
        }
    
    return cron_jobs


def check_environment():
    """Check Node/NVM and other critical environment health."""
    env = {}
    
    # Check Node availability
    try:
        node_version = subprocess.check_output(["node", "--version"], text=True).strip()
        env["node_version"] = node_version
        env["node_available"] = True
    except:
        env["node_available"] = False
        env["node_version"] = None
    
    # Check npm prefix
    try:
        npm_prefix = subprocess.check_output(["npm", "config", "get", "prefix"], text=True).strip()
        env["npm_prefix"] = npm_prefix
        env["npm_healthy"] = ".nvm" in npm_prefix
    except:
        env["npm_healthy"] = False
        env["npm_prefix"] = None
    
    # Check for npmrc prefix conflict
    npmrc_path = Path.home() / ".npmrc"
    env["npmrc_has_prefix"] = False
    if npmrc_path.exists():
        try:
            content = npmrc_path.read_text()
            env["npmrc_has_prefix"] = bool(re.search(r'^(prefix|globalconfig)=', content, re.MULTILINE))
        except:
            pass
    
    # Check nvm
    try:
        result = subprocess.run(
            ['bash', '-lc', 'export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && nvm current'],
            capture_output=True, text=True
        )
        nvm_current = result.stdout.strip()
        env["nvm_available"] = bool(nvm_current and nvm_current != "none")
        env["nvm_current"] = nvm_current if env["nvm_available"] else None
    except:
        env["nvm_available"] = False
        env["nvm_current"] = None
    
    return env


# ========== TIER-1 RECOVERY ACTIONS ==========

def retrigger_jan_greeting():
    """
    Tier-1: Retrigger Jan's daily greeting.
    Runs the same script that cron would run.
    """
    log("Executing Tier-1 recovery: retrigger_jan_greeting", "RECOVERY")
    
    try:
        script_path = AGENTS_DIR.parent / "skills" / "gmail" / "daily_greeting_jan.py"
        if not script_path.exists():
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Script not found: {script_path}",
                "evidence": {}
            }
        
        # Run the script
        result = subprocess.run(
            ["python3", str(script_path)],
            capture_output=True,
            text=True,
            cwd=AGENTS_DIR.parent,
            timeout=60
        )
        
        # Check evidence file
        log_file = AGENTS_DIR.parent / "skills" / "gmail" / "jan_greeting_log.json"
        evidence = {"log_file_exists": log_file.exists()}
        if log_file.exists():
            evidence["log_file_mtime"] = datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout[-500:] if len(result.stdout) > 500 else result.stdout,
            "stderr": result.stderr[-500:] if len(result.stderr) > 500 else result.stderr,
            "evidence": evidence
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "evidence": {}
        }


def fix_npmrc_prefix():
    """
    Tier-1: Fix npmrc prefix conflict by removing prefix/globalconfig lines.
    Creates timestamped backup before modification.
    """
    log("Executing Tier-1 recovery: fix_npmrc_prefix", "RECOVERY")
    
    npmrc_path = Path.home() / ".npmrc"
    
    try:
        if not npmrc_path.exists():
            return {
                "success": True,
                "stdout": "~/.npmrc does not exist, no fix needed",
                "stderr": "",
                "evidence": {"npmrc_exists": False}
            }
        
        content = npmrc_path.read_text()
        
        # Check if there's anything to fix
        if not re.search(r'^(prefix|globalconfig)=', content, re.MULTILINE):
            return {
                "success": True,
                "stdout": "No prefix/globalconfig lines found in ~/.npmrc",
                "stderr": "",
                "evidence": {"lines_removed": 0}
            }
        
        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = Path.home() / f".npmrc.backup-{timestamp}"
        npmrc_path.rename(backup_path)
        
        # Remove prefix/globalconfig lines
        new_content = re.sub(r'^(prefix|globalconfig)=.*\n?', '', content, flags=re.MULTILINE)
        
        # Write new content (even if empty, we keep the file as required)
        npmrc_path.write_text(new_content)
        
        # Verify fix
        result = subprocess.run(
            ['bash', '-lc', 'export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && npm config get prefix'],
            capture_output=True, text=True
        )
        new_prefix = result.stdout.strip()
        
        return {
            "success": ".nvm" in new_prefix,
            "stdout": f"Backup created: {backup_path}\nNew prefix: {new_prefix}",
            "stderr": "",
            "evidence": {
                "backup_path": str(backup_path),
                "new_prefix": new_prefix,
                "lines_removed": content.count('\n') - new_content.count('\n')
            }
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "evidence": {}
        }


# Registry of Tier-1 recovery actions
RECOVERY_ACTIONS = {
    "retrigger_jan_greeting": retrigger_jan_greeting,
    "fix_npmrc_prefix": fix_npmrc_prefix,
}


def evaluate_check(check, status):
    """Evaluate if a check condition is met."""
    condition = check.get("condition", "")
    
    # Simple condition evaluation (can be extended)
    if "jan_greeting.status == 'stale'" in condition:
        return status.get("cron_jobs", {}).get("jan_greeting", {}).get("status") == "stale"
    
    if "environment.npm_healthy == false" in condition:
        return not status.get("environment", {}).get("npm_healthy", True)
    
    if "environment.node_available == false" in condition:
        return not status.get("environment", {}).get("node_available", True)
    
    return False


def execute_recovery(action_def, status):
    """Execute a Tier-1 recovery action."""
    action_id = action_def["id"]
    
    # Check if action is allowed
    if action_def.get("tier") != 1:
        return None, "Tier-2 actions require manual approval"
    
    # Check cooldown
    cooldown = action_def.get("cooldown_minutes", 360)
    if is_in_cooldown(action_id, cooldown):
        return None, f"Action {action_id} is in cooldown"
    
    # Check max attempts
    max_attempts = action_def.get("max_attempts", 2)
    failed_count = get_failed_count(action_id)
    if failed_count >= max_attempts:
        return None, f"Action {action_id} failed {failed_count} times, escalating to ASK-FIRST"
    
    # Execute action
    python_action = action_def.get("python_action")
    if python_action and python_action in RECOVERY_ACTIONS:
        log(f"Executing recovery action: {action_id}", "RECOVERY")
        result = RECOVERY_ACTIONS[python_action]()
        
        # Log the recovery attempt
        recovery_entry = {
            "timestamp": datetime.now().isoformat(),
            "check_id": action_def.get("check_id", "unknown"),
            "action_id": action_id,
            "result": "success" if result["success"] else "failed",
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "evidence": result.get("evidence", {}),
            "next_allowed_time": (datetime.now() + timedelta(minutes=cooldown)).isoformat()
        }
        append_recovery_entry(recovery_entry)
        
        return result, None
    
    return None, f"Unknown python_action: {python_action}"


def run_recovery_checks(status):
    """Run all checks and execute Tier-1 recoveries."""
    remediation_taken = []
    escalation_alerts = []
    
    try:
        with open(RULES_FILE) as f:
            rules = json.load(f)
    except Exception as e:
        log(f"Failed to load rules: {e}", "ERROR")
        return remediation_taken, escalation_alerts
    
    for check in rules.get("checks", []):
        check_id = check.get("id")
        
        # Evaluate condition
        if not evaluate_check(check, status):
            continue
        
        log(f"Check triggered: {check_id}", "CHECK")
        
        # Try recovery actions
        for action in check.get("recovery_actions", []):
            action["check_id"] = check_id  # Inject check_id for logging
            result, error = execute_recovery(action, status)
            
            if error:
                if "ASK-FIRST" in error or "escalating" in error.lower():
                    escalation_alerts.append({
                        "severity": check.get("severity", "medium"),
                        "component": check_id,
                        "issue": f"Recovery action failed multiple times",
                        "suggestion": "Manual intervention required",
                        "error": error
                    })
                log(f"Recovery skipped for {action.get('id')}: {error}", "RECOVERY")
                continue
            
            if result:
                if result["success"]:
                    remediation_taken.append({
                        "check_id": check_id,
                        "action_id": action.get("id"),
                        "timestamp": datetime.now().isoformat(),
                        "result": "success",
                        "evidence": result.get("evidence", {})
                    })
                    log(f"Recovery successful: {action.get('id')}", "RECOVERY")
                else:
                    failed_count = get_failed_count(action.get("id"))
                    remediation_taken.append({
                        "check_id": check_id,
                        "action_id": action.get("id"),
                        "timestamp": datetime.now().isoformat(),
                        "result": "failed",
                        "error": result.get("stderr", "Unknown error"),
                        "failed_count": failed_count
                    })
                    log(f"Recovery failed: {action.get('id')} (attempt {failed_count})", "RECOVERY")
    
    return remediation_taken, escalation_alerts


def main():
    """Main watchdog check cycle with recovery."""
    log("Starting watchdog check with Tier-1 recovery")
    
    status = load_status()
    status["last_check"] = datetime.now().isoformat()
    
    # Run all checks
    status["agents"] = check_agents()
    status["cron_jobs"] = check_cron_jobs()
    status["environment"] = check_environment()
    
    # Execute recovery actions
    remediation, escalations = run_recovery_checks(status)
    status["remediation_taken"] = remediation
    status["escalation_alerts"] = escalations
    
    # Generate summary alerts (non-recovery issues)
    alerts = []
    
    # Check for issues that weren't auto-remediated
    if status["cron_jobs"].get("jan_greeting", {}).get("status") == "stale" and not any(r["check_id"] == "jan_greeting_stale" for r in remediation):
        alerts.append({
            "severity": "medium",
            "component": "cron:jan_greeting",
            "issue": "Stale but recovery failed or in cooldown",
            "suggestion": "Check recovery_log.json for details"
        })
    
    status["alerts"] = alerts
    
    # Save status
    save_status(status)
    
    # Cache status for next run
    save_cached_status(status)
    
    # Summary
    healthy_agents = sum(1 for a in status["agents"].values() if a["status"] == "healthy")
    stale_agents = sum(1 for a in status["agents"].values() if a["status"] == "stale")
    
    log(f"Check complete: {healthy_agents} healthy agents, {stale_agents} stale, {len(remediation)} remediations, {len(escalations)} escalations")
    
    # Print summary
    print()
    if remediation:
        print(f"🔧 Auto-recovery executed ({len(remediation)}):")
        for r in remediation:
            icon = "✅" if r["result"] == "success" else "❌"
            print(f"   {icon} {r['action_id']}: {r['result']}")
    
    if escalations:
        print(f"\n🚨 Escalations ({len(escalations)}):")
        for e in escalations:
            print(f"   [{e['severity'].upper()}] {e['component']}: {e['error']}")
    
    if alerts:
        print(f"\n⚠️  Manual attention needed ({len(alerts)}):")
        for a in alerts:
            print(f"   [{a['severity'].upper()}] {a['component']}: {a['issue']}")
    
    if not remediation and not escalations and not alerts:
        print("\n✅ All systems healthy (or no Tier-1 actions available)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
