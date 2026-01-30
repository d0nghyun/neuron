"""Message stream handler for Claude Agent SDK."""

import logging
from dataclasses import dataclass

from claude_agent_sdk import (
    AssistantMessage,
    ResultMessage,
    SystemMessage,
    TextBlock,
    ThinkingBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
)

logger = logging.getLogger(__name__)


@dataclass
class StreamResult:
    """Result from processing message stream."""

    result_text: str = ""
    total_cost: float = 0.0
    num_turns: int = 0
    is_error: bool = False


class MessageHandler:
    """Handles Claude Agent SDK message stream with logging."""

    def __init__(self) -> None:
        self._active_subagents: dict[str, dict] = {}
        self._result_text = ""
        self._total_cost = 0.0
        self._num_turns = 0
        self._is_error = False

    def _get_agent_context(self, parent_id: str | None) -> dict:
        """Get agent context for logging."""
        if parent_id and parent_id in self._active_subagents:
            info = self._active_subagents[parent_id]
            return {"agent": info.get("name", info.get("type")), "agent_id": parent_id}
        return {"agent": "main"}

    def handle(self, message) -> None:
        """Process a single message from the stream."""
        parent_id = getattr(message, "parent_tool_use_id", None)
        ctx = self._get_agent_context(parent_id)

        if isinstance(message, AssistantMessage):
            self._handle_assistant(message, ctx)
        elif isinstance(message, UserMessage):
            self._handle_user(message, ctx)
        elif isinstance(message, SystemMessage):
            self._handle_system(message, ctx)
        elif isinstance(message, ResultMessage):
            self._handle_result(message, ctx)

    def _handle_assistant(self, message: AssistantMessage, ctx: dict) -> None:
        if message.error:
            logger.warning("", extra={
                "event": "assistant.error", "error": message.error, **ctx
            })

        for block in message.content:
            if isinstance(block, TextBlock) and block.text:
                self._result_text = block.text
                logger.info("", extra={
                    "event": "agent.message", "text": block.text[:500], **ctx
                })
            elif isinstance(block, ThinkingBlock) and block.thinking:
                logger.debug("", extra={
                    "event": "thinking", "content": block.thinking[:500], **ctx
                })
            elif isinstance(block, ToolUseBlock):
                self._handle_tool_use(block, ctx)

    def _handle_tool_use(self, block: ToolUseBlock, ctx: dict) -> None:
        tool_input = block.input or {}

        if block.name == "Task":
            subagent_type = tool_input.get("subagent_type", "unknown")
            self._active_subagents[block.id] = {
                "type": subagent_type,
                "name": tool_input.get("description", subagent_type),
            }
            logger.info("", extra={
                "event": "subagent.start",
                "subagent": subagent_type,
                "subagent_id": block.id,
                **ctx,
            })
        else:
            logger.info("", extra={
                "event": "tool.call",
                "tool": block.name,
                "tool_id": block.id,
                **ctx,
            })

    def _handle_user(self, message: UserMessage, ctx: dict) -> None:
        if not isinstance(message.content, list):
            return

        for block in message.content:
            if isinstance(block, ToolResultBlock):
                if block.tool_use_id in self._active_subagents:
                    info = self._active_subagents.pop(block.tool_use_id)
                    logger.info("", extra={
                        "event": "subagent.end",
                        "subagent": info.get("type"),
                        "subagent_id": block.tool_use_id,
                        **ctx,
                    })

    def _handle_system(self, message: SystemMessage, ctx: dict) -> None:
        logger.debug("", extra={
            "event": "system",
            "subtype": message.subtype,
            **ctx,
        })

    def _handle_result(self, message: ResultMessage, ctx: dict) -> None:
        self._total_cost = message.total_cost_usd or 0
        self._num_turns = message.num_turns or 0
        self._is_error = message.is_error or False

        log_fn = logger.error if self._is_error else logger.info
        log_fn("", extra={
            "event": "agent.error" if self._is_error else "agent.done",
            "turns": self._num_turns,
            "cost": self._total_cost,
            **ctx,
        })

    def get_result(self) -> StreamResult:
        """Get the final result after processing all messages."""
        return StreamResult(
            result_text=self._result_text,
            total_cost=self._total_cost,
            num_turns=self._num_turns,
            is_error=self._is_error,
        )
