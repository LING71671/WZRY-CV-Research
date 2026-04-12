"""Game services initialization and management."""

from __future__ import annotations

import cv2
import numpy as np
import time
import threading
from queue import Queue
from typing import Optional

from wzry_ai.utils.logging_utils import get_logger
from wzry_ai.device.emulator_manager import init_emulator
from wzry_ai.game_manager import ClickExecutor, GameStateDetector, TemplateMatcher
from wzry_ai.utils.thread_supervisor import ThreadSupervisor

logger = get_logger(__name__)


class GameServices:
    """管理所有游戏服务的生命周期"""

    def __init__(self, adb_device: Optional[str] = None):
        self.adb_device = adb_device
        self.emulator_config = None
        self.scrcpy_tool = None
        self.frame_container = [None]
        self.frame_update_counter = [0]

        # 队列
        self.skill_queue = Queue(maxsize=1)
        self.status_queue = Queue(maxsize=5)
        self.model1_data_queue = Queue(maxsize=1)
        self.model2_data_queue = Queue(maxsize=1)
        self.pause_event = threading.Event()
        self.pause_event.set()  # 默认暂停

        # 检测器和执行器
        self.template_matcher = None
        self.click_executor = None
        self.state_detector = None
        self.thread_supervisor = ThreadSupervisor()

        # 状态
        self.combat_active = False
        self.modules_loaded = False
        self.current_hero_name = None

    def initialize(self) -> bool:
        """初始化所有服务"""
        try:
            # 初始化模拟器
            if not self._init_emulator():
                return False

            # 创建调试窗口
            self._create_debug_windows()

            # 初始化状态检测系统
            self._init_state_detection()

            # 初始化scrcpy连接
            self._init_scrcpy()

            # 启动战斗系统线程
            if not self._start_battle_system():
                logger.error("战斗系统启动失败")
                return False

            # 启动技能系统线程
            if not self._start_skill_system():
                logger.error("技能系统启动失败")
                return False

            # 设置线程监督
            self._setup_thread_supervision()

            logger.info("✓ 所有服务初始化完成")
            return True

        except Exception as e:
            logger.error(f"初始化失败: {e}", exc_info=True)
            return False

    def _init_emulator(self) -> bool:
        """初始化模拟器连接"""
        try:
            self.emulator_config = init_emulator()
            self.adb_device = self.emulator_config.serial
            logger.info(f"模拟器窗口: {self.emulator_config.window_title}")
            logger.info(f"ADB设备: {self.adb_device}")
            logger.info(
                f"分辨率: {self.emulator_config.client_size[0]}x{self.emulator_config.client_size[1]}"
            )
            return True
        except (OSError, RuntimeError, ConnectionError) as e:
            logger.error(f"模拟器初始化失败: {e}")
            logger.error("请确保模拟器已启动，分辨率为 1920x1080")
            return False

    def _create_debug_windows(self):
        """创建调试窗口"""
        from wzry_ai.config import DEFAULT_REGIONS

        cv2.namedWindow("EVE", cv2.WINDOW_NORMAL)
        cv2.namedWindow("EVE Check", cv2.WINDOW_NORMAL)
        cv2.moveWindow("EVE", 50, 50)
        cv2.moveWindow("EVE Check", 700, 50)
        cv2.imshow("EVE", np.zeros((360, 640, 3), dtype=np.uint8))

        _mm = DEFAULT_REGIONS["minimap"]
        cv2.resizeWindow("EVE Check", _mm["width"], _mm["height"])
        cv2.imshow("EVE Check", np.zeros((300, 300, 3), dtype=np.uint8))
        cv2.waitKey(1)
        logger.info("调试窗口已创建 (EVE / EVE Check)")

    def _init_state_detection(self):
        """初始化状态检测系统"""
        logger.info("初始化状态检测系统...")
        self.template_matcher = TemplateMatcher(match_scale=1.0)
        self.click_executor = ClickExecutor(adb_device=self.adb_device, use_adb=True)  # pyright: ignore[reportArgumentType]
        self.state_detector = GameStateDetector(
            self.template_matcher,
            self.click_executor,
            confirm_threshold=3,
            unknown_threshold=10,
        )
        logger.info("状态检测系统初始化完成")

    def _init_scrcpy(self):
        """初始化scrcpy连接"""
        import scrcpy
        from wzry_ai.device.ScrcpyTool import ScrcpyTool

        logger.info("初始化 ScrcpyTool 连接...")

        def on_frame(frame):
            if frame is not None:
                self.frame_container[0] = frame
                self.frame_update_counter[0] += 1

        device_serial = self.adb_device
        if device_serial is None:
            raise RuntimeError("ADB device not initialized")
        self.scrcpy_tool = ScrcpyTool(device_serial=device_serial)
        self.scrcpy_tool.client.add_listener(scrcpy.EVENT_FRAME, on_frame)
        self.scrcpy_tool.client.max_fps = 30
        self.scrcpy_tool.client.start(threaded=True)

        logger.info("ScrcpyTool 连接成功")
        time.sleep(1)  # 等待第一帧

    def _start_battle_system(self) -> bool:
        """启动战斗系统线程"""
        logger.info("正在启动战斗系统...")

        try:
            from wzry_ai.movement.movement_logic_yao import run_fusion_logic_v2

            battle_thread = threading.Thread(
                target=run_fusion_logic_v2,
                args=(
                    self.model1_data_queue,
                    self.model2_data_queue,
                    self.skill_queue,
                    self.status_queue,
                    self.pause_event,
                ),
                daemon=True,
                name="BattleSystem",
            )
            battle_thread.start()
            self.thread_supervisor.register_thread("battle_system", battle_thread)  # pyright: ignore[reportAttributeAccessIssue]
            logger.info("✓ 战斗系统线程已启动")
            return True

        except Exception as e:
            logger.error(f"战斗系统启动失败: {e}", exc_info=True)
            return False

    def _start_skill_system(self) -> bool:
        """启动技能系统线程"""
        logger.info("正在启动技能系统...")

        try:
            from wzry_ai.config import DEFAULT_SUPPORT_HERO

            # 动态加载技能逻辑类
            if DEFAULT_SUPPORT_HERO == "瑶":
                from wzry_ai.skills.yao_skill_logic_v2 import YaoSkillLogic

                skill_logic = YaoSkillLogic()
            elif DEFAULT_SUPPORT_HERO == "蔡文姬":
                from wzry_ai.skills.caiwenji_skill_logic_v2 import CaiwenjiSkillLogic

                skill_logic = CaiwenjiSkillLogic()
            elif DEFAULT_SUPPORT_HERO == "明世隐":
                from wzry_ai.skills.mingshiyin_skill_logic_v2 import (
                    MingshiyinSkillLogic,
                )

                skill_logic = MingshiyinSkillLogic()
            else:
                logger.error(f"不支持的英雄: {DEFAULT_SUPPORT_HERO}")
                logger.error("支持的英雄: 瑶, 蔡文姬, 明世隐")
                return False

            skill_thread = threading.Thread(
                target=skill_logic.run,
                args=(self.skill_queue,),
                daemon=True,
                name="SkillSystem",
            )
            skill_thread.start()
            self.thread_supervisor.register_thread("skill_system", skill_thread)  # pyright: ignore[reportAttributeAccessIssue]
            logger.info(f"✓ 技能系统线程已启动 (英雄: {DEFAULT_SUPPORT_HERO})")
            return True

        except Exception as e:
            logger.error(f"技能系统启动失败: {e}", exc_info=True)
            return False

    def _setup_thread_supervision(self):
        """设置线程监督"""
        logger.info("正在设置线程监督...")

        try:
            # ThreadSupervisor 使用 check_and_restart() 方法
            # 需要在主循环中定期调用，这里只是标记已设置
            logger.info("✓ 线程监督已配置（将在主循环中定期检查）")
        except Exception as e:
            logger.error(f"线程监督配置失败: {e}", exc_info=True)

    def cleanup(self):
        """清理资源"""
        try:
            if self.scrcpy_tool:
                self.scrcpy_tool.client.stop()
            self.thread_supervisor.stop_all()
            cv2.destroyAllWindows()
        except Exception as e:
            logger.error(f"清理资源时出错: {e}")


__all__ = ["GameServices"]
