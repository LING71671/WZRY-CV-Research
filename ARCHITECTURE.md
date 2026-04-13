# 王者荣耀AI项目架构指南

> 本文档是 `.sisyphus/plans/v1-architecture-modernization.md` 的精简版，供日常开发参考

## 核心原则

### 1. 单一代码根
- **所有活跃代码必须在 `src/wzry_ai/` 下**
- 禁止在根目录创建新的业务包
- 禁止绕过包命名空间的导入

### 2. 组合根模式
- `src/wzry_ai/app/` 是唯一的应用组合根
- 所有服务启动、线程编排、依赖注入都在 `app/` 中
- 其他包只提供可复用的组件，不自行启动

### 3. 域边界保护
- 保持 v1.0 的领域分离：`battle`, `movement`, `game_manager`, `detection`, `device`, `skills`, `utils`, `config`
- 每个域有明确的职责边界
- 跨域通信通过标准化的接口/DTO

## 目录结构

```
src/wzry_ai/
├── app/              # 组合根：启动、编排、服务生命周期
├── config/           # 配置常量和结构化配置
├── game_manager/     # UI状态机、模板匹配、点击流程
├── battle/           # 战斗语义：世界模型、威胁分析、决策
├── movement/         # 移动执行：跟随、寻路、卡点恢复
├── detection/        # 检测器：模型推理、模态融合
├── device/           # 设备：模拟器发现、ADB、scrcpy
├── skills/           # 技能系统：技能逻辑、英雄特定行为
├── utils/            # 跨域工具（仅限真正通用的）
└── compat/legacy/    # 遗留代码隔离区（有明确移除计划）

assets/
├── templates/        # UI模板图片
└── heroes/           # 英雄头像资源

models/               # YOLO模型权重
data/                 # 运行时数据、地图、配置
docs/                 # 文档
scripts/              # 操作员入口脚本
```

## 依赖规则

### ✅ 允许的依赖
- `app` → 任何活跃域包
- `config` ← 任何活跃域包（config 被所有包导入）
- `game_manager` → `config`, `utils`, `device`, `detection`（接口）
- `battle` → `config`, `utils`, `skills`（接口）, `detection`（标准化输出）
- `movement` → `config`, `utils`, `battle`（输出）
- `detection` → `config`, `utils`, `device`
- `skills` → `config`, `utils`, `battle`（接口）
- `device` → `config`, `utils`
- `utils` → 无业务域依赖

### ❌ 禁止的依赖
- `battle` ❌→ `game_manager`（战斗不依赖UI状态机内部）
- `device` ❌→ `battle`, `movement`, `skills`
- `config` ❌→ 任何运行时域
- `utils` ❌→ 业务域
- 活跃代码 ❌→ `compat/legacy`（除非通过批准的shim）
- 任何包 ❌→ 硬编码资源路径（必须通过resolver）

## 开发规范

### 添加新英雄
1. 在 `config/heroes/` 添加配置
2. 在 `skills/` 添加技能逻辑
3. 在 `battle/hero_registry.py` 注册
4. **不要修改入口点或无关基础设施**

### 添加新检测器
1. 在 `detection/` 添加检测器适配器
2. 暴露标准化的 `DetectorResult`
3. **不要泄露模型特定的结果格式到其他域**

### 添加新运行时模式
1. 在 `app/` 中定义模式配置
2. 特定UI逻辑放在 `game_manager/`（如果需要）
3. **不要在根目录添加新脚本或扩展 Master_Auto.py**

### 资源访问
- **必须**通过 `utils/resource_resolver.py`
- **禁止**硬编码相对路径如 `"image/xxx.png"`
- **禁止**依赖当前工作目录

### 导入规范
```python
# ✅ 正确
from wzry_ai.config import CONFIG_CONSTANT
from wzry_ai.battle.world_state import WorldState
import wzry_ai.detection.model1_detector as model1

# ❌ 错误
from config import CONFIG_CONSTANT  # 缺少包前缀
import battle.world_state  # 缺少包前缀
from compat.legacy import old_module  # 直接导入legacy
```

## 入口点

### 主入口
```bash
# 规范脚本入口点
python scripts/master_auto.py
```

### 启动流程
```
scripts/master_auto.py
  ↓
wzry_ai.app.main.main()
  ↓
wzry_ai.app.runtime.run_app_runtime()
  ↓
wzry_ai.app.orchestration.main()
  ├─ bootstrap_runtime_environment()
  └─ game_loop.run_game_loop()
      ├─ GameServices.initialize()
      └─ LoopHandlers.process_frame()
```

## 反模式警告

### 🚫 绝对禁止
1. 在根目录创建新的业务包
2. 在 `utils/` 中堆积领域逻辑
3. 硬编码资源路径
4. 在 `Master_Auto.py` 中添加业务逻辑
5. 让 `compat/legacy/` 成为永久代码
6. 在结构迁移时修改业务逻辑
7. 创建多个"规范"实现路径

### ⚠️ 需要审查
1. 跨域直接调用（应该通过接口）
2. 新的全局状态或单例
3. 在非 `app/` 中启动线程
4. 绕过 resolver 的资源访问
5. 循环依赖

## 验证清单

### 提交前检查
```bash
# 1. 导入测试
$env:PYTHONPATH='src'
python -c "import wzry_ai; import wzry_ai.app; import wzry_ai.config"

# 2. 编译检查
python -m compileall src

# 3. 启动测试
python scripts/master_auto.py  # 应该能启动到模拟器检测

# 4. 依赖扫描
# 确保没有导入 compat/legacy（除非是批准的shim）
```

## 快速参考

| 需求 | 放在哪里 | 不要放在 |
|------|---------|---------|
| 启动逻辑 | `app/` | `Master_Auto.py` |
| 战斗决策 | `battle/` | `game_manager/` |
| UI检测 | `game_manager/` | `battle/` |
| 移动执行 | `movement/` | `battle/` |
| 模型推理 | `detection/` | 业务域 |
| 设备连接 | `device/` | 业务域 |
| 技能逻辑 | `skills/` | `battle/` |
| 通用工具 | `utils/` | 任何域 |
| 配置常量 | `config/` | 硬编码 |
| 遗留代码 | `compat/legacy/` | 活跃包 |

## 获取帮助

- 完整架构计划：`.sisyphus/plans/v1-architecture-modernization.md`
- 变更记录：`.sisyphus/CHANGES-FROM-ORIGINAL.md`
- 现代化原因：`.sisyphus/WHY-MODERNIZE.md`
- 遗留系统注册：`.sisyphus/legacy-registry.md`
- Shim注册：`.sisyphus/shim-registry.md`

---

**记住：保持架构清晰比快速添加功能更重要。混乱的架构会让未来的开发越来越慢。**
