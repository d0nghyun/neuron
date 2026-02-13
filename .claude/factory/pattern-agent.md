# Agent Pattern

Reference pattern for creating agents. Combines task-oriented and role-based approaches.

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
- **NEVER** copy principles from CLAUDE.md into agent content
- **ALWAYS** reference "see CLAUDE.md" when mentioning principles
```

## Examples

### Task-Oriented Agent (specific operation)

```markdown
---
name: build-validator
description: Validates build output before deployment
tools: Bash, Read, Glob
model: haiku
permissionMode: bypassPermissions
quality_grade: A
quality_checked: 2026-02-13
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

### Role-Oriented Agent (with skill preloading)

```markdown
---
name: api-developer
description: Implement API endpoints following team conventions
tools: Read, Write, Edit, Bash
skills:
  - api-github
model: sonnet
permissionMode: bypassPermissions
quality_grade: B
quality_checked: 2026-02-13
---

# API Developer Agent

Implements API endpoints using preloaded skill knowledge.

## Execution Steps

### Step 1: Apply Skill Knowledge
Use preloaded api-github skill for authentication, rate limits, etc.

### Step 2: Implement Endpoint
Follow patterns from preloaded skill.

### Step 3: Return Result
```yaml
api_developer_result:
  status: success
  endpoint: "{created endpoint}"
```
```

## Reference Pattern (SSOT Enforcement)

Agents MUST reference external sources, never hardcode duplicated content.

| Content Type | Reference To |
|--------------|--------------|
| Principles | `CLAUDE.md` |
| Naming rules | `factory/README.md` |
| Quality grades | `factory/README.md` § Quality Grades |
| Domain knowledge | `vault/` or `skills/` |

```markdown
✗ Bad (hardcoded):
| Model | When |
| haiku | simple tasks |

✓ Good (reference):
**See**: `CLAUDE.md` for principles.
```

## Checklist Before Creating

- [ ] Does this agent already exist? (check agents/)
- [ ] Is this judgment-based? (if not, consider Skill)
- [ ] Is the scope well-defined?
- [ ] Are success criteria measurable?
- [ ] Does agent reference instead of copying? (SSOT)
