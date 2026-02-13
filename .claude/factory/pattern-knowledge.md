# Knowledge Pattern

Reference pattern for creating knowledge documents.

## What is Knowledge?

Knowledge files are reference documents and accumulated learnings.
They live in the private vault, not in the neuron repo.

## Location

| Type | Path |
|------|------|
| Project-specific | `vault/02-Projects/{project}/` |
| Reference docs | `vault/04-Resources/` |
| Session state | `vault/memory/` |

## Structure by Category

### ref-* (Reference)

```markdown
# {Topic} Reference

Quick reference for {topic}.

## Overview

{Brief description}

## Key Information

| Item | Value |
|------|-------|
| {key} | {value} |

## Details

{Detailed information}

## Related

- [link to related doc]
```

### guide-* (Decision Guide)

```markdown
# {Topic} Guide

## {Decision Type} Decision

"{Question this guide answers}"

```
Q1. {First question}
    YES → {action}
    NO  → Q2

Q2. {Second question}
    YES → {action}
    NO  → {default action}
```

### Examples

| Case | Decision | Reason |
|------|----------|--------|
| {case} | {decision} | {reason} |

## Quick Reference

{Summary table}

## Related

- [link to related doc]
```

### protocol-* (Protocol)

```markdown
# {Name} Protocol

## Purpose

{Why this protocol exists}

## When to Apply

- {trigger condition}

## Steps

### Step 1: {Action}

{Description}

### Step 2: {Action}

{Description}

## Verification

- [ ] {checkpoint}

## Exceptions

| Situation | Override |
|-----------|----------|
| {situation} | {what to do instead} |
```

### workflow-* (Workflow Spec)

```markdown
# {Workflow Name} Specification

## Overview

{What this workflow accomplishes}

## Trigger

{When this workflow starts}

## Flow

```
{Step 1}
    ↓
{Step 2}
    ↓
{Step 3} ─── {condition} ──→ {alternate path}
    ↓
{End state}
```

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| {input} | {type} | Yes/No | {description} |

## Outputs

| Output | Description |
|--------|-------------|
| {output} | {description} |

## Error Handling

| Error | Action |
|-------|--------|
| {error} | {recovery} |
```

### learn-* (Lessons - YAML)

```yaml
# Lessons & Facts
# Updated by wrapup agent

lessons:
  - type: lesson | pattern | fact
    situation: "{when this applies}"
    insight: "{what was learned}"
    action: "{what to do}"
    why_not_automated: "{why this can't be a hook/skill}"
    modules: [{module}]
    date: "{YYYY-MM-DD}"

_meta:
  updated_at: "{date}"
  version: {n}
```

## Decision Tree

```
Project config/domain knowledge? → vault/02-Projects/{project}/
General reference doc? → vault/04-Resources/
Session state/focus? → vault/memory/
Can be automated? → Consider hook/skill instead
```

## Checklist Before Creating

- [ ] Does similar knowledge already exist in vault?
- [ ] Is the scope focused (not too broad)?
- [ ] Can this be automated instead? (consider hook/skill first)
