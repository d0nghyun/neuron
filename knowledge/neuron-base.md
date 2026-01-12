# Neuron Base Policy

## Purpose

Defines universal policies all neuron submodules inherit.
Reference file for SSOT - see source files for full definitions.

## Required Policies

These cannot be overridden.

| Policy | Source | Summary |
|--------|--------|---------|
| 3 Axioms | [ai-axioms.md](ai-axioms.md) | Curiosity, Truth, Beauty |
| SSOT | [philosophy.md](philosophy.md) | One source, no duplication |
| Verify Before Done | [philosophy.md](philosophy.md) | Prove it works |
| Conventional Commits | [git-workflow.md](git-workflow.md) | `type(scope): description` |
| Co-Authored-By | [git-workflow.md](git-workflow.md) | `Claude Opus 4.5 <noreply@anthropic.com>` |

## Configurable Policies

Can override with documented reason.

| Policy | Default | Override Example |
|--------|---------|------------------|
| Language | English only | Korean for internal docs |
| Test-First | Required | Experimental/prototype |
| AI-First docs | Required | Domain-specific formats |

## Override Protocol

1. Add `## Overrides` section in submodule CLAUDE.md
2. List policy and reason

```markdown
## Overrides
- **Language**: Korean for internal docs (client requirement)
```

## Inheritance Declaration

Submodule CLAUDE.md must include:

```markdown
## Inherits

Neuron base: [neuron-base.md](../../knowledge/neuron-base.md)
```

Path: `modules/<repo>/CLAUDE.md` → `knowledge/neuron-base.md`

## Verification

- [ ] CLAUDE.md has `## Inherits` section
- [ ] References neuron-base.md with correct path
- [ ] Overrides documented with reasons (if any)
