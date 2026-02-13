# Arkraft Alpha Reviewer

## Overview

Post-alpha validation and Finter submission agent.

Bridges arkraft-agent-alpha (generates alpha.py) → Finter submission.

## Responsibilities

| Task | Description |
|------|-------------|
| Bias Detection | Check am.py for forward-looking bias |
| Issue Resolution | Fix detected problems |
| Finter Submission | Handle alpha submission workflow |
| Error Polling | Retry failed submissions |

## Commands

| Command | Purpose |
|---------|---------|
| `uv run arkraft-alpha-reviewer <alpha_dir>` | Review alpha |
| `uv run arkraft-alpha-reviewer <alpha_dir> -a fix` | Fix issues |
| `uv run arkraft-alpha-reviewer <alpha_dir> -a submit` | Submit to Finter |

## Example Usage

```bash
# Review alphas from arkraft-agent-alpha
uv run arkraft-alpha-reviewer ../arkraft-agent-alpha/workspace

# Fix detected issues
uv run arkraft-alpha-reviewer ../arkraft-agent-alpha/workspace -a fix

# Submit validated alphas
uv run arkraft-alpha-reviewer ../arkraft-agent-alpha/workspace -a submit
```

## Key Files

| Path | Purpose |
|------|---------|
| `src/main.py` | CLI entry point |
| `src/agent.py` | Agent configuration |
| `workspace/CLAUDE.md` | Agent instructions |
| `workspace/.mcp.json` | MCP server config |

## Architecture

```
arkraft-agent-alpha                arkraft-alpha-reviewer
(Phases 1-5)           →           (Review → Fix → Submit)

phase5/*_eval.json     →           review_result.json
phase4/{model}/am.py   →           submission_state.json
```
