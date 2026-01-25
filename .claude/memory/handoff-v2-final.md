# Handoff: Neuron v2 Final Cleanup

## State
| Field | Value |
|-------|-------|
| **Status** | in-progress |
| **Updated** | 2026-01-25 |
| **Branch** | claude/neuron-agent-skills-redesign-fgh1M |

---

## 잔여 이슈 (2개)

### Issue 1: meta/ 폴더 미삭제

```
neuron/
├─ meta/lessons.yaml          ← 구버전 (삭제 필요)
└─ .claude/memory/lessons.yaml ← 신버전
```

**문제**: 두 파일 내용 다름 (SSOT 위반)
- `meta/lessons.yaml`: Claude Code framework facts (v2 관련)
- `.claude/memory/lessons.yaml`: arkraft 관련 facts

**해결**:
```bash
# meta/lessons.yaml의 v2 관련 facts를 .claude/memory/lessons.yaml에 병합
# 그 후 meta/ 폴더 삭제
rm -rf meta/
```

### Issue 2: boot.md 경로 오류

**위치**: `.claude/agents/boot.md` Step 1

```markdown
### Step 1: Load Handoff State
Read handoff/_index.md   ← 삭제된 폴더 참조!
```

**해결**: Step 1 제거 또는 Tasks 연동으로 변경

---

## 핵심 문제: v2 사상 미전달

### 증상

AI가 프로젝트 설명 시:
> "Neuron은 Claude Code를 위한 AI 에이전트 프레임워크"

### 원인: CLAUDE.md에 핵심 사상 부재

| v2 핵심 개념 | CLAUDE.md 상태 |
|-------------|---------------|
| Neuron = Factory | 한 줄만 (섹션 없음) |
| Claude Code = Framework | 언급 없음 |
| Self-Evolution Pattern | 언급 없음 |
| Factory → Tasks → Next Session | 언급 없음 |
| Don't Reinvent | 언급 없음 |

### 해결: CLAUDE.md Executive Summary 추가

```markdown
## What is Neuron?

**Neuron = Component Factory. Claude Code = Framework.**

Neuron은 프레임워크가 아닙니다. Claude Code가 이미 프레임워크입니다.
Neuron은 Claude Code 위에서 동작하는 Component Factory입니다.

### Claude Code가 이미 제공하는 것 (바퀴 재발명 금지)
- `.claude/agents/*.md` - Agent 정의
- `.claude/skills/` - Skill 시스템
- `~/.claude/tasks/` - 세션 간 작업 관리
- Task tool - 최대 10개 병렬 실행
- Hooks - PreToolUse, PostToolUse, SubagentStart, SubagentStop
- Agent resume - agentId로 재개

### Neuron이 추가하는 것
- **Factory**: 없는 컴포넌트를 템플릿으로 생성
- **Registry**: 모든 컴포넌트 SSOT 추적
- **Philosophy**: 3 Axioms, 20 Principles 주입
- **Memory**: 세션 간 학습 지속

### Self-Evolution Pattern

Factory → Tasks → Next Session

1. boot.md가 누락된 컴포넌트 감지
2. Factory가 템플릿으로 컴포넌트 생성
3. Task 생성 (pending: session_restart)
4. 다음 세션에서 컴포넌트 사용 가능
```

---

## 완료된 작업

1. [x] meta/lessons.yaml 병합 후 삭제
2. [x] boot.md Step 1 수정 (handoff 참조 제거)
3. [x] CLAUDE.md에 "What is Neuron?" 섹션 추가
4. [x] 커밋 및 푸시 (451ebd0)

---

## 올바른 프로젝트 설명 (참고용)

**Neuron은 Claude Code 프레임워크 위에서 동작하는 Component Factory입니다.**

Claude Code가 agents, skills, tasks, hooks를 제공하면,
Neuron은 이를 조직화하고, 없는 컴포넌트를 자동 생성하며,
세션 간 학습을 지속합니다.

핵심 원리:
1. **Factory Pattern**: 템플릿 기반 컴포넌트 생성
2. **Registry as SSOT**: 모든 컴포넌트 상태 추적
3. **Philosophy Injection**: 3 Axioms, 20 Principles
4. **Self-Evolution**: 스스로 성장하는 시스템
