# Agent Architecture - Richard's OpenClaw System
**Updated:** 2026-02-23 23:55 CET

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           AGENT ARCHITECTURE OVERVIEW                            │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
│                              │   RICHARD        │
│                              │   (Human)        │
│                              └────────┬─────────┘
│                                       │ Commands
│                                       │ Requests
│                                       ▼
│┌──────────────────────────────────────────────────────────────────────────────┐
││                           MAIN SESSION (ME - ButtiBot)                        │
││                           Role: Coordinator / Supervisor                      │
││                           Status: ✅ ACTIVE                                   │
│├──────────────────────────────────────────────────────────────────────────────┤
││  Responsibilities:                                                            │
││  • Interpret user intent                                                      │
││  • Spawn/terminate sub-agents                                                 │
││  • Monitor agent health (via subagents tool)                                  │
││  • Route information between agents                                           │
││  • Manage context window                                                      │
││  • Escalate to human when needed                                              │
│└────────────────────┬─────────────────────────────┬───────────────────────────┘
│                     │                             │
│                     │ Spawns                      │ Spawns
│                     ▼                             ▼
│    ┌──────────────────────────┐    ┌──────────────────────────┐
│    │   FPL AGENT              │    │   BUNDESLIGA AGENT       │
│    │   ⚽ Premier League       │    │   ⚽ German Bundesliga    │
│    ├──────────────────────────┤    ├──────────────────────────┤
│    │ Trigger: Auto (cron)     │    │ Trigger: Auto (cron)     │
│    │ Schedule: 24h + 3h       │    │ Schedule: Fridays 10:00  │
│    │   before deadline        │    │                          │
│    │ Status: 🟡 STANDBY       │    │ Status: 🟡 STANDBY       │
│    │ Players: 11 tracked      │    │ Players: 11 tracked      │
│    │ Output: Telegram alerts  │    │ Output: Telegram alerts  │
│    └──────────────────────────┘    └──────────────────────────┘
│                     │                             │
│                     │                             │
│    ┌──────────────────────────┐    ┌──────────────────────────┐
│    │   CAREER AGENT           │    │   HEALTH AGENT           │
│    │   💼 Job Search          │    │   💪 Fitness Tracking      │
│    ├──────────────────────────┤    ├──────────────────────────┤
│    │ Trigger: Auto (cron)     │    │ Trigger: Manual          │
│    │ Schedule: Fridays 09:00  │    │ Schedule: On-demand      │
│    │ Status: 🟡 STANDBY       │    │ Status: 🔴 DORMANT       │
│    │ Sources: 10+ job boards  │    │ Data: Trio, Apple Health │
│    │ Output: Telegram summary │    │ Output: Weekly brief     │
│    └──────────────────────────┘    └──────────────────────────┘
│                     │                             │
│                     │                             │
│    ┌──────────────────────────┐    ┌──────────────────────────┐
│    │   SERIE A AGENT          │    │   FANTASY AGENT (legacy) │
│    │   ⚽ Italian League       │    │   ⚽ General FPL          │
│    ├──────────────────────────┤    ├──────────────────────────┤
│    │ Trigger: Manual          │    │ Trigger: Manual          │
│    │ Schedule: On-demand      │    │ Schedule: On-demand      │
│    │ Status: 🔴 DORMANT       │    │ Status: 🔴 DEPRECATED    │
│    │ Method: Screenshot       │    │ (replaced by FPL agent)  │
│    │ Output: Manual compare   │    │                          │
│    └──────────────────────────┘    └──────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUTOMATION LAYER                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Cron: Daily  │  │ Cron: Fri    │  │ Cron: Fri    │  │ Cron: Every  │         │
│  │ 10:00 CET    │  │ 09:00 CET    │  │ 10:00 CET    │  │ 6 hours      │         │
│  │              │  │              │  │              │  │              │         │
│  │ Jan's        │  │ Career       │  │ Bundesliga   │  │ FPL Deadline │         │
│  │ Greeting     │  │ Weekly Scan  │  │ Injury Check │  │ Check        │         │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA & STATE LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  MEMORY.md (407 lines)          Agent States         Skills (21 active)          │
│  ├─ Long-term memory            ├─ fpl-agent/        ├─ gmail                    │
│  ├─ User preferences            ├─ bundesliga-agent/  ├─ github                   │
│  └─ Key decisions               ├─ career-agent/      ├─ weather                  │
│                                 ├─ health-agent/      ├─ docker-essentials        │
│  Daily Logs                     ├─ seriea-agent/      ├─ git-workflows            │
│  ├─ memory/2026-02-23.md        └─ fantasy-agent/     ├─ ssh-tunnel               │
│  ├─ memory/2026-02-18.md                              ├─ regex-patterns           │
│  └─ memory/2026-02-19.md                              └─ ... 16 more              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Current Status Matrix

| Agent | Status | Trigger | Last Run | Next Run | Health |
|-------|--------|---------|----------|----------|--------|
| **Me (Main)** | 🟢 ACTIVE | Human commands | Now | Continuous | ✅ Healthy |
| **FPL** | 🟡 STANDBY | Cron (deadline-based) | - | GW28: Thu 19:30 | ⏳ Waiting |
| **Bundesliga** | 🟡 STANDBY | Cron (Fri 10:00) | - | Fri 28 Feb 10:00 | ⏳ Waiting |
| **Career** | 🟡 STANDBY | Cron (Fri 09:00) | - | Fri 28 Feb 09:00 | ⏳ Waiting |
| **Health** | 🔴 DORMANT | Manual | 2026-02-14 | On-demand | 💤 Inactive |
| **Serie A** | 🔴 DORMANT | Manual | Never | On-demand | 💤 Inactive |

## Supervisor Role Analysis

### Current Setup: I Act as Supervisor

**What I do as Coordinator:**
- ✅ Spawn agents via `sessions_spawn`
- ✅ Monitor via `subagents(action=list)`
- ✅ Route commands and context
- ✅ Manage git/commits
- ✅ Handle user requests
- ✅ Maintain MEMORY.md

**What's Missing (for full autonomy):**
- ❌ I don't auto-restart failed agents
- ❌ I don't monitor agent health continuously
- ❌ I don't escalate without user prompt
- ❌ I don't self-heal

### Do We Need a Dedicated Supervisor Agent?

**Option A: Keep Current (I act as supervisor)**
- Pros: Simple, direct control, you oversee everything
- Cons: Requires human to check, no self-healing
- Best for: Your current usage pattern

**Option B: Add Supervisor Agent**
- Pros: Self-healing, auto-restart, 24/7 monitoring
- Cons: More complexity, another layer
- Best for: Fully autonomous system

## Recommendation

**For now: Keep Option A (I supervise)**

Your pattern works well:
- You give me high-level commands
- I delegate to sub-agents
- You review results
- We iterate together

**Consider Option B when:**
- You want true "set and forget" automation
- Agents fail frequently and need restart
- You want 24/7 monitoring without human checks
- System scales to 10+ agents

## Immediate Improvements (No New Agent Needed)

1. **Add heartbeat check to main session**
   - Every 6 hours: Check if agents are healthy
   - Alert you if any issues

2. **Add agent status to daily summary**
   - "All agents healthy" or "FPL agent needs attention"

3. **Git auto-commit agent states**
   - Log when agents run/fail
   - Track success rates

**Bottom line:** I act as your supervisor/coordinator. The system works. We can add a dedicated supervisor later if you want full autonomy without human oversight.

