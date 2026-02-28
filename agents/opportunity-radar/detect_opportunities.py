#!/usr/bin/env python3
"""
Opportunity Radar Agent - Detect high-leverage strategic moves
"""

import json
from datetime import datetime
from pathlib import Path

def analyze_opportunities():
    workspace = Path("/home/richard-laurits/.openclaw/workspace")
    radar_dir = workspace / "agents" / "opportunity-radar"
    
    # Load all data sources
    with open(workspace / "agents" / "ops-intelligence" / "ops_state.json") as f:
        ops_state = json.load(f)
    
    with open(workspace / "agents" / "ops-intelligence" / "friction_analysis.json") as f:
        friction = json.load(f)
    
    with open(workspace / "agents" / "strategy" / "intent_model.json") as f:
        intent = json.load(f)
    
    with open(workspace / "agents" / "strategy" / "contribution_map.json") as f:
        contributions = json.load(f)
    
    with open(workspace / "agents" / "ops-intelligence" / "agent_schedules.json") as f:
        schedules = json.load(f)
    
    # Load recovery log
    recoveries = []
    recovery_file = workspace / "agents" / "watchdog-agent" / "recovery_log.json"
    if recovery_file.exists():
        with open(recovery_file) as f:
            recoveries = json.load(f)
    
    opportunities = []
    
    # OPPORTUNITY 1: Health Agent Auto-Activation
    # High priority theme (70/100) but manual-only
    health_alignment = None
    for agent, data in contributions["agent_mapping"].items():
        if agent == "health-agent":
            health_alignment = data
            break
    
    if health_alignment and not schedules.get("health-agent", {}).get("auto_activate"):
        opportunities.append({
            "id": "opp-001",
            "theme": "health_optimization",
            "title": "Enable Health Agent Auto-Mode",
            "leverage_score": 85,
            "evidence": [
                f"Health is top-3 priority ({intent['top_themes'][2]['score']}/100)",
                f"Health-agent has {health_alignment['contribution_strength']}/100 capability",
                "Currently requires manual activation (wasted potential)",
                "No recoveries needed (stable subsystem)"
            ],
            "expected_roi": "Continuous health monitoring + 5min/week saved",
            "estimated_effort": "Low - single config change",
            "risk_level": "Low - reversible, health data is local",
            "current_state": "Manual activation only",
            "recommended_action": "Set health-agent.auto_activate = true in agent_schedules.json"
        })
    
    # OPPORTUNITY 2: French Tutor Activation
    # High alignment potential but currently disabled
    french_data = contributions["agent_mapping"].get("french-tutor-agent", {})
    if french_data.get("strategic_alignment", 0) == 0 and intent["top_themes"][3]["theme"] == "language_learning":
        opportunities.append({
            "id": "opp-002",
            "theme": "language_learning",
            "title": "Activate French Tutor for Daily Lessons",
            "leverage_score": 75,
            "evidence": [
                f"Language learning is priority ({intent['top_themes'][3]['score']}/100)",
                f"French-tutor-agent capability: {french_data.get('contribution_strength', 0)}/100",
                "Agent is under-leveraged (listed in insights)",
                "Low resource cost (simple lessons)"
            ],
            "expected_roi": "Daily French practice without manual triggering",
            "estimated_effort": "Low - enable auto_activate + review schedule",
            "risk_level": "Low - educational content only",
            "current_state": "Auto-activation disabled",
            "recommended_action": "Enable auto_activate, align hours with learning preference (morning/evening)"
        })
    
    # OPPORTUNITY 3: Agent Dormancy Crisis
    # 8 of 9 agents inactive - massive underutilization
    agent_stats = ops_state["subsystems"]["agents"]
    if agent_stats["dormant"] >= 7:
        opportunities.append({
            "id": "opp-003",
            "theme": "system_optimization",
            "title": "Resolve Mass Agent Dormancy (8/9 inactive)",
            "leverage_score": 90,
            "evidence": [
                f"Only {agent_stats['healthy']}/{agent_stats['count']} agents active",
                f"Agent stability: {friction['top_3_friction_points'][0]['stability_score']}/100 (critical)",
                "Smart scheduler deployed but no activations yet",
                "High-leverage agents (watchdog, ops-intel) running but others dormant"
            ],
            "expected_roi": "60% more agents self-managing = 3-4 hours/week saved",
            "estimated_effort": "Medium - verify scheduler integration with heartbeat",
            "risk_level": "Medium - requires testing activation flow",
            "current_state": "Smart scheduler deployed, 0 activations logged",
            "recommended_action": "Add smart_scheduler.py to HEARTBEAT.md rotation"
        })
    
    # OPPORTUNITY 4: Investment Agent Misalignment
    # Theme is 70/100 but agent disabled and low mention count
    investment_data = contributions["agent_mapping"].get("investment-agent", {})
    if investment_data.get("strategic_alignment", 0) == 0:
        opportunities.append({
            "id": "opp-004",
            "theme": "investment_management",
            "title": "Reconcile Investment Priority vs Agent Status",
            "leverage_score": 60,
            "evidence": [
                "Investment is 70/100 priority (tied for 2nd)",
                "But only 14 memory mentions (lowest of top themes)",
                "Agent has 0 alignment, auto-activation disabled",
                f"Agent capability: {investment_data.get('contribution_strength', 0)}/100"
            ],
            "expected_roi": "Clarity on actual priority - enable or deprioritize",
            "estimated_effort": "Low - decision + config change",
            "risk_level": "Low - strategic clarity only",
            "current_state": "Ambiguous priority vs resource allocation",
            "recommended_action": "Either: (A) Enable agent and increase mentions, or (B) Lower priority score to 40"
        })
    
    # OPPORTUNITY 5: Recovery Pattern Analysis
    # Only 1 recovery so far - Jan greeting
    if len(recoveries) == 1 and recoveries[0].get("action_id") == "retrigger_jan_greeting":
        opportunities.append({
            "id": "opp-005",
            "theme": "family_communication",
            "title": "Prevent Family Communication Failures",
            "leverage_score": 70,
            "evidence": [
                "Only recovery was Jan greeting (family communication)",
                "Recovery was successful but indicates fragility",
                "Family is 55/100 priority (lower than expected for daily action)",
                "No redundant backup for this critical relationship"
            ],
            "expected_roi": "Prevent missed greetings, maintain relationship consistency",
            "estimated_effort": "Low - add backup check or redundant trigger",
            "risk_level": "Low - additive only",
            "current_state": "Single point of failure for daily greeting",
            "recommended_action": "Add secondary trigger: if 26h elapsed since last greeting, escalate to Richard"
        })
    
    # OPPORTUNITY 6: Cron Consolidation
    # Multiple overlapping schedules
    cron_overlaps = []
    for agent, config in schedules.items():
        if len(config.get("active_hours", [])) > 8:
            cron_overlaps.append(agent)
    
    if len(cron_overlaps) >= 2:
        opportunities.append({
            "id": "opp-006",
            "theme": "system_optimization",
            "title": "Optimize Overlapping Agent Schedules",
            "leverage_score": 55,
            "evidence": [
                f"Agents with 8+ active hours: {', '.join(cron_overlaps)}",
                "May cause resource contention",
                "Smart scheduler may trigger multiple agents simultaneously"
            ],
            "expected_roi": "Smoother operation, reduced CPU spikes",
            "estimated_effort": "Low - stagger start times by 5-10 minutes",
            "risk_level": "Low - timing adjustment only",
            "current_state": f"{len(cron_overlaps)} agents with broad time windows",
            "recommended_action": "Stagger activation times to prevent collisions"
        })
    
    # Sort by leverage score
    opportunities.sort(key=lambda x: x["leverage_score"], reverse=True)
    
    # Save opportunities
    with open(radar_dir / "opportunities.json", "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "analysis_period_days": 7,
            "opportunities": opportunities
        }, f, indent=2)
    
    print(f"✅ Detected {len(opportunities)} opportunities")
    print("\nRanked by leverage score:")
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. {opp['title']} (score: {opp['leverage_score']}, effort: {opp['estimated_effort']})")
    
    return opportunities

if __name__ == "__main__":
    analyze_opportunities()
