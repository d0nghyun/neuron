# Neuron

> Central nervous system for personal projects

## What is Neuron?

Neuron is the **hub repository** that orchestrates all personal projects. Like a brain's neuron network, it connects and coordinates different components through a modular submodule architecture.

**Core Functions:**
- Central policy and philosophy management
- Submodule-based project orchestration
- Shared knowledge and conventions
- MCP tools and skills registry
- Personal task and document management

When a new capability is needed (database, web service, etc.), a new repository is created and registered as a submodule here.

## Philosophy

See [CLAUDE.md](CLAUDE.md) for core principles.

## Documentation

| File | Audience | Purpose |
|------|----------|---------|
| `README.md` | Human | Project overview and usage guide |
| `RULES.md` | AI Agent | Enforcement rules for all components |
| `ARCHITECTURE.md` | Both | System map, flows, and file pointers |
| `CLAUDE.md` | AI Agent | Entry point, conventions, and context |
| `docs/diagram.md` | Human | Visual system architecture |

## Structure

See [docs/diagram.md](docs/diagram.md) for directory structure.

## How It Works

### Adding a New Project

```bash
# 1. Create new repository
cd ~/Git/personal
git init new-project

# 2. Register as submodule in neuron
cd neuron
git submodule add ../new-project modules/new-project
git commit -m "Add new-project submodule"
```

### Updating Submodules

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Update specific submodule
git submodule update --remote modules/specific-project
```

### Working with Submodules

```bash
# Clone neuron with all submodules
git clone --recurse-submodules <neuron-url>

# Initialize submodules after clone
git submodule init
git submodule update
```

## Getting Started

```bash
# Clone the repository
git clone <neuron-url>
cd neuron

# Initialize submodules
git submodule init
git submodule update

# Ready to use
```

---

*Built with simplicity, designed for growth.*
