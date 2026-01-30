"""Health check for Kubernetes liveness/readiness probes."""

import sys


def _check() -> int:
    """Check if agent is ready to run."""
    try:
        from claude_agent_sdk import query  # noqa: F401
        from .agent import get_agent_options  # noqa: F401

        return 0
    except Exception as e:
        print(f"Health check failed: {e}", file=sys.stderr)
        return 1


def ping():
    """CLI entry point."""
    sys.exit(_check())


if __name__ == "__main__":
    ping()
