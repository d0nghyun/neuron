# Release Workflow

## Overview

Neuron uses semantic versioning with automated review via independent subagent.

## Version Strategy

### Semantic Versioning

`v{MAJOR}.{MINOR}.{PATCH}`

| Commit Type | Version Bump |
|-------------|--------------|
| feat | MINOR |
| fix | PATCH |
| BREAKING CHANGE | MAJOR |
| docs/chore | No bump (accumulate) |

## PR + Review + Release Flow

### 1. Development Complete

Developer finishes feature/fix on working branch.

### 2. Run /pr Command

Claude Code executes:

1. Invoke **reviewer subagent** (independent context)
2. Subagent performs:
   - Code quality review
   - Impact analysis
   - Security check
   - Test coverage review
   - UNRELEASED.md update
3. Return approval status
4. Create PR with review summary

### 3. Reviewer Approval Status

| Status | Meaning | Action |
|--------|---------|--------|
| blocked | Critical issue found | Must fix before PR |
| changes-requested | Non-critical warnings | Proceed with caution |
| approve | All checks pass | Create PR |

### 4. Run /release Command

When ready to release, run `/release`. See [release.md](../.claude/commands/release.md) for execution details.

## Review Categories

| Category | Focus |
|----------|-------|
| Code Quality | Conventions, complexity, DRY |
| Impact | Breaking changes, dependencies |
| Security | Secrets, injection, validation |
| Testing | Coverage, edge cases |

## Key Files

| File | Purpose |
|------|---------|
| `.claude/agents/reviewer.md` | Subagent definition |
| `.claude/commands/pr.md` | PR workflow entry |
| `.claude/commands/release.md` | Release workflow entry |
| `docs/releasenotes/UNRELEASED.md` | Pending changes |
| `docs/releasenotes/v*.md` | Released versions |
