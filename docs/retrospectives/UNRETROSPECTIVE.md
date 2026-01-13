# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-13 | #TBD | Task verification workflow skipped - No verification criteria defined before slack-api skill creation | pending |
| 2026-01-13 | claude/task-completion-notifications-5WXXe | Task verification workflow skipped - No verification criteria defined before execution, violates Test-First and Verify Before Done | pending |
| 2026-01-13 | claude/task-completion-notifications-5WXXe | Debug logs without lifecycle - Writing to /tmp/ without cleanup strategy creates data accumulation risk | pending |
| 2026-01-13 | #TBD | Language policy violation - Korean text in neuron files violates CLAUDE.md English-only convention | pending |
| 2026-01-13 | #TBD | Branch naming inconsistency - Auto-generated branch doesn't follow feature/ prefix convention from git-workflow.md | pending |
| 2026-01-12 | - | 불필요한 확인 질문 (push 할까?) - Autonomous Execution 원칙 위반 | noted |
| 2026-01-13 | modeling#feat/neuron-quickstart | Test evaluation file exceeds 200-line limit (493 lines) - File size convention not enforced in test files | pending |

## Insights

> What worked well, lessons learned (updated by reviewer on each PR)

- **2026-01-13**: Principle #20 (Sustainable by Design) codifies "process over output" philosophy - Addresses gap where system had principles for quality/truth but not for long-term reproducibility. Complements Automate Repetition (#16) by focusing on reusability over automation.
- **2026-01-13**: Submodule inheritance model (Required vs Configurable policies) provides clear override semantics without duplicating neuron philosophy. Conceptual reference via GitHub link maintains context without creating hard dependency.
- **2026-01-13**: ADR structure with 상태/맥락/결정/결과 provides complete decision context. ADR-0001 (Confluence SSOT) and ADR-0002 (no tenant) demonstrate good practice of documenting "why not" decisions.
- **2026-01-13**: PM workflow aligned to philosophy principles (workflow.md lines 5-11 table) makes abstract principles concrete for non-technical domain.
- **2026-01-13**: Slack-api skill follows established pattern consistency - Matching github-api structure (frontmatter, sections, examples) makes skills predictable and easier to learn.
- **2026-01-13**: Comprehensive API documentation in skill files - Including auth, common operations, error handling, and rate limits in one place reduces context switching.
- **2026-01-13**: Telegram notification hook demonstrates good security practices - checks for required env vars, suppresses sensitive output, no hardcoded secrets.
- **2026-01-13**: Automation of repetitive notifications follows "Automate Repetition" principle - transforms manual status checks into automatic push notifications.
- **2026-01-13**: Transcript parsing for context extraction - Reading Claude session transcript to extract Q&A provides significantly better notification UX than generic metadata. Human can recall "what did I ask?" instantly from notification.
- **2026-01-13**: Text cleaning strategy for external APIs - Removing markdown/special chars before sending to Telegram prevents formatting issues. Length limits (100/150 chars) ensure mobile-friendly notifications.
- **2026-01-12**: Claude Code subagent에 `skills` 필드 존재. subagent가 skill을 자동 로드 가능. advisor에 neuron-knowledge skill 연결로 knowledge/ 참조 자동화.
- **2026-01-12**: Visual documentation (ASCII diagrams) makes abstract concepts concrete. Brain analogies help users remember agent roles naturally. Documentation reorganization (root → docs/) follows MECE principle.
- **2026-01-13**: WHY sections in SKILL.md critical rules dramatically improve beginner understanding. Explaining "Citadel fires people for this" adds real-world weight to abstract technical rules.
- **2026-01-13**: Progression maps with "YOU ARE HERE" markers reduce cognitive load for beginners navigating complex skill hierarchies.
- **2026-01-13**: Test-first approach for documentation - defining 15 evaluation questions before building the skill ensured completeness.
- **2026-01-13**: Task verification workflow codifies "Verify Before Done" into executable pattern. Define → Execute → Verify cycle prevents premature "done" declarations.
- **2026-01-13**: SSOT refactoring via reference pattern - Replacing duplicated content with references to canonical source maintains single source of truth without losing discoverability. Reader can follow reference when needed.
- **2026-01-13**: Slack bot permission troubleshooting - `groups:history` scope required for private channels. Token in `.env.local` must be updated after app reinstall. Environment variables in curl prevent special character issues.

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|

---

*Auto-updated by reviewer and self-improve agents.*
