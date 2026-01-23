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

## Fixed

-

## Removed

-

## Security

-

## Breaking Changes

- arkraft-agent-insight: CLI signature changed from `arkraft-insight <topic> <universe>` to `arkraft-insight <request>`. Users must update scripts accordingly.

---

*Auto-updated by reviewer agent on PR creation.*
