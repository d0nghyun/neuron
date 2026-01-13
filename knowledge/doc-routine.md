# Documentation Routine

정기적인 문서 품질 관리를 위한 루틴.

## Routine Summary

| 루틴 | 주기 | 트리거 | 담당 | 자동화 |
|------|------|--------|------|--------|
| SSOT 검증 | PR마다 | PR 생성 | reviewer | 자동 |
| 언어 정책 검증 | PR마다 | PR 생성 | reviewer | 자동 |
| API 필드 검증 | 월 1회 | 스케줄 | 수동 | Phase 2 |
| 문서 중복 스캔 | 릴리즈마다 | /release | reviewer | 반자동 |
| 지식 동기화 | 분기 1회 | 수동 | 담당자 | 수동 |

## PR Review Routine (Auto)

reviewer agent가 PR마다 자동 검증:

### Checklist

| 검사 | 통과 기준 |
|------|-----------|
| SSOT 준수 | 중복 정의 없음 |
| 언어 정책 | .claude/* = 영어 |
| 파일 크기 | 200줄 이하 |
| 참조 패턴 | ../.. 상대경로 없음 |
| deprecated API | 사용 없음 |

### Validation Commands

```bash
# SSOT 중복 검사 (예: team-registry)
grep -r "slackUserId\|jiraAccountId" --include="*.md" modules/pm-arkraft/
# 예상: yaml 파일만 매칭

# 언어 정책 검사 (.claude/ 내 한글 감지)
grep -P '[\uAC00-\uD7A3]' modules/pm-arkraft/.claude/**/*.md
# 예상: 매칭 없음

# deprecated API 필드 검사
grep -r "Epic Link\|customfield_10014" modules/pm-arkraft/
# 예상: 매칭 없음 (parent 사용)
```

## Release Routine (Semi-Auto)

/release 실행 시 문서 건강도 리포트 생성:

```markdown
## Documentation Health Report

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| SSOT violations | 0 | 0 | PASS |
| Language policy violations | 0 | 0 | PASS |
| Files over 200 lines | 1 | 0 | WARN |
| Deprecated API usage | 0 | 0 | PASS |
```

## Monthly API Validation (Manual → Phase 2)

### Current (Manual)

매월 첫째 주 실행:

- [ ] Jira API changelog 확인
  - https://developer.atlassian.com/cloud/jira/platform/changelog/
- [ ] Confluence API changelog 확인
- [ ] deprecated 필드 grep 검색
- [ ] 발견 시 UNRETROSPECTIVE.md에 기록

### Phase 2 (Automated)

7+ 인원, 주 2회 이상 사용 시 자동화:

```yaml
# .github/workflows/api-audit.yml
name: Monthly API Audit
on:
  schedule:
    - cron: '0 9 1 * *'  # 매월 1일
jobs:
  audit:
    steps:
      - name: Check deprecated fields
        run: grep -r "Epic Link" --include="*.md" || true
```

## Quarterly Knowledge Sync (Manual)

매 분기 neuron 정책 변경 반영:

### Checklist

1. [ ] neuron/knowledge/ 변경 확인
   ```bash
   git log --since="3 months ago" -- knowledge/
   ```

2. [ ] 서브모듈 CLAUDE.md "Inherited Policies" 검토
   - Required 정책 누락 확인
   - Override 사유 유효성 검토

3. [ ] 새 원칙 적용 결정
   - 적용: CLAUDE.md 업데이트
   - 미적용: override 사유 문서화

## Phase Triggers

| Phase | 트리거 조건 |
|-------|-------------|
| Phase 1 | 즉시 적용 (현재) |
| Phase 2 | 7+ 인원, 주 2회 이상 사용 |
| Phase 3 | 10+ 인원, 월 3+ ADR 생성 |

## Related

- [doc-policy.md](doc-policy.md) - 문서 정책
- [release-workflow.md](release-workflow.md) - 릴리즈 프로세스
