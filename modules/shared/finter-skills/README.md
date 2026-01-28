# finter-skills

Shared skills for Finter platform agents.

## Skills

| Skill | Purpose |
|-------|---------|
| `finter-data` | Data loading, ContentFactory, universe definitions |
| `finter-alpha` | BaseAlpha framework, backtesting |

## Usage

### In agent workspace

```bash
# Symlink or copy to workspace/.claude/skills/
ln -s /path/to/finter-skills/finter-data workspace/.claude/skills/
```

### In CLAUDE.md

```markdown
## Skills

- finter-data: `.claude/skills/finter-data/SKILL.md`
- finter-alpha: `.claude/skills/finter-alpha/SKILL.md`
```

## Source

Extracted from `finter-mcp/agents/skills/` (arkraft-legacy).

## Adding New Skills

1. Create `finter-{name}/` directory
2. Add `SKILL.md` with usage instructions
3. Add `references/` for documentation
4. Add `templates/` for code examples
