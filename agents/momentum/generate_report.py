#!/usr/bin/env python3
"""
Generate Weekly Momentum Report
Max 5 initiatives, focused on finish-or-kill decisions
"""

import json
from datetime import datetime
from pathlib import Path

def generate_report():
    """Generate MOMENTUM_REPORT.md with decisive recommendations."""
    
    momentum_dir = Path("/home/richard-laurits/.openclaw/workspace/agents/momentum")
    
    with open(momentum_dir / "momentum_state.json") as f:
        state = json.load(f)
    
    initiatives = state.get("initiatives", [])
    
    # Sort by momentum score (lowest first = most stalled)
    sorted_initiatives = sorted(initiatives, key=lambda x: x.get("momentum_score", 100))
    
    # Get top 5 that need attention
    attention_needed = [i for i in sorted_initiatives if i.get("momentum_score", 100) < 80][:5]
    
    now = datetime.now()
    
    report = f"""# Execution Momentum Report
Generated: {now.strftime("%Y-%m-%d %H:%M CET")}
Coverage: {state['total_initiatives']} tracked initiatives

## Executive Summary

**Momentum Overview:**
- Total initiatives: {state['total_initiatives']}
- Active (good momentum): {state['by_status'].get('active', 0)} ({round(state['by_status'].get('active', 0)/state['total_initiatives']*100)}%)
- In progress: {state['by_status'].get('in_progress', 0)}
- Stalled: {state['by_status'].get('stalled', 0)} ⚠️
- Not started: {state['by_status'].get('identified_not_started', 0)} 🚨

**Stagnation Signals:**
- No progress >10 days: {len(state['stagnation_signals'].get('no_progress_10_days', []))}
- Planning without execution: {len(state['stagnation_signals'].get('planning_without_execution', []))}
- Partial updates only: {len(state['stagnation_signals'].get('partial_updates', []))}

---

## Top 5 Initiatives Requiring Decisions

"""
    
    for i, init in enumerate(attention_needed, 1):
        score = init.get("momentum_score", 0)
        days = init.get("days_since_progress", 0)
        urgency = init.get("urgency", "medium")
        
        # Determine icon
        if score <= 20:
            icon = "🚨"
        elif score <= 50:
            icon = "⚠️"
        else:
            icon = "⚡"
        
        report += f"""### {i}. {icon} {init['name']}
**Type:** {init['type']} | **Source:** {init['source']}
**Momentum Score:** {score}/100 | **Days Since Progress:** {days}
**Status:** {init['status']} | **Urgency:** {urgency.upper()}

**Completion Criteria:**
{init.get('completion_criteria', 'Not defined')}

**DECISION REQUIRED:**
"""
        
        if init.get("recommendation") == "finish_or_kill":
            report += f"""➡️ **FINISH OR KILL** (Score: {score})

This initiative has momentum but is slipping. Choose:

**Option A: FINISH** (Recommended if <50% complete)
- [ ] Block 2 hours this week for focused execution
- [ ] Define specific completion milestone
- [ ] Set hard deadline (7 days max)
- [ ] Execute single push to completion

**Option B: KILL** (Acceptable if <20% complete)
- [ ] Archive related files to `agents/archive/`
- [ ] Document reason: "Strategic priority shifted"
- [ ] Free up mental space for higher-value work
- [ ] No guilt—explicit decisions > vague neglect

---

"""
        elif init.get("recommendation") == "kill_or_revive":
            report += f"""➡️ **KILL OR REVIVE** (Score: {score})

This initiative is effectively dead. Make it explicit:

**Option A: REVIVE** (Only if critical priority)
- [ ] Re-commit: Why does this matter NOW?
- [ ] Schedule 4-hour focused block
- [ ] Cut scope by 50%—ship minimum viable
- [ ] Or admit it's not happening

**Option B: KILL** (Recommended)
- [ ] Move all files to `initiatives/archive/{init['name'].replace(' ', '_').lower()}/`
- [ ] Update MEMORY.md with "Abandoned: [reason]"
- [ ] Remove from active tracking
- [ ] Cognitive load reduced ✓

---

"""
        else:
            report += f"""➡️ **ACCELERATE** (Score: {score})

This initiative has momentum but needs push to finish:
- [ ] Schedule 1-hour focused execution
- [ ] Identify single next action
- [ ] Complete within 3 days
- [ ] Mark as complete in next report

---

"""
    
    # Add momentum maintenance section
    report += f"""## Momentum Maintenance Protocol

### Weekly Ritual (5 minutes every Monday)
```bash
# 1. Check momentum
cat agents/momentum/MOMENTUM_REPORT.md

# 2. Make one finish-or-kill decision
# 3. Execute immediately (don't defer)
```

### Kill Criteria (Explicit Permission)
It's OK to kill an initiative if:
- ✅ Priority genuinely shifted
- ✅ sunk cost < cognitive load
- ✅ learning extracted, value captured
- ✅ guilt-free—it's strategic pruning

### Finish Criteria (Force Completion)
Force finish when:
- ✅ 70%+ complete (just ship it)
- ✅ Deadline within 7 days
- ✅ Blocker is procrastination, not complexity
- ✅ Perfect is enemy of done

---

## This Week's Decisive Action

**RECOMMENDATION:** Focus on the #1 stalled initiative above.

**Time allocation:**
- 80% energy → Top 1 stalled initiative (finish or kill)
- 15% energy → Top 2-3 (maintain momentum)
- 5% energy → Everything else (monitor only)

**Success metric:** By next report, either:
1. One initiative marked COMPLETE, or
2. One initiative explicitly KILLED and archived

No partial credit. No "still working on it."

---

## Archive Procedure

To kill an initiative (celebratory, not shameful):

```bash
# 1. Create archive directory
mkdir -p initiatives/archive/$(date +%Y%m%d)_name

# 2. Move all related files
cp -r agents/[initiative-name]/* initiatives/archive/$(date +%Y%m%d)_name/

# 3. Document learnings
echo "Abandoned: [reason]" >> initiatives/archive/$(date +%Y%m%d)_name/README.md

# 4. Remove from active tracking
# (Edit momentum_state.json if needed)

# 5. Celebrate freed cognitive space 🎉
```

---

## Philosophical Note

**Unfinished initiatives are cognitive debt.**

Each stalled project:
- Occupies mental RAM
- Creates background anxiety
- Reduces capacity for new opportunities
- Deludes you about actual capacity

**The goal is not to finish everything.**
The goal is to be explicit about what you're NOT doing.

Kill with clarity.
Finish with focus.

---

*Generated by Execution Momentum Agent*  
*All decisions are yours—this just surfaces the choice*
"""
    
    with open(momentum_dir / "MOMENTUM_REPORT.md", "w") as f:
        f.write(report)
    
    print("✅ MOMENTUM_REPORT.md generated")
    print(f"   Top 5 initiatives requiring decisions")
    return report

if __name__ == "__main__":
    generate_report()
