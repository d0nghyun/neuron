# Neuron v2 Vision

> **Neuron은 Claude Code 프레임워크 위에서 동작하는 Component Factory로, 철학 기반의 자가 진화 시스템이다.**

---

## 1. 정체성

```
Neuron ≠ Framework
Neuron = Component Factory

Claude Code = Framework (이미 제공)
Neuron = Factory (그 위에서 동작)
```

---

## 2. 바퀴 재발명 금지

| Claude Code 제공 | Neuron 추가 |
|-----------------|-------------|
| `.claude/agents/*.md` | **Factory** - 템플릿 기반 생성 |
| `.claude/skills/` | **Registry** - SSOT 추적 |
| `~/.claude/tasks/` | **Philosophy** - 3 Axioms, 20 Principles |
| Task tool (10 parallel) | **Memory** - 세션 간 학습 |
| Hooks | **Self-Evolution** - 자가 성장 |
| Agent resume (agentId) | |

---

## 3. Self-Evolution Pattern

```
system-boot.md (컴포넌트 감지)
    │ missing?
    ▼
Factory.create() (템플릿 기반 생성)
    │
    ▼
Task 생성 (pending: session_restart)
    │
    ▼
다음 세션 → 컴포넌트 사용 가능
```

---

## 4. 컴포넌트 분류

| 유형 | 역할 | 예시 |
|------|------|------|
| **Agent** | Judgment (판단) | advisor, reviewer, refactor |
| **Skill** | Execution (실행) | api-*, capability-*, /pr |
| **Hook** | Automation (자동화) | PreToolUse, PostToolUse |

### 결정 기준

```
판단/추론 필요? → Agent
외부 API? → Skill (api-*)
재사용 워크플로우? → Skill (capability-*)
자동 트리거? → Hook
```

---

## 5. SSOT 원칙

| SSOT | 역할 |
|------|------|
| `CLAUDE.md` | 철학, 라우팅, 핵심 규칙 |
| `.claude/factory/registry.yaml` | 컴포넌트 상태 |
| `.claude/memory/lessons.yaml` | 세션 간 학습 |

---

## 6. 세션 라이프사이클

```
Session Start → system-boot.md (MANDATORY)
    ├─ Registry 로드
    ├─ 컴포넌트 리졸버
    └─ 컨텍스트 주입

[Work]

Session End → system-wrapup.md (MANDATORY)
    ├─ 학습 추출 (facts, lessons, patterns)
    ├─ Registry 업데이트
    └─ 세션 연속성 확보 (Tasks)
```

---

## 7. 명명 규칙

```
Agents:   .claude/agents/{category}-{name}.md
          - system-*     → 코어 라이프사이클 (boot, wrapup, advisor)
          - role-*       → 판단/리뷰 (reviewer, refactor)
          - task-*       → 작업 지향 (self-improve)

Skills:   .claude/skills/{category}-{name}/SKILL.md
          - api-*        → 외부 서비스 래퍼
          - capability-* → 재사용 워크플로우
          - workflow-*   → 내부 워크플로우 (pr, release)

Contexts: .claude/contexts/ctx-{module}.yaml
Memory:   .claude/memory/{type}.yaml
Knowledge: .claude/knowledge/{topic}.md
```

---

## 8. 철학 기반

### 3 Axioms

| Axiom | Question | Drives |
|-------|----------|--------|
| Curiosity | "What if?" | 탐색, 학습, 능동 행동 |
| Truth | "Is it correct?" | 정확성, 검증, SSOT |
| Beauty | "Is it clean?" | 단순함, 우아함, 최소 복잡성 |

### 핵심 Principles

| # | Principle | 설명 |
|---|-----------|------|
| P1 | SSOT | 단일 진실 소스 |
| P3 | Simplicity First | 단순한 해결책 우선 |
| P13 | Autonomous Execution | 질문 전 실행 |
| P15 | Verify Before Done | 완료 전 검증 |
| P17 | Learn from Failure | 실패에서 학습 |

---

## 9. 자율 실행 원칙

```
"질문은 실패다"

User → 방향 설정
AI   → 실행 책임

불확실? → advisor 먼저 (user에게 묻기 전)
```

---

## 10. v2 폴더 구조

```
neuron/
├─ CLAUDE.md                 # SSOT
├─ .claude/
│  ├─ agents/       (6)      # Judgment
│  ├─ skills/       (10)     # Execution
│  ├─ factory/               # Templates + Registry
│  ├─ memory/       (4)      # Long-term state
│  ├─ knowledge/    (13)     # Reference docs
│  └─ contexts/     (1)      # Module configs
└─ modules/                  # Submodules
```

---

## References

- `CLAUDE.md` - 핵심 규칙 및 라우팅
- `.claude/factory/registry.yaml` - 컴포넌트 SSOT
- `.claude/memory/lessons.yaml` - v2 학습 내용 포함
