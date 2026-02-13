"""Agent configuration for Alpha Reviewer."""

from pathlib import Path

from claude_agent_sdk import AgentOptions

WORKSPACE_DIR = Path(__file__).parent.parent / "workspace"


def get_agent_options(max_turns: int = 30) -> AgentOptions:
    """Get agent options for Alpha Reviewer."""
    return AgentOptions(
        model="claude-sonnet-4-20250514",
        max_turns=max_turns,
        cwd=str(WORKSPACE_DIR),
        mcp_config=str(WORKSPACE_DIR / ".mcp.json"),
        system_prompt_file=str(WORKSPACE_DIR / "CLAUDE.md"),
        permission_mode="acceptEdits",
        permission_prompt_tool_allowlist=["Bash", "Task"],
    )
