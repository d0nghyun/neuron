---
name: ops-init-module
description: Activate a module's skills/agents for current session
allowed-tools: Bash, Read
user-invocable: true
---

# Module Init Skill

> Symlink module skills/agents into neuron for current session use.

## When to Activate

- User mentions working on a specific module
- Main agent identifies module context
- Need module-specific commands/skills

## Execution

Run the init script with the module path:

```bash
bash .claude/skills/ops-init-module/scripts/init.sh {module-path}
```

Replace `{module-path}` with the target module (e.g., `arkraft/arkraft-agent-pm`).

Report the output to the user.

## Guardrails

- **NEVER** delete existing symlinks from other modules
- Uses `ln -sf` to safely overwrite if exists

## Usage Examples

```
/ops-init-module arkraft/arkraft-agent-pm
/ops-init-module arkraft/arkraft-deploy
/ops-init-module schedule
```
