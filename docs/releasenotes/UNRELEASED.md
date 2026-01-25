# Unreleased

> Changes pending for the next release

## Added

- workflow-init-module skill for activating module skills/agents via symlink during session
- learn-failures.yaml for persistent failure tracking and pattern prevention
- arkraft-agent-insight: planner subagent for natural language request parsing (topic, universe, count extraction)
- boot agent: session initialization - loads handoff, focus, and relevant lessons at session start
- wrapup agent: session teardown - extracts facts/lessons/patterns and updates handoff at session end
- meta/lessons.yaml: structured long-term memory storage with fact/lesson/pattern types
- arkraft-agent-pm: specs/ knowledge cache for offline AI context loading (Confluence read-only mirror)
- arkraft-agent-pm: /ask command for project Q&A with cache-first, API-fallback strategy
- arkraft-agent-pm: /route command for expertise-based issue-to-assignee matching
- arkraft-agent-pm: /sync-specs command for Confluence to specs/ synchronization

## Changed

- Agent naming convention standardized: role-reviewer → code-reviewer, role-refactor → code-refactor, task-self-improve → system-self-improve
- Factory README updated with clarified naming conventions (system-*, code-*, api-*, workflow-*, capability-* prefixes)
- Factory README: added Location Decision guide for choosing between neuron-level vs module-level component placement
- system-boot agent: corrected glob paths from relative to absolute (.claude/agents/*.md, .claude/skills/*/SKILL.md, .claude/contexts/ctx-*.yaml)
- CLAUDE.md: Step 3 (Component Creation) now explicitly states "MANDATORY SEQUENCE - NO EXCEPTIONS" with numbered steps
- CLAUDE.md: Added emphasis on reading factory/pattern files and following naming conventions before component creation
- All skill SKILL.md files updated: directory names now match YAML name field for consistency
- All agent YAML name fields updated to match filename conventions (system-boot, system-wrapup, system-advisor, code-reviewer, code-refactor, system-self-improve)
- learn-failures.yaml added to document recurring issues and preventions (factory-skip, prefix-inconsistency)
- arkraft-agent-insight: simplified CLI to accept single natural language request instead of explicit topic/universe parameters
- arkraft-agent-insight: updated README with planner architecture diagram and multilingual examples
- CLAUDE.md: added Critical Rule #6 for mandatory session lifecycle (boot/wrapup)
- CLAUDE.md: updated Agents table and Routing table to include boot/wrapup agents
- CLAUDE.md: updated Session Protocol to replace manual handoff steps with agent-driven workflow
- CLAUDE.md: added meta/lessons.yaml to Personal Context table
- CLAUDE.md: redesigned Component Lifecycle - boot now lists available components only, main agent decides what's needed
- CLAUDE.md: simplified Session Lifecycle to universal boot→execute→wrapup (removed conditional logic)
- system-boot agent: changed from "required components" analysis to "available components" listing - no longer judges what's needed
- workflow-audit-modules skill: inlined module protocol documentation (independence requirement, registry schema)
- arkraft-agent-pm: CLAUDE.md updated with Commands section documenting /ask, /route, /sync-specs
- arkraft-agent-pm: specs/ directory repurposed from specifications to knowledge cache

## Fixed

-

## Removed

- Deleted 11 obsolete knowledge files (1393 lines):
  - git-advanced.md, git-github-settings.md, git-workflow.md (git workflows)
  - guide-decision.md, guide-repo-setup.md (consolidated into factory patterns)
  - protocol-module.md, protocol-self-improve.md (inlined into relevant components)
  - workflow-release.md, workflow-spec.md, workflow-task-verification.md (replaced by skills)
  - ref-neuron-v2-vision.md (v2 vision now implemented)

## Security

-

## Breaking Changes

- arkraft-agent-insight: CLI signature changed from `arkraft-insight <topic> <universe>` to `arkraft-insight <request>`. Users must update scripts accordingly.

---

*Auto-updated by reviewer agent on PR creation.*
