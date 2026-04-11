"""
英雄技能管理器模块 - 统一管理英雄的所有技能
负责管理单个英雄的技能创建、更新、释放等完整生命周期

[弃用说明] 此模块属于旧版技能体系，当前实际使用的技能逻辑已迁移到
hero_skill_logic_base.py + 各英雄的 *_skill_logic_v2.py 文件。
本模块保留但不再被任何核心逻辑使用。
"""

# 导入时间模块
import time
# time: 提供时间相关功能，如sleep

# 导入类型提示相关类
from typing import Dict, List, Optional, Any
# Dict: 字典类型，用于存储技能映射
# List: 列表类型
# Optional: 可选类型
# Any: 任意类型

# 从queue模块导入队列相关类
from queue import Queue, Empty
# Queue: 线程安全的数据队列
# Empty: 队列空异常

from utils.logging_utils import get_logger
logger = get_logger(__name__)

# 从skill_base模块导入基类和配置类
from .skill_base import SkillBase, SkillConfig, SkillRegistry, SkillType
# SkillBase: 技能抽象基类
# SkillConfig: 技能配置数据类
# SkillRegistry: 技能注册表，用于动态创建技能
# SkillType: 技能类型枚举

# 从skill_context模块导入技能上下文
from .skill_context import SkillContext
# SkillContext: 技能上下文，封装游戏状态

# 从skill_types模块导入具体技能类
from .skill_types import DamageSkill, AutoMaintenanceSkill
# DamageSkill: 伤害技能类，用于普攻管理
# AutoMaintenanceSkill: 自动维护技能类，用于买装备和升级

# 从hero_skill_configs模块导入配置获取函数
from .hero_skill_configs import get_hero_skill_config
# get_hero_skill_config: 根据英雄名称获取技能配置


class HeroSkillManager:
    """
    英雄技能管理器类
    
    功能描述：
        负责管理单个英雄的所有技能，包括：
        - 技能创建和初始化
        - 技能更新和状态管理
        - 技能释放优先级控制
        - 普攻管理
        - 自动维护（买装备、升级）
        
    参数说明：
        hero_name: 英雄名称，字符串类型
        log_enabled: 是否启用日志输出，布尔类型，默认为False
    """
    
    def __init__(self, hero_name: str, log_enabled: bool = False):
        """
        初始化英雄技能管理器
        
        参数说明：
            hero_name: 英雄名称，如"瑶"、"明世隐"等
            log_enabled: 是否启用日志，True会输出调试信息
        """
        self.hero_name = hero_name  # 保存英雄名称
        self.log_enabled = log_enabled  # 保存日志启用标志
        
        # ========== 加载技能配置 ==========
        self.config = get_hero_skill_config(hero_name)  # 从配置模块获取该英雄的技能配置
        if not self.config:  # 检查配置是否存在
            raise ValueError(f"未找到英雄 {hero_name} 的技能配置")  # 配置不存在则抛出异常
            
        # ========== 创建技能实例 ==========
        self.skills: Dict[str, SkillBase] = {}  # 存储所有技能的词典，key为skill_id
        self._create_skills()  # 调用方法创建技能实例
        
        # ========== 创建自动维护技能 ==========
        self.auto_maintenance_skills: Dict[str, AutoMaintenanceSkill] = {}  # 存储自动维护技能
        self._create_auto_maintenance_skills()  # 调用方法创建自动维护技能
        
        # ========== 设置普攻技能 ==========
        self.damage_skill: Optional[DamageSkill] = None  # 普攻技能引用，用于普攻管理
        self._setup_basic_attack()  # 调用方法设置普攻
        
        # ========== 初始化状态 ==========
        self.paused = False  # 暂停标志，True时停止释放技能（但继续自动维护）
        self.last_health_info = None  # 上次接收到的health_info数据
        
        # 输出初始化完成日志
        self._log(f"[{hero_name}] 技能管理器初始化完成，共 {len(self.skills)} 个技能")
        
    def _log(self, msg: str):
        """
        内部方法：输出日志
        
        参数说明：
            msg: 日志消息字符串
            
        功能说明：
            仅在log_enabled为True时输出日志信息
        """
        if self.log_enabled:  # 检查日志是否启用
            logger.info(msg)
            
    def _create_skills(self):
        """
        内部方法：根据配置创建技能实例
        
        功能说明：
            遍历配置中的技能列表，使用SkillRegistry动态创建技能实例
            将创建的技能存入skills字典，key为skill_id
        """
        skill_configs = self.config.get("skills", [])  # 从配置获取技能配置列表，默认为空列表
        
        for cfg in skill_configs:  # 遍历每个技能配置
            if isinstance(cfg, dict):  # 检查配置是否为字典类型
                # 如果是字典，使用解包操作符转换为SkillConfig对象
                cfg = SkillConfig(**cfg)
                
            try:
                skill = SkillRegistry.create_skill(cfg)  # 使用注册表创建技能实例
                self.skills[cfg.skill_id] = skill  # 将技能存入字典，key为skill_id
                self._log(f"  创建技能: {cfg.name} ({cfg.skill_id}) - {cfg.skill_type.value}")  # 输出创建日志
            except (KeyError, ValueError, AttributeError, ImportError) as e:  # 捕获创建过程中的异常
                self._log(f"  创建技能失败 {cfg.skill_id}: {e}")  # 输出错误日志
                
    def _create_auto_maintenance_skills(self):
        """
        内部方法：创建自动维护技能
        
        功能说明：
            根据配置创建自动购买装备和自动升级技能的AutoMaintenanceSkill实例
            这些技能不需要复杂的触发条件，按固定间隔执行
        """
        maintenance_cfg = self.config.get("auto_maintenance", {})  # 获取自动维护配置
        
        # ========== 创建买装备技能 ==========
        if maintenance_cfg.get("buy_item", {}).get("enabled", True):  # 检查买装备是否启用
            cfg = SkillConfig(
                skill_id="buy_item",  # 技能ID
                skill_type=SkillType.DAMAGE,  # 技能类型（占位，实际不使用）
                key=maintenance_cfg["buy_item"].get("key", "4"),  # 买装备按键，默认为"4"
                name="买装备",  # 技能名称
                cooldown=maintenance_cfg["buy_item"].get("interval", 3),  # 冷却时间（购买间隔）
                range=0,  # 范围为0（不需要目标）
            )
            cfg.trigger_params = {"buy_interval": maintenance_cfg["buy_item"].get("interval", 3)}  # 设置购买间隔参数
            skill = AutoMaintenanceSkill(cfg)  # 创建自动维护技能实例
            self.auto_maintenance_skills["buy_item"] = skill  # 存入自动维护技能字典
            
        # ========== 创建升级技能 ==========
        if maintenance_cfg.get("level_up", {}).get("enabled", True):  # 检查升级技能是否启用
            cfg = SkillConfig(
                skill_id="level_up",  # 技能ID
                skill_type=SkillType.DAMAGE,  # 技能类型（占位，实际不使用）
                key="level_up",  # 按键标识（实际使用数字键1/2/3）
                name="升级技能",  # 技能名称
                cooldown=maintenance_cfg["level_up"].get("interval", 5),  # 冷却时间（升级间隔）
                range=0,  # 范围为0（不需要目标）
            )
            cfg.trigger_params = {
                "levelup_interval": maintenance_cfg["level_up"].get("interval", 5),  # 升级间隔参数
                "priority": maintenance_cfg["level_up"].get("priority", ["R", "Q", "E"]),  # 升级优先级
            }
            skill = AutoMaintenanceSkill(cfg)  # 创建自动维护技能实例
            self.auto_maintenance_skills["level_up"] = skill  # 存入自动维护技能字典
            
    def _setup_basic_attack(self):
        """
        内部方法：设置普攻技能
        
        功能说明：
            从已创建的技能中找到第一个DamageSkill作为普攻管理器
            普攻管理器用于处理普通攻击逻辑
        """
        ba_config = self.config.get("basic_attack", {})  # 获取普攻配置
        if ba_config.get("enabled", True):  # 检查普攻是否启用
            # 遍历所有技能，找到第一个DamageSkill
            for skill in self.skills.values():
                if isinstance(skill, DamageSkill):  # 检查技能是否为DamageSkill类型
                    self.damage_skill = skill  # 设置为普攻技能
                    break  # 找到后跳出循环
                    
    def update(self, health_info: Dict):
        """
        更新技能状态并执行技能
        
        参数说明：
            health_info: 包含游戏状态的字典，通常由状态检测模块提供
            
        功能说明：
            主更新方法，每帧调用一次，负责：
            1. 保存health_info
            2. 检查暂停状态
            3. 创建技能上下文
            4. 执行自动维护
            5. 按优先级释放技能
            6. 执行普攻
        """
        self.last_health_info = health_info  # 保存本次health_info
        
        # 检查是否处于暂停状态
        if self.paused:  # 如果已暂停
            self._do_auto_maintenance()  # 只执行自动维护（买装备、升级）
            return  # 跳过后续技能释放
            
        # 创建技能上下文，用于技能判断
        context = SkillContext.from_health_info(health_info)  # 从health_info创建上下文
        
        # 执行自动维护（买装备、升级技能）
        self._do_auto_maintenance()
        
        # 按优先级排序技能（数字越小优先级越高）
        sorted_skills = sorted(
            self.skills.values(),  # 获取所有技能
            key=lambda s: s.config.priority  # 按priority字段排序
        )
        
        # 尝试按优先级释放技能
        for skill in sorted_skills:  # 遍历排序后的技能列表
            if skill.can_cast(context):  # 检查技能是否可以释放
                self._log(f"[{self.hero_name}] 释放技能: {skill.name}")  # 输出释放日志
                skill.cast(context)  # 执行技能释放
                
        # 执行普攻
        self._do_basic_attack(context)  # 调用普攻方法
        
    def _do_auto_maintenance(self):
        """
        内部方法：执行自动维护
        
        功能说明：
            遍历所有自动维护技能（买装备、升级），检查是否可以执行
            自动维护技能在暂停状态下也会执行
        """
        for skill in self.auto_maintenance_skills.values():  # 遍历所有自动维护技能
            # 检查技能是否有can_cast方法且可以执行
            if hasattr(skill, 'can_cast') and skill.can_cast(None):
                skill.cast(None)  # 执行自动维护操作
                
    def _do_basic_attack(self, context: SkillContext):
        """
        内部方法：执行普通攻击
        
        参数说明：
            context: SkillContext类型，技能上下文
            
        功能说明：
            检查普攻条件并执行普攻
            包括附身状态检查和普攻间隔检查
        """
        # 检查普攻技能是否存在且有should_basic_attack方法
        if self.damage_skill and hasattr(self.damage_skill, 'should_basic_attack'):
            ba_config = self.config.get("basic_attack", {})  # 获取普攻配置
            
            # 检查附身状态限制
            if context.is_attached and not ba_config.get("can_attack_when_attached", True):
                return  # 处于附身状态且配置不允许附身时普攻，直接返回
                
            # 检查是否应该普攻
            if self.damage_skill.should_basic_attack(context):
                self._log(f"[{self.hero_name}] 执行普攻")  # 输出普攻日志
                self.damage_skill.basic_attack()  # 执行普攻
                
    def pause(self):
        """
        暂停技能释放
        
        功能说明：
            将paused标志设置为True，暂停主动技能的释放
            自动维护（买装备、升级）不受影响，继续执行
        """
        self.paused = True  # 设置暂停标志为True
        self._log(f"[{self.hero_name}] 技能释放已暂停")  # 输出暂停日志
        
    def resume(self):
        """
        恢复技能释放
        
        功能说明：
            将paused标志设置为False，恢复主动技能的释放
        """
        self.paused = False  # 设置暂停标志为False
        self._log(f"[{self.hero_name}] 技能释放已恢复")  # 输出恢复日志
        
    def enable_skill(self, skill_id: str):
        """
        启用指定技能
        
        参数说明：
            skill_id: 技能ID字符串，如"Q"、"W"、"E"、"R"
            
        功能说明：
            将指定ID的技能设置为启用状态
        """
        if skill_id in self.skills:  # 检查技能是否存在
            self.skills[skill_id].enable()  # 调用技能的enable方法
            self._log(f"[{self.hero_name}] 技能 {skill_id} 已启用")  # 输出启用日志
            
    def disable_skill(self, skill_id: str):
        """
        禁用指定技能
        
        参数说明：
            skill_id: 技能ID字符串，如"Q"、"W"、"E"、"R"
            
        功能说明：
            将指定ID的技能设置为禁用状态
        """
        if skill_id in self.skills:  # 检查技能是否存在
            self.skills[skill_id].disable()  # 调用技能的disable方法
            self._log(f"[{self.hero_name}] 技能 {skill_id} 已禁用")  # 输出禁用日志
            
    def get_skill_status(self, skill_id: str = None) -> Dict:
        """
        获取技能状态
        
        参数说明：
            skill_id: 技能ID字符串，为None时返回所有技能状态
            
        返回值说明：
            Dict: 技能状态字典，包含技能ID、名称、启用状态、冷却状态等信息
        """
        if skill_id:  # 如果指定了技能ID
            skill = self.skills.get(skill_id)  # 获取指定技能
            return skill.get_status() if skill else {}  # 返回技能状态，不存在则返回空字典
            
        # 返回所有技能的状态字典
        return {
            skill_id: skill.get_status()  # 获取每个技能的状态
            for skill_id, skill in self.skills.items()  # 遍历所有技能
        }
        
    def run(self, queue: Queue):
        """
        主循环方法 - 从队列接收数据并更新技能
        
        参数说明：
            queue: Queue类型，数据队列，接收来自其他模块的health_info数据
            
        功能说明：
            持续运行，从队列获取数据并调用update方法更新技能
            队列为空时使用上次数据继续执行自动维护
            异常处理确保循环不会中断
        """
        self._log(f"[{self.hero_name}] 技能管理器启动")  # 输出启动日志
        
        while True:  # 无限循环，持续运行
            try:
                health_info = queue.get(timeout=0.1)  # 从队列获取数据，超时0.1秒
                self.update(health_info)  # 调用update方法更新技能
            except Empty:  # 队列为空异常
                # 没有新数据时，使用上一次的数据继续执行自动维护
                if self.last_health_info is not None:  # 检查是否有上次数据
                    self._do_auto_maintenance()  # 执行自动维护
            except (ValueError, AttributeError, RuntimeError) as e:  # 捕获其他异常
                self._log(f"[{self.hero_name}] 技能循环错误: {e}")  # 输出错误日志
                
            time.sleep(0.02)  # 休眠20毫秒，避免CPU占用过高


# ================= 便捷函数区域 =================
def create_skill_manager(hero_name: str, log_enabled: bool = False) -> HeroSkillManager:
    """
    创建技能管理器的便捷函数
    
    参数说明：
        hero_name: 英雄名称，字符串类型
        log_enabled: 是否启用日志，布尔类型，默认为False
        
    返回值说明：
        HeroSkillManager: 创建的英雄技能管理器实例
        
    功能说明：
        提供一种简便的方式创建HeroSkillManager实例
    """
    return HeroSkillManager(hero_name, log_enabled)  # 创建并返回管理器实例


def run_skill_logic(hero_name: str, queue: Queue, log_enabled: bool = False):
    """
    运行技能逻辑的便捷函数
    
    参数说明：
        hero_name: 英雄名称，字符串类型
        queue: Queue类型，数据队列，用于接收状态更新
        log_enabled: 是否启用日志，布尔类型，默认为False
        
    功能说明：
        创建技能管理器并启动主循环
        通常在新线程中调用此函数
    """
    manager = create_skill_manager(hero_name, log_enabled)  # 创建技能管理器
    manager.run(queue)  # 启动主循环
