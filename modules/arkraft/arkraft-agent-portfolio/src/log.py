"""JSON Lines logging configuration."""

import json
import logging
import sys
from datetime import UTC, datetime

_BUILTIN_ATTRS = {
    "name", "msg", "args", "created", "filename", "funcName", "levelname",
    "levelno", "lineno", "module", "msecs", "pathname", "process",
    "processName", "relativeCreated", "stack_info", "exc_info", "exc_text",
    "thread", "threadName", "taskName", "message",
}


class JSONFormatter(logging.Formatter):
    """JSON Lines formatter for K8s/ELK compatibility."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "ts": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
        }
        for key, val in record.__dict__.items():
            if key not in _BUILTIN_ATTRS:
                log_obj[key] = val
        msg = record.getMessage()
        if msg:
            log_obj["msg"] = msg
        return json.dumps(log_obj, ensure_ascii=False, default=str)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure JSON Lines logging for K8s/ELK."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logging.root.handlers = [handler]
    logging.root.setLevel(level)
