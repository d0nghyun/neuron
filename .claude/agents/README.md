# Agents Architecture

Agents are **judgment components** that analyze, decide, and delegate.

## Layer Model

```
┌─────────────────────────────────────────┐
│  META LAYER (Session lifecycle)         │
│  boot, wrapup, self-improve, updater    │
├─────────────────────────────────────────┤
│  BUSINESS LAYER (Delegation control)    │
│  orchestrator, advisor, recruiter       │
├─────────────────────────────────────────┤
│  WORKER LAYER (Domain execution)        │
│  code-reviewer, code-refactor, ...      │
└─────────────────────────────────────────┘
```

## Session Flow

```
Request → BOOT → ORCHESTRATOR → [Dynamic Discovery] → EXECUTE → WRAPUP
                                      │
                        ┌─────────────┴─────────────┐
                        ▼                           ▼
                   Agent exists              Agent missing
                        │                           │
                        ▼                           ▼
                 Delegate to Worker          Recruiter creates
```

### Flow Rules

1. **BOOT** runs at session start (mandatory)
2. **ORCHESTRATOR** analyzes request and discovers agents dynamically
3. **ORCHESTRATOR** delegates to worker OR recruiter
4. **WORKERS** execute domain tasks
5. **WRAPUP** runs at session end (mandatory)

## Layer Responsibilities

| Layer | Role | Agents |
|-------|------|--------|
| **META** | Session boundaries, system health | boot, wrapup, self-improve, updater |
| **BUSINESS** | Analyze, delegate, create | orchestrator, advisor, recruiter |
| **WORKER** | Execute domain tasks | code-reviewer, code-refactor, ... |

## Calling Convention

**Main agent calls META and BUSINESS only:**
```yaml
Task: { subagent_type: "system-boot", prompt: "..." }
Task: { subagent_type: "system-orchestrator", prompt: "..." }
Task: { subagent_type: "system-wrapup", prompt: "..." }
```

**ORCHESTRATOR calls WORKERS:**
```yaml
# Orchestrator decides which worker to use
Task: { subagent_type: "code-reviewer", prompt: "..." }
```

**ORCHESTRATOR calls RECRUITER when agent missing:**
```yaml
Task: { subagent_type: "system-recruiter", prompt: "Create agent for X" }
```

## FORBIDDEN

- ❌ Main agent calling workers directly (orchestrator decides)
- ❌ Creating agents without recruiter
- ❌ Skipping boot or wrapup
- ❌ Hardcoding agent selection (use dynamic discovery)

## Agent File Structure

```yaml
---
name: agent-name
layer: meta | business | worker
description: One-line purpose
tools: Tool1, Tool2, ...
model: haiku | sonnet | opus
---
```
