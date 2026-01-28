# finter-skills

Shared skills and agents for Finter platform quantitative research.

## Architecture

```
finter-skills/
├── finter-data/       # Data loading skill
├── finter-explore/    # Signal exploration skill
├── finter-alpha/      # Strategy implementation skill
└── .claude/
    ├── agents/
    │   └── quant-analyst.md              # Hypothesis validation agent
    ├── skills/
    │   └── workflow-alpha-hypothesis/    # Orchestration workflow
    └── knowledge/
        └── learn-failures.yaml           # Learning records
```

## Alpha Hypothesis Workflow

```
User Hypothesis
      │
      ▼
┌─────────────────────┐
│   quant-analyst     │  Autonomous judgment
│                     │
│   1. Question       │  Derive measurable questions
│   2. Criteria       │  Define own standards (not preset)
│   3. Measure        │  Use finter-data + finter-explore
│   4. Judge          │  YES/NO/MARGINAL with reasoning
│   5. Synthesize     │  PROCEED/MODIFY/REJECT
└─────────────────────┘
      │
      ├── PROCEED ──▶ finter-alpha (implement)
      ├── MODIFY ───▶ Loop back with changes
      └── REJECT ───▶ Report + alternatives
```

## Skills

| Skill | Purpose |
|-------|---------|
| `finter-data` | Data loading, ContentFactory, universe definitions |
| `finter-explore` | Signal analysis, IC calculation, diagnostics |
| `finter-alpha` | BaseAlpha framework, backtesting |
| `workflow-alpha-hypothesis` | Orchestrates hypothesis → judgment → decision |

## Agents

| Agent | Purpose |
|-------|---------|
| `quant-analyst` | Transforms qualitative hypotheses into quantitative judgments |

## Usage

### In agent workspace

```bash
# Symlink to workspace/.claude/
ln -s /path/to/finter-skills/finter-data workspace/.claude/skills/
ln -s /path/to/finter-skills/finter-explore workspace/.claude/skills/
ln -s /path/to/finter-skills/finter-alpha workspace/.claude/skills/
```

## Key Principles

1. **Judgment Before Implementation**: Never implement alpha without quant-analyst validation
2. **Self-Defined Criteria**: Agent defines its own thresholds with reasoning, not preset values
3. **Explicit Reasoning**: Every judgment includes why, not just pass/fail
4. **Learning Loop**: Record outcomes in `knowledge/learn-failures.yaml`

## Source

Extracted from `finter-mcp/agents/skills/` (arkraft-legacy).

## Adding New Skills

1. Create `finter-{name}/` directory
2. Add `SKILL.md` with usage instructions
3. Add `references/` for documentation
4. Add `templates/` for code examples
