# Handoff: Neuron v2 Redesign

## State
| Field | Value |
|-------|-------|
| **Status** | in-progress |
| **Updated** | 2026-01-25 |
| **Branch** | claude/neuron-agent-skills-redesign-fgh1M |
| **Session Outcome** | Phase 1-6 Complete, Additional Cleanup Identified |

---

## Executive Summary

**Core Insight**: Neuron = Component Factory, Claude Code = Framework

```
Claude Code provides:     Neuron provides:
├─ .claude/agents/       ├─ Factory templates
├─ .claude/skills/       ├─ Component resolver
├─ .claude/contexts/     ├─ Registry tracking
├─ ~/.claude/tasks/      ├─ Philosophy injection
├─ Task tool (parallel)  └─ Self-evolution logic
├─ CLAUDE_CODE_TASK_LIST_ID
└─ Agent resume (agentId)
```

**Self-Evolution Pattern**: Factory → Tasks → Next Session

---

## Progress Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Factory Structure + Templates | ✅ COMPLETE |
| 2 | Enhanced boot.md (Resolver, Factory Trigger) | ✅ COMPLETE |
| 3 | Registry Tracking | ✅ COMPLETE |
| 4 | Enhanced wrapup.md (Registry Update) | ✅ COMPLETE |
| 5 | E2E Test (arkraft) | ✅ COMPLETE |
| 6 | Commands → Skills Migration | ✅ COMPLETE |
| 7 | Skill Cleanup (redundant skills) | ⏳ NEXT |
| 8 | Folder Restructure | ⏳ PENDING |
| 9 | CLAUDE.md v2 Rewrite | ⏳ PENDING |

---

## Completed Implementation (Phase 1-6)

### Factory Structure
```
.claude/factory/
├─ templates/
│  ├─ agent-role.md           ✅
│  ├─ agent-task.md           ✅
│  ├─ skill-api.md            ✅
│  ├─ context-project.yaml    ✅
│  └─ pipeline-parallel.yaml  ✅
└─ registry.yaml              ✅
```

### Commands Migration Complete
| Command | Result |
|---------|--------|
| `handoff.md` | ❌ DELETED |
| `backlog.md` | ❌ DELETED |
| `sync.md` | ❌ DELETED |
| `pr.md` | ✅ → `.claude/skills/pr/SKILL.md` |
| `release.md` | ✅ → `.claude/skills/release/SKILL.md` |
| `audit-modules.md` | ✅ → `.claude/skills/audit-modules/SKILL.md` |

---

## Phase 7: Skill Cleanup (NEXT)

### Analysis Result

| Skill | Type | Action | Reason |
|-------|------|--------|--------|
| `api-jira/` | API | ✅ KEEP | 올바른 명명 |
| `api-confluence/` | API | ✅ KEEP | 올바른 명명 |
| `api-notion/` | API | ✅ KEEP | 올바른 명명 |
| `api-slack/` | API | ✅ KEEP | 올바른 명명 |
| `api-github/` | API | ✅ KEEP | 올바른 명명 |
| `api-google-calendar/` | API | ✅ KEEP | 올바른 명명 |
| `meta/` | Internal | ❌ DELETE | wrapup.md에서 처리 |
| `neuron-knowledge/` | Internal | ❌ DELETE | boot.md에서 처리 |
| `ui-ux-pro-max/` | Capability | ⚠️ RENAME | → `capability-ui-design/` |

### Execution
```bash
rm -rf .claude/skills/meta/
rm -rf .claude/skills/neuron-knowledge/
mv .claude/skills/ui-ux-pro-max/ .claude/skills/capability-ui-design/
# Update registry.yaml
```

---

## Phase 8: Folder Restructure

### Current Problems

| Folder | Issue |
|--------|-------|
| `handoff/` | Claude Code Tasks로 대체 가능 |
| `meta/` | CLAUDE.md가 참조하는 파일 3개 중 1개만 존재 |
| `knowledge/` | CLAUDE.md와 내용 중복 (SSOT 위반) |

### meta/ Analysis
| File | CLAUDE.md 언급 | 실제 존재 |
|------|---------------|----------|
| `identity.yaml` | ✅ | ❌ |
| `focus.yaml` | ✅ | ❌ |
| `team.yaml` | ✅ | ❌ |
| `lessons.yaml` | ✅ | ✅ |

### knowledge/ Analysis
| Path | Issue |
|------|-------|
| `01-core/ai-axioms.md` | CLAUDE.md와 중복 |
| `01-core/philosophy.md` | CLAUDE.md와 중복 |
| `03-architecture/extension-mechanisms.md` | 구버전 (Commands 언급) |

### Target Structure
```
neuron/
├─ CLAUDE.md                    # SSOT
├─ .claude/
│  ├─ agents/
│  ├─ skills/
│  │  ├─ api-*/                 # External APIs
│  │  ├─ capability-ui-design/  # renamed
│  │  ├─ pr/                    # migrated
│  │  ├─ release/               # migrated
│  │  └─ audit-modules/         # migrated
│  ├─ contexts/
│  ├─ factory/
│  ├─ memory/                   # NEW: from meta/
│  │  └─ lessons.yaml
│  └─ knowledge/                # NEW: from knowledge/
│     └─ *.md (non-duplicate only)
└─ modules/
```

### Deletions
| Target | Reason |
|--------|--------|
| `handoff/` | Claude Code Tasks 대체 |
| `meta/` | `.claude/memory/`로 이동 |
| `knowledge/` | `.claude/knowledge/`로 이동 (중복 제거) |

### Migration Commands
```bash
# meta → .claude/memory
mkdir -p .claude/memory
mv meta/lessons.yaml .claude/memory/
rm -rf meta/

# knowledge → .claude/knowledge (non-duplicate only)
mkdir -p .claude/knowledge
mv knowledge/02-workflow/*.md .claude/knowledge/
mv knowledge/03-architecture/decision-guide.md .claude/knowledge/
mv knowledge/03-architecture/module-protocol.md .claude/knowledge/
mv knowledge/04-operations/*.md .claude/knowledge/
rm -rf knowledge/

# handoff → DELETE (Tasks replaces)
rm -rf handoff/
```

---

## Phase 9: CLAUDE.md v2 Rewrite

### Current Issues
- Commands 섹션 존재 (deprecated → skills로 변경 필요)
- Component Factory 개념 없음
- Registry 시스템 설명 없음
- Skill 카테고리 (api-*/capability-*) 설명 없음
- 참조하는 meta/ 파일들 존재하지 않음

### New Structure Outline
```markdown
# Neuron v2 - Component Factory

## Critical Rules (간소화)
## Core Philosophy (3 Axioms, 20 Principles 유지)
## Component System (NEW)
  - Agents: Judgment
  - Skills: api-* | capability-*
  - Factory: Templates + Registry
## Session Lifecycle (boot/wrapup)
## Routing (Commands → Skills 변경)
## Conventions
```

---

## Decision Guide

### Agent vs Skill vs Hook
| Need | Choose | Example |
|------|--------|---------|
| Judgment/reasoning | **Agent** | Code review, architecture |
| External API | **Skill (api-*)** | Jira, GitHub |
| Reusable workflow | **Skill (capability-*)** | UI design, release |
| Automated trigger | **Hook** | Pre-commit |

### Naming Convention
```
Agents: .claude/agents/{name}.md
Skills: .claude/skills/{type}-{name}/SKILL.md
  - api-*        → External service wrappers
  - capability-* → Reusable workflows
  - (no prefix)  → Migrated from commands (pr, release, audit-modules)
```

---

## Next Session Checklist

```
PHASE 7: SKILL CLEANUP
[ ] Delete .claude/skills/meta/
[ ] Delete .claude/skills/neuron-knowledge/
[ ] Rename ui-ux-pro-max → capability-ui-design
[ ] Update registry.yaml (remove deleted, update renamed)

PHASE 8: FOLDER RESTRUCTURE
[ ] Create .claude/memory/
[ ] Move meta/lessons.yaml → .claude/memory/
[ ] Create .claude/knowledge/
[ ] Move knowledge/**/*.md → .claude/knowledge/ (non-duplicate)
[ ] Delete handoff/, meta/, knowledge/
[ ] Update boot.md paths
[ ] Update wrapup.md paths

PHASE 9: CLAUDE.MD REWRITE
[ ] Add Component System section
[ ] Add Factory concept
[ ] Update Routing (Commands → Skills)
[ ] Fix meta/ file references
[ ] Update knowledge/ paths
```

---

## Session Learnings

### Facts
- Claude Code Tasks replaces custom handoff system
- Commands are deprecated in Claude Code
- CLAUDE.md references 3 meta files that don't exist (identity, focus, team)
- knowledge/ content duplicates CLAUDE.md (SSOT violation)
- Skills meta/ and neuron-knowledge/ are redundant with boot/wrapup

### Lessons
- Consolidate all config under `.claude/` for consistency
- SSOT: CLAUDE.md is the source, knowledge/ should not duplicate
- Delete > Migrate when content is redundant

### Patterns
- Everything under `.claude/` for discoverability
- api-* for external, capability-* for workflows
- Agent for judgment, Skill for execution

---

## References
- `.claude/factory/registry.yaml` - Component SSOT
- `.claude/agents/boot.md` - Component resolver
- `.claude/agents/wrapup.md` - Registry updater
