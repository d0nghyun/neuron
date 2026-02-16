# Agent Pattern

Reference pattern for creating agents. Two types: task-oriented (do X) and role-oriented (be X).

## Frontmatter (Required)

```yaml
---
name: {name}
description: {one-line description}
tools: {comma-separated tool list}
skills:                              # Optional: preload skill content into agent context
  - {skill-name}
model: haiku | sonnet | opus
permissionMode: bypassPermissions    # Auto-approve all tool permissions
quality_grade: B                     # A/B/C/D — set by ops-factory-sync
quality_checked: 2026-01-01          # Last audit date
---
```

### Skills Preloading

When an agent needs domain knowledge from skills, list them in the `skills` field.
The skill content is injected into the agent's context at startup.

**When to preload skills:**
- Agent repeatedly uses same skill → preload it
- Agent needs domain-specific knowledge → preload relevant skill
- Agent calls external APIs → preload the api-* skill

**When NOT to preload:**
- Generic agents → don't need specific domain knowledge

## Structure

```markdown
# {Name} Agent

{One-line purpose statement}

## Purpose

{2-3 sentences explaining what this agent does and when to use it}

## Mental Model (Required for role-oriented agents)

Identity and judgment framework. This is what makes an agent more than a script.

- **Identity**: Who am I? What is my raison d'etre?
- **Principles**: What do I believe about my domain?
- **Judgment**: How do I decide? What thresholds do I use?

Example:
> I am a {role}. I believe {core principle}.
> If {primary condition} is met, I proceed.
> {Guiding philosophy for edge-case decisions}.

## Input Specification

```yaml
input:
  required:
    - name: "{param}"
      type: "{type}"
      description: "{description}"
```

## Execution Steps

### Step 1: {Action Name}
{Description of what to do}

### Step N: Generate Output
```yaml
{name}_result:
  status: success | failed
  {output_fields}
```

## Guardrails

- **NEVER** {prohibited action}
- **ALWAYS** {required action}
- **NEVER** copy principles from CLAUDE.md into agent content
- **ALWAYS** reference "see CLAUDE.md" when mentioning principles
```

## MECE Boundary

| Concern | Lives In | NOT in Agent |
|---------|----------|--------------|
| How to use tools | Skill | Agent |
| How to think/judge | Agent (mental_model) | - |
| Team composition | Orchestrator CLAUDE.md | Agent |

Agent = **identity + judgment**. It references skills by name, never duplicates tool how-to.

## Examples

### Task-Oriented Agent (no mental model needed)

```markdown
---
name: {task-name}
description: {Specific operation to perform}
tools: Bash, Read, Glob
model: haiku
permissionMode: bypassPermissions
---

# {Task Name} Agent

{What this task validates/produces.}

## Execution Steps
### Step 1: {Check preconditions}
### Step 2: {Execute core operation}
### Step 3: {Return result with status}
```

### Role-Oriented Agent (with mental model + skills)

```markdown
---
name: {role-name}
description: {domain role}
tools: Read, Write, Edit, Bash
skills:
  - {domain-skill}
model: opus
---

# {Role Name} Agent

{Purpose in domain context.}

## Mental Model

- **Identity**: {Who am I? Raison d'etre}
- **Principles**: {Domain beliefs that guide decisions}
- **Judgment**: {Thresholds for proceed/stop/escalate}

## Execution Steps
### Step 1: {Read inputs}
### Step 2: {Execute using preloaded skills}
### Step 3: {Produce output artifacts}
```
```

## SSOT Enforcement

Agents reference, never hardcode. Tool how-to lives in Skills, not in Agent.

| Content | Source |
|---------|--------|
| Principles | `CLAUDE.md` |
| Tool usage | `skills/{name}` (preloaded) |
| Team structure | Orchestrator's CLAUDE.md |
| Domain knowledge | `vault/` |

## Checklist

- [ ] Agent already exists? (check agents/)
- [ ] Judgment-based? (if not → Skill)
- [ ] Role-oriented? → mental_model section required
- [ ] Skills referenced by name, not duplicated?
- [ ] No team composition logic? (that belongs in Team Blueprint)
