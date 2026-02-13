#!/bin/bash
cat << 'EOF'
<system-reminder>
## Neuron — Intent First

Before responding, assess silently:
1. What does the user want? (intent)
2. How complex is it? (trivial / moderate / complex)
3. What approach fits?
   - DIRECT: conversation, small edits, questions → just do it
   - DELEGATE: focused independent work → Task tool (subagent)
   - COLLABORATE: quality-critical work → Worker produces, Reviewer checks, fix loop until clean

Context loading:
- Project work: read vault/02-Projects/{project}/ as needed
- No need to load everything upfront — pull context when needed

New components: read factory/README.md → select pattern → create
Rules: read RULES.md before creating or modifying components.

Record: after significant work, write vault/memory/YYYY-MM-DD.md via ops-daily-memo format.

Reference: CLAUDE.md for principles. ARCHITECTURE.md for system map.
</system-reminder>
EOF
