#!/usr/bin/env python3
"""
Executive Loop - Main Autonomy Orchestrator
Coordinates all agents with full safety
"""

import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from coordinator import (
    check_kill_switch, can_execute_action, execute_action,
    print_dashboard, log
)
from pathlib import Path
from datetime import datetime

WORKSPACE = Path("/home/richard-laurits/.openclaw/workspace")

def run_executive_loop():
    """Run one cycle of the executive autonomy loop."""
    
    print("\n" + "=" * 70)
    print("  EXECUTIVE AUTONOMY LOOP")
    print("=" * 70)
    
    # Check kill switch first
    if check_kill_switch():
        print("\n🔴 KILL SWITCH IS ON - Executive loop halted")
        print_dashboard()
        return
    
    print("\n🟢 Kill Switch: OFF - Autonomy enabled")
    
    # 1. Load strategic priorities
    print("\n📊 PHASE 1: Strategic Priorities")
    try:
        with open(WORKSPACE / "agents" / "strategy" / "intent_model.json") as f:
            intent = json.load(f)
        
        top_themes = intent.get("top_themes", [])[:3]
        print("   Inferred top priorities:")
        for t in top_themes:
            print(f"     {t['rank']}. {t['theme']} ({t['score']}/100)")
    except Exception as e:
        print(f"   ⚠️ Could not load priorities: {e}")
        top_themes = []
    
    # 2. Check schedules and plan adjustments
    print("\n📅 PHASE 2: Schedule Analysis")
    try:
        with open(WORKSPACE / "agents" / "ops-intelligence" / "agent_schedules.json") as f:
            schedules = json.load(f)
        
        print("   Current schedule status:")
        for agent, config in list(schedules.items())[:5]:
            status = "AUTO" if config.get("auto_activate") else "MANUAL"
            hours = len(config.get("active_hours", []))
            print(f"     {agent:25} {status:8} {hours}h active")
        
        # Calculate planned adjustments
        planned = []
        for agent, config in schedules.items():
            if not config.get("auto_activate") and any(t['theme'] in str(config) for t in top_themes):
                planned.append(f"Consider enabling {agent}")
        
        if planned:
            print(f"\n   📋 Planned adjustments:")
            for p in planned[:3]:
                print(f"     • {p}")
        else:
            print(f"\n   ✅ No immediate schedule changes needed")
    
    except Exception as e:
        print(f"   ⚠️ Could not analyze schedules: {e}")
    
    # 3. Plan actions for next 24h
    print("\n🎯 PHASE 3: Planned Actions (Next 24h)")
    
    planned_actions = []
    
    # Check Jan greeting
    try:
        with open(WORKSPACE / "skills" / "gmail" / "jan_greeting_log.json") as f:
            logs = json.load(f)
        
        if logs:
            last = logs[-1]
            last_time = datetime.fromisoformat(last.get("timestamp", "1970-01-01").replace("Z", ""))
            hours_ago = (datetime.now() - last_time).total_seconds() / 3600
            
            if hours_ago > 24:
                planned_actions.append({
                    "action": "retrigger_jan_greeting",
                    "type": "side_effect",
                    "integration": "gmail",
                    "target": "janlaurits@icloud.com",
                    "reason": f"Last greeting {hours_ago:.1f}h ago (>24h)",
                    "priority": "high"
                })
                print(f"   🚨 Jan greeting stale ({hours_ago:.1f}h) - PLAN: Send now")
            else:
                print(f"   ✅ Jan greeting recent ({hours_ago:.1f}h) - skip")
    except Exception as e:
        print(f"   ⚠️ Could not check Jan greeting: {e}")
    
    # Check FIDE lesson
    try:
        with open(WORKSPACE / "agents" / "french-tutor-agent" / "fide_progress.json") as f:
            progress = json.load(f)
        
        last_lesson = progress.get("exam_prep", {}).get("current_day", 0)
        print(f"   📚 FIDE lesson: Day {last_lesson} - auto-scheduled for tomorrow 07:00")
    except:
        pass
    
    # 4. Execute safest action
    print("\n⚡ PHASE 4: Action Execution")
    
    if planned_actions:
        # Pick highest priority
        action = planned_actions[0]
        print(f"\n   Selected: {action['action']} ({action['reason']})")
        
        # Check authorization
        allowed, reason = can_execute_action(
            action['action'],
            action['type'],
            action['integration'],
            action['target']
        )
        
        if allowed:
            print(f"   ✅ Authorized: {reason}")
            return action
        else:
            print(f"   ❌ Blocked: {reason}")
            return None
    else:
        print("   ℹ️ No actions queued for execution")
        return None
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    from coordinator import print_dashboard
    
    # Show dashboard first
    print_dashboard()
    
    # Run executive loop
    action = run_executive_loop()
    
    if action:
        print(f"\n🎯 READY TO EXECUTE: {action['action']}")
        print(f"   Run with: execute_action('{action['action']}', ...)")
