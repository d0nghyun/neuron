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

Add override to Configurable table in submodule CLAUDE.md with reason:

```markdown
### Configurable

| Policy | Default | This Project |
|--------|---------|--------------|
| Language | English only | Korean allowed (client requirement) |
```

## Inheritance Declaration

Submodule CLAUDE.md must include `## Inherited Policies` section with:

1. GitHub URL reference to neuron (conceptual, not physical dependency)
2. Required policies table (inlined, not file reference)
3. Configurable policies table with project-specific values

**DO NOT use relative paths** like `../../knowledge/neuron-base.md`.
Submodules must work standalone. See [repo-setup.md](repo-setup.md) for template.

## Verification

- [ ] CLAUDE.md has `## Inherited Policies` section
- [ ] Required policies inlined in table
- [ ] No parent-relative paths (works standalone)
- [ ] Configurable overrides documented with reasons
