# Retrospective v0.3.0

> Released: 2026-01-15

## Patterns

> Recurring issues detected by reviewer agent

| Date | PR | Pattern | Status |
|------|-----|---------|--------|
| 2026-01-15 | claude/refactor-submodule-mapping-h6mdU | Branch naming doesn't follow git-workflow.md convention (claude/ prefix instead of feature/) | pending |
| 2026-01-15 | claude/refactor-submodule-mapping-h6mdU | Test-First principle violated: compliance audit script has no test suite | pending |
| 2026-01-15 | claude/refactor-submodule-mapping-h6mdU | Task verification workflow skipped (no verification criteria defined) | pending |
| 2026-01-14 | claude/optimize-neural-activation-WWCmm | Branch naming doesn't follow git-workflow.md convention (missing feature/docs/fix prefix) | pending |
| 2026-01-14 | claude/optimize-neural-activation-WWCmm | Task verification workflow skipped for documentation changes | pending |
| 2026-01-14 | claude/optimize-neural-activation-WWCmm | SSOT violation: Skill routing table duplicated in CLAUDE.md and advisor.md | pending |
| 2026-01-14 | submodules | Documentation location unclear - created in Git then moved to Confluence (SSOT violation) | pending |
| 2026-01-14 | submodules | Multi-submodule commits lack scope clarity in message | pending |
| 2026-01-14 | submodules | Submodule dirty state committed (uncommitted changes within submodule) | pending |
| 2026-01-14 | arkraft-fe | API routes lack test coverage despite external dependencies | pending |
| 2026-01-13 | pm-arkraft | Language policy unclear for submodule .claude/ directories (Korean in neuron infra) | resolved (neuron-base.md clarified) |
| 2026-01-13 | pm-arkraft | SSOT violation through documentation duplication (team registry in assign.md) | pending |
| 2026-01-13 | pm-arkraft | Deprecated Jira API field 'Epic Link' used instead of 'parent' | pending |

## Insights

> What worked well, lessons learned

- 2026-01-15: Principle citation requirement creates explicit reasoning trail - [P#] format makes decision rationale auditable
- 2026-01-15: Automated compliance checking enables scalable governance - audit script can verify policies across all submodules
- 2026-01-15: Template embedding in knowledge/ ensures consistency - repo-setup.md provides copy-paste template with all required sections
- 2026-01-15: Bias toward action guideline operationalizes P13 - "low confidence = exceptional case" prevents analysis paralysis
- 2026-01-15: "Questions are failures" philosophy articulates autonomous execution - reframes user questions as system improvement opportunities
- 2026-01-14: Critical Rules section uses structural prominence to enforce compliance - placing rules at document top increases visibility
- 2026-01-14: Skill enforcement through advisor output format - adding required_skill field creates programmatic enforcement point
- 2026-01-14: Trigger keyword table enables systematic detection - maps service names to required skills
- 2026-01-14: SSOT correction - recognized Git docs should not duplicate Confluence ADR, deleted local file
- 2026-01-14: IAM credentials added with Bearer Token fallback demonstrates proper backward compatibility strategy
- 2026-01-14: Submodule architecture properly isolates changes - neuron commit is clean pointer update
- 2026-01-14: Release notes comprehensively document changes across multiple submodules
- 2026-01-14: Environment variable externalizes endpoint config - moving from hardcoded IP to production domain improves portability
- 2026-01-14: .env.example serves as documentation for required configuration without storing actual values
- 2026-01-14: Fallback pattern in env var usage (process.env.X || 'default') provides development convenience
- 2026-01-14: File splitting kept functions cohesive - results.py, logging_utils.py, user_prompts.py each have clear single responsibility
- 2026-01-14: Agent-specific prompt files (alpha.py, insight.py) improved maintainability without breaking public API (get_system_prompt)
- 2026-01-14: IAM credentials support added with backward compatibility (Bearer Token fallback) enables smooth migration
- 2026-01-14: Incremental approach to Trading page - AUM calculation added without disrupting existing functionality
- 2026-01-14: Conditional data fetching pattern (fetch balances only when active strategy exists) prevents unnecessary API calls
- 2026-01-14: useMemo for portfolio metrics calculation optimizes re-render performance
- 2026-01-13: team-registry.yaml demonstrates proper SSOT implementation for cross-system IDs (Jira/Slack)
- 2026-01-13: Setup guide provides clear API token configuration without storing secrets

## Improvements

> System fixes by self-improve agent

| Date | PR | Target | Change | Root Cause |
|------|-----|--------|--------|------------|
