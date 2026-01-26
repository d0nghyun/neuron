# Guide: Agent vs Skill Decision

Quick reference for deciding between agent and skill components.

## Decision Criteria

| Question | Agent | Skill |
|----------|-------|-------|
| Does it make judgment calls? | ✅ Yes | ❌ No |
| Does it decide WHEN/HOW to act? | ✅ Yes | ❌ No |
| Does it compose other components? | ✅ Yes | ❌ No |
| Is it a deterministic workflow? | ❌ No | ✅ Yes |
| Does it call external APIs? | ❌ No | ✅ Yes |
| Can it be reused by multiple agents? | ❌ No | ✅ Yes |

## Examples

### Correct: Skill

```yaml
workflow-code-review: Review code changes (deterministic steps)
workflow-code-refactor: Apply refactoring patterns (deterministic)
workflow-code-test: Run test suite (deterministic)
api-google-calendar: Google Calendar API wrapper
```

### Correct: Agent

```yaml
feature-dev: Decides when to refactor/test/review (judgment)
frontend-dev: Decides when to apply design patterns (judgment)
code-reviewer: Reviews code AND decides if changes needed (judgment)
```

### Anti-Pattern Examples

❌ `code-review` as agent that only runs review steps
  → Should be `workflow-code-review` skill

❌ `code-refactor` as agent that only applies patterns
  → Should be `workflow-code-refactor` skill

❌ `google-calendar` as agent that only wraps API
  → Should be `api-google-calendar` skill

## Composition Pattern

Agents compose skills via frontmatter:

```yaml
---
name: feature-dev
layer: worker
skills:
  - workflow-code-refactor
  - workflow-code-test
  - workflow-code-review
---
```

Agent decides **when** to invoke each skill based on context.

## Migration Path

If you find an agent that should be a skill:

1. Create new skill in `skills/{type}-{name}/SKILL.md`
2. Create agent that composes the skill (if needed)
3. Update references to use new skill
4. Remove old agent file
5. Update documentation

## Red Flags

| Signal | Problem | Solution |
|--------|---------|----------|
| Agent has no branching logic | Not making decisions | Convert to skill |
| Agent just calls APIs | No judgment | Convert to api-* skill |
| Agent follows fixed steps | Deterministic | Convert to workflow-* skill |
| Multiple agents duplicate same workflow | Should be shared | Extract to skill |

## Reference

- `agents/README.md` - Full agent architecture
- `factory/README.md` - Component selection guide
- `factory/pattern-agent.md` - Agent template
- `factory/pattern-skill.md` - Skill template
