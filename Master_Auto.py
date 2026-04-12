# pyright: reportMissingImports=false
from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
SRC_ROOT = REPO_ROOT / "src"

src_root_str = str(SRC_ROOT)
if src_root_str not in sys.path:
    sys.path.insert(0, src_root_str)

from wzry_ai.app.main import main as _packaged_main


def main(adb_device=None):
    return _packaged_main(adb_device=adb_device)


if __name__ == "__main__":
    from wzry_ai.config import ADB_DEVICE_SERIAL

    main(adb_device=ADB_DEVICE_SERIAL)
