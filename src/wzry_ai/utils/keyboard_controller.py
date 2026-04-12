"""
Windows API 键盘控制器

功能说明：
    使用 Windows API PostMessage 向模拟器窗口发送键盘消息
    用于控制英雄移动、释放技能、使用辅助装等游戏操作

注意事项：
    需要模拟器窗口在前台或支持后台消息接收才能正常工作
"""

# 导入ctypes库，用于调用Windows系统底层的API函数
import ctypes

# 从ctypes导入wintypes和windll，用于Windows数据类型和DLL调用
from ctypes import wintypes, windll

# 导入win32con模块，包含Windows常量定义（如WM_KEYDOWN等消息类型）
import win32con

# 导入win32gui模块，用于Windows GUI操作（如查找窗口）
import win32gui

# 导入win32api模块，用于Windows API调用
import win32api

# 导入random模块，用于生成随机数（模拟人类操作的随机延迟）
import random

# 导入time模块，用于添加时间延迟
import time
from typing import Optional

# 从配置导入窗口名称（如果配置中有定义）
try:
    # 尝试从config模块读取WINDOW_NAME作为默认窗口名
    from wzry_ai import config as _config_module

    _configured_window_name = getattr(_config_module, "WINDOW_NAME", None)
    DEFAULT_WINDOW_NAME = (
        _configured_window_name
        if isinstance(_configured_window_name, str)
        else "MuMu安卓设备"
    )
except ImportError:
    # 如果导入失败（config模块不存在或没有WINDOW_NAME），使用默认值
    DEFAULT_WINDOW_NAME = "MuMu安卓设备"

# 尝试从 emulator_manager 导入窗口查找器
EmulatorWindowFinder = None
HAS_WIN32 = False
try:
    from wzry_ai.device.emulator_manager import EmulatorWindowFinder, HAS_WIN32

    HAS_EMULATOR_FINDER = HAS_WIN32
except ImportError:
    HAS_EMULATOR_FINDER = False

# 从logging_utils导入日志工具
from wzry_ai.utils.logging_utils import get_logger

# 获取当前模块的日志记录器
logger = get_logger(__name__)


class KeyboardController:
    """
    键盘控制器类

    功能说明：
        使用Windows API PostMessage向模拟器窗口发送键盘消息
        支持按键按下、释放、点击等操作
    """

    # 虚拟键码映射表
    # 将字符按键映射到Windows虚拟键码（VK Code）
    # 虚拟键码是Windows系统用于标识按键的数字代码
    VK_CODES = {
        "w": 0x57,
        "a": 0x41,
        "s": 0x53,
        "d": 0x44,  # 方向键WASD
        "q": 0x51,
        "e": 0x45,
        "r": 0x52,
        "t": 0x54,  # 技能键QERT
        "f": 0x46,
        "c": 0x43,
        "u": 0x55,
        "b": 0x42,  # 功能键FCUB
        "1": 0x31,
        "2": 0x32,
        "3": 0x33,
        "4": 0x34,  # 数字键1-4
        "space": 0x20,  # 空格键
    }

    # 扩展键标记集合
    # 这些键在发送消息时需要设置扩展标志位
    EXTENDED_KEYS = {
        "up",
        "down",
        "left",
        "right",
        "home",
        "end",
        "prior",
        "next",
        "insert",
        "delete",
    }

    def __init__(self, window_name: Optional[str] = None, hwnd: Optional[int] = None):
        """
        初始化键盘控制器

        功能说明：
            查找目标窗口并建立连接，准备发送键盘消息
            优先查找渲染子窗口（class name 包含 "subWin" 或 "NativeWindow"），
            如果找不到则使用顶层窗口

        参数说明：
            window_name: 目标窗口名称，如果为None则使用默认配置中的窗口名
            hwnd: 直接指定窗口句柄（优先使用），如果提供则跳过窗口查找
        """
        # 如果直接提供了窗口句柄，直接使用
        if hwnd is not None and hwnd != 0:
            self._hwnd = hwnd
            self.window_name = window_name or "Unknown"
            logger.info(f"使用指定窗口句柄: {self._hwnd}")
            return

        # 设置窗口名称，优先使用传入的参数，否则使用默认值
        self.window_name = window_name or DEFAULT_WINDOW_NAME

        # 尝试使用 EmulatorWindowFinder 查找窗口（支持进程名/类名匹配）
        top_hwnd = 0
        if HAS_EMULATOR_FINDER and EmulatorWindowFinder is not None:
            try:
                finder = EmulatorWindowFinder()
                # 尝试查找窗口（不检查分辨率，因为我们只需要发送消息）
                hwnd_found, title_found, rect_found, emu_type = finder.find_window(
                    check_resolution=False
                )
                top_hwnd = hwnd_found
                if title_found:
                    self.window_name = title_found
                logger.info(
                    f"通过 EmulatorWindowFinder 找到窗口: '{title_found}' (HWND: {top_hwnd})"
                )
            except Exception as e:
                logger.warning(f"EmulatorWindowFinder 查找失败: {e}，回退到标题查找")
                top_hwnd = 0

        # 如果 finder 没有找到，使用传统标题查找
        if top_hwnd == 0:
            top_hwnd = win32gui.FindWindow(None, self.window_name)
            if top_hwnd == 0:
                # 抛出运行时错误，提示用户检查窗口名称
                raise RuntimeError(f"找不到窗口: {self.window_name}")

        # 尝试查找渲染子窗口
        render_hwnd = self._find_render_child_window(top_hwnd)

        if render_hwnd:
            self._hwnd = render_hwnd
            self._render_hwnd = render_hwnd
            logger.info(f"已连接到渲染子窗口: {self.window_name} (HWND: {self._hwnd})")
        else:
            # 降级使用顶层窗口
            self._hwnd = top_hwnd
            self._render_hwnd = None
            logger.info(f"已连接到顶层窗口: {self.window_name} (HWND: {self._hwnd})")

        # 记录初始化成功信息
        logger.info(
            f"KeyboardController 初始化完成: hwnd={self._hwnd}, 渲染子窗口={self._render_hwnd}"
        )

    def _find_render_child_window(self, parent_hwnd: int) -> Optional[int]:
        """
        查找渲染子窗口

        功能说明：
            使用EnumChildWindows枚举父窗口的所有子窗口，
            查找class name包含"subWin"、"NativeWindow"或MuMu特有的Qt窗口类的渲染窗口

        参数说明：
            parent_hwnd: 父窗口句柄

        返回：
            渲染子窗口句柄，如果找不到则返回None
        """
        child_windows = []

        def enum_child_callback(hwnd, extra):
            """枚举子窗口回调函数"""
            try:
                class_name = win32gui.GetClassName(hwnd)
                child_windows.append((hwnd, class_name))
            except Exception:
                pass
            return True

        # 枚举所有子窗口
        try:
            win32gui.EnumChildWindows(parent_hwnd, enum_child_callback, None)
        except Exception as e:
            logger.warning(f"枚举子窗口时出错: {e}")
            return None

        # 查找渲染子窗口（支持多种class name模式）
        RENDER_CLASS_PATTERNS = [
            "subwin",  # 通用子窗口
            "nativewindow",  # 原生窗口
            "qt5156qwindowicon",  # MuMu 12 Qt5.15 渲染窗口
            "qt5154qwindowicon",  # MuMu Qt5.15.4 渲染窗口
            "qt6qwindowicon",  # MuMu Qt6 渲染窗口
            "qt5qwindowicon",  # MuMu Qt5 渲染窗口
            "nemuwin",  # MuMu 渲染窗口
            "mumurender",  # MuMu 渲染窗口
        ]

        for hwnd, class_name in child_windows:
            class_name_lower = class_name.lower()
            for pattern in RENDER_CLASS_PATTERNS:
                if pattern in class_name_lower:
                    logger.debug(f"找到渲染子窗口: {class_name} (HWND: {hwnd})")
                    return hwnd

        # 没有找到渲染子窗口，尝试使用最大可见子窗口策略
        if child_windows:
            logger.debug(f"未找到匹配的渲染子窗口，尝试使用最大可见子窗口策略")
            largest_visible = self._find_largest_visible_child(parent_hwnd)
            if largest_visible:
                return largest_visible

        logger.debug(
            f"未找到渲染子窗口，找到的子窗口: {[(hwnd, cls) for hwnd, cls in child_windows]}"
        )
        return None

    def _find_largest_visible_child(self, parent_hwnd: int) -> Optional[int]:
        """
        查找最大的可见子窗口

        功能说明：
            当无法通过class name匹配渲染窗口时，选择面积最大的可见子窗口

        参数说明：
            parent_hwnd: 父窗口句柄

        返回：
            最大可见子窗口句柄，如果找不到则返回None
        """
        largest_hwnd = None
        largest_area = 0

        def enum_callback(hwnd, extra):
            nonlocal largest_hwnd, largest_area
            try:
                if win32gui.IsWindowVisible(hwnd):
                    rect = win32gui.GetWindowRect(hwnd)
                    width = rect[2] - rect[0]
                    height = rect[3] - rect[1]
                    area = width * height
                    if area > largest_area:
                        largest_area = area
                        largest_hwnd = hwnd
            except Exception:
                pass
            return True

        try:
            win32gui.EnumChildWindows(parent_hwnd, enum_callback, None)
        except Exception as e:
            logger.warning(f"枚举子窗口查找最大可见窗口时出错: {e}")

        if largest_hwnd:
            class_name = win32gui.GetClassName(largest_hwnd)
            logger.debug(
                f"选择最大可见子窗口: {class_name} (HWND: {largest_hwnd}, area: {largest_area})"
            )

        return largest_hwnd

    def _send_key(self, key, is_press):
        """
        发送单个按键消息（内部方法）

        功能说明：
            向目标窗口发送按键按下或释放的消息（使用PostMessage异步发送）

        参数说明：
            key: 要发送的按键字符
            is_press: True表示按下，False表示释放
        """
        # 检查窗口句柄是否有效
        if not self._hwnd:
            logger.error("PostMessage 失败: 窗口句柄为空，请检查模拟器是否启动")
            return

        # 使用IsWindow验证句柄是否仍然有效
        if not win32gui.IsWindow(self._hwnd):
            logger.error(f"窗口句柄已失效: {self._hwnd}，尝试重新查找")
            # 可以尝试重新初始化
            return

        # 将按键转换为小写，确保大小写不敏感
        normalized_key = key.lower()
        # 检查按键是否在支持的映射表中
        if normalized_key not in self.VK_CODES:
            # 不支持的按键，记录错误日志并返回
            logger.error(f"未知按键: {key}")
            return

        # 获取该按键的虚拟键码
        vk_code = self.VK_CODES[normalized_key]
        # 使用MapVirtualKeyW将虚拟键码转换为扫描码（scancode）
        # 扫描码是键盘硬件层面的按键标识
        scan_code = windll.user32.MapVirtualKeyW(vk_code, 0)

        # 构建lparam参数（消息附加参数）
        # 如果是扩展键，设置第24位扩展标志
        extended = 1 << 24 if normalized_key in self.EXTENDED_KEYS else 0

        # 根据是按下还是释放构建不同的消息参数
        if is_press:
            # WM_KEYDOWN消息：按键按下
            # lparam格式：(扫描码 << 16) | 重复次数(1) | 扩展标志
            lparam = (scan_code << 16) | 1 | extended
            msg = win32con.WM_KEYDOWN
            msg_name = "DOWN"
        else:
            # WM_KEYUP消息：按键释放
            # lparam格式：(扫描码 << 16) | 重复次数 | 扩展标志 | 先前按键状态(1<<30) | 转换状态(1<<31)
            lparam = (scan_code << 16) | 0xC0000001 | extended
            msg = win32con.WM_KEYUP
            msg_name = "UP"

        # 调用Windows API PostMessage异步发送消息到目标窗口
        # PostMessage是异步的，不等待窗口处理完成
        # 注意: pywin32的PostMessage成功时返回None，失败时抛出异常
        try:
            win32api.PostMessage(self._hwnd, msg, vk_code, lparam)

            # 使用类级别的计数器控制日志频率
            if not hasattr(self, "_key_send_count"):
                self._key_send_count = 0
            self._key_send_count += 1
            # 前10次每次都输出，之后每100次输出一次
            if self._key_send_count < 10:
                logger.debug(
                    f"PostMessage: key={key}, msg={msg_name}, hwnd={self._hwnd}"
                )
            elif self._key_send_count % 100 == 0:
                logger.debug(f"PostMessage (第{self._key_send_count}次): key={key}")
        except Exception as e:
            logger.error(
                f"PostMessage 失败: key={key}, hwnd={self._hwnd}, msg={msg_name}, error={e}"
            )

    def press(self, key):
        """
        按下按键（按住不放）

        功能说明：
            发送按键按下消息，但不发送释放消息，实现按住效果

        参数说明：
            key: 要按下的按键字符
        """
        # 调用内部方法发送按下消息
        self._send_key(key, True)

    def release(self, key):
        """
        释放按键

        功能说明：
            发送按键释放消息，与press方法配对使用

        参数说明：
            key: 要释放的按键字符
        """
        # 调用内部方法发送释放消息
        self._send_key(key, False)

    def tap(self, key, duration=None):
        """
        点击按键（按下后释放）

        功能说明：
            模拟一次完整的按键点击操作（按下+延迟+释放）
            延迟时间可以随机化，模仿人类操作

        参数说明：
            key: 要点击的按键字符
            duration: 按键持续时间（秒），None则使用随机值(0.04-0.06秒)
        """
        # 如果未指定持续时间，生成随机持续时间（40-60毫秒）
        # 随机延迟可以使操作更像人类而非机器
        if duration is None:
            duration = random.uniform(0.04, 0.06)

        # 发送按下消息
        self.press(key)
        # 等待指定的持续时间
        time.sleep(duration)
        # 发送释放消息
        self.release(key)


# 全局键盘控制器实例（单例模式）
# 使用全局变量存储键盘控制器实例，避免重复创建
_keyboard = None


def _get_keyboard():
    """
    获取键盘控制器实例（内部函数）

    功能说明：
        使用单例模式获取键盘控制器实例
        如果实例不存在则创建，存在则直接返回
    """
    # 声明使用全局变量_keyboard
    global _keyboard
    # 检查实例是否已创建
    if _keyboard is None:
        # 实例不存在，创建新的键盘控制器
        _keyboard = KeyboardController()
    # 返回键盘控制器实例
    return _keyboard


def press(key):
    """
    按下按键（便捷函数）

    功能说明：
        全局便捷函数，无需创建KeyboardController实例即可使用

    参数说明：
        key: 要按下的按键字符
    """
    try:
        # 获取键盘控制器实例并调用其press方法
        _get_keyboard().press(key)
    except Exception as e:
        logger.error(f"press({key}) 失败: {e}")


def release(key):
    """
    释放按键（便捷函数）

    功能说明：
        全局便捷函数，无需创建KeyboardController实例即可使用

    参数说明：
        key: 要释放的按键字符
    """
    # 获取键盘控制器实例并调用其release方法
    _get_keyboard().release(key)


def tap(key, times=1, interval=None):
    """
    点击按键（便捷函数）

    功能说明：
        全局便捷函数，支持多次点击和自定义点击间隔

    参数说明：
        key: 要点击的按键字符
        times: 点击次数，默认为1次
        interval: 点击间隔（秒），None则使用随机值(0.03-0.07秒)
    """
    # 获取键盘控制器实例
    kb = _get_keyboard()
    # 循环执行指定次数的点击
    for i in range(times):
        # 调用实例的tap方法，使用随机持续时间
        kb.tap(key, duration=None)
        # 如果不是最后一次点击，添加间隔延迟
        if i < times - 1:
            # 如果未指定间隔，生成随机间隔（30-70毫秒）
            sleep_time = (
                interval if interval is not None else random.uniform(0.03, 0.07)
            )
            # 等待指定时间
            time.sleep(sleep_time)
