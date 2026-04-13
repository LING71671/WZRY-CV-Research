# 🌌 WZRY AI: 基于计算机视觉的人机交互算法研究平台

<div align="center">

**[ 警告：本项目仅为算法研究演示，作者从未授权将其用于任何商业游戏环境 ]**

[![License](https://img.shields.io/badge/License-GPL--3.0-brightgreen.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Control](https://img.shields.io/badge/Hardware-ADB%20/%20Scrcpy-orange.svg)]()

</div>

> [!CAUTION]
> # 🛰️ 法律免责声明与风险预警 (LEGAL DISCLAIMER & RISK WARNING)
> 
> **本程序仅作为【计算机视觉（CV）】与【人机交互（HCI）】领域的纯学术研究 Demo。作者在此明确声明：从未授权任何人将本项目代码与任何受版权保护、包含用户协议限制的游戏客户端（包括但不限于腾讯旗下的《王者荣耀》）联调运行。**
> 
> 1. **零授权声明**：本项目不分发任何游戏资产，亦不提供任何运行授权。代码的本质是一套**基于图像特征进行逻辑决策的数学演示流程**。任何将其部署到实际游戏环境的行为，均属**未经作者许可的滥用行为**。
> 2. **违约责任预警**：由于《腾讯游戏许可及服务协议》严禁使用任何第三方自动化工具，使用者若执意自行运行本项目，即构成了**针对腾讯公司的单方面违约**。由此产生的封号、诉讼、虚拟财产损失等后果，由使用者**独立、排他地承担全部法律责任**。
> 3. **物理模拟本质**：本项目仅通过 ADB 和 Scrcpy 协议进行物理级模拟操作。它不篡改内存、不截获封包、不破坏计算机信息系统安全。即便如此，其在技术上的“非侵入性”并不能豁免使用者违反第三方平台协议的责任。
> 4. **零容忍政策**：本项目作者强烈反对并谴责一切破坏游戏公平性的行为。项目初衷仅为探索 AI 在复杂 UI 环境下的感知能力，严禁用于任何破坏网络空间秩序的非法用途。
> 
> **一旦你下载、克隆或以任何方式运行本项目代码，即表示你已阅读并完全同意上述所有声明。使用者因违规运行产生的一切纠纷，项目作者概不负责。**

---

## 🔬 项目定位

本项目是一个专注于**高帧率实时视觉识别**与**复杂状态决策系统**的科研 Demo。其价值在于验证 YOLO 模型在动态 UI 场景下的感知精度，以及有限状态机（FSM）在多变环境下的决策稳定性。

### 🛡️ 技术合规性设计（防御式定位）
- **非侵入式**：不读取内存，不拦截数据封包，不注入任何游戏进程。
- **物理模拟**：通过 ADB 与 Scrcpy 协议模拟物理触控，技术上仅作为“虚拟操作员”。
- **学术优先**：核心价值在于多模态视觉数据融合（Modal Fusion）与复杂策略链条的实现。


### 🎯 核心能力

- **端到端流程自动化验证**：验证从场景初始化到任务结算的全生命周期逻辑闭环
- **基于 FSM 的战术决策模型**：研究高阶有限状态机在复杂对抗环境下的决策稳定性
- **多模态视觉感知融合**：研究小地图特征与全场景视觉特征的方位角匹配与数据融合
- **复杂 UI 交互逻辑**：验证针对不同特征目标的技能释放与交互逻辑
- **自主路径规划与导航**：包含动态障碍物规避、路径记忆投影及地形鲁棒性测试

### ⚠️ 运行红线
- **严禁商业化**：严禁通过本项目或衍生版本进行任何营利行为。
- **模拟器专用**：本项目针对 Windows 系统下的模拟器环境进行深度优化。
- **环境要求**：模拟器分辨率必须严格设定为 **1920x1080**，否则识别系统将失效。

---

## ✨ 功能特性

### 🏗️ 场景导航与环境初始化

- ✅ 环境驱动程序（模拟器）自主引导
- ✅ 基于模板匹配的任务场景定位
- ✅ UI 目标特征匹配与其逻辑锁定
- ✅ 非预期干扰项（弹窗/状态异常）的自主识别与分类处理
- ✅ 实验任务生命周期管理与自动重叠验证

### 🧠 策略决策智能体 (Decision Agent)

- ✅ **战术决策 FSM**：实现跟随、对抗、避险、补给状态的毫秒级时延流转
- ✅ **实时风险定量评估**：基于视觉动态特征的感知网格威胁评估
- ✅ **特征目标筛选算法**：复杂背景下的交互目标锁定与优先级排序
- ✅ **动作单元授时触发**：模拟人类交互特征的授时动作序列生成
- ✅ **空间导航控制**：验证基于相对坐标投影的绕路逻辑与跟随稳定性

### 👁️ 视觉检测系统

- ✅ **模态1（小地图检测）**：基于 YOLO 的小地图英雄位置检测
- ✅ **模态2（全屏检测）**：基于 YOLO 的全屏血条检测
- ✅ **模态3（辅助检测）**：额外的视觉检测支持
- ✅ **模态融合**：通过方位角匹配融合多模态数据
- ✅ **模板匹配**：用于 UI 状态识别的模板匹配引擎
- ✅ **OCR 识别**：支持中文文字识别（PaddleOCR）

### 🧪 算法验证案例 (Case Studies)

本项目选取以下具备代表性交互特征的英雄模型作为算法验证对象：
- **Case 1 (Yao)**：验证挂接式交互(Attached Interaction)下的状态跟随
- **Case 2 (Cai Wenji)**：验证区域持续增益(Area Buff)下的位置保持
- **Case 3 (Ming Shiyin)**：验证链式连接(Link Connection)下的动态距离补偿

---

## 🚀 快速开始

### 环境要求

- **操作系统**：Windows 10/11
- **Python**：3.11 或更高版本
- **模拟器**：MuMu 模拟器（推荐最新版本）
- **分辨率**：模拟器必须设置为 1920x1080
- **内存**：建议 8GB 以上
- **显卡**：支持 CUDA 的 NVIDIA 显卡（可选，用于加速 YOLO 推理）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-repo/wzry_ai.git
cd wzry_ai
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包括：
- `opencv-python` - 图像处理
- `ultralytics` - YOLO 目标检测
- `torch` - 深度学习框架
- `scrcpy-client` - 安卓屏幕镜像
- `adbutils` - ADB 设备管理
- `paddleocr` - 中文 OCR 识别
- `pywin32` - Windows API 访问

#### 3. 准备模型文件

将 YOLO 模型权重文件放置到 `models/` 目录：
- `models/model1.pt` - 小地图检测模型
- `models/model2.pt` - 全屏血条检测模型
- `models/model3.pt` - 辅助检测模型（可选）

#### 4. 配置模拟器

1. 安装并启动 MuMu 模拟器
2. 设置分辨率为 1920x1080
3. 开启 USB 调试模式
4. 安装王者荣耀游戏

#### 5. 运行项目

```bash
# 推荐使用规范脚本入口点
python scripts/master_auto.py
```

---

## 📁 项目结构

```
wzry_ai_v1.0_20260409/
├── src/wzry_ai/              # 核心代码包
│   ├── app/                  # 应用程序入口和编排
│   │   ├── main.py          # 主入口点
│   │   ├── runtime.py       # 运行时加载
│   │   ├── bootstrap.py     # 启动引导
│   │   └── orchestration.py # 服务编排
│   ├── config/              # 配置管理
│   │   ├── base.py         # 基础配置
│   │   ├── templates.py    # 模板配置
│   │   ├── emulator.py     # 模拟器配置
│   │   └── heroes/         # 英雄配置
│   ├── detection/          # 视觉检测
│   │   ├── model1_detector.py      # 小地图检测
│   │   ├── model2_detector.py      # 全屏检测
│   │   ├── model3_detector.py      # 辅助检测
│   │   └── modal_fusion.py         # 模态融合
│   ├── game_manager/       # 游戏状态管理
│   │   ├── state_detector.py       # 状态检测器
│   │   ├── state_definitions.py    # 状态定义
│   │   ├── state_transitions.py    # 状态转换
│   │   ├── template_matcher.py     # 模板匹配
│   │   ├── hero_selector.py        # 英雄选择
│   │   └── popup_handler.py        # 弹窗处理
│   ├── battle/             # 战斗系统
│   │   ├── battle_fsm.py          # 战斗状态机
│   │   ├── threat_analyzer.py     # 威胁分析
│   │   ├── target_selector.py     # 目标选择
│   │   └── world_state.py         # 世界状态
│   ├── skills/             # 技能系统
│   │   ├── hero_skill_logic_base.py    # 技能基类
│   │   ├── yao_skill_logic_v2.py       # 瑶技能逻辑
│   │   ├── caiwenji_skill_logic_v2.py  # 蔡文姬技能逻辑
│   │   └── mingshiyin_skill_logic_v2.py # 明世隐技能逻辑
│   ├── movement/           # 移动控制
│   │   ├── unified_movement.py    # 统一移动控制器
│   │   └── base_follow_logic.py   # 跟随逻辑
│   ├── device/             # 设备管理
│   │   ├── ADBTool.py            # ADB 工具
│   │   ├── ScrcpyTool.py         # Scrcpy 工具
│   │   └── emulator_manager.py   # 模拟器管理
│   ├── utils/              # 工具模块
│   │   ├── frame_manager.py      # 帧管理器
│   │   ├── logging_utils.py      # 日志工具
│   │   ├── keyboard_controller.py # 键盘控制
│   │   ├── ocr_helper.py         # OCR 辅助
│   │   └── resource_resolver.py  # 资源解析器
│   └── compat/             # 兼容性层
│       └── legacy/         # 遗留代码
├── assets/                 # 资源文件
│   ├── templates/         # 模板图片
│   └── heroes/            # 英雄肖像
├── models/                # YOLO 模型权重
├── data/                  # 运行时数据
├── docs/                  # 文档
├── scripts/               # 脚本
│   ├── master_auto.py     # 规范主入口
│   └── one_off/           # 一次性工具脚本 (本地忽略)
├── requirements.txt       # 依赖列表
└── README.md             # 本文件
```

---

## 🏗️ 架构设计

### 整体架构

项目采用模块化分层架构，各模块职责清晰：

```
┌─────────────────────────────────────────────────────────┐
│                    Master_Auto.py                        │
│                   (主入口和线程编排)                      │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Device   │  │ Detection│  │  Game    │
│ Manager  │  │  System  │  │ Manager  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │             │             │
     ▼             ▼             ▼
┌──────────────────────────────────────┐
│         Battle System                │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │ FSM  │  │Skills│  │ Move │      │
│  └──────┘  └──────┘  └──────┘      │
└──────────────────────────────────────┘
```

### 核心系统

#### 1. 设备管理系统 (Device)

负责与模拟器的连接和通信：
- **ADBTool**：封装 ADB 命令，提供点击、滑动、截图等操作
- **ScrcpyTool**：通过 scrcpy 协议获取实时视频流
- **EmulatorManager**：自动发现和连接 MuMu 模拟器

#### 2. 视觉检测系统 (Detection)

多模态视觉检测和融合：
- **Model1Detector**：小地图英雄检测（YOLO）
- **Model2Detector**：全屏血条检测（YOLO）
- **Model3Detector**：辅助检测（可选）
- **ModalFusion**：通过方位角匹配融合多模态数据

#### 3. 游戏状态管理 (Game Manager)

UI 状态识别和流程控制：
- **StateDetector**：基于模板匹配的状态检测
- **StateDefinitions**：定义 20+ 种游戏状态
- **StateTransitions**：状态转换规则
- **HeroSelector**：自动选择和锁定英雄
- **PopupHandler**：处理各种弹窗

#### 4. 战斗系统 (Battle)

智能战斗决策：
- **BattleFSM**：战斗状态机（跟随/战斗/撤退/回城）
- **ThreatAnalyzer**：威胁等级评估
- **TargetSelector**：目标选择逻辑
- **WorldState**：世界状态维护

#### 5. 技能系统 (Skills)

英雄技能释放：
- **HeroSkillLogicBase**：技能逻辑基类
- **YaoSkillLogicV2**：瑶的技能逻辑
- **CaiwenjiSkillLogicV2**：蔡文姬的技能逻辑
- **MingshiyinSkillLogicV2**：明世隐的技能逻辑

#### 6. 移动系统 (Movement)

智能移动控制：
- **UnifiedMovement**：统一移动控制器
- **StuckDetector**：卡地形检测和自动绕路
- **BaseFollowLogic**：跟随逻辑

### 数据流

```
Scrcpy视频流 → 帧管理器 → 多模态检测
                              ↓
                         模态融合
                              ↓
                         世界状态
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              战斗状态机            游戏状态机
                    ↓                   ↓
            ┌───────┴───────┐          ↓
            ↓               ↓          ↓
        技能系统        移动系统    UI操作
            ↓               ↓          ↓
            └───────┬───────┘──────────┘
                    ↓
              ADB命令执行
```

---

## ⚙️ 配置说明

### 基础配置 (config/base.py)

```python
# 游戏模式
GAME_MODE = 'ai'              # 游戏模式：'ai'=人机, 'rank'=排位
AI_DIFFICULTY = 'simple'      # 人机难度：'simple'=简单

# 英雄选择
DEFAULT_SUPPORT_HERO = '瑶'   # 默认辅助英雄
HERO_SELECT_PRIORITY = ['瑶', '蔡文姬', '明世隐']

# 检测参数
MODEL1_CONFIDENCE_THRESHOLD = 0.5  # 模型1置信度阈值
MODEL2_CONFIDENCE_THRESHOLD = 0.6  # 模型2置信度阈值

# 移动参数
FOLLOW_THRESHOLD = 50         # 跟随阈值（像素）
SAFE_ENEMY_DISTANCE = 200     # 安全距离（像素）
MOVE_INTERVAL = 0.03          # 移动指令间隔（秒）

# 战斗参数
RETREAT_HP_THRESHOLD = 30     # 撤退血量阈值（%）
FIGHT_ENEMY_DISTANCE = 300    # 战斗距离（像素）
```

### 模板配置 (config/templates.py)

定义各种 UI 状态的模板图片和 ROI 区域：

```python
TEMPLATE_CONFIDENCE_THRESHOLDS = {
    'confirm': {'threshold': 0.8, 'roi': (800, 500, 1120, 700)},
    'start_game': {'threshold': 0.85, 'roi': (700, 800, 1220, 1000)},
    # ... 更多模板配置
}
```

### 英雄配置 (config/heroes/)

- **mapping.py**：英雄名称映射（中文 ↔ 拼音）
- **support_config.py**：辅助英雄配置
- **state_configs.py**：英雄状态配置

---

## 🔧 开发指南

### 添加新英雄

1. 在 `src/wzry_ai/skills/` 创建新的技能逻辑文件：

```python
# src/wzry_ai/skills/newhero_skill_logic_v2.py
from wzry_ai.skills.hero_skill_logic_base import HeroSkillLogicBase

class NewHeroSkillLogic(HeroSkillLogicBase):
    def check_and_use_skills(self):
        # 实现英雄特定的技能逻辑
        pass
```

2. 在 `config/heroes/mapping.py` 添加英雄名称映射
3. 在 `config/heroes/support_config.py` 添加英雄配置
4. 在 `assets/heroes/` 添加英雄肖像图片

### 调整检测参数

修改 `config/base.py` 中的相关参数：

```python
# 提高检测精度（但可能降低召回率）
MODEL1_CONFIDENCE_THRESHOLD = 0.7

# 调整移动灵敏度
FOLLOW_THRESHOLD = 30  # 更小的值 = 更灵敏
```

### 添加新的游戏状态

1. 在 `game_manager/state_definitions.py` 添加状态枚举
2. 在 `STATE_SIGNATURES` 添加状态特征
3. 在 `game_manager/state_transitions.py` 添加转换规则
4. 在 `assets/templates/` 添加模板图片

### 调试技巧

#### 启用详细日志

```python
# 在 config/base.py 中
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 可视化检测结果

检测器会自动显示检测结果窗口，可以实时查看：
- 小地图检测结果
- 全屏血条检测结果
- 融合后的实体信息

#### 使用 OCR 调试

```python
from wzry_ai.utils.ocr_helper import OCRHelper
ocr = OCRHelper()
result = ocr.recognize(image)
print(result)
```

---

## 📊 性能优化

### YOLO 推理优化

1. **使用 GPU 加速**：
   ```python
   # 在 config/base.py 中
   YOLO_DEVICE = 'cuda'  # 使用 GPU
   ```

2. **调整输入尺寸**：
   ```python
   YOLO_IMGSZ = 640  # 更小的尺寸 = 更快的推理
   ```

3. **启用 TensorRT**（需要 NVIDIA GPU）：
   ```bash
   # 导出 TensorRT 引擎
   yolo export model=models/model1.pt format=engine
   ```

### 帧率优化

```python
# 在 config/base.py 中
FPS = 30  # 降低目标帧率
M2_DETECT_INTERVAL = 2  # 增加检测间隔
```

### 多线程优化

项目已经使用多线程架构：
- 主线程：游戏状态管理
- 检测线程：视觉检测
- 技能线程：技能释放
- 移动线程：移动控制

---

## 🐛 常见问题

### Q: 无法连接到模拟器

**A**: 检查以下几点：
1. MuMu 模拟器是否已启动
2. 模拟器分辨率是否为 1920x1080
3. USB 调试是否已开启
4. ADB 路径是否正确配置

### Q: 检测不准确

**A**: 尝试以下方法：
1. 调整置信度阈值（`MODEL1_CONFIDENCE_THRESHOLD`）
2. 检查模型文件是否正确
3. 确保游戏画面清晰，无遮挡
4. 调整模板匹配的 ROI 区域

### Q: 移动卡顿或不流畅

**A**: 
1. 降低目标帧率（`FPS`）
2. 增加移动指令间隔（`MOVE_INTERVAL`）
3. 检查 CPU 占用率
4. 关闭不必要的后台程序

### Q: 技能释放不及时

**A**:
1. 检查技能冷却时间配置
2. 调整技能释放条件（血量阈值等）
3. 查看技能日志，确认逻辑是否正确

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 贡献流程

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 代码风格
- 添加详细的中文注释
- 编写单元测试（如适用）
- 更新相关文档

---

---

## 📄 许可证

本项目采用 **GPL-3.0 许可证** - 详见 `LICENSE` 文件

---

<div align="center">

**[ END OF DOCUMENT ]**

</div>
