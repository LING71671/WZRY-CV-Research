"""测试游戏服务模块"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from wzry_ai.app.services import GameServices


class TestGameServices:
    """测试GameServices类"""
    
    @pytest.fixture
    def services(self):
        """创建测试用的游戏服务实例"""
        with patch('wzry_ai.app.services.init_emulator'):
            with patch('wzry_ai.app.services.cv2'):
                return GameServices(adb_device="test_device")
    
    def test_initialization(self, services):
        """测试初始化"""
        assert services.adb_device == "test_device"
        assert services.emulator_config is None
        assert services.scrcpy_tool is None
        assert services.frame_container == [None]
        assert services.frame_update_counter == [0]
        assert services.combat_active is False
        assert services.modules_loaded is False
        assert services.current_hero_name is None
    
    def test_queues_initialization(self, services):
        """测试队列初始化"""
        assert services.skill_queue is not None
        assert services.status_queue is not None
        assert services.model1_data_queue is not None
        assert services.model2_data_queue is not None
        assert services.pause_event is not None
    
    def test_pause_event_default_state(self, services):
        """测试暂停事件默认状态"""
        assert services.pause_event.is_set() is True
    
    def test_thread_supervisor_initialization(self, services):
        """测试线程监督器初始化"""
        assert services.thread_supervisor is not None
    
    @patch('wzry_ai.app.services.init_emulator')
    @patch('wzry_ai.app.services.cv2')
    def test_init_emulator_success(self, mock_cv2, mock_init_emulator):
        """测试成功初始化模拟器"""
        # 模拟模拟器配置
        mock_config = Mock()
        mock_config.serial = "emulator-5554"
        mock_config.window_title = "Test Emulator"
        mock_config.client_size = (1920, 1080)
        mock_init_emulator.return_value = mock_config
        
        services = GameServices()
        result = services._init_emulator()
        
        assert result is True
        assert services.emulator_config == mock_config
        assert services.adb_device == "emulator-5554"
    
    @patch('wzry_ai.app.services.init_emulator')
    def test_init_emulator_failure(self, mock_init_emulator):
        """测试模拟器初始化失败"""
        mock_init_emulator.side_effect = OSError("Connection failed")
        
        services = GameServices()
        result = services._init_emulator()
        
        assert result is False
    
    @patch('wzry_ai.app.services.cv2')
    def test_create_debug_windows(self, mock_cv2, services):
        """测试创建调试窗口"""
        services._create_debug_windows()
        
        # 验证窗口创建调用
        assert mock_cv2.namedWindow.called
        assert mock_cv2.moveWindow.called
        assert mock_cv2.imshow.called
    
    @patch('wzry_ai.app.services.TemplateMatcher')
    @patch('wzry_ai.app.services.ClickExecutor')
    @patch('wzry_ai.app.services.GameStateDetector')
    def test_init_state_detection(self, mock_detector, mock_executor, mock_matcher, services):
        """测试初始化状态检测系统"""
        services._init_state_detection()
        
        assert services.template_matcher is not None
        assert services.click_executor is not None
        assert services.state_detector is not None
    
    def test_cleanup(self, services):
        """测试资源清理"""
        # 模拟scrcpy工具
        services.scrcpy_tool = Mock()
        services.scrcpy_tool.client = Mock()
        
        # 执行清理
        with patch('wzry_ai.app.services.cv2'):
            services.cleanup()
        
        # 验证清理调用
        services.scrcpy_tool.client.stop.assert_called_once()


class TestGameServicesIntegration:
    """测试GameServices集成场景"""
    
    @pytest.mark.skip(reason="需要真实设备连接，跳过以避免ADB错误")
    @patch('wzry_ai.device.ScrcpyTool')
    @patch('wzry_ai.app.services.init_emulator')
    @patch('wzry_ai.app.services.cv2')
    @patch('wzry_ai.app.services.TemplateMatcher')
    @patch('wzry_ai.app.services.ClickExecutor')
    @patch('wzry_ai.app.services.GameStateDetector')
    @patch('scrcpy.EVENT_FRAME', 'frame')
    def test_full_initialization_success(
        self, mock_detector, mock_executor, 
        mock_matcher, mock_cv2, mock_init_emulator, mock_scrcpy
    ):
        """测试完整初始化流程成功"""
        # 模拟模拟器配置
        mock_config = Mock()
        mock_config.serial = "emulator-5554"
        mock_config.window_title = "Test Emulator"
        mock_config.client_size = (1920, 1080)
        mock_init_emulator.return_value = mock_config
        
        # 模拟scrcpy客户端
        mock_client = Mock()
        mock_client.start = Mock()
        mock_client.add_listener = Mock()
        mock_scrcpy_instance = Mock()
        mock_scrcpy_instance.client = mock_client
        mock_scrcpy.return_value = mock_scrcpy_instance
        
        services = GameServices()
        result = services.initialize()
        
        assert result is True
    
    @patch('wzry_ai.app.services.init_emulator')
    def test_full_initialization_failure(self, mock_init_emulator):
        """测试完整初始化流程失败"""
        mock_init_emulator.side_effect = RuntimeError("Emulator not found")
        
        services = GameServices()
        result = services.initialize()
        
        assert result is False


class TestGameServicesState:
    """测试GameServices状态管理"""
    
    @pytest.fixture
    def services(self):
        """创建测试用的游戏服务实例"""
        with patch('wzry_ai.app.services.init_emulator'):
            with patch('wzry_ai.app.services.cv2'):
                return GameServices()
    
    def test_combat_active_state(self, services):
        """测试战斗激活状态"""
        assert services.combat_active is False
        services.combat_active = True
        assert services.combat_active is True
    
    def test_modules_loaded_state(self, services):
        """测试模块加载状态"""
        assert services.modules_loaded is False
        services.modules_loaded = True
        assert services.modules_loaded is True
    
    def test_current_hero_name_state(self, services):
        """测试当前英雄名称状态"""
        assert services.current_hero_name is None
        services.current_hero_name = "瑶"
        assert services.current_hero_name == "瑶"
    
    def test_frame_container_update(self, services):
        """测试帧容器更新"""
        test_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        services.frame_container[0] = test_frame
        assert services.frame_container[0] is not None
        assert services.frame_container[0].shape == (1080, 1920, 3)
    
    def test_frame_update_counter(self, services):
        """测试帧更新计数器"""
        initial_count = services.frame_update_counter[0]
        services.frame_update_counter[0] += 1
        assert services.frame_update_counter[0] == initial_count + 1
