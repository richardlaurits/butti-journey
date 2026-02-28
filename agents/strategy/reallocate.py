#!/usr/bin/env python3
"""
Strategic Reallocator - Adjust schedules based on priority alignment
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

def reallocate_strategic_attention():
    workspace = Path("/home/richard-laurits/.openclaw/workspace")
    strategy_dir = workspace / "agents" / "strategy"
    ops_dir = workspace / "agents" / "ops-intelligence"
    
    # Load contribution map
    with open(strategy_dir / "contribution_map.json") as f:
        contributions = json.load(f)
    
    # Load current schedules
    with open(ops_dir / "agent_schedules.json") as f:
        current_schedules = json.load(f)
    
    # Backup current schedules
    backup_path = ops_dir / f"agent_schedules.json.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    shutil.copy(ops_dir / "agent_schedules.json", backup_path)
    
    # Get strategic priorities
    top_themes = contributions["top_themes"]
    agent_mapping = contributions["agent_mapping"]
    
    # Reallocation rules
    reallocation_log = []
    
    for agent_name, schedule in current_schedules.items():
        if agent_name not in agent_mapping:
            continue
        
        mapping = agent_mapping[agent_name]
        alignment = mapping["strategic_alignment"]
        
        original_hours = schedule.get("active_hours", [])
        original_days = schedule.get("active_days", [])
        
        changes = []
        
        # HIGH ALIGNMENT: Increase frequency
        if alignment >= 60:
            if len(original_hours) < 8:
                # Add more hours during peak times
                new_hours = list(set(original_hours + [9, 10, 11, 14, 15, 16, 17, 18]))
                schedule["active_hours"] = sorted(new_hours)[:10]  # Cap at 10
                changes.append(f"Expanded hours: {original_hours} -> {schedule['active_hours']}")
            
            if len(original_days) < 5 and agent_name != "bundesliga-agent":
                # Add more days (but respect domain constraints)
                if "fantasy" in agent_name:
                    new_days = list(set(original_days + ["tuesday", "wednesday", "thursday"]))
                elif "career" in agent_name:
                    new_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
                else:
                    new_days = original_days
                
                if new_days != original_days:
                    schedule["active_hours"] = original_hours  # Restore hours
                    changes.append(f"Optimized days for {agent_name}")
        
        # MEDIUM ALIGNMENT: Optimize existing
        elif alignment >= 40:
            # Keep current but ensure efficiency
            if schedule.get("max_idle_hours", 24) > 48:
                schedule["max_idle_hours"] = 48
                changes.append(f"Reduced max_idle_hours to 48")
        
        # LOW ALIGNMENT: Reduce or pause
        elif alignment < 20:
            if agent_name not in ["health-agent", "travel-agent"]:  # Keep sensitive agents manual
                schedule["auto_activate"] = False
                changes.append(f"Disabled auto-activation (low alignment: {alignment})")
        
        if changes:
            reallocation_log.append({
                "agent": agent_name,
                "alignment": alignment,
                "changes": changes,
                "timestamp": datetime.now().isoformat()
            })
    
    # Special: Boost top-tier agents further
    high_performers = [a for a, d in agent_mapping.items() if d["leverage_score"] >= 40]
    for agent in high_performers:
        if agent in current_schedules:
            current_schedules[agent]["priority_boost"] = True
    
    # Save updated schedules
    with open(ops_dir / "agent_schedules.json", "w") as f:
        json.dump(current_schedules, f, indent=2)
    
    # Log decisions
    decision_entry = {
        "timestamp": datetime.now().isoformat(),
        "reallocations": reallocation_log,
        "reasoning": f"Adjusted based on top themes: {', '.join(top_themes[:3])}",
        "backup": str(backup_path)
    }
    
    with open(strategy_dir / "strategy_decisions.log", "a") as f:
        f.write(json.dumps(decision_entry) + "\n")
    
    print("=== Strategic Reallocation Complete ===")
    print(f"\nBased on top themes: {', '.join(top_themes[:3])}")
    print(f"\nChanges made ({len(reallocation_log)}):")
    for entry in reallocation_log:
        print(f"  {entry['agent']} (alignment={entry['alignment']:.1f}):")
        for change in entry['changes']:
            print(f"    - {change}")
    
    print(f"\nBackup saved: {backup_path}")
    
    return reallocation_log

if __name__ == "__main__":
    reallocate_strategic_attention()
