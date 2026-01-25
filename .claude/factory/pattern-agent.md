# Agent Pattern

Reference pattern for creating agents. Combines task-oriented and role-based approaches.

## Frontmatter (Required)

```yaml
---
name: {name}
description: {one-line description}
tools: {comma-separated tool list}
model: haiku | sonnet | opus
---
```

## Structure

```markdown
# {Name} Agent

{One-line purpose statement}

## Purpose

{2-3 sentences explaining what this agent does and when to use it}

## Input Specification

```yaml
input:
  required:
    - name: "{param}"
      type: "{type}"
      description: "{description}"
  optional:
    - name: "{param}"
      type: "{type}"
      default: "{default}"
```

## Execution Steps

### Step 1: {Action Name}

{Description of what to do}

### Step 2: {Action Name}

{Description of what to do}

### Step N: Generate Output

Output format:

```yaml
{name}_result:
  status: success | failed
  {output_fields}
  metadata:
    timestamp: {ISO 8601}
```

## Success Criteria

| Criterion | Validation |
|-----------|------------|
| {criterion} | {how to verify} |

## Guardrails

- **NEVER** {prohibited action}
- **ALWAYS** {required action}
```

## Examples

### Task-Oriented Agent (specific operation)

```markdown
---
name: build-validator
description: Validates build output before deployment
tools: Bash, Read, Glob
model: haiku
---

# Build Validator Agent

Validates build artifacts meet deployment requirements.

## Execution Steps

### Step 1: Check Build Exists

```bash
ls -la dist/
```

### Step 2: Validate Bundle Size

```bash
du -sh dist/
# Must be < 5MB
```

### Step 3: Return Result

```yaml
build_validator_result:
  status: success
  bundle_size: "2.3MB"
  files_count: 15
```
```

### Role-Oriented Agent (ongoing responsibility)

```markdown
---
name: advisor
description: Knowledge-based recommendations with rationale
tools: Read, Glob, Grep
model: sonnet
---

# Advisor Agent

Provides recommendations before user decisions.

## When to Invoke

- Before architectural decisions
- When multiple valid approaches exist
- User asks "should I...?" questions

## Execution Steps

### Step 1: Gather Context

Read relevant files and understand current state.

### Step 2: Analyze Options

List pros/cons of each approach.

### Step 3: Recommend

```yaml
advisor_recommendation:
  recommended: "{option}"
  rationale: "{why}"
  alternatives:
    - option: "{alt1}"
      tradeoff: "{consideration}"
```
```

## Checklist Before Creating

- [ ] Does this agent already exist? (check agents/)
- [ ] Is this judgment-based? (if not, consider Skill)
- [ ] Is the scope well-defined?
- [ ] Are success criteria measurable?
