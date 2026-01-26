---
name: workflow-code-test
description: Integration tests, E2E validation, and cross-module verification. Tests features in realistic scenarios.
allowed-tools: Read, Glob, Grep, Bash, Task
user-invocable: true
---

# Code Test Workflow

> Integration testing, E2E validation, and cross-module verification.

## When to Activate

- User requests testing of a feature or module
- Before deploying or releasing code
- Verifying integration between modules

## Prerequisites

- Feature/module to test is identified
- Test infrastructure exists or can be set up
- Services/dependencies are accessible

## Workflow Steps

### Step 1: Load Project Context

Read CLAUDE.md. Discover existing test infrastructure:

```bash
find . -type f -name "*.test.*" -o -name "*.spec.*" | head -20
```

### Step 2: Analyze Test Requirements

Determine what needs testing:
- Feature/module under test
- Success criteria
- Dependencies and services
- Existing test infrastructure

### Step 3: Set Up Test Environment

```bash
# Start services if needed
# Set up test database
# Create test data
# Install dependencies
```

### Step 4: Execute Test Suite

**Unit/Integration tests:**
```bash
npm test
# or pytest, go test, etc.
```

**E2E tests:**
```bash
npm run test:e2e
```

**Connectivity tests:**
```bash
curl -X GET http://localhost:3000/api/endpoint
```

### Step 5: Document Test Execution

Record each test run with:
- Command executed
- Output received
- Result (PASS/FAIL)
- Evidence (logs, screenshots)

### Step 6: Test Web Connectivity (when applicable)

```bash
curl -i http://localhost:PORT/health
curl -X POST http://localhost:PORT/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

Browser testing:
1. Open feature in browser
2. Check Network tab for successful requests
3. Verify data loads correctly
4. Test user interactions
5. Check for CORS or connectivity errors

### Step 7: Cross-Module Verification

For features spanning multiple modules:
- Verify module exports correctly
- Verify imports and usage
- Test communication between modules
- Verify data flow end-to-end

### Step 8: Failure Analysis

For each failure, document:
- Exact error message
- What was expected vs actual
- Root cause analysis
- Reproduction steps
- Suggested fix

## Output

```yaml
workflow_result:
  status: pass | fail
  date: "<date>"
  feature: "<name>"
  summary: "<1-2 sentence summary>"
  results:
    unit_tests:
      total: <n>
      passed: <n>
      failed: <n>
    integration_tests:
      total: <n>
      passed: <n>
      failed: <n>
    e2e_tests:
      total: <n>
      passed: <n>
      failed: <n>
    connectivity:
      total: <n>
      passed: <n>
      failed: <n>
  coverage: "<percentage>"
  failures:
    - test: "<name>"
      error: "<message>"
      root_cause: "<analysis>"
  recommendation: ready | fix-required | more-testing-needed
```

## Test Scope Guidance

| Scope | When | Tools |
|-------|------|-------|
| Unit | Single function/component | Jest, pytest |
| Integration | Module interactions | Test framework + mocks |
| E2E | Complete feature flow | Cypress, Playwright |
| Connectivity | API/web communication | curl, browser DevTools |

## Guardrails

- **NEVER** skip environment verification
- **NEVER** ignore test failures without root cause analysis
- **NEVER** test only the happy path
- **NEVER** assume connectivity without verification
- **ALWAYS** verify test environment is clean before testing
- **ALWAYS** test edge cases and error scenarios
- **ALWAYS** document results with evidence
- **ALWAYS** include reproduction steps for failures
