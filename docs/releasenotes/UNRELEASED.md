# Unreleased

> Changes pending for the next release

## Added

- arkraft-agent-insight: planner subagent for natural language request parsing (topic, universe, count extraction)
- boot agent: session initialization - loads handoff, focus, and relevant lessons at session start
- wrapup agent: session teardown - extracts facts/lessons/patterns and updates handoff at session end
- meta/lessons.yaml: structured long-term memory storage with fact/lesson/pattern types

## Changed

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
