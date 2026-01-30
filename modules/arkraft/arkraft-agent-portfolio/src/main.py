"""CLI entry point."""

import argparse
import asyncio
import json
import logging

from claude_agent_sdk import query

from .agent import WORKSPACE_DIR, get_agent_options
from .handler import MessageHandler
from .log import setup_logging

logger = logging.getLogger(__name__)


def _ensure_output_dir():
    """Ensure output directory exists before agent runs."""
    output_dir = WORKSPACE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


async def run_portfolio_agent(
    request: str = "",
    max_turns: int = 20,
) -> dict:
    """Run portfolio agent."""
    _ensure_output_dir()

    prompt = f"""## Portfolio Request

**User Request:** {request or "Build optimal portfolio"}
**OUTPUT_DIR:** {WORKSPACE_DIR}

## Instructions

1. Fetch alpha pool data via MCP
2. Analyze alphas for portfolio construction
3. Generate portfolio weights and rationale
4. Save results to {{OUTPUT_DIR}}/output/portfolio.json
"""

    logger.info("", extra={
        "event": "agent.start",
        "request": request or "Default",
        "max_turns": max_turns,
        "workspace": str(WORKSPACE_DIR),
    })

    handler = MessageHandler()
    options = get_agent_options(max_turns)

    try:
        async for message in query(prompt=prompt, options=options):
            handler.handle(message)
    except Exception as e:
        logger.error(
            "", extra={"event": "agent.failed", "error": str(e)}, exc_info=True
        )
        result = handler.get_result()
        return {
            "success": False,
            "error": str(e),
            "cost": result.total_cost,
            "turns": result.num_turns,
        }

    result = handler.get_result()
    portfolio = _load_portfolio(result.result_text)

    if portfolio:
        logger.info("", extra={
            "event": "result.success",
            "alpha_count": len(portfolio.get("alphas", [])),
        })
        return {
            "success": True,
            "portfolio": portfolio,
            "cost": result.total_cost,
            "turns": result.num_turns,
        }

    logger.error("", extra={
        "event": "result.failed",
        "response_preview": result.result_text[:500],
    })
    return {
        "success": False,
        "raw_response": result.result_text,
        "cost": result.total_cost,
        "turns": result.num_turns,
        "error": "Failed to generate portfolio",
    }


def _load_portfolio(fallback_text: str) -> dict | None:
    """Load portfolio from file or extract from response text."""
    portfolio_path = WORKSPACE_DIR / "output" / "portfolio.json"

    if portfolio_path.exists():
        try:
            with open(portfolio_path) as f:
                portfolio = json.load(f)
            logger.info("", extra={
                "event": "file.loaded",
                "path": str(portfolio_path),
                "bytes": portfolio_path.stat().st_size,
            })
            return portfolio
        except Exception as e:
            logger.warning("", extra={
                "event": "file.error",
                "path": str(portfolio_path),
                "error": str(e),
            })
    else:
        logger.warning(
            "", extra={"event": "file.not_found", "path": str(portfolio_path)}
        )

    # Fallback: extract JSON from response
    start = fallback_text.find("{")
    end = fallback_text.rfind("}") + 1
    if start < 0 or end <= start:
        return None

    try:
        portfolio = json.loads(fallback_text[start:end])
        logger.info("", extra={"event": "fallback.success", "bytes": end - start})
        return portfolio
    except json.JSONDecodeError as e:
        logger.warning("", extra={"event": "fallback.failed", "error": str(e)})
        return None


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate portfolio")
    parser.add_argument("request", nargs="?", default="", help="Portfolio request")
    parser.add_argument(
        "-t", "--max-turns", type=int, default=20,
        help="Max agent turns (default: 20)",
    )
    args = parser.parse_args()

    setup_logging()

    result = asyncio.run(run_portfolio_agent(args.request, args.max_turns))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
