# Unreleased

> Changes pending for the next release

## Added

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

## Fixed

-

## Removed

- **[arkraft-fe]** Removed unused color variants from design system
  - ColorVariant: removed `info`, `cyan`, `magenta`, `yellow`
  - TitleColor: removed `orange`, `cyan`, `yellow`, `magenta`, `white`, `purple`
  - CSS color classes: removed `cyan-*`, `magenta-*` references

## Security

-

## Breaking Changes

- **[arkraft-fe]** Design system color API changes
  - Components using removed ColorVariant values (`info`, `cyan`, `magenta`, `yellow`) must migrate to new variants
  - TitleColor props must use new values: `default`, `blue`, `green`, `amber`, `red`
  - CSS classes referencing `gray-*` should use `neutral-*`

---

*Auto-updated by reviewer agent on PR creation.*
