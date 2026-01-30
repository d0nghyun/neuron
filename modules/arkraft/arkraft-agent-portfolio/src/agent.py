"""Agent configuration."""

import os
from pathlib import Path

from claude_agent_sdk import ClaudeAgentOptions

WORKSPACE_DIR = Path(
    os.environ.get("WORKSPACE_PATH", Path(__file__).parent.parent / "workspace")
)


def get_agent_options(max_turns: int = 20) -> ClaudeAgentOptions:
    """Get Claude Agent options."""
    return ClaudeAgentOptions(
        cwd=str(WORKSPACE_DIR),
        permission_mode="bypassPermissions",
        max_turns=max_turns,
        setting_sources=["project"],
    )
