#!/usr/bin/env python3
"""
Contribution Mapper - Map agents to strategic themes and score contribution
"""

import json
from datetime import datetime
from pathlib import Path

def map_contributions():
    workspace = Path("/home/richard-laurits/.openclaw/workspace")
    strategy_dir = workspace / "agents" / "strategy"
    
    # Load intent model
    with open(strategy_dir / "intent_model.json") as f:
        intent = json.load(f)
    
    top_themes = {t["theme"]: t["score"] for t in intent["top_themes"][:3]}
    
    # Agent to theme mapping
    agent_mapping = {
        "career-agent": {
            "themes": ["career_advancement"],
            "contribution_strength": 95,
            "resource_cost": "high",
            "autonomy_level": "Heal"
        },
        "fpl-agent": {
            "themes": ["fantasy_entertainment"],
            "contribution_strength": 90,
            "resource_cost": "medium",
            "autonomy_level": "Heal"
        },
        "bundesliga-agent": {
            "themes": ["fantasy_entertainment"],
            "contribution_strength": 70,
            "resource_cost": "low",
            "autonomy_level": "Heal"
        },
        "seriea-agent": {
            "themes": ["fantasy_entertainment"],
            "contribution_strength": 60,
            "resource_cost": "low",
            "autonomy_level": "Observe"
        },
        "health-agent": {
            "themes": ["health_optimization"],
            "contribution_strength": 85,
            "resource_cost": "medium",
            "autonomy_level": "Ask-First"
        },
        "french-tutor-agent": {
            "themes": ["language_learning"],
            "contribution_strength": 80,
            "resource_cost": "low",
            "autonomy_level": "Heal"
        },
        "investment-agent": {
            "themes": ["investment_management"],
            "contribution_strength": 75,
            "resource_cost": "low",
            "autonomy_level": "Observe"
        },
        "travel-agent": {
            "themes": ["family_communication"],
            "contribution_strength": 50,
            "resource_cost": "low",
            "autonomy_level": "Ask-First"
        },
        "fantasy-agent": {
            "themes": ["fantasy_entertainment"],
            "contribution_strength": 40,
            "resource_cost": "low",
            "autonomy_level": "Observe"
        },
        "watchdog-agent": {
            "themes": ["career_advancement", "health_optimization", "fantasy_entertainment", "family_communication"],
            "contribution_strength": 100,
            "resource_cost": "low",
            "autonomy_level": "Heal",
            "notes": "Enables all other agents"
        },
        "ops-intelligence": {
            "themes": ["career_advancement", "health_optimization", "fantasy_entertainment", "family_communication"],
            "contribution_strength": 90,
            "resource_cost": "low",
            "autonomy_level": "Heal",
            "notes": "Optimizes system efficiency"
        }
    }
    
    # Calculate strategic alignment score
    for agent, data in agent_mapping.items():
        alignment = 0
        for theme in data["themes"]:
            if theme in top_themes:
                alignment += top_themes[theme] * (data["contribution_strength"] / 100)
        
        data["strategic_alignment"] = round(alignment / len(data["themes"]), 1)
        
        # Calculate leverage score (alignment / cost)
        cost_multiplier = {"high": 3, "medium": 2, "low": 1}
        data["leverage_score"] = round(data["strategic_alignment"] / cost_multiplier.get(data["resource_cost"], 2), 1)
    
    # Identify insights
    under_leveraged = [a for a, d in agent_mapping.items() if d["strategic_alignment"] < 40 and d["contribution_strength"] > 70]
    over_allocated = [a for a, d in agent_mapping.items() if d["resource_cost"] == "high" and d["strategic_alignment"] < 50]
    high_leverage = sorted(agent_mapping.items(), key=lambda x: x[1]["leverage_score"], reverse=True)[:3]
    
    contribution_map = {
        "generated_at": datetime.now().isoformat(),
        "top_themes": list(top_themes.keys()),
        "agent_mapping": agent_mapping,
        "insights": {
            "under_leveraged": under_leveraged,
            "over_allocated": over_allocated,
            "high_leverage": [{"agent": a, "score": d["leverage_score"]} for a, d in high_leverage]
        }
    }
    
    with open(strategy_dir / "contribution_map.json", "w") as f:
        json.dump(contribution_map, f, indent=2)
    
    print("=== Agent Contribution Mapping ===")
    print(f"\nTop 3 Strategic Themes: {', '.join(top_themes.keys())}")
    print("\nAgent Alignment Scores:")
    for agent, data in sorted(agent_mapping.items(), key=lambda x: x[1]["strategic_alignment"], reverse=True):
        print(f"  {agent:20} alignment={data['strategic_alignment']:5.1f} leverage={data['leverage_score']:4.1f} cost={data['resource_cost']}")
    
    print(f"\nInsights:")
    print(f"  Under-leveraged: {under_leveraged}")
    print(f"  High-leverage agents: {[a for a, _ in high_leverage]}")
    
    return contribution_map

if __name__ == "__main__":
    map_contributions()
