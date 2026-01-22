---
name: neuron-knowledge
description: Reference Neuron project knowledge and policies. Use when discussing git workflow, conventions, architecture, or project philosophy. Auto-check knowledge/ folder for guidance.
allowed-tools: Read, Glob, Grep
---

# Neuron Knowledge Reference

## When to Activate

This skill activates when the user asks about:
- Git workflow, commits, branches, PRs
- Project conventions and standards
- Architecture and module organization
- Philosophy and principles
- **Personal context**: team, projects, priorities (long-term memory)

## Knowledge Locations

| Type | Location | Purpose |
|------|----------|---------|
| Philosophy/Workflow | `knowledge/` | Principles, conventions, guides |
| Personal Context | `meta/` | Team, projects, priorities |
| Module Registry | `modules/_registry.yaml` | All registered modules |

## Memory Model

```
Short-term (CLAUDE.md)  ←  Always loaded, compact summary
         ↓
Long-term (meta/)       ←  This skill fetches details on demand
```

## How to Use

1. **Discover**: Check `knowledge/` or `meta/` based on query type
2. **Read**: Load relevant documentation
3. **Reference**: Quote specific sections in responses

## Examples

**Philosophy query:**
> "How should I name my branches?"
1. Read `knowledge/git-workflow.md`
2. Find the Branch Strategy section

**Personal context query:**
> "What projects am I working on?"
1. Read `meta/focus.yaml`
2. Return current focus and active modules

**Team query:**
> "Who's on my team?"
1. Read `meta/team.yaml`
2. Return team structure
