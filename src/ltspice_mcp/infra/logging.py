# In the name of God, the Most Gracious, the Most Merciful
"""Structured log helpers for ltspice-mcp."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from os import PathLike

Logger = structlog.stdlib.BoundLogger

_LOG_FILE_NAME = "ltspice-mcp.log"
_LOG_FILE_MAX_BYTES = 5 * 1024 * 1024
_LOG_FILE_BACKUP_COUNT = 3


def _attach_file_handler(log_folder: Path, numeric_level: int) -> None:
    """Add a RotatingFileHandler under ``log_folder`` to the root logger."""

    log_folder.mkdir(parents=True, exist_ok=True)
    log_path = (log_folder / _LOG_FILE_NAME).resolve(strict=False)
    root_logger = logging.getLogger()
    for item in root_logger.handlers:
        if isinstance(item, RotatingFileHandler) and Path(item.baseFilename) == log_path:
            return
    handler = RotatingFileHandler(
        log_folder / _LOG_FILE_NAME,
        maxBytes=_LOG_FILE_MAX_BYTES,
        backupCount=_LOG_FILE_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setLevel(numeric_level)
    handler.setFormatter(logging.Formatter("%(message)s"))
    root_logger.addHandler(handler)


def configure_logging(
    level: str = "info", *, log_folder: str | PathLike[str] | None = None
) -> None:
    """Configure the stdlib log and structlog once per process."""

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, format="%(message)s")
    if log_folder is not None:
        _attach_file_handler(Path(log_folder), numeric_level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(**context: object) -> Logger:
    """Return a bound logger for ltspice-mcp."""

    logger: Logger = structlog.get_logger("ltspice_mcp")
    if context:
        bound_logger: Logger = logger.bind(**context)
        return bound_logger
    return logger
