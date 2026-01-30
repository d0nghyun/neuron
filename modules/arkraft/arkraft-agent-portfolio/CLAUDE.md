# Arkraft Portfolio Agent

## Overview

Claude Agent wrapper for portfolio construction and optimization.

Key responsibilities:
- Fetch alpha/portfolio data from alpha-pool API
- AI-assisted portfolio construction from curated alphas
- Weight optimization and risk analysis
- Output structured portfolio.json

## Commands

| Command | Purpose |
|---------|---------|
| `uv run arkraft-portfolio "request"` | Run agent |
| `./run.sh web` | Start web UI (localhost:8001) |

## Key Files

| Path | Purpose |
|------|---------|
| `src/agent.py` | Claude Agent options |
| `src/main.py` | CLI entry point |
| `workspace/` | Agent execution environment |
| `workspace/CLAUDE.md` | Agent instructions |
| `workspace/.mcp.json` | MCP server config |
