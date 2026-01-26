# Approval Criteria Reference

Decision matrix for PR and code review approval status.

## Status Definitions

| Status | Meaning | Next Action |
|--------|---------|-------------|
| approve | All checks pass, ready to merge | Proceed with merge |
| changes-requested | Issues found, needs fixes | Author addresses feedback |
| blocked | Critical issues, cannot proceed | Escalate or redesign |

## Approval Decision Matrix

### Approve When

All of these conditions are met:
- No critical or high severity findings
- All tests pass
- No security vulnerabilities
- Breaking changes documented (if any)
- Release notes updated

### Changes Requested When

Any of these conditions exist:
- Medium severity findings present
- Style/convention violations
- Missing test coverage
- Documentation gaps
- Performance concerns (non-critical)

### Blocked When

Any of these conditions exist:
- Critical security vulnerability
- Breaking change without migration path
- Data loss risk
- System stability threat
- Credential/secret exposure

## Finding Severity Levels

| Severity | Definition | Impact |
|----------|------------|--------|
| critical | System failure or security breach | Blocks merge |
| high | Significant bug or vulnerability | Blocks merge |
| medium | Quality issue or tech debt | Request changes |
| low | Style or minor improvement | Note in review |
| info | Observation or suggestion | Optional |

## Automatic Blocks

These issues always block approval:

```
- Hardcoded secrets/credentials
- SQL injection vulnerabilities
- XSS vulnerabilities
- Unvalidated user input in security context
- Breaking changes to public API without version bump
```

## Override Authority

| Situation | Who Can Override |
|-----------|------------------|
| Low/Medium findings | Reviewer discretion |
| High findings | Senior developer + documented reason |
| Critical findings | No override - must fix |
| Blocked status | Architecture review required |
