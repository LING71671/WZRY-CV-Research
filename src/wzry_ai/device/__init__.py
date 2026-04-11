"""设备通信模块 - ADB、Scrcpy、模拟器管理"""

from wzry_ai.device.ADBTool import ADBTool, tap, swipe
from wzry_ai.device.ScrcpyTool import ScrcpyTool
from wzry_ai.device.emulator_manager import (
    EmulatorManager,
    EmulatorPortFinder,
    EmulatorWindowFinder,
    MuMuConfigManager,
    MuMuConfig,
    ADBPathFinder,
    get_adb_path,
    init_emulator,
    init_mumu,
    HAS_WIN32,
)

__all__ = [
    # ADB工具
    'ADBTool',
    'tap',
    'swipe',
    # Scrcpy工具
    'ScrcpyTool',
    # 模拟器管理
    'EmulatorManager',
    'EmulatorPortFinder',
    'EmulatorWindowFinder',
    'MuMuConfigManager',
    'MuMuConfig',
    'ADBPathFinder',
    'get_adb_path',
    'init_emulator',
    'init_mumu',
    'HAS_WIN32',
]
