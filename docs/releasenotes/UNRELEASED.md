# Unreleased

> Changes pending for the next release

## Added

- **[Personal KB Architecture]** Hybrid short/long-term memory model for personal context management
  - Short-term memory: Compact summary in CLAUDE.md (~50 tokens, always loaded)
  - Long-term memory: Detailed YAML in meta/ folder (accessed via neuron-knowledge skill on demand)
  - meta/projects.yaml: Project registry with priorities, status, deliverables
  - meta/team.yaml: Team structure, roles, contacts
  - neuron-knowledge skill extended to access meta/ folder for personal context queries
  - Memory architecture: CLAUDE.md → meta/ retrieval pattern for scalable context management
- **[ui-ux-pro-max skill]** Comprehensive UI/UX design intelligence skill
  - 50+ UI styles (glassmorphism, minimalism, brutalism, neumorphism, etc.)
  - 97 color palettes organized by product type (SaaS, e-commerce, healthcare, fintech)
  - 57 font pairings with Google Fonts integration
  - 99 UX guidelines covering accessibility, performance, touch targets
  - 25 chart types with library recommendations
  - Support for 9 tech stacks: React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, Jetpack Compose
  - Python BM25 search engine for retrieving design recommendations
  - Design system generator with reasoning rules and anti-patterns
  - Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

## Changed

- **[P16 Automate Repetition]** Expanded principle with Automation Hierarchy guidance
  - CLAUDE.md description updated: "Code for deterministic, AI for judgment. Context is expensive."
  - philosophy.md adds hierarchy table: Code layer (deterministic) vs AI layer (judgment)
  - Clarifies when to use code (hooks, scripts) vs AI (review, architecture)
  - Emphasizes AI context cost as decision factor
- **[MCP Migration]** Advisor agent routing updated for MCP tool integration
  - Skill Enforcement section renamed to MCP Tool Routing
  - Routing table updated: Skill names → MCP tool prefixes (mcp__github__*, mcp__atlassian__*, etc.)
  - Output format changed: removed `required_skill`, added `mcp_tools` array
  - Added Google Calendar and Slack to routing table
- **[arkraft-fe]** Unified design system color palette to Blue/Green/Red semantic system
  - Phase colors simplified: insight/design/explore use blue variants, implement uses amber, evaluate uses green
  - Color naming standardized: `gray-*` → `neutral-*`, `cyan-*` → `blue-*`
  - Design tokens reorganized with clear semantic categories
  - 110+ component files updated for consistency
- **[submodules]** Updated all project submodules to latest stable versions
  - arkraft: 4e3e705 → 4381d9f (137 commits: research infrastructure, K8s migration, frontend redesign)
  - arkraft-fe: 6587482 → 1a20f2c (9 commits: HTML report rendering, data reports API, financial research page)
  - finter: 707dc66 → b98bf8e (12 commits: HTML report generation, flexible-report-generator integration, analysis API with agent logs)
  - pm-arkraft: 4ef7b4d → 5be5d13 (6 commits: ADR Confluence migration, Google Calendar scheduling, Slack notifications)
- **[modules]** Reorganized submodule structure into logical groups
  - modules/arkraft/ (active): pm-arkraft, arkraft-jupyter, arkraft-agent-report
  - modules/arkraft-legacy/ (legacy): arkraft, arkraft-fe, finter
  - modules/modeling (standalone)
  - Registry version bumped to v2 with updated module keys matching new paths

## Fixed

-

## Removed

- **[MCP Migration]** Removed skill files replaced by MCP tools (855 lines deleted)
  - .claude/skills/github-api/SKILL.md - use mcp__github__* tools
  - .claude/skills/jira-api/SKILL.md - use mcp__atlassian__* tools
  - .claude/skills/notion-api/SKILL.md - use mcp__notion__* tools
  - .claude/skills/confluence-api/SKILL.md - use mcp__atlassian__* tools
  - .claude/skills/slack-api/SKILL.md - use mcp__slack__* tools
  - .claude/skills/google-calendar/SKILL.md - use mcp__google-calendar__* tools
- **[Redundant Procedures]** Removed procedures superseded by better patterns
  - .claude/procedures/self-test.md - superseded by task-verification-workflow.md
  - .github/PULL_REQUEST_TEMPLATE.md - superseded by /pr skill dynamic generation
- **[hippo submodule]** Suspended hippo memory management module
  - Removed from .gitmodules and modules/ directory
  - Moved to archived section in modules/_registry.yaml with status: suspended
  - Archived on 2026-01-22
- **[arkraft-fe]** Removed unused color variants from design system
  - ColorVariant: removed `info`, `cyan`, `magenta`, `yellow`
  - TitleColor: removed `orange`, `cyan`, `yellow`, `magenta`, `white`, `purple`
  - CSS color classes: removed `cyan-*`, `magenta-*` references

## Security

- **[.gitignore]** Added .credentials/ directory to prevent credential leakage

## Breaking Changes

- **[Advisor Agent]** Output format changed for external service routing
  - Removed fields: `skill_required`, `required_skill`, `skill_reason`
  - Added field: `mcp_tools` (array of MCP tool names)
  - Changed field: `tool_reason` (replaces `skill_reason`)
  - Consumers must update to new output schema
- **[arkraft-fe]** Design system color API changes
  - Components using removed ColorVariant values (`info`, `cyan`, `magenta`, `yellow`) must migrate to new variants
  - TitleColor props must use new values: `default`, `blue`, `green`, `amber`, `red`
  - CSS classes referencing `gray-*` should use `neutral-*`

---

*Auto-updated by reviewer agent on PR creation.*
