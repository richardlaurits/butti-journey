#!/usr/bin/env python3
"""
Strategic Memory Curator
Extracts and structures long-term intelligence from logs and memory files
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

WORKSPACE = Path("/home/richard-laurits/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "agents" / "memory"

def parse_date(date_str):
    """Parse various date formats."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str[:19], fmt)
        except:
            continue
    return None

def extract_entities_from_memory():
    """Extract entities from MEMORY.md."""
    entities = {}
    
    memory_file = WORKSPACE / "MEMORY.md"
    if not memory_file.exists():
        return entities
    
    content = memory_file.read_text()
    lines = content.split('\n')
    
    current_date = None
    
    for line in lines:
        # Extract dates
        date_match = re.search(r'\*\*\[(\d{4}-\d{2}-\d{2})', line)
        if date_match:
            current_date = parse_date(date_match.group(1))
        
        # Extract people
        people_patterns = [
            (r'(?:Jan|Pernilla|Arthur|Sigrid) Laurits', 'family'),
            (r'Richard', 'self'),
            (r'\b(Jan Laurits)\b', 'family'),
            (r'\b(Pernilla Laurits)\b', 'family'),
        ]
        
        for pattern, entity_type in people_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                name = match.group(1) if match.groups() else match.group(0)
                name = name.title()
                
                if name not in entities:
                    entities[name] = {
                        "type": "person",
                        "subtype": entity_type,
                        "first_seen": current_date.isoformat() if current_date else None,
                        "last_active": current_date.isoformat() if current_date else None,
                        "mentions": 0,
                        "themes": set(),
                        "status": "active"
                    }
                
                entities[name]["mentions"] += 1
                if current_date:
                    entities[name]["last_active"] = current_date.isoformat()
                
                # Detect themes from context
                if 'email' in line.lower() or 'greeting' in line.lower():
                    entities[name]["themes"].add("family_communication")
                if 'health' in line.lower() or 'diabetes' in line.lower():
                    entities[name]["themes"].add("health_optimization")
    
    # Convert sets to lists for JSON
    for entity in entities.values():
        entity["themes"] = list(entity["themes"])
    
    return entities

def extract_projects_from_git():
    """Extract projects/initiatives from git commits."""
    projects = {}
    
    git_log = WORKSPACE / ".git"
    if not git_log.exists():
        return projects
    
    # Read git log
    import subprocess
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%ai|%s", "-50"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.strip().split('\n'):
            if '|' not in line:
                continue
            
            parts = line.split('|', 2)
            if len(parts) < 3:
                continue
            
            commit_hash, date_str, message = parts
            commit_date = parse_date(date_str)
            
            # Extract project names
            project_patterns = [
                (r'Career Agent', 'career_advancement'),
                (r'FPL|Fantasy', 'fantasy_entertainment'),
                (r'Bundesliga|SerieA', 'fantasy_entertainment'),
                (r'French|FIDE', 'language_learning'),
                (r'Health|diabetes', 'health_optimization'),
                (r'Watchdog|Ops.?Intelligence', 'system_optimization'),
                (r'Job (crawler|market)', 'career_advancement'),
            ]
            
            for pattern, theme in project_patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    project_name = re.search(pattern, message, re.IGNORECASE).group(0)
                    
                    if project_name not in projects:
                        projects[project_name] = {
                            "type": "project",
                            "first_seen": commit_date.isoformat() if commit_date else None,
                            "last_active": commit_date.isoformat() if commit_date else None,
                            "commits": 0,
                            "themes": [theme],
                            "status": "active",
                            "recent_messages": []
                        }
                    
                    projects[project_name]["commits"] += 1
                    if commit_date:
                        projects[project_name]["last_active"] = commit_date.isoformat()
                    
                    if len(projects[project_name]["recent_messages"]) < 5:
                        projects[project_name]["recent_messages"].append(message[:80])
                    
                    break
    
    except Exception as e:
        print(f"Git extraction error: {e}")
    
    return projects

def extract_agents():
    """Extract agents as entities."""
    agents = {}
    
    agents_dir = WORKSPACE / "agents"
    if not agents_dir.exists():
        return agents
    
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue
        
        agent_name = agent_dir.name
        
        # Get last activity from logs
        logs = list(agent_dir.glob("*.log"))
        last_activity = None
        if logs:
            newest = max(logs, key=lambda p: p.stat().st_mtime)
            last_activity = datetime.fromtimestamp(newest.stat().st_mtime)
        
        # Determine theme mapping
        theme_map = {
            "career-agent": "career_advancement",
            "fpl-agent": "fantasy_entertainment",
            "bundesliga-agent": "fantasy_entertainment",
            "seriea-agent": "fantasy_entertainment",
            "fantasy-agent": "fantasy_entertainment",
            "health-agent": "health_optimization",
            "french-tutor-agent": "language_learning",
            "investment-agent": "investment_management",
            "travel-agent": "family_communication",
            "watchdog-agent": "system_optimization",
            "ops-intelligence": "system_optimization",
            "opportunity-radar": "system_optimization",
            "strategy": "system_optimization"
        }
        
        agents[agent_name] = {
            "type": "agent",
            "theme": theme_map.get(agent_name, "unknown"),
            "first_seen": None,  # Would need git history
            "last_active": last_activity.isoformat() if last_activity else None,
            "log_count": len(logs),
            "status": "active" if last_activity and (datetime.now() - last_activity).days < 7 else "dormant"
        }
    
    return agents

def extract_recovery_patterns():
    """Extract recovery actions as patterns."""
    patterns = {}
    
    recovery_file = WORKSPACE / "agents" / "watchdog-agent" / "recovery_log.json"
    if recovery_file.exists():
        with open(recovery_file) as f:
            recoveries = json.load(f)
        
        for recovery in recoveries:
            action_id = recovery.get("action_id", "unknown")
            
            if action_id not in patterns:
                patterns[action_id] = {
                    "type": "recovery_pattern",
                    "count": 0,
                    "first_seen": recovery.get("timestamp"),
                    "last_seen": recovery.get("timestamp"),
                    "success_rate": 0,
                    "theme": "system_reliability"
                }
            
            patterns[action_id]["count"] += 1
            patterns[action_id]["last_seen"] = recovery.get("timestamp")
            
            # Calculate success rate
            if recovery.get("result") == "success":
                patterns[action_id]["success_rate"] += 1
    
    # Normalize success rates
    for pattern in patterns.values():
        if pattern["count"] > 0:
            pattern["success_rate"] = round(pattern["success_rate"] / pattern["count"] * 100, 1)
    
    return patterns

def calculate_volatility(entity_data):
    """Calculate how often an entity changes status."""
    # Simple heuristic: more mentions = more volatile if status changes
    mentions = entity_data.get("mentions", 1)
    if mentions > 20:
        return "high"
    elif mentions > 5:
        return "medium"
    return "low"

def build_strategic_memory():
    """Build complete strategic memory model."""
    
    all_entities = {}
    
    # Extract from all sources
    memory_entities = extract_entities_from_memory()
    git_projects = extract_projects_from_git()
    agents = extract_agents()
    patterns = extract_recovery_patterns()
    
    # Merge all
    all_entities.update(memory_entities)
    all_entities.update(git_projects)
    all_entities.update(agents)
    all_entities.update(patterns)
    
    # Calculate derived fields
    now = datetime.now()
    
    for name, data in all_entities.items():
        # Calculate days since last active
        last_active_str = data.get("last_active")
        if last_active_str:
            try:
                last_active = datetime.fromisoformat(last_active_str.replace('Z', '+00:00'))
                days_inactive = (now - last_active).days
                data["days_inactive"] = days_inactive
                
                # Auto-detect status based on inactivity
                if days_inactive > 60:
                    data["status"] = "obsolete" if data.get("type") == "project" else "dormant"
                elif days_inactive > 30:
                    data["status"] = "stale"
            except:
                data["days_inactive"] = None
        
        # Calculate volatility
        data["volatility_score"] = calculate_volatility(data)
        
        # Add metadata
        data["entity_id"] = hashlib.md5(name.encode()).hexdigest()[:8]
    
    # Build structured memory
    strategic_memory = {
        "generated_at": now.isoformat(),
        "analysis_period_days": 90,
        "total_entities": len(all_entities),
        "entity_types": {},
        "by_theme": {},
        "entities": all_entities
    }
    
    # Aggregate by type
    for entity in all_entities.values():
        entity_type = entity.get("type", "unknown")
        strategic_memory["entity_types"][entity_type] = strategic_memory["entity_types"].get(entity_type, 0) + 1
        
        # Aggregate by theme
        themes = entity.get("themes", [entity.get("theme", "unknown")])
        for theme in themes if isinstance(themes, list) else [themes]:
            if theme not in strategic_memory["by_theme"]:
                strategic_memory["by_theme"][theme] = []
            strategic_memory["by_theme"][theme].append(entity)
    
    return strategic_memory

def main():
    """Main curation process."""
    print("=== Strategic Memory Curation ===\n")
    
    memory = build_strategic_memory()
    
    # Save structured memory
    MEMORY_DIR.mkdir(exist_ok=True)
    with open(MEMORY_DIR / "strategic_memory.json", "w") as f:
        json.dump(memory, f, indent=2, default=str)
    
    print(f"✅ Extracted {memory['total_entities']} entities")
    print(f"\nBy type:")
    for entity_type, count in memory['entity_types'].items():
        print(f"  {entity_type}: {count}")
    
    print(f"\nBy theme:")
    for theme, entities in memory['by_theme'].items():
        print(f"  {theme}: {len(entities)} entities")
    
    return memory

if __name__ == "__main__":
    main()
