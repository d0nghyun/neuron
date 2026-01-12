# Neuron - AI Entry Point

## Critical Rules

### Advisor-before-AskUser

**NEVER ask user questions without checking Advisor first.**

```
Ambiguous situation → Task(subagent_type="advisor") → high/medium? → Proceed
                                                    → low? → Ask user
```

## Routing

| Situation | Route |
|-----------|-------|
| Need principles/philosophy/judgment | `Task(subagent_type="advisor")` |
| Code review needed | `Task(subagent_type="reviewer")` |
| Refactoring decision | `Task(subagent_type="refactor")` |
| GitHub API | `Skill(github-api)` |
| Jira API | `Skill(jira-api)` |
| Notion API | `Skill(notion-api)` |
| Confluence API | `Skill(confluence-api)` |
| Create PR | `/pr` |
| Create release | `/release` |
| Sync main branch | `/sync` |
| Extract backlog | `/backlog` |

## Core Philosophy

**Axioms**: Curiosity, Truth, Beauty — all decisions trace back to these.

**Key Principles**:
- **SSOT**: One source, no duplication
- **MECE**: Clear boundaries, complete coverage
- **Simplicity First**: Simple > complex, avoid over-engineering
- **Incremental**: Build only what's needed now
- **Autonomous Execution**: Act first, ask only when blocked
- **Front-load Pain**: Analyze before coding
- **Verify Before Done**: Prove it works, don't assume

Full details: `Task(subagent_type="advisor")` or read `knowledge/philosophy.md`

## Decision Signal Recognition

**Before executing location decisions, check architecture first:**
- New functionality? -> Separate repo -> Submodule (see "Working with This Repository")
- Location within neuron? -> Then execute location decision

**Execute immediately when user states:**
- Location: "put in docs", "store in X", "use Y folder" (after architecture check)
- Tool: "use Notion", "with GitHub", "via MCP"
- Approach: "I'll do X", "going to Y", "decided to Z"

**Confirm only when:**
- Multiple valid approaches exist AND user hasn't chosen
- Destructive action without explicit intent
- Ambiguous scope (what vs where vs how unclear)

**Default**: Trust user's stated decision. Act, don't ask.

## Conventions

- **Language**: English for all neuron files (submodules may differ)
- **File size**: Max 200 lines
- **Commits**: Conventional commits, `Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>`
- **Auto-commit**: Commit when logical unit complete
- **Auto-PR**: Run `/pr` on completion

## New Functionality

1. Check if it fits existing modules
2. If new module needed → create separate repo → register as submodule under `modules/`
