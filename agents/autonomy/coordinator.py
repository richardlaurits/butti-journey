#!/usr/bin/env python3
"""
AUTONOMY COORDINATOR - Full Autonomy with Safety Guardrails

Hard Requirements:
1. Global kill switch (read ~/.openclaw/KILL_SWITCH)
2. Idempotency markers for side-effects
3. Cooldowns (24h side-effects, 6h recoveries)
4. Circuit breakers (3 failures = 60min DOWN)
5. No duplicate remediation
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

KILL_SWITCH_FILE = Path.home() / ".openclaw" / "KILL_SWITCH"
MARKERS_DIR = Path.home() / ".openclaw" / "markers"
CIRCUIT_FILE = Path.home() / ".openclaw" / "circuit_breakers.json"
AUTONOMY_LOG = Path.home() / ".openclaw" / "autonomy.log"

WORKSPACE = Path("/home/richard-laurits/.openclaw/workspace")

def log(msg, level="INFO"):
    """Log autonomy events."""
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {level}: {msg}"
    print(entry)
    with open(AUTONOMY_LOG, "a") as f:
        f.write(entry + "\n")

# ========== 1. GLOBAL KILL SWITCH ==========

def check_kill_switch():
    """Check if autonomy is globally disabled."""
    if not KILL_SWITCH_FILE.exists():
        return False
    
    try:
        content = KILL_SWITCH_FILE.read_text().strip().upper()
        return content == "ON"
    except:
        return False

# ========== 2. CIRCUIT BREAKER ==========

def load_circuit_breakers():
    """Load circuit breaker states."""
    if not CIRCUIT_FILE.exists():
        return {}
    
    with open(CIRCUIT_FILE) as f:
        return json.load(f)

def save_circuit_breakers(breakers):
    """Save circuit breaker states."""
    with open(CIRCUIT_FILE, "w") as f:
        json.dump(breakers, f, indent=2, default=str)

def check_circuit_breaker(integration):
    """Check if integration is available."""
    breakers = load_circuit_breakers()
    
    if integration not in breakers:
        return True, "HEALTHY"
    
    state = breakers[integration]
    
    # Check if currently DOWN
    if state.get("status") == "DOWN":
        down_until = state.get("down_until")
        if down_until:
            down_time = datetime.fromisoformat(down_until)
            if datetime.now() < down_time:
                remaining = (down_time - datetime.now()).total_seconds() / 60
                return False, f"DOWN (retry in {int(remaining)}min)"
            else:
                # Reset to healthy
                state["status"] = "HEALTHY"
                state["consecutive_failures"] = 0
                save_circuit_breakers(breakers)
                return True, "HEALTHY (recovered)"
    
    return True, state.get("status", "HEALTHY")

def record_failure(integration):
    """Record a failure for circuit breaker."""
    breakers = load_circuit_breakers()
    
    if integration not in breakers:
        breakers[integration] = {
            "status": "HEALTHY",
            "consecutive_failures": 0,
            "last_failure": None,
            "down_until": None
        }
    
    state = breakers[integration]
    state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    state["last_failure"] = datetime.now().isoformat()
    
    # Trip circuit after 3 failures
    if state["consecutive_failures"] >= 3:
        state["status"] = "DOWN"
        state["down_until"] = (datetime.now() + timedelta(minutes=60)).isoformat()
        log(f"Circuit BREAKER TRIPPED for {integration} - DOWN for 60 minutes", "CIRCUIT")
    else:
        log(f"Circuit breaker warning for {integration}: {state['consecutive_failures']}/3 failures", "WARN")
    
    save_circuit_breakers(breakers)

def record_success(integration):
    """Reset failure count on success."""
    breakers = load_circuit_breakers()
    
    if integration in breakers:
        state = breakers[integration]
        if state.get("consecutive_failures", 0) > 0:
            state["consecutive_failures"] = 0
            state["status"] = "HEALTHY"
            state["last_failure"] = None
            save_circuit_breakers(breakers)
            log(f"Circuit breaker reset for {integration}", "CIRCUIT")

# ========== 3. IDEMPOTENCY MARKERS ==========

def get_marker_path(action_id):
    """Get path for action marker."""
    MARKERS_DIR.mkdir(parents=True, exist_ok=True)
    return MARKERS_DIR / f"{action_id}.last_success.json"

def check_marker(action_id, cooldown_hours=24):
    """Check if action was recently executed."""
    marker_file = get_marker_path(action_id)
    
    if not marker_file.exists():
        return True, "No marker - action allowed"
    
    try:
        with open(marker_file) as f:
            marker = json.load(f)
        
        last_run = datetime.fromisoformat(marker.get("timestamp", "1970-01-01"))
        hours_ago = (datetime.now() - last_run).total_seconds() / 3600
        
        if hours_ago < cooldown_hours:
            remaining = cooldown_hours - hours_ago
            return False, f"COOLDOWN: {action_id} ran {hours_ago:.1f}h ago, wait {remaining:.1f}h more"
        
        return True, f"Marker expired ({hours_ago:.1f}h ago), action allowed"
    
    except Exception as e:
        log(f"Marker error for {action_id}: {e}", "ERROR")
        return True, "Marker corrupt - allowing action"

def write_marker(action_id, target, evidence, action_type="side_effect"):
    """Write marker after successful action."""
    marker = {
        "timestamp": datetime.now().isoformat(),
        "action_id": action_id,
        "action_type": action_type,
        "target": target,
        "evidence": evidence
    }
    
    marker_file = get_marker_path(action_id)
    with open(marker_file, "w") as f:
        json.dump(marker, f, indent=2)
    
    log(f"Marker written: {action_id} -> {target}", "MARKER")

# ========== 4. DUPLICATE REMEDIATION CHECK ==========

def check_duplicate_remediation(check_id, cooldown_hours=6):
    """Check if another component already remediated this."""
    # Check in markers for any recent remediation
    for marker_file in MARKERS_DIR.glob("*.last_success.json"):
        try:
            with open(marker_file) as f:
                marker = json.load(f)
            
            # Check if this is a remediation marker
            if check_id in marker.get("action_id", ""):
                last_run = datetime.fromisoformat(marker.get("timestamp", "1970-01-01"))
                hours_ago = (datetime.now() - last_run).total_seconds() / 3600
                
                if hours_ago < cooldown_hours:
                    return False, f"DUPLICATE: {marker['action_id']} remediated {hours_ago:.1f}h ago"
        
        except:
            pass
    
    return True, "No recent remediation found"

# ========== 5. MAIN AUTONOMY GATE ==========

def can_execute_action(action_id, action_type, integration, target, check_id=None):
    """
    Main gatekeeper for all autonomous actions.
    Returns (allowed: bool, reason: str)
    """
    # 1. Kill switch
    if check_kill_switch():
        return False, "KILL_SWITCH is ON - all autonomous actions disabled"
    
    # 2. Circuit breaker
    allowed, status = check_circuit_breaker(integration)
    if not allowed:
        return False, f"Circuit breaker: {integration} is {status}"
    
    # 3. Duplicate check (if remediation)
    if check_id:
        allowed, reason = check_duplicate_remediation(check_id)
        if not allowed:
            return False, reason
    
    # 4. Cooldown check
    if action_type == "side_effect":
        # Side effects: 24h cooldown, max 1 per 24h per target
        marker_id = f"{action_id}_{target}"
        allowed, reason = check_marker(marker_id, cooldown_hours=24)
        if not allowed:
            return False, f"Side-effect cooldown: {reason}"
    else:
        # Non-side-effect: 6h cooldown, max 2 attempts
        allowed, reason = check_marker(action_id, cooldown_hours=6)
        if not allowed:
            return False, f"Recovery cooldown: {reason}"
    
    return True, "All checks passed - action authorized"

def execute_action(action_id, action_type, integration, target, func, check_id=None):
    """
    Execute an action with full safety wrapping.
    Returns (success: bool, result: any, evidence: dict)
    """
    # Check if allowed
    allowed, reason = can_execute_action(action_id, action_type, integration, target, check_id)
    if not allowed:
        log(f"BLOCKED: {action_id} - {reason}", "BLOCK")
        return False, None, {"blocked_reason": reason}
    
    # Execute
    log(f"EXECUTING: {action_id} ({action_type}) -> {target}", "EXEC")
    
    try:
        result = func()
        
        # Record success
        record_success(integration)
        
        # Write marker for side-effects
        if action_type in ["side_effect", "recovery"]:
            evidence = {
                "result": str(result)[:200] if result else "success",
                "integration": integration,
                "target": target
            }
            
            if action_type == "side_effect":
                marker_id = f"{action_id}_{target}"
            else:
                marker_id = action_id
            
            write_marker(marker_id, target, evidence, action_type)
        
        log(f"SUCCESS: {action_id}", "SUCCESS")
        return True, result, evidence
    
    except Exception as e:
        # Record failure
        record_failure(integration)
        log(f"FAILED: {action_id} - {e}", "FAIL")
        return False, None, {"error": str(e)}

# ========== 6. AUTONOMY DASHBOARD ==========

def get_dashboard():
    """Generate full autonomy dashboard."""
    dashboard = {
        "timestamp": datetime.now().isoformat(),
        "kill_switch": {
            "state": "ON 🔴" if check_kill_switch() else "OFF 🟢",
            "file": str(KILL_SWITCH_FILE),
            "readable": not check_kill_switch()
        },
        "circuit_breakers": load_circuit_breakers(),
        "recent_markers": [],
        "blocked_actions": [],
        "system_status": "operational"
    }
    
    # Recent markers
    for marker_file in sorted(MARKERS_DIR.glob("*.last_success.json"), 
                              key=lambda p: p.stat().st_mtime, reverse=True)[:10]:
        try:
            with open(marker_file) as f:
                marker = json.load(f)
            dashboard["recent_markers"].append({
                "action": marker_file.stem,
                "timestamp": marker.get("timestamp"),
                "target": marker.get("target")
            })
        except:
            pass
    
    # Check for blocked actions from log
    if AUTONOMY_LOG.exists():
        with open(AUTONOMY_LOG) as f:
            lines = f.readlines()
        
        blocked = [l for l in lines if "BLOCKED:" in l][-5:]
        for line in blocked:
            if "BLOCKED:" in line:
                parts = line.strip().split("BLOCKED: ")
                if len(parts) > 1:
                    dashboard["blocked_actions"].append(parts[1])
    
    return dashboard

def print_dashboard():
    """Print formatted dashboard."""
    dashboard = get_dashboard()
    
    print("\n" + "=" * 70)
    print("  AUTONOMY DASHBOARD")
    print("=" * 70)
    
    print(f"\n🔴 KILL SWITCH: {dashboard['kill_switch']['state']}")
    print(f"   File: {dashboard['kill_switch']['file']}")
    
    print(f"\n⚡ CIRCUIT BREAKERS:")
    for integration, state in dashboard['circuit_breakers'].items():
        status_icon = "🟢" if state['status'] == "HEALTHY" else "🔴" if state['status'] == "DOWN" else "🟡"
        print(f"   {status_icon} {integration:12} {state['status']:10} (failures: {state.get('consecutive_failures', 0)})")
    
    print(f"\n📍 RECENT MARKERS:")
    if dashboard['recent_markers']:
        for m in dashboard['recent_markers'][:5]:
            ts = m['timestamp'][:19] if m['timestamp'] else 'unknown'
            print(f"   • {m['action']:30} -> {m['target'][:30]:30} ({ts})")
    else:
        print("   No markers yet")
    
    print(f"\n🚫 BLOCKED ACTIONS:")
    if dashboard['blocked_actions']:
        for a in dashboard['blocked_actions']:
            print(f"   • {a[:60]}")
    else:
        print("   None recently")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    print_dashboard()
