# Shared Module Pattern

Guide for creating shared skill/component libraries used across multiple projects.

## When to Use

Create a shared module when:
- Multiple projects need the same skills/knowledge
- Skills are domain-specific (not general Neuron components)
- Maintenance should be centralized

## Structure

```
modules/shared/{domain}-skills/
├── README.md                    # Usage instructions
├── {skill-name}/
│   ├── SKILL.md                 # Skill documentation
│   ├── references/              # Domain knowledge
│   │   ├── framework.md
│   │   └── mental_models/
│   └── templates/               # Code examples
```

## Example: finter-skills

Domain-specific skills for Finter platform:

```
modules/shared/finter-skills/
├── README.md
├── finter-data/
│   ├── SKILL.md
│   ├── references/
│   │   ├── framework.md
│   │   ├── preprocessing.md
│   │   └── universes/
│   └── templates/
└── finter-alpha/
    ├── SKILL.md
    └── references/
```

## Usage in Projects

### Option 1: Symlink (Development)

```bash
cd /path/to/agent-workspace/.claude/skills/
ln -s /path/to/neuron/modules/shared/finter-skills/finter-data .
```

### Option 2: Submodule (Production)

```bash
cd /path/to/agent-workspace
git submodule add <repo-url> .claude/skills/finter-skills
```

### Document in CLAUDE.md

```markdown
## Skills

- finter-data: `.claude/skills/finter-data/SKILL.md`
- finter-alpha: `.claude/skills/finter-alpha/SKILL.md`
```

## Shared vs Neuron Level

| Type | Location |
|------|----------|
| General Neuron component | `neuron/.claude/` |
| Domain-specific, multi-project | `modules/shared/{domain}-skills/` |
| Project-specific | `project/.claude/` |

## Converting to Independent Repo

When skills mature:

1. Create new repo for `{domain}-skills`
2. Move `modules/shared/{domain}-skills/` to repo
3. Add as submodule to neuron: `git submodule add <url> modules/shared/{domain}-skills`
4. Update dependent projects to use submodule

## Advantages

- **Single Source of Truth**: One place to update domain knowledge
- **Version Control**: Each project can pin to specific version
- **Portability**: Skills can be used outside Neuron
- **Collaboration**: Multiple projects contribute improvements

## Related

- `factory/README.md`: Component creation patterns
- `guide-module-checklist.md`: Module requirements
