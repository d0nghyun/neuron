# Decision Guide

## Project Scope Decision

"Where should this feature live?"

```
Q1. Is it used across multiple projects?
    YES → Add to neuron itself
    NO  → Q2

Q2. Is it an independent domain? (resume, blog, finance, etc.)
    YES → New repo → Register as submodule
    NO  → Add to neuron/scripts/ or existing module
```

### Examples

| Feature | Decision | Reason |
|---------|----------|--------|
| Git workflow policy | neuron | Cross-project convention |
| Resume manager | New repo | Independent domain |
| Utility script (one-off) | neuron/scripts/ | Too small for repo |
| Blog system | New repo | Independent domain |

## MCP Placement Decision

"Where should this MCP be registered?"

```
Q1. Is it used by multiple projects?
    YES → neuron (shared)
    NO  → Project-specific

Q2. Is it a general-purpose service?
    YES → neuron (shared)
    NO  → Project-specific
```

### Examples

| MCP | Placement | Reason |
|-----|-----------|--------|
| GitHub API | neuron | All projects use git |
| Notion API | neuron | Multiple projects may use docs |
| Project-specific DB | Project | Only that project uses it |
| Slack API | neuron | Cross-project notifications |

## Quick Reference

| Question | neuron | New Submodule | Project-specific |
|----------|--------|---------------|------------------|
| Cross-project? | Yes | - | No |
| Independent domain? | - | Yes | - |
| General-purpose MCP? | Yes | - | No |
| One-off script? | scripts/ | - | - |
