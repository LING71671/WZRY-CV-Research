"""Package-owned runtime orchestration entry."""

from __future__ import annotations

from importlib import import_module
from typing import Optional

from .bootstrap import bootstrap_runtime_environment


def _get_logger():
    logging_utils = import_module("utils.logging_utils")
    return getattr(logging_utils, "get_logger")(__name__)


def main(adb_device: Optional[str] = None) -> None:
    """Own the stable packaged runtime entry without resolving through shims."""
    bootstrap_runtime_environment()
    logger = _get_logger()

    config_module = import_module("config")
    resolved_device = adb_device
    if resolved_device is None:
        resolved_device = getattr(config_module, "ADB_DEVICE_SERIAL", None)

    logger.debug(
        "packaged app orchestration entry resolved",
        extra={"adb_device": resolved_device},
    )


__all__ = ["main"]
