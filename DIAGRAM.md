# Supervisor Decision Flow

Decision flowchart for the Neuron Supervisor. Every branch maps to documented
behavior in CLAUDE.md, ARCHITECTURE.md, RULES.md, or factory/README.md.

```mermaid
flowchart TD
    REQ([Request received]) --> HOOK[enforce-claude-md.sh fires<br/>intent-first reminder]
    HOOK --> ASSESS{Assess intent<br/>& complexity}

    %% --- Intent classification ---
    ASSESS -->|Trivial| DIRECT[DIRECT mode<br/>Supervisor handles inline]
    ASSESS -->|Moderate| COMPOSE_D[Compose for DELEGATE]
    ASSESS -->|Complex| COMPOSE_C[Compose for COLLABORATE]

    %% --- DIRECT path ---
    DIRECT --> RESPOND([Respond to user])

    %% --- DELEGATE compose ---
    COMPOSE_D --> CAP_D{Capability<br/>exists?}
    CAP_D -->|Agent/skill in .claude/| REUSE_D[Reuse existing component]
    CAP_D -->|In modules/ but inactive| ACTIVATE_D[ops-init-module<br/>activate via symlink]
    CAP_D -->|Not found| RECRUIT_D[system-recruiter<br/>create via factory pattern]
    REUSE_D --> DELEGATE
    ACTIVATE_D --> DELEGATE
    RECRUIT_D --> DELEGATE

    DELEGATE[DELEGATE<br/>Supervisor spawns subagent] --> WORK_D[Worker produces output]
    WORK_D --> REVIEW_D{Run system-reviewer<br/>audit output}
    REVIEW_D -->|Clean| RETRO_D{Moderate+ task?}
    REVIEW_D -->|Issues found| DECIDE_D{Supervisor decides}
    DECIDE_D -->|Revise| WORK_D
    DECIDE_D -->|Skip issue| RETRO_D
    DECIDE_D -->|Reject & escalate| ASK_USER([Ask user for guidance])
    RETRO_D -->|Yes| RETROSPECT_D[ops-retrospect<br/>review decision paths]
    RETRO_D -->|Trivial, skip| RECORD_D
    RETROSPECT_D --> RECORD_D[Record to vault/memory]
    RECORD_D --> RESPOND

    %% --- COLLABORATE compose ---
    COMPOSE_C --> CAP_C{Capability<br/>exists?}
    CAP_C -->|All components exist| REUSE_C[Reuse existing components]
    CAP_C -->|Module inactive| ACTIVATE_C[ops-init-module<br/>activate via symlink]
    CAP_C -->|Component missing| RECRUIT_C[system-recruiter<br/>create via factory pattern]
    REUSE_C --> TEAM
    ACTIVATE_C --> TEAM
    RECRUIT_C --> TEAM

    TEAM[Assemble team<br/>orchestrator + workers + reviewer] --> SPAWN{Task independence?}
    SPAWN -->|Independent tasks| PARALLEL[Spawn workers in parallel]
    SPAWN -->|Dependent tasks| SEQUENTIAL[Chain workers sequentially]
    PARALLEL --> WORKER_OUT[Workers produce output]
    SEQUENTIAL --> WORKER_OUT

    WORKER_OUT --> REVIEWER[system-reviewer<br/>audits output]
    REVIEWER -->|Issues found| ORCH_DECIDE{Orchestrator decides}
    REVIEWER -->|Clean review| CHECKPOINT
    ORCH_DECIDE -->|Fix| WORKER_OUT
    ORCH_DECIDE -->|Skip| CHECKPOINT
    ORCH_DECIDE -->|Reject| ASK_USER

    CHECKPOINT{Supervisor checkpoint<br/>approve / revise / reject}
    CHECKPOINT -->|Approve| RETRO_C[ops-retrospect<br/>review decision paths]
    CHECKPOINT -->|Revise| WORKER_OUT
    CHECKPOINT -->|Reject| ASK_USER

    RETRO_C --> RECORD_C[Record to vault/memory<br/>ops-daily-memo]
    RECORD_C --> RESPOND

    %% --- Recruiter sub-flow ---
    subgraph FACTORY [Factory Creation]
        direction TB
        F1[Read factory/pattern-*.md] --> F2{Component type?}
        F2 -->|Judgment/identity| F3[Create Agent<br/>pattern-agent.md]
        F2 -->|Tool how-to| F4[Create Skill<br/>pattern-skill.md]
        F2 -->|Multi-agent| F5[Create Team Blueprint<br/>pattern-team.md]
        F2 -->|Auto trigger| F6[Create Hook<br/>pattern-hook.md]
        F3 --> F7{Location?}
        F4 --> F7
        F5 --> F7
        F6 --> F7
        F7 -->|Cross-module| F8[neuron .claude/]
        F7 -->|Single module| F9[module .claude/]
    end

    RECRUIT_D -.-> FACTORY
    RECRUIT_C -.-> FACTORY

    ASK_USER --> ASSESS
```

## Branch Reference

| Decision Node | Source | Section |
|---------------|--------|---------|
| enforce-claude-md.sh fires | ARCHITECTURE.md | Hook Flow |
| Assess intent & complexity | CLAUDE.md | Intent-Based Approach |
| Trivial / Moderate / Complex | CLAUDE.md | Intent-Based Approach table |
| DIRECT mode | ARCHITECTURE.md | Execute Modes |
| DELEGATE mode | ARCHITECTURE.md | Execute Modes |
| COLLABORATE mode | ARCHITECTURE.md | Execute Modes |
| Capability exists? | ARCHITECTURE.md | Orchestration Pipeline |
| ops-init-module activate | ARCHITECTURE.md | Orchestration Pipeline, Module Lifecycle |
| system-recruiter create | ARCHITECTURE.md | When to Trigger Recruiter |
| Compose (skill/agent/team) | CLAUDE.md | Supervisor Responsibilities, step 2 |
| Reuse existing component | factory/README.md | Before Creating, step 2 |
| Spawn parallel vs sequential | ARCHITECTURE.md | Team Assembly |
| Workers produce output | ARCHITECTURE.md | Collaborate Flow, step 2 |
| system-reviewer audit | CLAUDE.md | Supervisor Responsibilities, step 4 |
| Reviewer reports only | ARCHITECTURE.md | Collaborate Flow, step 4 |
| Orchestrator decides fix/skip | ARCHITECTURE.md | Collaborate Flow, step 5-6 |
| Supervisor checkpoint | ARCHITECTURE.md | Orchestration Pipeline |
| ops-retrospect | CLAUDE.md | Supervisor Responsibilities, step 5 |
| Moderate+ trigger | ops-retrospect SKILL.md | When to Activate |
| Record to vault/memory | ARCHITECTURE.md | Orchestration Pipeline (ops-daily-memo) |
| Factory pattern selection | factory/README.md | Component Selection Guide, Decision Tree |
| Location decision | factory/README.md | Location Decision |
| Ask user for guidance | CLAUDE.md | Principles (Autonomy - ask what you cannot find) |
