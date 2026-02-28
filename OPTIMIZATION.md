# OPTIMIZATION.md - Token Economy

**Goal:** Minimize token usage across all agents without sacrificing quality.

## Hard Rules

### 1. Call Caps (MAX 50 calls/run)
- **Top-level agents:** Max 50 function calls per execution
- **Sub-agents:** Max 40 calls per task
- **Loop detection:** Abort if same error signature 3x in a row
- **Retry limit:** Max 2 retries per failed step

### 2. Output Caps
- **Micro-steps:** 300–500 output tokens max
- **Final summary:** 1,500–2,500 output tokens max
- **Reflections:** Only at the end, or every 5–10 steps (NOT after each step)

### 3. Context Management
- **DOM/HTML:** Never feed raw HTML; always extract markdown/text
- **Tool outputs:** Truncate to essentials (strip logs, timestamps, metadata)
- **Memory files:** Keep MEMORY.md <15KB; archive daily logs >30 days old
- **Logs:** Summarize; don't transcript

### 4. Loop Detection
Abort and summarize if:
- Same URL fails 3x (JS load timeout, 404, etc)
- Same selector fails 3x (web scraping)
- Same API error 3x (rate limit, auth, etc)
- Same data format error 3x

**Action:** Stop → Document failure → Request human input

### 5. Reflection Strategy
- **Kill:** Self-critique after every step
- **Keep:** Reflection every 5–10 steps, or end-of-run only
- **Cap:** Max 200 tokens per reflection block

## Implementation Checklist

- [x] Call caps documented here
- [x] Output caps specified
- [ ] Loop detector added to agents (in-progress)
- [ ] Memory archival automated (in-progress)
- [ ] All agents updated with caps (pending)

## Memory Archival Schedule

- **Frequency:** Weekly (every Thursday)
- **Archive:** Files >30 days old → `memory/archive/YYYY-MM-DD.md`
- **Keep live:** Last 30 days in `memory/`
- **Result:** MEMORY.md stays lean, history preserved

## Per-Agent Caps

| Agent | Call Cap | Output Cap | Reflection |
|-------|----------|-----------|------------|
| health-agent | 40 | 1,500 | Every 5 steps |
| fpl-agent | 30 | 800 | End only |
| bundesliga-agent | 30 | 800 | End only |
| career-agent | 50 | 2,000 | Every 5 steps |
| main | 50 | 1,500 | Every 10 steps |

---

**Updated:** 2026-02-18 16:35 CET
