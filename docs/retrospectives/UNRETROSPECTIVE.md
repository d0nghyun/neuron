# Unretrospective

> Learnings pending for the next release

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-13 | #TBD | Language policy violation - Korean text in neuron files violates CLAUDE.md English-only convention | pending |
| 2026-01-13 | #TBD | Branch naming inconsistency - Auto-generated branch doesn't follow feature/ prefix convention from git-workflow.md | pending |
| 2026-01-12 | - | 불필요한 확인 질문 (push 할까?) - Autonomous Execution 원칙 위반 | noted |
| 2026-01-13 | modeling#feat/neuron-quickstart | Test evaluation file exceeds 200-line limit (493 lines) - File size convention not enforced in test files | pending |

## Insights

> What worked well, lessons learned (updated by reviewer on each PR)

- **2026-01-13**: Telegram notification hook demonstrates good security practices - checks for required env vars, suppresses sensitive output, no hardcoded secrets.
- **2026-01-13**: Automation of repetitive notifications follows "Automate Repetition" principle - transforms manual status checks into automatic push notifications.
- **2026-01-12**: Claude Code subagent에 `skills` 필드 존재. subagent가 skill을 자동 로드 가능. advisor에 neuron-knowledge skill 연결로 knowledge/ 참조 자동화.
- **2026-01-12**: Visual documentation (ASCII diagrams) makes abstract concepts concrete. Brain analogies help users remember agent roles naturally. Documentation reorganization (root → docs/) follows MECE principle.
- **2026-01-13**: WHY sections in SKILL.md critical rules dramatically improve beginner understanding. Explaining "Citadel fires people for this" adds real-world weight to abstract technical rules.
- **2026-01-13**: Progression maps with "YOU ARE HERE" markers reduce cognitive load for beginners navigating complex skill hierarchies.
- **2026-01-13**: Test-first approach for documentation - defining 15 evaluation questions before building the skill ensured completeness.
- **2026-01-13**: Task verification workflow codifies "Verify Before Done" into executable pattern. Define → Execute → Verify cycle prevents premature "done" declarations.

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|

---

*Auto-updated by reviewer and self-improve agents.*
