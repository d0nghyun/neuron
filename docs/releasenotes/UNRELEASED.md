# Unreleased

> Changes pending for the next release

## Added

- **[API Skills Restored]** Reverted MCP migration, restored 6 API skill files to reduce context overhead
  - .claude/skills/api/github/SKILL.md - GitHub REST API (issues, PRs, repos)
  - .claude/skills/api/jira/SKILL.md - Jira REST API (issues, sprints, boards)
  - .claude/skills/api/confluence/SKILL.md - Confluence REST API (pages, spaces, content)
  - .claude/skills/api/notion/SKILL.md - Notion REST API (pages, databases, blocks)
  - .claude/skills/api/slack/SKILL.md - Slack Web API (messaging, channels)
  - .claude/skills/api/google-calendar/SKILL.md - Google Calendar API (events, scheduling)
  - Skills use .credentials/*.json instead of .env.local for authentication
  - All skills organized under .claude/skills/api/ directory structure
  - Reason: MCP tools consumed excessive context tokens, skills provide lighter-weight alternative
- **[Personal KB Architecture]** Hybrid short/long-term memory model for personal context management
  - Short-term memory: Compact summary in CLAUDE.md (~50 tokens, always loaded)
  - Long-term memory: Detailed YAML in meta/ folder (accessed via neuron-knowledge skill on demand)
  - meta/projects.yaml: Project registry with priorities, status, deliverables
  - meta/team.yaml: Team structure, roles, contacts
  - neuron-knowledge skill extended to access meta/ folder for personal context queries
  - Memory architecture: CLAUDE.md → meta/ retrieval pattern for scalable context management
- **[knowledge/agents.md]** New file for detailed agent documentation (extracted from CLAUDE.md)
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

- **[CLAUDE.md]** Refactored for simplicity (215 → 154 lines)
  - Agent System section compressed to 10-line table, details moved to `knowledge/agents.md`
  - Added Session Protocol section for session lifecycle management
  - Removed duplicate content between Critical Rules and Agent System
- **[P16 Automate Repetition]** Expanded principle with Automation Hierarchy guidance
  - CLAUDE.md description updated: "Code for deterministic, AI for judgment. Context is expensive."
  - philosophy.md adds hierarchy table: Code layer (deterministic) vs AI layer (judgment)
  - Clarifies when to use code (hooks, scripts) vs AI (review, architecture)
  - Emphasizes AI context cost as decision factor
- **[MCP Revert]** Advisor agent routing reverted to skill-based approach
  - MCP Tool Routing section renamed back to Skill Enforcement
  - Routing table reverted: MCP tool prefixes → Skill names (github-api, jira-api, etc.)
  - Output format reverted: removed `mcp_tools` array, restored `required_skill`
  - Reason: MCP tools consumed excessive context, skills provide simpler interface
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

- **[MCP Example Config]** Removed .mcp.example.json template
  - No longer needed after reverting MCP migration
  - Skills provide simpler, context-efficient alternative to MCP tools
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

- **[Advisor Agent]** Output format reverted to skill-based routing (MCP changes rolled back)
  - Removed field: `mcp_tools` (array of MCP tool names)
  - Restored fields: `skill_required`, `required_skill`, `skill_reason`
  - Changed field: `skill_reason` (replaces `tool_reason`)
  - Consumers expecting MCP format must revert to skill-based schema
- **[arkraft-fe]** Design system color API changes
  - Components using removed ColorVariant values (`info`, `cyan`, `magenta`, `yellow`) must migrate to new variants
  - TitleColor props must use new values: `default`, `blue`, `green`, `amber`, `red`
  - CSS classes referencing `gray-*` should use `neutral-*`

---

*Auto-updated by reviewer agent on PR creation.*
