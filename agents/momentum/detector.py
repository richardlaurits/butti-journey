#!/usr/bin/env python3
"""
Execution Momentum Agent
Detects stalled initiatives and forces finish-or-kill decisions
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/richard-laurits/.openclaw/workspace")
MOMENTUM_DIR = WORKSPACE / "agents" / "momentum"

def detect_initiatives():
    """Scan all sources for active initiatives."""
    initiatives = []
    
    # 1. From strategy decisions (strategic reallocations)
    strategy_log = WORKSPACE / "agents" / "strategy" / "strategy_decisions.log"
    if strategy_log.exists():
        with open(strategy_log) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    # Each reallocation is an initiative
                    for realloc in entry.get("reallocations", []):
                        initiatives.append({
                            "id": f"init-{len(initiatives)+1:03d}",
                            "name": f"Reallocate {realloc['agent']}",
                            "type": "strategic_reallocation",
                            "source": "strategy_decisions",
                            "started": realloc.get("timestamp"),
                            "last_activity": realloc.get("timestamp"),
                            "target": realloc.get("agent"),
                            "status": "in_progress",
                            "completion_criteria": f"Verify {realloc['agent']} shows activity in logs"
                        })
                except:
                    pass
    
    # 2. From agent configurations (agent deployments)
    for agent_dir in (WORKSPACE / "agents").iterdir():
        if not agent_dir.is_dir():
            continue
        
        # Check for recent setup
        py_files = list(agent_dir.glob("*.py"))
        newest = max((f.stat().st_mtime for f in py_files), default=0)
        
        if newest > 0:
            newest_dt = datetime.fromtimestamp(newest)
            days_since = (datetime.now() - newest_dt).days
            
            # If agent created in last 30 days, it's a recent initiative
            if days_since < 30:
                # Check if it has activity
                activity_log = agent_dir / "activity.log"
                has_activity = activity_log.exists() and activity_log.stat().st_size > 0
                
                initiatives.append({
                    "id": f"init-{len(initiatives)+1:03d}",
                    "name": f"Deploy {agent_dir.name}",
                    "type": "agent_deployment",
                    "source": "agent_directory",
                    "started": newest_dt.isoformat(),
                    "last_activity": datetime.fromtimestamp(activity_log.stat().st_mtime).isoformat() if has_activity else newest_dt.isoformat(),
                    "target": agent_dir.name,
                    "status": "active" if has_activity else "stalled",
                    "completion_criteria": "Agent shows regular activity in logs"
                })
    
    # 3. From FIDE French program (major 90-day goal)
    fide_progress = WORKSPACE / "agents" / "french-tutor-agent" / "fide_progress.json"
    if fide_progress.exists():
        with open(fide_progress) as f:
            progress = json.load(f)
        
        exam_prep = progress.get("exam_prep", {})
        current_day = exam_prep.get("current_day", 0)
        
        initiatives.append({
            "id": f"init-{len(initiatives)+1:03d}",
            "name": "FIDE A1 French Exam Preparation",
            "type": "learning_goal",
            "source": "fide_curriculum",
            "started": exam_prep.get("start_date"),
            "last_activity": progress.get("practice_log", [{}])[-1].get("date") if progress.get("practice_log") else exam_prep.get("start_date"),
            "target": "FIDE A1 certification",
            "status": "active" if current_day > 0 else "not_started",
            "completion_criteria": "Pass FIDE A1 exam by 2026-05-29",
            "deadline": "2026-05-29"
        })
    
    # 4. From cron jobs (automated initiatives)
    heartbeat = WORKSPACE / "HEARTBEAT.md"
    if heartbeat.exists():
        content = heartbeat.read_text()
        
        # Extract cron-scheduled initiatives
        cron_patterns = [
            (r'### (.*?\(.*?\))', 'cron_job'),
            (r'### (Jan\'s Daily Greeting)', 'family_communication'),
            (r'### (FIDE French Lesson)', 'language_learning'),
        ]
        
        for pattern, initiative_type in cron_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                name = match.group(1)
                initiatives.append({
                    "id": f"init-{len(initiatives)+1:03d}",
                    "name": name,
                    "type": initiative_type,
                    "source": "heartbeat_cron",
                    "started": None,  # Ongoing
                    "last_activity": datetime.now().isoformat(),  # Assume active if in cron
                    "target": "system_automation",
                    "status": "active",
                    "completion_criteria": "Continuous operation"
                })
    
    # 5. From opportunity radar (identified but not executed)
    opportunities_file = WORKSPACE / "agents" / "opportunity-radar" / "opportunities.json"
    if opportunities_file.exists():
        with open(opportunities_file) as f:
            opp_data = json.load(f)
        
        for opp in opp_data.get("opportunities", []):
            if opp.get("leverage_score", 0) >= 75:
                initiatives.append({
                    "id": f"init-{len(initiatives)+1:03d}",
                    "name": f"Implement: {opp['title']}",
                    "type": "optimization",
                    "source": "opportunity_radar",
                    "started": opp_data.get("generated_at"),
                    "last_activity": opp_data.get("generated_at"),
                    "target": opp.get("theme", "system"),
                    "status": "identified_not_started",
                    "completion_criteria": opp.get("recommended_action", "Execute optimization")
                })
    
    return initiatives

def calculate_momentum(initiatives):
    """Calculate momentum scores for each initiative."""
    now = datetime.now()
    
    for initiative in initiatives:
        last_str = initiative.get("last_activity")
        started_str = initiative.get("started")
        
        if last_str:
            try:
                last = datetime.fromisoformat(last_str.replace('Z', '+00:00').replace(' CET', ''))
                days_since = (now - last).days
                initiative["days_since_progress"] = days_since
            except:
                initiative["days_since_progress"] = 999
        else:
            initiative["days_since_progress"] = 999
        
        # Calculate momentum score (0-100)
        days = initiative.get("days_since_progress", 999)
        status = initiative.get("status", "unknown")
        
        if status == "complete":
            momentum = 100
        elif status == "active":
            # Active but losing momentum over time
            if days <= 3:
                momentum = 95
            elif days <= 7:
                momentum = 80
            elif days <= 14:
                momentum = 60
            elif days <= 21:
                momentum = 40
            else:
                momentum = 20
        elif status == "stalled":
            momentum = 10
        elif status == "identified_not_started":
            momentum = 0
        else:
            momentum = 50
        
        initiative["momentum_score"] = momentum
        
        # Determine recommendation
        if momentum >= 80:
            initiative["recommendation"] = "maintain"
        elif momentum >= 50:
            initiative["recommendation"] = "accelerate"
        elif momentum >= 20:
            initiative["recommendation"] = "finish_or_kill"
            initiative["urgency"] = "high"
        else:
            initiative["recommendation"] = "kill_or_revive"
            initiative["urgency"] = "critical"
    
    return initiatives

def detect_stagnation_patterns(initiatives):
    """Detect specific stagnation patterns."""
    
    stagnation_signals = {
        "no_progress_10_days": [],
        "partial_updates": [],
        "planning_without_execution": [],
        "repeated_rescheduling": []
    }
    
    for initiative in initiatives:
        days = initiative.get("days_since_progress", 0)
        status = initiative.get("status", "")
        
        # Pattern 1: No progress >10 days
        if days > 10 and status != "complete":
            stagnation_signals["no_progress_10_days"].append(initiative["id"])
        
        # Pattern 2: Identified but never started
        if status == "identified_not_started":
            stagnation_signals["planning_without_execution"].append(initiative["id"])
        
        # Pattern 3: Stalled status
        if status == "stalled":
            stagnation_signals["partial_updates"].append(initiative["id"])
    
    return stagnation_signals

def main():
    """Main momentum detection."""
    print("=== Execution Momentum Detection ===\n")
    
    # Detect initiatives
    initiatives = detect_initiatives()
    print(f"Detected {len(initiatives)} initiatives\n")
    
    # Calculate momentum
    initiatives = calculate_momentum(initiatives)
    
    # Detect stagnation
    stagnation = detect_stagnation_patterns(initiatives)
    
    # Build momentum state
    momentum_state = {
        "generated_at": datetime.now().isoformat(),
        "total_initiatives": len(initiatives),
        "by_status": {},
        "stagnation_signals": stagnation,
        "initiatives": initiatives
    }
    
    # Aggregate by status
    for init in initiatives:
        status = init.get("status", "unknown")
        momentum_state["by_status"][status] = momentum_state["by_status"].get(status, 0) + 1
    
    # Save state
    MOMENTUM_DIR.mkdir(exist_ok=True)
    with open(MOMENTUM_DIR / "momentum_state.json", "w") as f:
        json.dump(momentum_state, f, indent=2, default=str)
    
    print("Status breakdown:")
    for status, count in momentum_state["by_status"].items():
        print(f"  {status}: {count}")
    
    print(f"\nStagnation signals:")
    for pattern, ids in stagnation.items():
        print(f"  {pattern}: {len(ids)} initiatives")
    
    print(f"\n✅ momentum_state.json generated")
    
    return initiatives

if __name__ == "__main__":
    main()
