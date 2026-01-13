# Unreleased

> Changes pending for the next release

## Added

- Telegram notification on Claude Code Stop event
  - Extracts user question and assistant answer from transcript for context-rich notifications
  - Concise message format with Q&A instead of verbose metadata
  - Debug logging for troubleshooting hook execution
  - Auto-loads .env.local for Claude subprocesses
  - Includes session resume command for quick continuation
  - Opt-in via TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars
- **modules/modeling**: finter-quickstart skill - 15-minute beginner onboarding path to first backtest
- **modules/modeling**: /finter-skills:start command - Interactive routing based on user experience level
- **modules/modeling**: Skill routing decision tree in CLAUDE.md - Machine-readable keyword mapping for Claude
- **modules/modeling**: Skill progression map - Visual guide from quickstart to advanced skills
- **modules/modeling**: Claude evaluation test framework - 15 test questions across 5 categories (onboarding, skill selection, execution, edge cases)
- **modules/modeling**: WHY explanations for critical rules in finter-alpha and finter-portfolio skills
- **knowledge/task-verification-workflow.md**: Universal task verification pattern (Define → Execute → Verify → Feedback)
- **CLAUDE.md**: Routing entry for task verification workflow
- **.claude/agents/reviewer.md**: Step 2b verification check

## Changed

- Moved `diagram.md` from root to `docs/diagram.md` for better documentation organization
- Enhanced architecture diagram with new sections:
  - Agent System with brain analogies (PFC, Hippocampus, ACC, Neuroplasticity)
  - Advisor-before-AskUser decision flow visualization
  - Routing Table categorizing Agents vs Skills vs Commands
  - PR/Release workflow diagram showing agent integration
  - Expanded directory structure with actual module names
- **modules/modeling**: Standardized commands/setup.md to English (was Korean) per neuron language policy
- **knowledge/_index.yaml**: Added trigger pattern for task verification workflow
- Telegram notification hook enhancements:
  - Session emoji for visual distinction between concurrent sessions
  - Task keyword extraction from first user message for context
  - Consistent header format across question/permission/stop modes
- SSOT refactoring:
  - **knowledge/neuron-base.md**: Verification section now references repo-setup.md checklist
  - **knowledge/release-workflow.md**: Step 4-7 execution now references /release command

## Fixed

-

## Removed

-

## Security

-

## Breaking Changes

-

---

*Auto-updated by reviewer agent on PR creation.*
