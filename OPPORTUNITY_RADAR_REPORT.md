# Opportunity Radar Report
**System:** OpenClaw (Richard Laurits)  
**Generated:** 2026-02-23 23:25 CET  
**Runtime:** OpenClaw 2026.2.22-2 (Kimi K2.5)  

---

## Executive Summary

This OpenClaw system shows mature organization with 21 active skills, dual Gmail integration, and agent orchestration patterns. **Critical finding:** 6 agent directories exist but 0 active sub-agents — full automation potential is dormant. Token usage is efficient (1.1k/134 in/out), but context bloat is emerging in MEMORY.md (407 lines, 20KB). Gateway is healthy (RPC ok) but Node version manager dependency creates fragility. **Highest leverage opportunity:** Activate the 4 defined agents (FPL, Bundesliga, Health, Career) with proper cron scheduling vs current placeholder state.

---

## Efficiency Findings

### 🔴 HIGH IMPACT

| Finding | Current State | Impact | Fix |
|---------|--------------|--------|-----|
| **Dormant Agents** | 6 agent dirs, 0 active sessions | 100% automation loss | Spawn sessions with `sessions_spawn` |
| **Uncommitted Skills** | 8 new skills unstaged in git | Risk of loss, no rollback | `git add skills/` + commit |
| **Missing Cron Jobs** | Fantasy intel scripts exist but no cron | Manual checking required | Add 2 cron entries (23:00 daily, Fri 08:00) |
| **Git Hygiene** | 41 unstaged files, mixed tracked/untracked | Chaos risk, no audit trail | Commit `.env.*` pattern to `.gitignore`, stage rest |

### 🟡 MEDIUM IMPACT

| Finding | Details | Recommendation |
|---------|---------|----------------|
| **MEMORY.md bloat** | 407 lines, growing without archival | Archive entries >30 days to `memory/archive/` |
| **Multiple model configs** | 3 auth profiles (anthropic, kimi-coding, moonshot) | Remove unused (anthropic, kimi-coding) |
| **Skills without SKILL.md** | 16 Python files but only 20 SKILL.md | Audit: 4 skills may lack documentation |
| **Duplicate state files** | `monitor_state.json`, `forward_state.json` scattered | Consolidate to `.openclaw/state/` |

### 🟢 LOW IMPACT

| Finding | Details |
|---------|---------|
| **Large venv** | 294MB — normal for Python projects |
| **Job screenshots** | 2.9MB unused since crawler v2 diagnostic | Clean if career agent abandoned |
| **Memory files** | 442 lines total across 4 daily logs — acceptable |

---

## Risk Findings

### 🔴 CRITICAL RISKS

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Gateway fragility** | Medium | High | Service uses NVM Node path (`/home/richard-laurits/.nvm/versions/node/v22.22.0/bin/node`). NVM upgrades break systemd. Run `openclaw doctor --repair` to fix service file. |
| **Token exposure** | Low | Critical | `.env.brave` and `.env.kimi` contain API keys. They are in git working tree but not committed. **Action:** Add to `.gitignore` immediately if not already. |
| **No agent supervision** | High | Medium | Sub-agents spawn but no parent monitors them. Add `subagents(action=list)` to heartbeat. |

### 🟡 MODERATE RISKS

| Risk | Details |
|------|---------|
| **Fantasy scripts are stubs** | `nightly-scraper.py`, `friday-scraper.py` contain only placeholder logic. Real web scraping not implemented despite Brave API being configured. |
| **Gmail token persistence** | `token.pickle` in git history (deleted now but in history). Regenerate if repo ever public. |
| **No backup strategy** | No automated backup of MEMORY.md, config, or state files. |

---

## Architecture Improvements

### 1. Agent Orchestration Layer (Priority 1)

**Current:** Manual agent spawning, no supervision  
**Target:** Self-healing agent mesh

```bash
# Add to HEARTBEAT.md
openclaw cron 23:00 --task "sessions_spawn(task='Run FPL nightly scraper', label='fpl-agent', thread=true)"
openclaw cron fri-08:00 --task "sessions_spawn(task='Run Bundesliga Friday scraper', label='bundesliga-agent', thread=true)"
openclaw cron sun-20:00 --task "sessions_spawn(task='Weekly health summary', label='health-agent', thread=true)"
```

**Implementation:**
1. Convert 4 agent directories to spawnable sessions
2. Add `subagents(action=list)` check to heartbeat
3. Auto-restart agents that fail 3x

### 2. Token Optimization Enforcement (Priority 2)

**Current:** OPTIMIZATION.md exists but not enforced  
**Target:** Hard caps at runtime

Add to `~/.openclaw/openclaw.json`:
```json
"agents": {
  "defaults": {
    "maxCalls": 50,
    "maxOutputTokens": 2500,
    "reflectionInterval": 10
  }
}
```

### 3. State Consolidation (Priority 3)

**Current:** State files scattered across skills/  
**Target:** Centralized state in `.openclaw/state/`

```
.openclaw/state/
  ├── gmail/
  │   ├── monitor_state.json
  │   └── responder_state.json
  ├── agents/
  │   ├── fpl_last_run.json
  │   └── health_weekly.json
  └── system/
      └── last_heartbeat.json
```

---

## Automation Opportunities

### Immediate (This Week)

| Opportunity | Effort | Value | Command |
|-------------|--------|-------|---------|
| **Activate FPL agent** | 30 min | High | `sessions_spawn(task='Check FPL injuries for Haaland, Salah, Saka...', label='fpl-agent')` |
| **Activate Bundesliga agent** | 30 min | High | `sessions_spawn(task='Check Bundesliga injuries for Kane, Díaz...', label='bundesliga-agent')` |
| **Git cleanup** | 15 min | Medium | `git add skills/api-dev skills/dns-networking ... && git commit -m "Add 8 Linux skills"` |
| **Add .gitignore** | 5 min | High | `echo ".env.*" >> .gitignore && echo "__pycache__/" >> .gitignore` |

### Short Term (This Month)

| Opportunity | Effort | Value |
|-------------|--------|-------|
| **Implement real FPL scraper** | 2h | High — currently placeholder |
| **Health data integration** | 4h | High — Nightscout API for Trio |
| **Calendar triage agent** | 3h | Medium — parse invites, suggest prep |
| **Shopping list agent** | 2h | Low — family value, simple start |

### Long Term (Next Quarter)

| Opportunity | Effort | Value |
|-------------|--------|-------|
| **Self-healing agent mesh** | 8h | High — auto-restart, health checks |
| **Memory RAG system** | 6h | Medium — semantic search over all memory |
| **Multi-device gateway** | 4h | Medium — phone pairing for mobile triggers |

---

## Immediate 5-Step Improvement Plan

### Step 1: Secure Secrets (5 min)
```bash
cd ~/.openclaw/workspace
echo ".env.*" >> .gitignore
echo "token.pickle" >> .gitignore
echo "**/__pycache__/" >> .gitignore
git add .gitignore && git commit -m "Secure: ignore env files and pycache"
```

### Step 2: Commit New Skills (5 min)
```bash
git add skills/api-dev skills/dns-networking skills/docker-essentials \
        skills/emergency-rescue skills/git-essentials skills/git-workflows \
        skills/regex-patterns skills/ssh-tunnel \
        agents/bundesliga-agent agents/fpl-agent agents/seriea-screenshots
git commit -m "Add 8 Linux skills + fantasy intel agents"
```

### Step 3: Fix Gateway Service (10 min)
```bash
openclaw doctor --repair
# Or manually: edit ~/.config/systemd/user/openclaw-gateway.service
# Change ExecStart from NVM path to /usr/bin/node
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

### Step 4: Activate First Agent (15 min)
```bash
# Test FPL agent manually
sessions_spawn(
  task="Check FPL injuries for Haaland, Salah, Saka, Son, Gabriel, Rice, Timber, Guéhi, Solanke, Hill, Thiago. Use web_search with freshness=pw. Report any injuries or suspensions to Richard via Telegram.",
  label="fpl-agent",
  thread=true
)
```

### Step 5: Archive Old Memory (10 min)
```bash
mkdir -p memory/archive
# Move entries from MEMORY.md dated before 2026-02-01
git add memory/archive/ && git commit -m "Archive old memory entries"
```

---

## High-Leverage Upgrades for Autonomy

### Upgrade 1: Agent Supervisor Pattern
Create a `supervisor-agent` that:
- Runs every 6 hours via cron
- Lists all subagents with `subagents(action=list)`
- Restarts any agent that hasn't reported in 24h
- Sends Telegram summary of agent health

**Value:** Self-healing system, no manual intervention  
**Effort:** 2 hours

### Upgrade 2: Intent-Based Routing
Add to `SOUL.md` or `AGENTS.md`:
```markdown
## Intent Routing
- "Check my team" → FPL agent
- "Any injuries?" → FPL + Bundesliga agents
- "Job market" → Career agent
- "Health update" → Health agent
- "Morning briefing" → All agents (aggregated)
```

Implement routing logic in main session to spawn appropriate specialist.  
**Value:** Natural language triggers automation  
**Effort:** 3 hours

### Upgrade 3: Progressive Memory Archival
Automate weekly via cron:
```bash
0 3 * * 0 cd ~/.openclaw/workspace && python3 -c "
import re
from datetime import datetime, timedelta
# Parse MEMORY.md, extract entries >30 days old
# Archive to memory/archive/YYYY-MM-DD.md
# Truncate MEMORY.md
"
```

**Value:** Keeps MEMORY.md lean (<15KB), preserves history  
**Effort:** 1 hour

---

## Appendix: System Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Active skills | 21 | ✅ Good |
| Active sub-agents | 0 | 🔴 Critical |
| Agent directories | 6 | ⚠️ Dormant |
| Git commits (30d) | 18 | ✅ Active dev |
| Unstaged files | 41 | 🔴 Cleanup needed |
| MEMORY.md lines | 407 | ⚠️ Approaching limit |
| Daily logs | 4 files | ✅ Acceptable |
| Cron jobs | 1 | ⚠️ Underutilized |
| Gateway RPC | ok | ✅ Healthy |
| Model | Kimi K2.5 | ✅ Current |

---

## Structural Gap Analysis: Current vs Ideal Autonomous Architecture

### Ideal Autonomous Agent Architecture

Based on modern agent orchestration patterns (AutoGPT, OpenAI Assistants, LangChain, CrewAI):

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    IDEAL AUTONOMOUS AGENT ARCHITECTURE                      │
└────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│ 1. ORCHESTRATION LAYER (Control Plane)                                  │
│    - Agent lifecycle management (spawn/monitor/terminate)               │
│    - Task routing & delegation                                          │
│    - Failure recovery & retry logic                                     │
│    - Resource allocation (token budgets, rate limits)                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. AGENT MESH (Worker Pool)                                            │
│    - Specialized sub-agents (FPL, Career, Health, etc.)                 │
│    - Each agent: stateful, isolated, bounded context                    │
│    - Inter-agent communication protocol                                 │
│    - Health checks & heartbeat                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. STATE & MEMORY LAYER                                                 │
│    - Vector DB for semantic memory (RAG)                                │
│    - Structured state (JSON/YAML configs)                               │
│    - Temporal memory (session history, logs)                            │
│    - Ephemeral cache (short-term context)                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. TOOL & SKILL REGISTRY                                                │
│    - Skills as composable units                                         │
│    - Tool discovery & dynamic loading                                   │
│    - Capability advertisements (what can I do?)                         │
│    - Versioning & rollback                                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5. SCHEDULING & EVENT SYSTEM                                            │
│    - Cron-based periodic tasks                                          │
│    - Event-driven triggers (webhooks, file changes)                     │
│    - Conditional workflows (if-this-then-that)                          │
│    - Priority queue for task scheduling                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 6. OBSERVABILITY & GOVERNANCE                                           │
│    - Logging & audit trails                                             │
│    - Cost tracking per agent/task                                       │
│    - Performance metrics (latency, success rate)                        │
│    - Circuit breakers for failing services                              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Gap Analysis Matrix

| Architecture Layer | Ideal State | Current State | Gap Severity | Evidence |
|-------------------|-------------|---------------|--------------|----------|
| **1. Orchestration** | Central control plane with lifecycle management | Manual spawning, no supervision | 🔴 CRITICAL | `subagents list` shows 0 active; no auto-restart |
| **2. Agent Mesh** | Stateful workers with health checks | 6 directories, 0 running sessions | 🔴 CRITICAL | Agents exist as files only, never activated |
| **3. State & Memory** | Vector DB + structured state + ephemeral cache | File-based only, no RAG | 🟡 MEDIUM | MEMORY.md is flat text, no semantic search |
| **4. Tool Registry** | Dynamic discovery, capability ads | Static skill loading | 🟢 LOW | 21 skills loaded but no discovery mechanism |
| **5. Scheduling** | Cron + event triggers + priority queue | 1 cron job only (daily greeting) | 🟡 MEDIUM | FPL/Bundesliga agents have no cron |
| **6. Observability** | Logs, metrics, cost tracking, circuit breakers | Git commits, basic logs | 🟡 MEDIUM | No per-agent cost tracking, no metrics |

### Detailed Structural Gaps

#### Gap 1: Missing Control Plane (CRITICAL)

**What's Missing:**
- No supervisor agent monitoring sub-agent health
- No automatic restart on failure
- No task queue or work distribution
- No token budget enforcement per agent

**Impact:**
- Agents must be manually spawned every time
- Failed agents stay dead until human intervention
- No way to prioritize urgent tasks
- Token overruns possible (no hard caps enforced)

**Implementation Path:**
```python
# agents/supervisor-agent/SUPERVISOR.md
"""
Role: System orchestrator
Tasks:
  1. Every 6h: subagents(action=list) → check health
  2. If agent missing >24h: auto-restart with sessions_spawn
  3. Track token usage per agent
  4. Alert on repeated failures (>3x)
  5. Maintain registry of active agents
"""
```

#### Gap 2: State Layer Not Semantic (MEDIUM)

**What's Missing:**
- No vector database for memory retrieval
- No semantic search over MEMORY.md
- No automatic context window management
- No memory summarization/compression

**Current:** Flat markdown files (MEMORY.md: 407 lines)  
**Ideal:** ChromaDB/Pinecone with embeddings + RAG retrieval

**Evidence:**
- You rely on `memory_search` FTS (full-text search) only
- No semantic similarity matching
- Context grows linearly with each session

**Quick Win:**
```bash
# Add to skills/memory-rag/
pip install chromadb sentence-transformers
# Embed MEMORY.md sections
# Retrieve by semantic similarity, not just keyword
```

#### Gap 3: No Event-Driven Architecture (MEDIUM)

**What's Missing:**
- Webhook listeners for external events
- File watcher triggers (e.g., new screenshot → process)
- Conditional workflows (if email from X → do Y)
- Real-time data pipelines

**Current:** Pull-based only (cron every 30min)  
**Ideal:** Push + pull hybrid

**Use Cases Blocked:**
- "When I get a calendar invite → prepare briefing"
- "When new FPL injury news breaks → alert immediately"
- "When Dexcom reading is low → notify instantly"

**Implementation:**
```python
# Event router (new agent)
sources:
  - gmail_webhook: new_important_email
  - fpl_api_poll: injury_news
  - dexcom_stream: glucose_alert
  
rules:
  - if: "email.from == 'pernilla@'" → action: "priority_alert"
  - if: "fpl.injury == 'your_player'" → action: "telegram_alert"
```

#### Gap 4: Agent Isolation Violated (MEDIUM)

**What's Missing:**
- Agents share filesystem (no sandbox)
- No resource limits (CPU, memory, disk)
- No network isolation
- No secret management per agent

**Current:** All agents read/write to same `~/.openclaw/workspace/`  
**Ideal:** Containerized/isolated environments

**Risk:**
- One buggy agent can corrupt shared state
- No rollback capability per agent
- Secrets visible to all agents

**Mitigation:**
```bash
# Per-agent working directories
agents/
  fpl-agent/
    workspace/        # isolated
    secrets.env       # agent-specific
    state.json        # private state
```

#### Gap 5: No Capability Registry (LOW)

**What's Missing:**
- Agents don't advertise what they can do
- No dynamic skill discovery
- No composition (Agent A + Agent B → new capability)

**Current:** Hardcoded routing in main session  
**Ideal:** Self-describing agents

**Example:**
```yaml
# agents/fpl-agent/CAPABILITIES.yaml
capabilities:
  - name: "analyze_gameweek"
    input: ["gameweek_number"]
    output: "briefing_text"
    triggers: ["cron:23:00", "command:check_fpl"]
  
  - name: "check_injuries"
    input: ["player_list"]
    output: "alerts"
    triggers: ["cron:23:00"]
```

#### Gap 6: Observability Gaps (MEDIUM)

**What's Missing:**
- Per-agent cost tracking
- Success/failure rate metrics
- Latency percentiles
- Alerting on anomalies

**Current:** Git commit history as audit log  
**Ideal:** Prometheus/Grafana or simple metrics file

**Data Not Tracked:**
- How many tokens does FPL agent use per run?
- What's the failure rate of career agent?
- Which skills are never used?

**Quick Implementation:**
```json
// ~/.openclaw/workspace/.metrics/agents.json
{
  "fpl-agent": {
    "runs": 45,
    "tokens_avg": 1200,
    "success_rate": 0.94,
    "last_run": "2026-02-23T22:00:00Z"
  }
}
```

### Architecture Maturity Score

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Orchestration | 2/10 | 10 | No control plane, manual only |
| Agent Isolation | 4/10 | 10 | Separate dirs, shared filesystem |
| State Management | 5/10 | 10 | File-based, no RAG, growing bloat |
| Scheduling | 3/10 | 10 | 1 cron job, no event triggers |
| Observability | 3/10 | 10 | Git logs only, no metrics |
| Tool Registry | 6/10 | 10 | 21 skills, static loading |
| **TOTAL** | **23/60** | **60** | **38% maturity** |

### Target State: 6-Month Roadmap

| Phase | Focus | Deliverables | Maturity Target |
|-------|-------|--------------|-----------------|
| **1 (Month 1)** | Foundation | Supervisor agent, basic metrics, git hygiene | 45% |
| **2 (Month 2-3)** | Activation | All 6 agents running via cron, event triggers | 55% |
| **3 (Month 4)** | Intelligence | RAG memory, semantic search, auto-summarization | 65% |
| **4 (Month 5-6)** | Optimization | Token budgets, circuit breakers, cost tracking | 75% |

### Critical Path to Autonomy

**What's blocking full autonomy:**

1. **No Supervisor** → Manual restart required  
   *Fix: Build supervisor-agent (2h)*

2. **No Persistent State** → Agents lose context on restart  
   *Fix: Session persistence with `thread=true` (30min)*

3. **No Event System** → Can't react to real-time data  
   *Fix: Webhook listener agent (4h)*

4. **No Self-Healing** → Failures require human  
   *Fix: Retry logic + circuit breakers (3h)*

5. **No Intent Routing** → Must explicitly spawn agents  
   *Fix: Natural language router (4h)*

**Total to "self-driving": ~14 hours of focused work**

---

*Report generated autonomously by Opportunity Radar analysis.*  
*Next recommended review: 2026-03-23 (30 days)*
