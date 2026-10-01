"""
logger.py
---------
Central logging configuration for the whole project.

Usage:
    from logger import get_logger
    log = get_logger(__name__)
    log.info("message")
"""

import os
import logging

LOG_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "06_Logs")
)
LOG_FILE = os.path.join(LOG_DIR, "application.log")

os.makedirs(LOG_DIR, exist_ok=True)

_CONFIGURED = False


def _configure_root() -> None:
    """Configure the root logger once for the whole application."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filemode="a",
    )

    # Also log to console (useful for notebooks)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(levelname)-7s | %(name)s | %(message)s"
    ))
    logging.getLogger().addHandler(console)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name."""
    _configure_root()
    return logging.getLogger(name)