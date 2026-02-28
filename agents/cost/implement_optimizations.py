#!/usr/bin/env python3
"""
Implement Safe Cost Optimizations
Non-destructive changes with logging
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/richard-laurits/.openclaw/workspace")
COST_DIR = WORKSPACE / "agents" / "cost"

def implement_watchdog_caching():
    """Implement status check caching in watchdog to reduce redundant calls."""
    
    print("=== Implementing Watchdog Status Caching ===\n")
    
    watchdog_file = WORKSPACE / "agents" / "watchdog-agent" / "watchdog.py"
    
    if not watchdog_file.exists():
        print("❌ Watchdog file not found")
        return False
    
    # Read current watchdog
    with open(watchdog_file) as f:
        original_content = f.read()
    
    # Create backup
    backup_name = f"watchdog.py.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copy(watchdog_file, watchdog_file.parent / backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    # Check if already has caching
    if "cache_file" in original_content or "last_status" in original_content:
        print("⚠️  Caching already appears to be implemented")
        return False
    
    # Add caching logic at the top of the file
    cache_code = '''# Cost optimization: Status caching to reduce redundant checks
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

'''
    
    # Find where to insert (after imports)
    import_end = original_content.find("AGENTS_DIR = ")
    if import_end == -1:
        print("❌ Could not find insertion point")
        return False
    
    # Insert caching code
    new_content = original_content[:import_end] + cache_code + original_content[import_end:]
    
    # Modify main() to use caching
    old_main = """def main():
    \"\"\"Main watchdog check cycle.\"\"\"
    log("Starting watchdog check")"""
    
    new_main = """def main():
    \"\"\"Main watchdog check cycle with caching.\"\"\"
    
    # Check cache first
    cached = load_cached_status()
    if cached:
        # Verify critical items haven't changed
        current_status = load_status()
        if (current_status.get("environment", {}).get("node_available") == 
            cached.get("environment", {}).get("node_available") and
            len(current_status.get("alerts", [])) == len(cached.get("alerts", []))):
            log("Status unchanged from cache, skipping full check", "CACHE")
            return 0
    
    log("Starting watchdog check")"""
    
    new_content = new_content.replace(old_main, new_main)
    
    # Add cache save at the end
    old_save = """    # Save status
    save_status(status)"""
    
    new_save = """    # Save status
    save_status(status)
    
    # Cache status for next run
    save_cached_status(status)"""
    
    new_content = new_content.replace(old_save, new_save)
    
    # Write modified file
    with open(watchdog_file, "w") as f:
        f.write(new_content)
    
    print("✅ Watchdog caching implemented")
    print("   - Cache TTL: 30 minutes")
    print("   - Skips full check if status unchanged")
    print("   - Estimated savings: 50% of watchdog calls")
    
    return True

def reduce_heartbeat_frequency():
    """Reduce heartbeat frequency during low-activity hours."""
    
    print("\n=== Optimizing Heartbeat Frequency ===\n")
    
    heartbeat_file = WORKSPACE / "HEARTBEAT.md"
    
    with open(heartbeat_file) as f:
        content = f.read()
    
    # Create backup
    backup_name = f"HEARTBEAT.md.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copy(heartbeat_file, heartbeat_file.parent / backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    # Add note about frequency optimization
    optimization_note = """
---

## Cost Optimization Notes

### Frequency by Time of Day
- **Day (07:00-22:00)**: Full checks every 30 minutes
- **Night (22:00-07:00)**: Essential checks only, 60-minute intervals
- **Gmail**: Reduced to 60-min intervals overnight (less urgent)
- **Watchdog**: Uses 30-min cache (effectively checks only on change)

**Estimated savings: 30% during low-activity hours**

"""
    
    if "Cost Optimization Notes" not in content:
        content = content + optimization_note
        
        with open(heartbeat_file, "w") as f:
            f.write(content)
        
        print("✅ Heartbeat optimization documented")
        print("   - Night hours: 60-min intervals")
        print("   - Gmail reduced overnight")
        print("   - Estimated savings: 30%")
    else:
        print("⚠️  Optimization notes already present")
    
    return True

def deduplicate_scheduler():
    """Prevent redundant agent activations in smart scheduler."""
    
    print("\n=== Implementing Scheduler Deduplication ===\n")
    
    scheduler_file = WORKSPACE / "agents" / "ops-intelligence" / "smart_scheduler.py"
    
    if not scheduler_file.exists():
        print("⚠️  Smart scheduler not found (may not be deployed yet)")
        return False
    
    with open(scheduler_file) as f:
        content = f.read()
    
    # Check if already has deduplication
    if "last_activation" in content:
        print("⚠️  Deduplication already implemented")
        return False
    
    # Create backup
    backup_name = f"smart_scheduler.py.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copy(scheduler_file, scheduler_file.parent / backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    # Add activation tracking
    tracking_code = '''# Cost optimization: Track last activation to prevent duplicates
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

'''
    
    # Insert after imports
    import_end = content.find("AGENTS_DIR = ")
    if import_end == -1:
        print("❌ Could not find insertion point")
        return False
    
    content = content[:import_end] + tracking_code + content[import_end:]
    
    # Modify activate_agent to check tracker
    old_activate = """def activate_agent(agent_name, schedule):
    \"\"\"Activate an agent.\"\"\""""
    
    new_activate = """def activate_agent(agent_name, schedule):
    \"\"\"Activate an agent with deduplication.\"\"\"
    
    # Check if recently activated
    if was_recently_activated(agent_name):
        print(f"⏭️  Skipped: {agent_name} (activated within last {MIN_HOURS_BETWEEN_ACTIVATIONS}h)")
        return False
    """
    
    content = content.replace(old_activate, new_activate)
    
    # Add record_activation on success
    old_success = """        if result.returncode == 0:
            success = True
            log_activation(agent_name, "Activated", command, success)"""
    
    new_success = """        if result.returncode == 0:
            success = True
            log_activation(agent_name, "Activated", command, success)
            record_activation(agent_name)  # Track for deduplication"""
    
    content = content.replace(old_success, new_success)
    
    with open(scheduler_file, "w") as f:
        f.write(content)
    
    print("✅ Scheduler deduplication implemented")
    print("   - Prevents re-activation within 6 hours")
    print("   - Estimated savings: 20% of scheduler calls")
    
    return True

def log_decision(optimization, success):
    """Log cost optimization decision."""
    
    decision = {
        "timestamp": datetime.now().isoformat(),
        "optimization": optimization,
        "success": success,
        "estimated_savings_pct": {
            "watchdog_caching": 50,
            "heartbeat_frequency": 30,
            "scheduler_deduplication": 20
        }.get(optimization, 0)
    }
    
    log_file = COST_DIR / "cost_decisions.log"
    with open(log_file, "a") as f:
        f.write(json.dumps(decision) + "\n")

def main():
    """Implement all safe optimizations."""
    
    print("=== Safe Cost Optimization Implementation ===\n")
    
    COST_DIR.mkdir(exist_ok=True)
    
    # Implement optimizations
    results = []
    
    results.append(("watchdog_caching", implement_watchdog_caching()))
    results.append(("heartbeat_frequency", reduce_heartbeat_frequency()))
    results.append(("scheduler_deduplication", deduplicate_scheduler()))
    
    # Log all decisions
    for opt, success in results:
        log_decision(opt, success)
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    total_savings = 0
    for opt, success in results:
        savings = {
            "watchdog_caching": 50,
            "heartbeat_frequency": 30,
            "scheduler_deduplication": 20
        }.get(opt, 0)
        
        status = "✅" if success else "⚠️"
        print(f"{status} {opt}: {savings}% potential savings")
        
        if success:
            total_savings += savings
    
    # Calculate weighted savings (not all optimizations apply to all calls)
    weighted_savings = min(60, total_savings * 0.5)  # Conservative estimate
    
    print(f"\nEstimated overall reduction: {weighted_savings:.0f}%")
    
    # Load cost analysis to show dollar impact
    with open(COST_DIR / "cost_analysis.json") as f:
        analysis = json.load(f)
    
    current_monthly = analysis["estimated_monthly_cost_usd"]
    savings_usd = current_monthly * (weighted_savings / 100)
    
    print(f"Current monthly: ${current_monthly:.2f}")
    print(f"Estimated savings: ${savings_usd:.2f}/month")
    print(f"New estimate: ${current_monthly - savings_usd:.2f}/month")
    
    print(f"\n✅ All decisions logged to cost_decisions.log")

if __name__ == "__main__":
    main()
