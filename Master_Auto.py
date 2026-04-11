# pyright: reportMissingImports=false
from __future__ import annotations

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent
SRC_ROOT = REPO_ROOT / "src"

for candidate in (SRC_ROOT, REPO_ROOT):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from config import ADB_DEVICE_SERIAL
from wzry_ai.app.main import main as _packaged_main


def main(adb_device=None):
    return _packaged_main(adb_device=adb_device)


if __name__ == "__main__":
    main(adb_device=ADB_DEVICE_SERIAL)
