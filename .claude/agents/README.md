# Agents

Agents are **judgment components** that analyze, decide, and delegate.

## Neuron Agents

Neuron is a factory. Its agents are factory management, not workers.

| Agent | Role | Analogy |
|-------|------|---------|
| `system-recruiter` | Creates components using factory patterns | Builder |
| `system-reviewer` | Audits components for pattern compliance | QA |

Workers (feature-dev, frontend-dev, etc.) belong in their respective modules, not here.

## How It Works

```
Module needs a component
     │
     ▼
Main agent → Recruiter creates it (following factory patterns)
     │
     ▼
Reviewer verifies quality
     │
     ▼
Component lives in the module's .claude/
```

## Agent vs Skill

| Component | Role | Example |
|-----------|------|---------|
| **Agent** | Makes judgment calls | recruiter decides naming + structure |
| **Skill** | Executes workflow | ops-init-module bootstraps .claude/ |

## Agent File Structure

```yaml
---
name: agent-name
description: One-line purpose
tools: Tool1, Tool2, ...
model: haiku | sonnet | opus
---
```
