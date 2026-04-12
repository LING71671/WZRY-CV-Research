"""Main loop frame processing handlers."""

from __future__ import annotations

import time
import cv2
import numpy as np
from typing import TYPE_CHECKING
from queue import Empty

from wzry_ai.utils.logging_utils import get_logger
from wzry_ai.config import DEFAULT_REGIONS
from wzry_ai.utils.frame_manager import set_full_frame, set_minimap_frame
from wzry_ai.utils.utils import safe_queue_put

if TYPE_CHECKING:
    from .services import GameServices

from wzry_ai.detection import model1_detector, model2_detector

logger = get_logger(__name__)


class LoopHandlers:
    """处理主循环的各个阶段"""

    def __init__(self, services: GameServices):
        self.services = services
        self.last_frame_counter = 0
        self.stale_frame_count = 0
        self._fps_counter = 0
        self._fps_timer = time.time()
        self._current_fps = 0.0
        self._last_supervision_check = time.time()

        # 检测结果缓存
        self._detect_lock = None
        self._detect_results = {
            "model1": None,
            "model2": None,
            "model3": None,
            "fusion": None,
            "minimap": None,
        }

        # 启动检测线程
        self._start_detection_threads()

    def _start_detection_threads(self):
        """启动检测线程"""
        logger.info("正在启动检测线程...")

        # 启动模态1检测线程（小地图检测）
        model1_managed = self.services.thread_supervisor.register(
            "model1_detection",
            self._run_model1_detection,
            daemon=True,
        )
        model1_managed.create_thread().start()
        logger.info("✓ Model1 检测线程已启动")

        # 启动模态2检测线程（全屏血条检测）
        model2_managed = self.services.thread_supervisor.register(
            "model2_detection",
            self._run_model2_detection,
            daemon=True,
        )
        model2_managed.create_thread().start()
        logger.info("✓ Model2 检测线程已启动")

        # 启动游戏状态检测线程
        state_managed = self.services.thread_supervisor.register(
            "state_detection",
            self._run_state_detection,
            daemon=True,
        )
        state_managed.create_thread().start()
        logger.info("✓ 游戏状态检测线程已启动")

        logger.info("所有检测线程启动完成")

    def _run_model1_detection(self):
        """Model1 检测线程（小地图英雄检测）"""
        logger.info("Model1 检测线程运行中...")

        try:
            detector_module = model1_detector
            logger.info("Model1 检测器初始化成功")
        except Exception as e:
            logger.error(f"Model1 检测器初始化失败: {e}", exc_info=True)
            return

        while True:
            try:
                # 获取小地图帧
                from wzry_ai.utils.frame_manager import get_minimap_frame

                minimap_frame = get_minimap_frame()

                if minimap_frame is None:
                    time.sleep(0.05)
                    continue

                # 执行检测
                result = detector_module.detect(frame=minimap_frame)

                if result:
                    # 清空队列并放入最新结果
                    while not self.services.model1_data_queue.empty():
                        try:
                            self.services.model1_data_queue.get_nowait()
                        except Empty:
                            break

                    safe_queue_put(self.services.model1_data_queue, result)

                time.sleep(0.033)  # ~30fps

            except Exception as e:
                logger.error(f"Model1 检测错误: {e}", exc_info=True)
                time.sleep(1)

    def _run_model2_detection(self):
        """Model2 检测线程（全屏血条检测）"""
        logger.info("Model2 检测线程运行中...")

        try:
            detector_module = model2_detector
            logger.info("Model2 检测器初始化成功")
        except Exception as e:
            logger.error(f"Model2 检测器初始化失败: {e}", exc_info=True)
            return

        while True:
            try:
                # 获取全屏帧
                from wzry_ai.utils.frame_manager import get_full_frame

                full_frame = get_full_frame()

                if full_frame is None:
                    time.sleep(0.05)
                    continue

                # 执行检测
                result = detector_module.detect(frame=full_frame)

                if result:
                    # 清空队列并放入最新结果
                    while not self.services.model2_data_queue.empty():
                        try:
                            self.services.model2_data_queue.get_nowait()
                        except Empty:
                            break

                    safe_queue_put(self.services.model2_data_queue, result)

                time.sleep(0.033)  # ~30fps

            except Exception as e:
                logger.error(f"Model2 检测错误: {e}", exc_info=True)
                time.sleep(1)

    def _run_state_detection(self):
        """游戏状态检测线程"""
        logger.info("游戏状态检测线程运行中...")

        while True:
            try:
                frame = self._get_current_frame()
                if frame is None:
                    time.sleep(0.1)
                    continue

                # 执行状态检测
                state_detector = self.services.state_detector
                if state_detector is None:
                    time.sleep(0.1)
                    continue

                result = state_detector.detect(frame)

                # 记录状态变化
                action_taken = bool(result.details.get("action_taken"))
                action = result.details.get("action")
                if action_taken and action is not None:
                    logger.info(f"游戏状态: {result.state} -> 执行动作: {action}")

                # 状态检测频率较低（每0.5秒一次）
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"状态检测错误: {e}", exc_info=True)
                time.sleep(1)

    def process_frame(self):
        """处理一帧"""
        # 更新FPS
        self._update_fps()

        # 定期检查线程健康状态（每5秒一次）
        current_time = time.time()
        if current_time - self._last_supervision_check >= 5.0:
            restarted = self.services.thread_supervisor.check_and_restart()
            if restarted:
                logger.warning(f"已重启线程: {', '.join(restarted)}")
            self._last_supervision_check = current_time

        # 获取当前帧
        frame = self._get_current_frame()
        if frame is None:
            time.sleep(0.016)
            return

        # 处理帧（简化版）
        self._process_game_frame(frame)

        # 显示调试窗口
        self._update_debug_windows(frame)

        # 控制帧率
        time.sleep(0.033)  # ~30fps

    def _update_fps(self):
        """更新FPS计数"""
        self._fps_counter += 1
        now = time.time()
        if now - self._fps_timer >= 1.0:
            self._current_fps = self._fps_counter / (now - self._fps_timer)
            self._fps_counter = 0
            self._fps_timer = now

    def _get_current_frame(self):
        """获取当前帧"""
        if self.services.frame_container[0] is None:
            return None

        # 检查帧是否更新
        if self.services.frame_update_counter[0] == self.last_frame_counter:
            self.stale_frame_count += 1
            if self.stale_frame_count >= 300:  # 5秒未更新
                logger.warning("⚠️ scrcpy 帧连续5秒未更新")
                self.stale_frame_count = 0
            return None

        self.stale_frame_count = 0
        self.last_frame_counter = self.services.frame_update_counter[0]
        return self.services.frame_container[0].copy()

    def _process_game_frame(self, frame):
        """处理游戏帧（简化版）"""
        # 裁剪小地图
        mm = DEFAULT_REGIONS["minimap"]
        h, w = frame.shape[:2]
        base_w, base_h = (
            DEFAULT_REGIONS["full"]["width"],
            DEFAULT_REGIONS["full"]["height"],
        )
        sx, sy = w / base_w, h / base_h
        mx = max(0, int(mm["left"] * sx))
        my = max(0, int(mm["top"] * sy))
        mw = min(int(mm["width"] * sx), w - mx)
        mh = min(int(mm["height"] * sy), h - my)
        minimap_crop = frame[my : my + mh, mx : mx + mw].copy()

        # 设置帧
        set_minimap_frame(minimap_crop)
        set_full_frame(frame)

    def _update_debug_windows(self, frame):
        """更新调试窗口"""
        # 简化版：只显示原始画面
        h, w = frame.shape[:2]
        small_frame = cv2.resize(frame, (w // 2, h // 2))

        # 添加FPS文字
        cv2.putText(
            small_frame,
            f"FPS: {self._current_fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.imshow("EVE", small_frame)

        # 显示小地图区域
        mm = DEFAULT_REGIONS["minimap"]
        h, w = frame.shape[:2]
        base_w, base_h = (
            DEFAULT_REGIONS["full"]["width"],
            DEFAULT_REGIONS["full"]["height"],
        )
        sx, sy = w / base_w, h / base_h
        mx = max(0, int(mm["left"] * sx))
        my = max(0, int(mm["top"] * sy))
        mw = min(int(mm["width"] * sx), w - mx)
        mh = min(int(mm["height"] * sy), h - my)
        minimap_crop = frame[my : my + mh, mx : mx + mw].copy()

        cv2.imshow("EVE Check", minimap_crop)
        cv2.waitKey(1)


__all__ = ["LoopHandlers"]
