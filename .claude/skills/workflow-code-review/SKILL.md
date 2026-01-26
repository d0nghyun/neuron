---
name: workflow-code-review
description: Reviews code changes for quality, impact, security, and test coverage. Updates release notes and retrospectives.
allowed-tools: Read, Glob, Grep, Bash, Edit
user-invocable: true
---

# Code Review Workflow

> Comprehensive code review with release notes and retrospective updates.

## When to Activate

- User requests code review
- Before creating a PR
- User asks to check code quality

## Prerequisites

- Git repository with uncommitted or staged changes
- `docs/releasenotes/UNRELEASED.md` exists
- `CLAUDE.md` exists for project context

## Workflow Steps

### Step 1: Load Project Context

Read CLAUDE.md to understand project philosophy and conventions.

### Step 2: Gather Changes

```bash
git diff --stat
git diff --name-only
git log -1 --format="%s"
```

### Step 3: Philosophy Compliance

Verify each Principle (P#1-7) from CLAUDE.md is followed in the changes.

### Step 4: Task Verification Check

Verify task-verification-workflow was followed:

| Check | Pass Criteria |
|-------|---------------|
| Criteria defined? | Verification criteria existed at task start |
| Criteria executable? | Each criterion has concrete "how to verify" |
| Verification run? | Evidence of each criterion being tested |
| All passed? | All criteria show PASS status |

### Step 5: Policy Compliance

| Policy | Check |
|--------|-------|
| Commit format | Conventional commits (type(scope): description)? |
| Branch naming | feature/, fix/, docs/, chore/ prefix? |
| File size | Under 200 lines? |
| Language | English content? |

### Step 6: Review Categories

**Code Quality**: Naming conventions, functions under 50 lines, no duplication, proper error handling.

**Impact Analysis**: Affected modules, breaking changes, API compatibility.

**Security**: No hardcoded secrets, input validation, no injection risks.

**Test Coverage**: New features have tests, edge cases considered.

### Step 7: Update Release Notes

Read `docs/releasenotes/UNRELEASED.md` and append changes following `knowledge/ref-release-notes-format.md`.

### Step 8: Detect Improvements

| Signal | Indicates |
|--------|-----------|
| Same issue in 3+ reviews | Policy needs clarification |
| Missing guideline caused issue | Knowledge gap |
| Same code pattern 2+ times | Automation candidate |

### Step 9: Update Retrospective

Update `docs/retrospectives/UNRETROSPECTIVE.md` with patterns and insights.

## Output

```yaml
workflow_result:
  status: approve | changes-requested | blocked
  summary: "<1-2 sentence summary>"
  findings:
    - severity: "<info|warning|error>"
      location: "<file:line>"
      message: "<description>"
  version_recommendation:
    type: patch | minor | major
    reason: "<why>"
  release_notes_updated: true | false
  improvement_detected: true | false
```

## Guardrails

- **NEVER** approve code without reading CLAUDE.md first
- **ALWAYS** check all review categories
- **ALWAYS** update release notes before approving
- **NEVER** skip task verification check
