"""FastAPI web server for dev UI."""

import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .log import setup_logging
from .main import run_portfolio_agent

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Arkraft Portfolio Agent - Dev UI")

STATIC_DIR = Path(__file__).parent.parent / "static"


class GenerateRequest(BaseModel):
    request: str = ""
    max_turns: int = 20


@app.get("/")
async def index():
    """Serve index.html."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/generate")
async def generate(req: GenerateRequest) -> dict[str, Any]:
    """Run portfolio agent and return results."""
    logger.info(
        "",
        extra={
            "event": "web.generate.start",
            "request": req.request,
            "max_turns": req.max_turns,
        },
    )

    result = await run_portfolio_agent(
        request=req.request,
        max_turns=req.max_turns,
    )

    logger.info(
        "",
        extra={
            "event": "web.generate.complete",
            "success": result.get("success"),
            "cost": result.get("cost"),
        },
    )

    return result


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
