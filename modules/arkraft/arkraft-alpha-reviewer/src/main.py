"""CLI entry point for Alpha Reviewer Agent."""

import argparse
import asyncio
import json
import logging
from pathlib import Path

from claude_agent_sdk import query

from .agent import WORKSPACE_DIR, get_agent_options

logger = logging.getLogger(__name__)


def setup_logging():
    """Setup JSON logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", %(message)s}',
    )


async def run_reviewer(
    alpha_dir: str,
    action: str = "review",
    max_turns: int = 30,
) -> dict:
    """Run alpha reviewer agent.

    Args:
        alpha_dir: Path to alpha output directory (e.g., arkraft-agent-alpha/workspace)
        action: review | submit | fix
        max_turns: Maximum agent turns

    Returns:
        Result dict with status and details
    """
    alpha_path = Path(alpha_dir)

    # Find eval files
    phase5_dir = alpha_path / "phase5"
    if not phase5_dir.exists():
        return {"success": False, "error": f"phase5 directory not found: {phase5_dir}"}

    eval_files = list(phase5_dir.glob("*_eval.json"))
    if not eval_files:
        return {"success": False, "error": "No eval.json files found in phase5/"}

    prompt = f"""## Alpha Review Request

**Action:** {action}
**Alpha Directory:** {alpha_path}
**Eval Files:** {[f.name for f in eval_files]}

## Instructions

Based on the action requested:

### If action=review:
1. Read all *_eval.json files in phase5/
2. For each alpha with outcome=DEPLOYED:
   - Check phase4/{model_name}/am.py for forward-looking bias
   - Validate train/test split implementation
   - Check for data leakage patterns
3. Report findings with verdict: PASS | BIAS_DETECTED | NEEDS_FIX

### If action=fix:
1. Read bias detection report
2. Fix identified issues in am.py
3. Re-run validation
4. Save corrected alpha to phase4_fixed/

### If action=submit:
1. Verify alpha passed review (no bias detected)
2. Call Finter submit API
3. Track submission state
4. Report submission result

## Output

Save results to workspace/review_result.json:
```json
{{
  "action": "{action}",
  "alphas_reviewed": [],
  "verdict": "PASS|BIAS_DETECTED|SUBMITTED|FAILED",
  "details": {{}}
}}
```
"""

    logger.info(f'{{"event": "reviewer.start", "action": "{action}", "alpha_dir": "{alpha_dir}"}}')

    options = get_agent_options(max_turns)
    result_text = ""

    try:
        async for message in query(prompt=prompt, options=options):
            if hasattr(message, "content"):
                for block in message.content:
                    if hasattr(block, "text"):
                        result_text = block.text
    except Exception as e:
        logger.error(f'{{"event": "reviewer.failed", "error": "{e}"}}')
        return {"success": False, "error": str(e)}

    # Load result file if created
    result_path = WORKSPACE_DIR / "review_result.json"
    if result_path.exists():
        with open(result_path) as f:
            return {"success": True, **json.load(f)}

    return {"success": True, "raw_response": result_text}


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Review and submit alpha strategies")
    parser.add_argument(
        "alpha_dir",
        help="Path to alpha output directory (arkraft-agent-alpha/workspace)",
    )
    parser.add_argument(
        "-a", "--action",
        choices=["review", "fix", "submit"],
        default="review",
        help="Action to perform",
    )
    parser.add_argument(
        "-t", "--max-turns",
        type=int,
        default=30,
        help="Max agent turns",
    )
    args = parser.parse_args()

    setup_logging()
    result = asyncio.run(run_reviewer(args.alpha_dir, args.action, args.max_turns))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
