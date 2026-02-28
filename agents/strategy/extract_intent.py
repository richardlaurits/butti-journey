#!/usr/bin/env python3
"""
Strategic Intent Engine - Extract and formalize Richard's priorities
"""

import json
import re
from datetime import datetime
from pathlib import Path

def extract_intent_model():
    workspace = Path("/home/richard-laurits/.openclaw/workspace")
    
    # Read MEMORY.md for explicit priorities
    theme_mentions = {}
    with open(workspace / "MEMORY.md") as f:
        memory = f.read()
        
        # Count mentions of key themes
        theme_keywords = {
            "career": ["career", "job", "linkedin", "work", "position", "hiring"],
            "family": ["pernilla", "jan", "arthur", "sigrid", "family", "greeting"],
            "health": ["health", "diabetes", "tir", "omnipod", "dexcom", "weight", "training"],
            "fantasy": ["fantasy", "fpl", "bundesliga", "seriea", "football", "premier league"],
            "language": ["french", "language", "lesson", "tutor"],
            "investment": ["investment", "portfolio", "stock", "crypto"]
        }
        
        for theme, keywords in theme_keywords.items():
            count = sum(len(re.findall(kw, memory, re.IGNORECASE)) for kw in keywords)
            theme_mentions[theme] = count

    # Check agent configuration depth
    detailed_agents = {}
    for agent_dir in (workspace / "agents").iterdir():
        if not agent_dir.is_dir():
            continue
        
        py_files = list(agent_dir.glob("*.py"))
        sh_files = list(agent_dir.glob("*.sh"))
        json_files = list(agent_dir.glob("*.json"))
        
        complexity = len(py_files) + len(sh_files) + len(json_files)
        
        if complexity > 0:
            detailed_agents[agent_dir.name] = {
                "complexity": complexity,
                "has_scripts": len(py_files) + len(sh_files) > 0,
                "has_config": len(json_files) > 0
            }

    # Define themes
    themes = {
        "career_advancement": {"score": 0, "evidence": [], "volatility": "medium"},
        "family_communication": {"score": 0, "evidence": [], "volatility": "low"},
        "fantasy_entertainment": {"score": 0, "evidence": [], "volatility": "high"},
        "health_optimization": {"score": 0, "evidence": [], "volatility": "low"},
        "language_learning": {"score": 0, "evidence": [], "volatility": "medium"},
        "investment_management": {"score": 0, "evidence": [], "volatility": "medium"}
    }

    # Score from memory mentions
    theme_map = {
        "career": "career_advancement",
        "family": "family_communication",
        "health": "health_optimization",
        "fantasy": "fantasy_entertainment",
        "language": "language_learning",
        "investment": "investment_management"
    }

    for theme_key, count in theme_mentions.items():
        mapped = theme_map.get(theme_key)
        if mapped and count > 0:
            themes[mapped]["score"] += min(40, count * 5)
            themes[mapped]["evidence"].append(f"{count} mentions in memory")

    # Score from agent complexity
    complexity_map = {
        "career-agent": "career_advancement",
        "fpl-agent": "fantasy_entertainment",
        "bundesliga-agent": "fantasy_entertainment",
        "health-agent": "health_optimization",
        "french-tutor-agent": "language_learning",
        "investment-agent": "investment_management"
    }

    for agent, data in detailed_agents.items():
        mapped = complexity_map.get(agent)
        if mapped:
            themes[mapped]["score"] += min(30, data["complexity"] * 5)
            themes[mapped]["evidence"].append(f"{agent} configured ({data['complexity']} files)")

    # Boost for recent recovery (shows current attention)
    themes["family_communication"]["score"] += 15
    themes["family_communication"]["evidence"].append("Recent recovery action (high attention)")

    # Normalize
    for theme in themes:
        themes[theme]["score"] = min(100, themes[theme]["score"])

    # Sort
    sorted_themes = sorted(themes.items(), key=lambda x: x[1]["score"], reverse=True)

    # Build model
    intent_model = {
        "generated_at": datetime.now().isoformat(),
        "analysis_period_days": 7,
        "top_themes": [{"rank": i+1, "theme": k, **v} for i, (k, v) in enumerate(sorted_themes)],
        "signals": {
            "memory_mentions": theme_mentions,
            "agent_complexity": {k: v["complexity"] for k, v in detailed_agents.items()},
        }
    }

    return intent_model, sorted_themes

if __name__ == "__main__":
    model, sorted_themes = extract_intent_model()
    
    strategy_dir = Path("/home/richard-laurits/.openclaw/workspace/agents/strategy")
    strategy_dir.mkdir(exist_ok=True)
    
    with open(strategy_dir / "intent_model.json", "w") as f:
        json.dump(model, f, indent=2)
    
    print("Strategic Priorities:")
    for i, (theme, data) in enumerate(sorted_themes, 1):
        print(f"{i}. {theme}: {data['score']}/100 (volatility: {data['volatility']})")
        print(f"   Evidence: {', '.join(data['evidence'])}")
