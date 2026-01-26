# Orchestrator Pattern

Reference pattern for creating orchestrator agents that delegate rather than execute.

## When to Use

- Agent needs to coordinate multiple sub-agents
- Task requires breaking down into smaller pieces
- Different parts need different models (cost optimization)
- Complex workflows with dependencies

## Frontmatter

```yaml
---
name: {name}-orchestrator
description: Orchestrates {domain} by delegating to specialized agents
tools: Task, Read, Glob, Grep
model: opus
permissionMode: bypassPermissions
delegates_to:
  - agent: {agent-name}
    when: "{condition}"
    model: haiku | sonnet | opus
  - agent: {agent-name}
    when: "{condition}"
    model: haiku | sonnet | opus
---
```

## Structure

```markdown
# {Name} Orchestrator

{One-line purpose: what this orchestrator coordinates}

## Routing Table

| Request Pattern | Delegate To | Model | Reason |
|-----------------|-------------|-------|--------|
| "{pattern}" | {agent} | {model} | {why} |

## Delegation Flow

### Step 1: Analyze

Classify incoming request by scope, risk, domain.

### Step 2: Route

Select agent and model based on routing table.

### Step 3: Delegate

Use Task tool:
- subagent_type: {agent}
- model: {model}
- prompt: {specific task}

### Step 4: Aggregate

Collect results, handle errors, report.

## Parallel vs Sequential

| Situation | Approach |
|-----------|----------|
| Tasks are independent | Parallel (multiple Task calls) |
| Task B needs Task A result | Sequential |
| Uncertain dependency | Sequential (safer) |
```

## Model Selection Matrix

```
| Scope / Risk | read   | write  | deploy | system |
|--------------|--------|--------|--------|--------|
| micro        | haiku  | haiku  | sonnet | sonnet |
| file         | haiku  | sonnet | sonnet | opus   |
| module       | sonnet | sonnet | opus   | opus   |
| system       | sonnet | opus   | opus   | opus   |
```

## Example: Feature Development Orchestrator

```markdown
---
name: feature-orchestrator
description: Orchestrates feature development from design to PR
tools: Task, Read, Glob
model: opus
permissionMode: bypassPermissions
delegates_to:
  - agent: code-refactor
    when: "needs code changes"
    model: sonnet
  - agent: code-reviewer
    when: "code ready for review"
    model: sonnet
  - agent: general-purpose
    when: "needs PR creation"
    model: haiku
---

# Feature Orchestrator

Coordinates end-to-end feature development.

## Routing Table

| Phase | Delegate To | Model |
|-------|-------------|-------|
| Design analysis | system-advisor | haiku |
| Implementation | code-refactor | sonnet |
| Review | code-reviewer | sonnet |
| PR creation | general-purpose + workflow-pr | haiku |

## Flow

1. Analyze feature request
2. Delegate design review (parallel: advisor)
3. Delegate implementation (sequential: refactor)
4. Delegate code review (sequential: reviewer)
5. Delegate PR creation (sequential: workflow)
6. Report complete feature status
```

## Checklist

- [ ] Does this need orchestration? (if single agent suffices, don't orchestrate)
- [ ] Are delegated agents well-defined?
- [ ] Is model selection cost-efficient?
- [ ] Are dependencies correctly identified?
- [ ] Is error handling specified?
