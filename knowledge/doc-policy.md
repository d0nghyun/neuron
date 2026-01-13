# Documentation Policy

## Philosophy

문서는 코드와 동일한 수준의 관리가 필요하다.
SSOT(Single Source of Truth)를 유지하고, 자동화된 검증으로 품질을 보장한다.

## Document Location Matrix

| 문서 유형 | 위치 | SSOT 원칙 | 예시 |
|-----------|------|-----------|------|
| 철학/원칙 | neuron/knowledge/ | 참조만 허용 | philosophy.md |
| 모듈 메타데이터 | modules/_registry.yaml | 단일 출처 | 상태, 도메인, 태그 |
| 프로젝트 워크플로우 | {module}/docs/ | 서브모듈 소유 | ai-pm-workflow.md |
| 팀/설정 정보 | {module}/*.yaml | 단일 출처 | team-registry.yaml |
| 아키텍처 결정 | {module}/decisions/ | ADR 패턴 | 0001-decision.md |
| 명령어 정의 | {module}/.claude/commands/ | 서브모듈 소유 | assign.md |
| 범용 스킬 | neuron/.claude/skills/ | neuron 소유 | jira-api/ |
| 릴리즈 노트 | 각 저장소별 | 저장소 소유 | UNRELEASED.md |

## SSOT Rules

### Hierarchy

```
neuron (메타 정책)
  ↓ 참조 (URL, 개념적)
submodule (프로젝트 정책)
  ↓ 참조
commands/docs (실행 문서)
```

### Rules

1. **상위 → 하위**: 참조만 허용, 복사 금지
   - Good: "neuron 철학은 github.com/d0nghyun/neuron 참조"
   - Bad: 철학 내용을 서브모듈에 복사

2. **동일 레벨**: 한 곳에서만 정의
   - Good: `team-registry.yaml`이 SSOT, 다른 문서는 참조
   - Bad: 여러 문서에 팀 정보 중복

3. **외부 시스템**: Git = Working SSOT, Confluence = Stakeholder View
   - 방향: Git → Confluence (단방향)

## Language Policy

### Decision Tree

```
파일 위치 확인
     │
     ├── neuron/* → 영어 (예외 없음)
     │
     └── submodule/*
           │
           ├── .claude/* → 영어 (AI 인프라)
           │   - commands/*.md
           │   - agents/*.md
           │   - skills/*.md
           │   - procedures/*.md
           │
           └── 콘텐츠 파일 → 서브모듈 정책 따름
               - docs/*.md
               - decisions/*.md
               - README.md
```

### Rationale

- `.claude/` 디렉토리는 Claude Code 인프라 → AI-First 원칙 → 영어
- 비즈니스 문서는 서브모듈 정책에 따라 로컬 언어 허용

## Version Control

| 항목 | 정책 | 예시 |
|------|------|------|
| 커밋 메시지 | Conventional Commits | `feat(docs): add policy` |
| ADR 번호 | 4자리 순차 | 0001, 0002 |
| 릴리즈 노트 | UNRELEASED.md → vX.Y.Z.md | 릴리즈 시 변환 |

## Related

- [module-protocol.md](module-protocol.md) - 서브모듈 관리
- [repo-setup.md](repo-setup.md) - 저장소 초기 설정
