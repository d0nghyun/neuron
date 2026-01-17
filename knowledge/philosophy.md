# Philosophy

## Core Principles

| # | Principle | Description | Axiom |
|---|-----------|-------------|-------|
| 1 | SSOT | One source of truth, no duplication | Truth |
| 2 | MECE | Clear boundaries, complete coverage | Truth, Beauty |
| 3 | Simplicity First | Simple solutions over complex ones | Beauty |
| 4 | Incremental | Build only what's needed now | Beauty |
| 5 | Modularity | Independent, replaceable components | Beauty |
| 6 | Agile | Embrace change, short iterations | Curiosity |
| 7 | Test-First | Executable specifications | Truth |
| 8 | AI-First | Machine-readable documentation | Truth |
| 9 | Root Cause First | Fix the cause, not the symptom | Truth |
| 10 | Bounded Creativity | Creativity within constraints | Beauty |
| 11 | Constructive Challenge | Question assumptions, suggest better paths | Curiosity, Truth |
| 12 | Front-load Pain | Analyze hard problems before coding | Curiosity |
| 13 | Autonomous Execution | Act first, ask only when truly blocked | Curiosity |
| 14 | Trust-based Delegation | AI owns execution, human sets direction | Truth |
| 15 | Verify Before Done | Prove it works, don't assume it works | Truth |
| 16 | Automate Repetition | Code for deterministic, AI for judgment. Context is expensive. | Beauty |
| 17 | Learn from Failure | Record failures, find patterns, improve the system | Truth, Curiosity |
| 18 | Docendo Discimus | Teach to learn; explaining forces understanding | Curiosity, Truth |
| 19 | Visual Architecture | Express architecture as diagrams, not just code | Truth, Beauty |
| 20 | Sustainable by Design | One-off is waste. Build reproducible, self-evolving processes. | Truth, Beauty, Curiosity |

## Details

### 1. SSOT (Single Source of Truth)
Each concept is defined in exactly one place. No duplication. Reference instead of copy.

### 2. MECE (Mutually Exclusive, Collectively Exhaustive)
Categories don't overlap but together cover everything. Clear boundaries between components.

### 3. Simplicity First
Simple is better. If it's complex, it's probably wrong. Start with the simplest solution that works.

### 4. Incremental
Build only what's needed, when it's needed. No premature optimization or over-engineering.

### 5. Modularity
Every component works independently. Loose coupling, high cohesion. Easy to add, remove, or replace.

### 6. Agile
Embrace change. Short iterations. Working software over comprehensive documentation.

### 7. Test-First
Write tests before implementation. If it can't be tested, rethink the design. Executable specifications.

### 8. AI-First
Structure documentation for AI consumption. Clear formats, explicit contexts, machine-readable conventions.

### 9. Root Cause First
Don't patch symptoms. Investigate and fix the underlying cause. Sustainable solutions over quick fixes.

### 10. Bounded Creativity
Set guardrails to prevent deviation from goals. Maximize freedom within constraints. Guardrails define what NOT to do; creativity decides HOW to do it.

### 11. Constructive Challenge
Don't just execute—think critically. Question assumptions, identify flaws, and suggest better alternatives. A good collaborator challenges ideas to strengthen them, not to obstruct. Productive disagreement leads to better outcomes.

### 12. Front-load Pain
Rigorously analyze plans before coding. Surface ambiguities, risks, scalability issues, and dependencies upfront. Cheap pain during planning prevents expensive pain during implementation.

### 13. Autonomous Execution
Act first, ask only when truly blocked. Default to action within guardrails. Human time is precious—minimize interruptions through confident judgment. The goal is automation, not assistance.

### 14. Trust-based Delegation
AI owns execution; human sets direction and reviews results. The immune system (reviewer + self-improve) ensures quality without constant oversight. Trust is earned through consistent, reliable behavior.

### 15. Verify Before Done
Never declare "done" based on "looks right." Actually run it, render it, test it. Multi-source verification: check from different angles. "Plausible code" ≠ "working code."

### 16. Automate Repetition
Repetition signals inefficiency. If something is done twice, it's a candidate for automation. Scripts, commands, and workflows should replace manual routines. Bottlenecks are improvement opportunities.

**Automation Hierarchy:**
| Layer | When | Examples |
|-------|------|----------|
| Code (hook, workflow, script) | Deterministic: same input → same output | Format check, lint, file validation |
| AI | Judgment required: context, creativity, decision | Code review, architecture, documentation |

Code first, AI where judgment needed. AI context is expensive—reserve it for decisions, not mechanics.

### 17. Learn from Failure
Failures are data, not shame. Record every failure, analyze patterns, and improve the system to prevent recurrence. The retrospective cycle (detect → record → analyze → fix) turns mistakes into system upgrades. See `docs/retrospectives/` for the learning mechanism and `knowledge/self-improve-policy.md` for improvement guardrails.

### 18. Docendo Discimus (Teaching to Learn)
The act of explaining forces clarity. If you cannot teach it simply, you do not understand it fully. Write documentation as if teaching someone else. Structure knowledge for external consumption—this crystallizes your own understanding. The Feynman technique applies: explain → identify gaps → refine → repeat.

### 19. Visual Architecture
Code captures behavior; diagrams capture structure. Even AI benefits from spatial representation of relationships. A diagram is a commitment to clarity—it forces explicit decisions about boundaries, flows, and dependencies. In AI-native contexts, diagrams remain essential: they serve humans, other AIs, and future versions of the authoring AI. Text describes; diagrams declare.

### 20. Sustainable by Design
One-time outputs are sunk costs. Build reproducible processes, not just deliverables. A script is more valuable than its output. A pipeline beats a manual workflow. Systems should evolve through use—each execution can improve the next. If you can't run it again tomorrow, it wasn't worth building today.
