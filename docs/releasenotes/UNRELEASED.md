# Unreleased

> Neuron v2 — Intent-First Architecture

## Added

- system-reviewer agent: Quality gate for component pattern compliance, SSOT, naming
- ARCHITECTURE.md: System map (neuron vs vault, what lives where)
- Intent-based approach: DIRECT / DELEGATE / COLLABORATE routing

## Changed

- enforce-claude-md.sh: Rigid protocol (BOOT → ORCHESTRATE → EXECUTE → WRAPUP) replaced with intent-first guidance
- CLAUDE.md: Simplified to router (principles + structure + approach). No session protocol.
- factory/README.md: Removed 3-layer hierarchy (meta/business/worker), orchestrator references
- factory/pattern-agent.md: Removed `layer` field from frontmatter
- agents/README.md: Replaced layer model with flat agent list + intent flow
- system-recruiter.md: Removed orchestrator/advisor flow, layer assignment step
- docs/diagram.md: Rewritten for intent-first architecture

## Removed

- system-boot agent: Context loading is now on-demand
- system-orchestrator agent: Main agent does intent analysis directly
- system-wrapup agent: Vault writes happen inline when needed
- system-advisor agent: Removed with orchestrator
- system-updater agent: Mechanical maintenance, rarely triggered
- system-self-improve agent: Never triggered organically
- feature-dev agent: Workers belong in modules, not neuron
- frontend-dev agent: Workers belong in modules, not neuron
- arkraft-qa-tester agent: Project-specific, belongs in module
- factory/pattern-orchestrator.md: No separate orchestrator pattern needed
- 3-layer hierarchy (meta/business/worker): Agents are just agents

## Breaking Changes

- Session no longer runs BOOT → ORCHESTRATE → EXECUTE → WRAPUP
- No `layer` field in agent frontmatter
- Worker agents must live in their module's `.claude/agents/`, not neuron level
