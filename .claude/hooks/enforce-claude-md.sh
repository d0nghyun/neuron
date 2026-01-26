#!/bin/bash
# Enforce Neuron session protocol on every user prompt
# stdout goes to Claude's context as system-reminder

cat << 'EOF'
<system-reminder>
## Neuron Session Protocol (MANDATORY)

### Session Flow
```
Request → BOOT → ORCHESTRATE → EXECUTE → WRAPUP
```

1. **BOOT**: Run `system-boot` agent FIRST. Do NOT respond until boot completes.
2. **ORCHESTRATE**: Delegate non-trivial requests to `system-orchestrator`
3. **EXECUTE**: Orchestrator delegates to workers. You do NOT call workers directly.
4. **WRAPUP**: Run `system-wrapup` before session ends.

### Layer Structure
| Layer | Agents | Role |
|-------|--------|------|
| META | boot, wrapup, self-improve, updater | Session lifecycle |
| BUSINESS | orchestrator, advisor, recruiter | Analyze, delegate, create |
| WORKER | code-reviewer, code-refactor, ... | Execute domain tasks |

### FORBIDDEN
- Calling worker agents directly (let orchestrator decide)
- Creating agents/skills yourself (use recruiter)
- Skipping boot or wrapup
- Using opus for tasks haiku can handle

### Component Creation (when missing)
1. Read `factory/README.md` → select component type
2. Read `factory/pattern-{type}.md` → get structure
3. Follow naming convention from pattern
4. Create at correct location with correct prefix

Reference: CLAUDE.md for principles, structure details, and conventions.
</system-reminder>
EOF
