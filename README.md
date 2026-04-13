# 🌌 WZRY AI: 基于计算机视觉的人机交互算法研究平台

<div align="center">

**[ 警告：本项目仅为算法研究演示，作者从未授权将其用于任何商业游戏环境 ]**

[![License](https://img.shields.io/badge/License-GPL--3.0-brightgreen.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Control](https://img.shields.io/badge/Hardware-ADB%20/%20Scrcpy-orange.svg)]()

</div>

> [!CAUTION]
> # 🛰️ 异构感知系统法律免责声明与风险预警 (LEGAL DISCLAIMER)
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

### ⚠️ 环境红线 (Constraint Constraints)
- **非商业化声明**：严禁将本研究成果用于任何营利性或商业化黑灰产。
- **特定仿真环境**：本项目仅针对特定虚拟化指令集环境进行深度调优。
- **输入维度约束**：采样分辨率必须严格锁定为 **1920x1080**。

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

## 🔬 科研环境部署 (Research Environment Deployment)

### 📋 环境预设 (Environmental Prerequisites)

- **操作系统**：Windows 10/11
- **运行环境**：Python 3.11 或更高版本
- **虚拟交互层**：MuMu 模拟器（用于提供标准的 Android 仿真 API）
- **显示标准**：分辨率必须锁定为 **1920x1080**
- **计算资源**：建议 8GB RAM 以上；NVIDIA GPU (支持 CUDA) 以获得更好的 YOLO 推理实时响应

### 🛠️ 系统系统初始化与构建 (System Initialization)

#### 1. 工作空间准备
```bash
git clone https://github.com/LING71671/WZRY-CV-Research.git
cd WZRY-CV-Research
```

#### 2. 依赖层级安装
主要验证套件包括：
- `opencv-python`：底层图像处理与矩阵计算
- `ultralytics`：YOLO v8 目标检测框架支持
- `torch`：张量运算深度学习引擎
- `scrcpy-client` & `adbutils`：Android 远程镜像协议与设备管理协议支持
- `paddleocr`：多模态文本特征提取

```bash
pip install -r requirements.txt
```

#### 3. 加载预训练权重数据集 (Dataset Weights)
将对应的模型权重放置于 `models/` 目录：
- `models/map_weights.pt`：小地图特征检测权重
- `models/combat_weights.pt`：针对动态特征的目标检测权重

#### 4. 建立虚拟交互通道 (Actuator Link)
1. 启动仿真计算实例（模拟器）
2. 确保虚拟化实例的采样频率与分辨率符合 1920x1080
3. 开启实例层级的底层指令调试协议 (ADB Protocol)

#### 5. 初始化研究流 (Initialize Research Stream)
执行以下指令以启动编排层，开始算法验证流程：
```bash
python scripts/master_auto.py
```

---

## 📁 项目结构

```
wzry_ai_v1.0_20260409/
├── src/wzry_ai/              # 算法逻辑抽象层 (Core Logic Abstraction)
│   ├── app/                  # 应用生命周期编排 (Orchestration)
│   │   ├── main.py          # 顶层入口服务
│   │   ├── runtime.py       # 运行时加载单元
│   │   ├── bootstrap.py     # 引导协议封装 (Bootstrap)
│   │   └── orchestration.py # 系统拓扑逻辑编排
│   ├── config/              # 实验参数集管理 (Hyper-parameters)
│   │   ├── base.py         # 系统静态常量集
│   │   ├── templates.py    # 感知特征先验知识库
│   │   ├── emulator.py     # 仿真实例映射配置
│   │   └── heroes/         # 验证案例特定参数
│   ├── detection/          # 多模态感知推理单元 (Perception)
│   │   ├── model1_detector.py      # 空间感知逻辑 (Spatial Sense)
│   │   ├── model2_detector.py      # 全帧感知回归算子
│   │   ├── model3_detector.py      # 特征增强感知辅助
│   │   └── modal_fusion.py         # 异构传感器数据融合架构
│   ├── game_manager/       # 实时场景编排 (Scenario Logic)
│   │   ├── state_detector.py       # 实时场景状态解析 (Scenario Parsing)
│   │   ├── state_definitions.py    # 状态拓扑空间映射定义
│   │   ├── state_transitions.py    # 状态转移矩阵逻辑实现
│   │   ├── template_matcher.py     # 相关性匹配校验引擎
│   │   ├── hero_selector.py        # 研究主体(Case Study)特征锁定
│   │   └── popup_handler.py        # 环境随机扰动项(Noise)滤除
│   ├── battle/             # 逻辑决策中枢 (Tactical Loop)
│   │   ├── battle_fsm.py          # 行为决策状态机模型 (FSM)
│   │   ├── threat_analyzer.py     # 环境显著性风险评估评估
│   │   ├── target_selector.py     # 交互目标最优权值排序
│   │   └── world_state.py         # 仿真环境时空序列建模
│   ├── skills/             # 交互动作序列 (Action Sequences)
│   │   ├── hero_skill_logic_base.py    # 执行逻辑抽象基类
│   │   ├── yao_skill_logic_v2.py       # 交互案例 A (Attached)
│   │   ├── caiwenji_skill_logic_v2.py  # 交互案例 B (Area)
│   │   └── mingshiyin_skill_logic_v2.py # 交互案例 C (Linked)
│   ├── movement/           # 空间动力学控制 (Kinetic Control)
│   │   ├── unified_movement.py    # 指令投影坐标控制器
│   │   └── base_follow_logic.py   # 自适应跟随反馈控制
│   ├── device/             # 环境交互接口 (Env Interface)
│   │   ├── ADBTool.py            # 底层指令传输协议
│   │   ├── ScrcpyTool.py         # 视觉同步流传输协议
│   │   └── emulator_manager.py   # 实例句柄生命周期管理
├── assets/                 # 环境特征资源
├── models/                # 预训练神经网络权重
├── scripts/               # 实验流水线控制脚本
└── README.md             # 本研究说明文档
```

---

## 🏗️ 架构设计

### 整体架构

项目采用模块化分层架构，各模块职责清晰：

```
┌─────────────────────────────────────────────────────────┐
│                    Master_Auto.py                        │
│                   (中枢编排与流水线调度)                    │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Interface│  │感知系统   │  │ 场景引擎  │
│ (Device) │  │(Sensors) │  │(Scenario)│
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │             │             │
     ▼             ▼             ▼
┌──────────────────────────────────────┐
│         决策执行层 (Decision Layer)     │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │ FSM  │  │Action│  │ Move │      │
│  └──────┘  └──────┘  └──────┘      │
└──────────────────────────────────────┘
```

### 数据流 (Data Pipeline)

```
高帧率视觉流 → 帧缓存编排 → 多模态感知推理
                               ↓
                          感知数据融合
                               ↓
                        环境世界模型建立
                               ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              战术决策 FSM         场景拓扑状态机
                    ↓                   ↓
            ┌───────┴───────┐          ↓
            ↓               ↓          ↓
        交互动作序列     轨迹空间规划    UI 状态反馈
            ↓               ↓          ↓
            └───────┬───────┘──────────┘
                    ↓
              仿真环境指令输出 (Actuator)
```

---

## ⚙️ 配置说明

### 实验场景分类设定
SCENARIO_CATEGORY = 'calibration'     # 系统校准场景
ENV_INTENSITY = 'standard'           # 测试环境对抗强度

# 验证目标索引
DEFAULT_CASE_TARGET = 'Case_A'       # 默认研究案例
TARGET_PRIORITY_LIST = ['Case_A', 'Case_B', 'Case_C']

# 感知层超参数 (Inference Hyper-parameters)
REGION_CONFIDENCE_THRESHOLD = 0.5    # 局部特征检测截断阈值
GLOBAL_CONFIDENCE_THRESHOLD = 0.6    # 全域目标回归截断阈值

# 空间轨迹参量
FOLLOW_DELTA_PX = 50                 # 轨迹偏差容忍度（像素）
SAFE_RECOGNITION_RADIUS = 200        # 对抗性风险防御半径（像素）
MOVEMENT_STEP_INTERVAL = 0.03        # 原子指令下发步长（秒）

# 决策模型阈值
RISK_THRESHOLD_PERCENT = 30          # 触发补给/回归行为的资源阈值
ENGAGEMENT_RADIUS = 300              # 有效动作序列作用距离 (Engagement)
```

---

## 🔧 架构扩展与自定义研究案例 (Extension Guide)

### 扩展示例：增加新的实验案例

1. 在 `src/wzry_ai/skills/` 继承交互逻辑基类：

```python
# src/wzry_ai/skills/newcase_logic_v2.py
from wzry_ai.skills.hero_skill_logic_base import HeroSkillLogicBase

class NewCaseLogic(HeroSkillLogicBase):
    def check_and_use_skills(self):
        # 实现特定动态场景下的交互序列逻辑
        pass
```

2. 在 `config/heroes/mapping.py` 注册新的案例特征索引
3. 在 `config/heroes/support_config.py` 配置案例超参数
4. 在 `assets/heroes/` 提供对应的视觉特征模板

### 感知参数调优

通过修改 `config/base.py` 调整感知层灵敏度：

```python
# 提升特征提取精度指标 (Inference Precision)
REGION_CONFIDENCE_THRESHOLD = 0.7

# 调整轨迹控制灵敏度指标
FOLLOW_DELTA_PX = 30  # 更小的值 = 轨迹拟合度更高
```

### 异常场景注册

1. 在 `game_manager/state_definitions.py` 定义新的场景状态空间
2. 在 `STATE_SIGNATURES` 注册新的视觉特征签名
3. 在 `game_manager/state_transitions.py` 更新转移矩阵规则
4. 在 `assets/templates/` 补充对应的环境特征模板

### 实验调试工具

#### 详细日志追踪
```python
# 在 config/base.py 系统初始化阶段
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 感知可视化输出
感知层会自动输出实时检测热力图与结果，涵盖：
- 区域特征检测结果 (Localizer)
- 全域目标回归结果 (Regressor)
- 融合后的实体概率分布

---

## 📊 推理性能调优 (Performance)

### YOLO 推理矩阵加速

1. **启用 CUDA 核加速**：
   ```python
   # config/base.py
   YOLO_DEVICE = 'cuda'  # 启用 NVIDIA GPU 加速层
   ```

2. **多尺度特征缩放**：
   ```python
   YOLO_IMGSZ = 640  # 调整张量输入维度以换取性能
   ```

3. **引擎量化导出**（针对高性能推理）：
   ```bash
   yolo export model=models/map_weights.pt format=engine # 导出 TensorRT
   ```

### 帧调度优化

```python
# 在 config/base.py 中调整流水线压力
FPS = 30                        # 目标采样频率
GLOBAL_INFERENCE_INTERVAL = 2    # 全域推理跳帧比率
```

---

## 🐛 科研环境异常排查 (Troubleshooting)

### Q: 仿真链路连接失败
**分析**: 检测底层 ADB 协议与仿真硬件（模拟器）的握手状态：
1. 确认虚拟化引擎是否运行
2. 校验仿真分辨率是否严格匹配 1920x1080
3. 检查虚拟设备层的 USB 调试权限是否处于 Active 状态

### Q: 感知精度不符合预期
**分析**: 尝试以下调优策略：
1. 迭代感知层置信度超参数（`REGION_CONFIDENCE_THRESHOLD`）
2. 校验权重文件版本与特征索引的匹配度
3. 增加模板匹配的 ROI 区域，减少背景噪声干扰

### Q: 控制序列执行时延过高
**分析**: 
1. 降低推理频率控制参数（`FPS`）
2. 增加控制动作序列的执行间隔（`MOVEMENT_STEP_INTERVAL`）
3. 监控 CPU 占用，识别感知推理过程中的性能瓶颈

---

## 🤝 协作与学术交流 (Research Collaboration)

欢迎提交算法改进意见、反馈实验异常或提出新的研究课题。

### 协作流程
1. 克隆研究副本 (Fork)
2. 构建特性分支 (`git checkout -b research/NewTopic`)
3. 提交算法改进建议 (`git commit -m 'Implement New Algorithm Strategy'`)
4. 发起同步请求 (Pull Request)

### 规范
- 建议遵循 PEP 8 开发规范
- 必须包含严谨的中文算法注释
- 更新相关的实验数据表格（如适用）

---

## 📄 许可证

本项目采用 **GPL-3.0 许可证** - 详见 `LICENSE` 文件

---

<div align="center">

**[ END OF DOCUMENT ]**

</div>
