#!/usr/bin/env python3
"""
Cost Optimizer Agent
Monitors model usage and identifies cost reduction opportunities
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/richard-laurits/.openclaw/workspace")
COST_DIR = WORKSPACE / "agents" / "cost"

def analyze_session_usage():
    """Analyze OpenClaw session logs for usage patterns."""
    sessions_dir = Path("/home/richard-laurits/.openclaw/agents/main/sessions")
    
    if not sessions_dir.exists():
        return {}
    
    usage = {
        "total_sessions": 0,
        "total_size_bytes": 0,
        "by_type": {},
        "large_sessions": [],
        "recent_activity": []
    }
    
    for session_file in sessions_dir.glob("*.jsonl"):
        if session_file.name.endswith(".lock"):
            continue
            
        size = session_file.stat().st_size
        usage["total_sessions"] += 1
        usage["total_size_bytes"] += size
        
        # Estimate cost from file size (rough heuristic: 1KB ~ 100 tokens)
        estimated_tokens = size / 10
        
        # Identify session type from filename or content
        session_type = "unknown"
        if "cron" in session_file.name:
            session_type = "cron_job"
        elif "direct" in session_file.name or len(session_file.name) < 40:
            session_type = "interactive"
        else:
            session_type = "background"
        
        usage["by_type"][session_type] = usage["by_type"].get(session_type, 0) + 1
        
        # Track large sessions (>500KB = heavy usage)
        if size > 500000:
            usage["large_sessions"].append({
                "file": session_file.name,
                "size_kb": round(size / 1024, 1)
            })
    
    return usage

def analyze_agent_call_frequency():
    """Analyze how often each agent triggers model calls."""
    agents_dir = WORKSPACE / "agents"
    
    agent_usage = {}
    
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue
        
        agent_name = agent_dir.name
        
        # Count log entries
        log_count = 0
        log_files = list(agent_dir.glob("*.log"))
        for log_file in log_files:
            with open(log_file) as f:
                log_count += len(f.readlines())
        
        # Check for scripts that might trigger model calls
        py_files = list(agent_dir.glob("*.py"))
        sh_files = list(agent_dir.glob("*.sh"))
        
        # Estimate complexity (lines of code)
        total_lines = 0
        for py_file in py_files:
            try:
                with open(py_file) as f:
                    total_lines += len(f.readlines())
            except:
                pass
        
        agent_usage[agent_name] = {
            "log_entries": log_count,
            "script_count": len(py_files) + len(sh_files),
            "code_lines": total_lines,
            "estimated_calls_per_day": estimate_daily_calls(agent_name, log_count)
        }
    
    return agent_usage

def estimate_daily_calls(agent_name, log_count):
    """Estimate daily model calls based on agent type and logs."""
    # Heuristics based on agent purpose
    call_frequency = {
        "watchdog-agent": 6,  # Every 4 hours = 6x/day
        "ops-intelligence": 1,  # Daily check
        "strategy": 1,  # Weekly but averaged
        "opportunity-radar": 1,  # Weekly
        "memory": 1,  # Weekly
        "momentum": 1,  # Weekly
        "french-tutor-agent": 1,  # Daily lesson
        "health-agent": 0.5,  # Every 2 days
        "career-agent": 1,  # Daily scan
        "fpl-agent": 0.3,  # Few times per week
        "bundesliga-agent": 0.3,
        "seriea-agent": 0.2,
        "fantasy-agent": 0.1,
        "investment-agent": 0.3,
        "travel-agent": 0.1,
    }
    
    return call_frequency.get(agent_name, 0.5)

def analyze_heartbeat_cost():
    """Analyze HEARTBEAT.md for cost implications."""
    heartbeat_file = WORKSPACE / "HEARTBEAT.md"
    
    if not heartbeat_file.exists():
        return {}
    
    content = heartbeat_file.read_text()
    
    # Count check types
    checks = {
        "gmail_monitor": content.lower().count("gmail"),
        "watchdog": content.lower().count("watchdog"),
        "linkedin_jobs": content.lower().count("linkedin"),
        "french_lesson": content.lower().count("french"),
        "jan_greeting": content.lower().count("jan"),
    }
    
    # Estimate frequency
    frequency_notes = {
        "var 30:e minut": "every 30 min",
        "var 4:e timme": "every 4 hours",
        "daily": "daily",
        "varje": "each/regular"
    }
    
    return {
        "check_types": checks,
        "estimated_checks_per_day": 48,  # 30-min intervals
        "high_frequency_checks": [k for k, v in checks.items() if v > 0]
    }

def calculate_cost_heuristics(usage, agent_usage, heartbeat):
    """Calculate cost estimates and identify optimization opportunities."""
    
    # Rough cost model (relative units)
    # Kimi k2.5: ~$0.50 per 1M tokens input, $1.50 per 1M tokens output
    # Average session: ~10K tokens = $0.015 per session
    
    COST_PER_SESSION = 0.015  # USD
    
    analysis = {
        "generated_at": datetime.now().isoformat(),
        "estimated_daily_cost_usd": 0,
        "estimated_monthly_cost_usd": 0,
        "by_agent": {},
        "optimizations": []
    }
    
    total_daily_calls = 0
    
    for agent_name, data in agent_usage.items():
        daily_calls = data["estimated_calls_per_day"]
        daily_cost = daily_calls * COST_PER_SESSION
        monthly_cost = daily_cost * 30
        
        analysis["by_agent"][agent_name] = {
            "daily_calls": daily_calls,
            "daily_cost_usd": round(daily_cost, 3),
            "monthly_cost_usd": round(monthly_cost, 2),
            "cost_profile": calculate_profile(daily_calls),
            "optimization_potential": []
        }
        
        total_daily_calls += daily_calls
        
        # Identify optimization opportunities
        agent_opt = analysis["by_agent"][agent_name]
        
        # Caching opportunity: repetitive checks
        if agent_name in ["watchdog-agent", "ops-intelligence"]:
            agent_opt["optimization_potential"].append({
                "type": "caching",
                "description": "Cache results if no state change detected",
                "potential_savings_pct": 40
            })
        
        # Frequency reduction: non-critical agents
        if agent_name in ["health-agent", "investment-agent"] and daily_calls < 1:
            agent_opt["optimization_potential"].append({
                "type": "reduce_frequency",
                "description": "Reduce check frequency (currently low value)",
                "potential_savings_pct": 50
            })
        
        # Batching: multiple small checks
        if agent_name == "career-agent":
            agent_opt["optimization_potential"].append({
                "type": "batching",
                "description": "Batch multiple scan types into single call",
                "potential_savings_pct": 30
            })
    
    # Calculate totals
    analysis["estimated_daily_cost_usd"] = round(total_daily_calls * COST_PER_SESSION, 2)
    analysis["estimated_monthly_cost_usd"] = round(analysis["estimated_daily_cost_usd"] * 30, 2)
    
    # System-wide optimizations
    if heartbeat.get("estimated_checks_per_day", 0) > 20:
        analysis["optimizations"].append({
            "scope": "system_wide",
            "type": "reduce_heartbeat_frequency",
            "current": "Every 30 minutes",
            "proposed": "Every 60 minutes during low-activity hours",
            "potential_savings_pct": 30,
            "risk": "Low - non-time-critical checks"
        })
    
    # Cache redundant status checks
    analysis["optimizations"].append({
        "scope": "watchdog",
        "type": "cache_status_checks",
        "description": "Don't re-check if status unchanged from last check",
        "potential_savings_pct": 50,
        "risk": "Low - add timestamp comparison"
    })
    
    # De-duplicate agent activation
    analysis["optimizations"].append({
        "scope": "smart_scheduler",
        "type": "prevent_redundant_activations",
        "description": "Track last activation time, skip if already active",
        "potential_savings_pct": 20,
        "risk": "Low - state tracking only"
    })
    
    return analysis

def calculate_profile(daily_calls):
    """Calculate cost profile category."""
    if daily_calls >= 5:
        return "heavy"
    elif daily_calls >= 1:
        return "moderate"
    elif daily_calls >= 0.5:
        return "light"
    else:
        return "minimal"

def main():
    """Main cost analysis."""
    print("=== Cost Optimizer Analysis ===\n")
    
    # Gather data
    usage = analyze_session_usage()
    agent_usage = analyze_agent_call_frequency()
    heartbeat = analyze_heartbeat_cost()
    
    # Calculate heuristics
    analysis = calculate_cost_heuristics(usage, agent_usage, heartbeat)
    
    # Save analysis
    COST_DIR.mkdir(exist_ok=True)
    with open(COST_DIR / "cost_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    print(f"Session usage:")
    print(f"  Total sessions: {usage.get('total_sessions', 0)}")
    print(f"  Total size: {usage.get('total_size_bytes', 0) / 1024 / 1024:.1f} MB")
    print(f"  By type: {usage.get('by_type', {})}")
    
    print(f"\nEstimated costs:")
    print(f"  Daily: ${analysis['estimated_daily_cost_usd']:.2f}")
    print(f"  Monthly: ${analysis['estimated_monthly_cost_usd']:.2f}")
    
    print(f"\nTop cost agents:")
    sorted_agents = sorted(analysis["by_agent"].items(), 
                          key=lambda x: x[1]["daily_cost_usd"], 
                          reverse=True)[:5]
    for agent, data in sorted_agents:
        print(f"  {agent}: ${data['daily_cost_usd']}/day (${data['monthly_cost_usd']}/mo) - {data['cost_profile']}")
    
    print(f"\nSystem optimizations identified: {len(analysis['optimizations'])}")
    for opt in analysis['optimizations']:
        print(f"  - {opt['type']}: {opt.get('potential_savings_pct', 0)}% savings")
    
    print(f"\n✅ cost_analysis.json generated")
    
    return analysis

if __name__ == "__main__":
    main()
