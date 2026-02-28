#!/usr/bin/env python3
"""
Memory Pruning Logic
Detects stale, redundant, and conflicting entries
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import shutil

MEMORY_DIR = Path("/home/richard-laurits/.openclaw/workspace/agents/memory")

def detect_stale_items(memory):
    """Detect entities inactive >60 days."""
    stale = []
    
    for name, data in memory.get("entities", {}).items():
        days_inactive = data.get("days_inactive")
        
        if days_inactive and days_inactive > 60:
            stale.append({
                "entity": name,
                "type": data.get("type"),
                "days_inactive": days_inactive,
                "last_active": data.get("last_active"),
                "suggested_action": "Review for archival" if days_inactive > 90 else "Mark dormant",
                "severity": "high" if days_inactive > 90 else "medium"
            })
    
    return sorted(stale, key=lambda x: x["days_inactive"], reverse=True)

def detect_redundant_entries(memory):
    """Detect potential redundancies."""
    redundant = []
    
    entities = memory.get("entities", {})
    
    # Check for similar names (potential duplicates)
    names = list(entities.keys())
    for i, name1 in enumerate(names):
        for name2 in names[i+1:]:
            # Simple similarity: shared words
            words1 = set(name1.lower().replace('-', ' ').split())
            words2 = set(name2.lower().replace('-', ' ').split())
            
            shared = words1 & words2
            if len(shared) >= 2 and name1 != name2:
                redundant.append({
                    "entity_1": name1,
                    "entity_2": name2,
                    "shared_terms": list(shared),
                    "suggested_action": "Merge or clarify distinction",
                    "severity": "low"
                })
    
    # Check for agents with same theme (potential overlap)
    theme_groups = {}
    for name, data in entities.items():
        if data.get("type") == "agent":
            theme = data.get("theme", "unknown")
            if theme not in theme_groups:
                theme_groups[theme] = []
            theme_groups[theme].append(name)
    
    for theme, agents in theme_groups.items():
        if len(agents) > 3:  # Many agents on same theme
            redundant.append({
                "entities": agents,
                "theme": theme,
                "count": len(agents),
                "suggested_action": f"Review if {len(agents)} agents for '{theme}' is excessive",
                "severity": "medium"
            })
    
    return redundant

def detect_contradictions(memory):
    """Detect potential contradictions."""
    contradictions = []
    
    entities = memory.get("entities", {})
    
    # Check for status mismatches
    for name, data in entities.items():
        # An entity marked active but inactive >30 days
        if data.get("status") == "active" and data.get("days_inactive", 0) > 30:
            contradictions.append({
                "entity": name,
                "issue": "Status 'active' but no activity for >30 days",
                "data": {
                    "status": data.get("status"),
                    "days_inactive": data.get("days_inactive"),
                    "last_active": data.get("last_active")
                },
                "suggested_action": "Update status to 'dormant' or trigger activation",
                "severity": "medium"
            })
    
    # Check for theme mismatches (agent theme vs recent activity theme)
    # This would require cross-referencing with activity logs
    
    return contradictions

def generate_review_report(memory, stale, redundant, contradictions):
    """Generate MEMORY_REVIEW.md with pruning suggestions."""
    
    now = datetime.now()
    
    report = f"""# Memory Review Report
Generated: {now.strftime("%Y-%m-%d %H:%M CET")}
Coverage: Last 90 days of system activity

## Summary

- **Total entities tracked**: {memory['total_entities']}
- **Stale items detected**: {len(stale)}
- **Redundant entries**: {len(redundant)}
- **Potential contradictions**: {len(contradictions)}

**⚠️ IMPORTANT**: This report contains SUGGESTIONS only. No automatic deletion has occurred.
All recommendations require manual review and approval.

---

## Stale Items ({len(stale)} detected)

Entities with no activity for >60 days. Consider archival or reactivation.

"""
    
    if stale:
        for item in stale[:10]:  # Top 10
            report += f"""### {item['entity']}
- **Type:** {item['type']}
- **Last active:** {item['last_active'][:10] if item['last_active'] else 'Unknown'}
- **Days inactive:** {item['days_inactive']}
- **Severity:** {item['severity'].upper()}
- **Suggestion:** {item['suggested_action']}

"""
    else:
        report += "No stale items detected. ✓\n\n"
    
    report += f"""---

## Redundant Entries ({len(redundant)} detected)

Potential duplicates or excessive fragmentation.

"""
    
    if redundant:
        for item in redundant[:5]:
            if "entity_1" in item:
                report += f"""### Similar Names Detected
- **Entities:** {item['entity_1']} ↔ {item['entity_2']}
- **Shared terms:** {', '.join(item['shared_terms'])}
- **Suggestion:** {item['suggested_action']}

"""
            else:
                report += f"""### Theme Overlap
- **Theme:** {item['theme']}
- **Entities ({item['count']}):** {', '.join(item['entities'][:5])}{'...' if item['count'] > 5 else ''}
- **Suggestion:** {item['suggested_action']}

"""
    else:
        report += "No redundancies detected. ✓\n\n"
    
    report += f"""---

## Potential Contradictions ({len(contradictions)} detected)

Data inconsistencies that may indicate errors or outdated information.

"""
    
    if contradictions:
        for item in contradictions[:5]:
            report += f"""### {item['entity']}
- **Issue:** {item['issue']}
- **Severity:** {item['severity'].upper()}
- **Suggestion:** {item['suggested_action']}

Details:
```json
{item['data']}
```

"""
    else:
        report += "No contradictions detected. ✓\n\n"
    
    report += f"""---

## Recommended Actions

### Immediate (This Week)
"""
    
    # Generate prioritized recommendations
    high_priority = [s for s in stale if s['severity'] == 'high']
    if high_priority:
        report += f"1. Review {len(high_priority)} high-priority stale items\n"
    
    if contradictions:
        report += f"2. Resolve {len(contradictions)} data contradictions\n"
    
    if not high_priority and not contradictions:
        report += "1. No immediate actions required\n"
    
    report += f"""
### This Month
"""
    
    medium_priority = [s for s in stale if s['severity'] == 'medium']
    if medium_priority:
        report += f"- Review {len(medium_priority)} medium-priority stale items\n"
    
    if redundant:
        report += f"- Evaluate {len(redundant)} potential redundancies\n"
    
    report += f"""
### Maintenance
- Run memory curator weekly
- Review this report before major system changes
- Archive obsolete entities monthly

---

## Archive Procedure

To archive an entity (non-destructive):

```bash
# 1. Backup current memory
cp agents/memory/strategic_memory.json \\
   agents/memory/strategic_memory.json.backup-$(date +%Y%m%d)

# 2. Edit strategic_memory.json
# Move entity from 'entities' to 'archived_entities'

# 3. Verify
python3 agents/memory/curator.py
```

---

## Entity Lifecycle

```
Active → Dormant (>30d) → Stale (>60d) → Obsolete (>90d)
   ↑                                    ↓
   └──────── Reactivation ──────────────┘  (if priority changes)
```

**Note:** Entities marked 'obsolete' can be safely archived but are retained in backups indefinitely.

---

*This report was generated by the Strategic Memory Curator*
*All changes are logged and reversible*
"""
    
    return report

def backup_memory():
    """Create timestamped backup before any changes."""
    memory_file = MEMORY_DIR / "strategic_memory.json"
    if memory_file.exists():
        backup_name = f"strategic_memory.json.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy(memory_file, MEMORY_DIR / backup_name)
        return backup_name
    return None

def main():
    """Run pruning analysis."""
    print("=== Memory Pruning Analysis ===\n")
    
    # Load strategic memory
    with open(MEMORY_DIR / "strategic_memory.json") as f:
        memory = json.load(f)
    
    # Create backup
    backup = backup_memory()
    if backup:
        print(f"✅ Backup created: {backup}")
    
    # Detect issues
    stale = detect_stale_items(memory)
    redundant = detect_redundant_entries(memory)
    contradictions = detect_contradictions(memory)
    
    print(f"\nAnalysis results:")
    print(f"  Stale items: {len(stale)}")
    print(f"  Redundant entries: {len(redundant)}")
    print(f"  Contradictions: {len(contradictions)}")
    
    # Generate report
    report = generate_review_report(memory, stale, redundant, contradictions)
    
    with open(MEMORY_DIR / "MEMORY_REVIEW.md", "w") as f:
        f.write(report)
    
    print(f"\n✅ MEMORY_REVIEW.md generated")
    
    return stale, redundant, contradictions

if __name__ == "__main__":
    main()
