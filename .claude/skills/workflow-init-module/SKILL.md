---
name: workflow-init-module
description: Activate a module's skills/agents for current session
allowed-tools: Bash, Read
user-invocable: true
---

# Module Init Skill

> Symlink module skills/agents into neuron for current session use.

## When to Activate

- User mentions working on a specific module
- Boot agent identifies module context
- Need module-specific commands/skills

## Prerequisites

- Module exists at `modules/{module-path}/.claude/`
- Module has commands, skills, or agents defined

## Workflow Steps

### Step 1: Validate Module

```bash
MODULE="{module-path}"  # e.g., arkraft/arkraft-agent-pm
MODULE_CLAUDE="modules/$MODULE/.claude"

[ -d "$MODULE_CLAUDE" ] || { echo "Module not found: $MODULE"; exit 1; }
```

### Step 2: Create Symlinks

```bash
PREFIX="${MODULE//\//_}"  # arkraft/arkraft-agent-pm → arkraft_arkraft-agent-pm

# Commands → Skills
if [ -d "$MODULE_CLAUDE/commands" ]; then
  for cmd in "$MODULE_CLAUDE/commands"/*.md; do
    [ -f "$cmd" ] || continue
    cmd_name=$(basename "$cmd" .md)
    target=".claude/skills/${PREFIX}--${cmd_name}"
    mkdir -p "$target"
    ln -sf "$(pwd)/$cmd" "$target/SKILL.md"
    echo "Linked: /${PREFIX}--${cmd_name}"
  done
fi

# Skills
if [ -d "$MODULE_CLAUDE/skills" ]; then
  for skill in "$MODULE_CLAUDE/skills"/*; do
    [ -d "$skill" ] || continue
    skill_name=$(basename "$skill")
    ln -sf "$(pwd)/$skill" ".claude/skills/${PREFIX}--${skill_name}"
    echo "Linked: /${PREFIX}--${skill_name}"
  done
fi

# Agents
if [ -d "$MODULE_CLAUDE/agents" ]; then
  for agent in "$MODULE_CLAUDE/agents"/*.md; do
    [ -f "$agent" ] || continue
    agent_name=$(basename "$agent" .md)
    ln -sf "$(pwd)/$agent" ".claude/agents/${PREFIX}--${agent_name}.md"
    echo "Linked agent: ${PREFIX}--${agent_name}"
  done
fi
```

### Step 3: Complete

Report linked skills/agents to user.

## Output

```yaml
init_result:
  status: success
  module: {module-path}
  skills_linked: [{list}]
  agents_linked: [{list}]
```

## Guardrails

- **NEVER** delete existing symlinks from other modules
- **ALWAYS** use `ln -sf` to safely overwrite if exists

## Usage Examples

```
/init-module arkraft/arkraft-agent-pm
/init-module arkraft/arkraft-deploy
/init-module modeling/alpha
```
