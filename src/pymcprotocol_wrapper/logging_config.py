"""Logging configuration helper for pymcprotocol_wrapper.

Provides a simple function to configure the package logger used by
`utils.log_message` and other components.
"""

from __future__ import annotations

import logging
from typing import Optional


def configure_logging(level: int = logging.INFO, handler: Optional[logging.Handler] = None, fmt: Optional[str] = None) -> None:
    """Configure the `pymcprotocol_wrapper` logger.

    Args:
        level: Root log level for the package logger (default: `logging.INFO`).
        handler: Optional `logging.Handler` to attach. If `None`, a
            `StreamHandler` to stderr is created.
        fmt: Optional format string for the handler. If not provided a
            sensible default is used.

    This function clears any existing handlers on the `pymcprotocol_wrapper`
    logger to avoid duplicated log messages when called multiple times.
    """
    logger = logging.getLogger("pymcprotocol_wrapper")
    logger.setLevel(level)

    if fmt is None:
        fmt = "%(asctime)s %(name)s %(levelname)s: %(message)s"

    if handler is None:
        handler = logging.StreamHandler()

    # Prevent duplicated handlers on repeated calls by clearing existing ones.
    if logger.handlers:
        logger.handlers.clear()

    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)


def configure_debug_console() -> None:
    """Convenience helper that sets debug level and a simple console handler."""
    configure_logging(level=logging.DEBUG)
