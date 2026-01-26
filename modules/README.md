# Modules

Submodules registered under neuron. Named after brain parts.

## Naming Convention

| Name | Brain Part | Purpose |
|------|-----------|---------|
| `hippo` | Hippocampus | Memory, long-term storage (docs, resume) |
| `cortex` | Cortex | Processing, analysis |
| `synapse` | Synapse | External connections, APIs |

## Current Modules

| Module | Domain | Status | Description |
|--------|--------|--------|-------------|
| [hippo](https://github.com/d0nghyun/hippo) | tools | active | Memory and context management system |
| [pm-arkraft](https://gitlab.quantit.io/ark/arkraft/pm-arkraft) | work | active | Project management for arkraft |
| [modeling](https://github.com/Quantit-Github/modeling) | work | active | Finter quantitative trading skills |
| [arkraft](https://github.com/Quantit-Github/arkraft) | work | active | AI-Powered Quant Research Platform |
| [finter](https://gitlab.quantit.io/ark/finter) | work | active | Finter backend service |
| [arkraft-fe](https://gitlab.quantit.io/ark/arkraft/arkraft-fe) | work | legacy | Arkraft frontend (legacy) |

See `_registry.yaml` for full metadata.

## Shared

`shared/` is not a module. It stores domain-specific agent resources that can be referenced across modules.

| Directory | Purpose |
|-----------|---------|
| `finter-skills/` | Finter platform skills (data loading, alpha framework) |

**Usage**: Symlink to module's `.claude/skills/` or reference directly.

**What goes here**:
- Domain-specific skills (not neuron system skills)
- E2E testing guides for specific platforms
- Agent setup instructions for external services

**What doesn't go here**:
- Neuron system knowledge → `.claude/knowledge/`
- Session state → `.claude/contexts/`

## Task Management

Each module manages its own tasks via `TODO.md` in its repo (like release notes pattern).
