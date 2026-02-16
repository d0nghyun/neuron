# Team Blueprint Pattern

Reference pattern for creating team blueprints. Defines how agents compose into collaborative structures.

## When to Use

- Multiple agents need to collaborate on a shared goal
- Work has phases that route between different roles
- Organization structure needs to be reusable or customizable

## Frontmatter (Required)

```yaml
---
name: {name}
description: {one-line description}
orchestrator: {agent-name}
members: [{agent-name}, ...]
quality_grade: B
quality_checked: 2026-01-01
---
```

## Structure

```markdown
# {Name} Team

{One-line purpose: what this team achieves when assembled}

## Roles

### Orchestrator: {agent-name}

{What the orchestrator does in this team context}

Responsibilities:
- Decomposes intent into phased tasks
- Routes work to appropriate members
- Collects results and decides phase transitions
- Validates output or delegates validation

### Member: {agent-name}

{What this member contributes}

- Receives: {input type from orchestrator}
- Produces: {output artifact}
- Reports to: orchestrator

## Phases

### Phase 1: {Name}
- **Actor**: {agent-name}
- **Input**: {what they receive}
- **Output**: `artifacts/{phase}/{file}` — {format}
- **Transition**: → Phase 2

### Phase N: {Name}
...

## Routing

- Handoff: file-based via `artifacts/` (loose coupling)
- Parallel: {which phases/actors can run simultaneously}
- Skip: {conditions under which phases can be omitted}
- Adapt: orchestrator may reorder phases based on intermediate results

## Constraints

- {e.g., "Phase 5 artifacts must exist before Phase 6 starts"}
- {e.g., "Registration must be sequential, not parallel"}
```

## MECE Boundary

| Concern | Lives In | NOT in Team Blueprint |
|---------|----------|-----------------------|
| Who does what (roles) | Team Blueprint | - |
| How to use tools | Skill | Team Blueprint |
| How to think/judge | Agent (mental_model) | Team Blueprint |
| When to auto-trigger | Hook | Team Blueprint |

Team Blueprint = **composition only**. It references agents and skills by name, never duplicates their content.

## Flexibility Principle

Blueprints are **guides, not rigid scripts**. The orchestrator agent has judgment to:
- Add ad-hoc phases (e.g., "baseline" before "implement")
- Skip phases when data indicates
- Reassign work between members
- Request additional members not in the original blueprint

## Where Team Composition Lives

Team blueprints are NOT a separate directory. They live in the **orchestrator agent's context**:

| Context | Location |
|---------|----------|
| Claude SDK agent | `workspace/CLAUDE.md` (system prompt) |
| Claude Code subagent | `.claude/agents/{orchestrator}.md` |
| Client variant | Override the orchestrator's CLAUDE.md per client |

The orchestrator agent IS the team definition. Its CLAUDE.md contains roles, phases, and routing.

## Examples

### Minimal Team (2 roles)

```markdown
---
name: team-{name}
description: {Worker} + {reviewer} pair
orchestrator: {lead-agent}
members: [{worker}, {reviewer}]
---

# {Name} Team

{Worker} produces, {reviewer} validates, {lead} decides.

## Roles
### Orchestrator: {lead-agent}
Routes tasks, reviews findings, approves/rejects.

### Member: {worker}
Executes assigned work per spec.

### Member: {reviewer}
Validates output for quality, correctness.

## Phases
### Phase 1: Execute → {worker}
### Phase 2: Review → {reviewer}
### Phase 3: Decide → {lead} (fix / approve / reject)
```

### Complex Team (adaptive phases)

```markdown
---
name: team-{domain}-{workflow}
description: {N}-phase {domain} workflow
orchestrator: {lead-agent}
members: [{worker-1}, {worker-2}, {worker-3}]
---

# {Domain Workflow} Team

{What this team achieves.}

## Roles
### Orchestrator: {lead-agent}
{Decomposes intent, assigns, collects, verifies.}

### Member: {worker-1}
{Contribution and output artifact.}

## Phases
### Phase 1: {Name} → {actor} → {output artifact}
### Phase 2: {Name} → {actor} (parallel) → {output}
### Phase N: {Name} → {orchestrator} → {final artifact}

## Routing
- {Which phases can run in parallel}
- {Skip conditions}
- {Loop-back conditions}
```

## Checklist Before Creating

- [ ] All member agents defined in agents/?
- [ ] All required skills defined in skills/?
- [ ] Orchestrator has judgment capability (not just routing)?
- [ ] Phases can be added/removed without breaking handoffs?
- [ ] MECE: no overlap with agent mental_model or skill how-to?
