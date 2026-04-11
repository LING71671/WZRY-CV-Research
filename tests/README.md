# 测试文档

## 概述

本目录包含王者荣耀AI项目的全面测试套件，涵盖单元测试、集成测试和端到端测试。

## 测试结构

```
tests/
├── __init__.py              # 测试包初始化
├── conftest.py              # Pytest配置和全局fixtures
├── README.md                # 本文档
├── test_config.py           # 配置模块测试
├── test_hero_registry.py    # 英雄注册表测试
├── test_integration.py      # 集成测试
├── test_pathfinding.py      # 寻路算法测试
├── test_resource_resolver.py # 资源解析器测试
├── test_services.py         # 游戏服务测试
└── test_template_matcher.py # 模板匹配器测试
```

## 快速开始

### 安装依赖

```bash
pip install pytest pytest-cov
```

### 运行所有测试

```bash
# 方式1: 使用pytest直接运行
pytest tests/ -v

# 方式2: 使用测试脚本
python run_tests.py
```

### 运行特定类型的测试

```bash
# 只运行单元测试
python run_tests.py unit

# 只运行集成测试
python run_tests.py integration

# 运行快速测试（排除慢速测试）
python run_tests.py fast
```

### 生成覆盖率报告

```bash
python run_tests.py coverage
```

覆盖率报告将生成在 `htmlcov/index.html`

### 运行特定测试文件

```bash
# 运行单个测试文件
pytest tests/test_config.py -v

# 或使用脚本
python run_tests.py tests/test_config.py
```

### 运行特定测试函数

```bash
pytest tests/test_config.py::TestConfigConstants::test_grid_size -v
```

## 测试分类

### 单元测试 (Unit Tests)

测试单个模块或函数的功能，不依赖外部系统。

- `test_config.py` - 配置常量和值测试
- `test_hero_registry.py` - 英雄注册表逻辑测试
- `test_resource_resolver.py` - 资源路径解析测试
- `test_pathfinding.py` - A*寻路算法测试
- `test_template_matcher.py` - 模板匹配逻辑测试

### 集成测试 (Integration Tests)

测试多个模块间的交互和集成。

- `test_integration.py` - 跨模块集成测试
- `test_services.py` - 游戏服务集成测试

## 测试覆盖范围

### 核心模块

1. **英雄系统** (`battle/hero_registry.py`)
   - 英雄注册表结构验证
   - 技能逻辑获取
   - 决策器获取
   - 附身技能查询

2. **资源管理** (`utils/resource_resolver.py`)
   - 仓库根目录发现
   - 规范路径构建
   - 资源文件解析
   - 路径回退机制

3. **模板匹配** (`game_manager/template_matcher.py`)
   - 模板加载和缓存
   - 单模板检测
   - 批量模板检测
   - ROI优化
   - RGB验证

4. **寻路系统** (`detection/model1_astar_follow.py`)
   - A*算法实现
   - 启发函数
   - 障碍物避让
   - 坐标转换

5. **配置系统** (`config/`)
   - 配置常量验证
   - 配置值合理性检查
   - 跨模块配置一致性

6. **游戏服务** (`app/services.py`)
   - 服务初始化
   - 队列管理
   - 状态管理
   - 资源清理

## 编写新测试

### 测试命名规范

- 测试文件: `test_<module_name>.py`
- 测试类: `Test<ClassName>`
- 测试函数: `test_<function_description>`

### 示例测试

```python
import pytest
from wzry_ai.module import function_to_test

class TestMyFeature:
    """测试我的功能"""
    
    @pytest.fixture
    def sample_data(self):
        """创建测试数据"""
        return {"key": "value"}
    
    def test_basic_functionality(self, sample_data):
        """测试基本功能"""
        result = function_to_test(sample_data)
        assert result is not None
        assert result["key"] == "expected_value"
    
    def test_edge_case(self):
        """测试边界情况"""
        result = function_to_test(None)
        assert result is None
```

### 使用Fixtures

全局fixtures定义在 `conftest.py` 中：

- `project_root_path` - 项目根目录路径
- `src_path_fixture` - src目录路径
- `test_data_dir` - 测试数据目录
- `mock_frame` - 模拟游戏帧
- `mock_gray_frame` - 模拟灰度帧

## 测试标记

使用pytest标记来分类测试：

```python
@pytest.mark.slow
def test_slow_operation():
    """慢速测试"""
    pass

@pytest.mark.integration
def test_module_integration():
    """集成测试"""
    pass
```

运行特定标记的测试：

```bash
pytest -m slow          # 只运行慢速测试
pytest -m "not slow"    # 排除慢速测试
pytest -m integration   # 只运行集成测试
```

## 持续集成

测试可以集成到CI/CD流程中：

```yaml
# .github/workflows/test.yml 示例
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest tests/ --cov=src/wzry_ai
```

## 调试测试

### 详细输出

```bash
pytest tests/ -vv
```

### 显示print输出

```bash
pytest tests/ -s
```

### 在第一个失败时停止

```bash
pytest tests/ -x
```

### 运行上次失败的测试

```bash
pytest tests/ --lf
```

### 使用pdb调试

```bash
pytest tests/ --pdb
```

## 性能测试

对于性能敏感的代码，可以添加性能测试：

```python
import time

def test_pathfinding_performance():
    """测试寻路性能"""
    start_time = time.time()
    # 执行寻路
    result = a_star(start, goal, obstacle_map)
    end_time = time.time()
    
    # 确保在合理时间内完成
    assert end_time - start_time < 1.0
```

## 常见问题

### 导入错误

确保PYTHONPATH正确设置：

```bash
export PYTHONPATH=src:$PYTHONPATH  # Linux/Mac
$env:PYTHONPATH="src;$env:PYTHONPATH"  # Windows PowerShell
```

### 模块未找到

检查 `conftest.py` 中的路径设置是否正确。

### 测试超时

对于长时间运行的测试，使用 `@pytest.mark.slow` 标记。

## 贡献指南

1. 为新功能编写测试
2. 确保测试覆盖率 > 80%
3. 运行所有测试确保通过
4. 更新测试文档

## 参考资源

- [Pytest官方文档](https://docs.pytest.org/)
- [Pytest-cov文档](https://pytest-cov.readthedocs.io/)
- [Python测试最佳实践](https://docs.python-guide.org/writing/tests/)
