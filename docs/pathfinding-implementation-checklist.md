# 寻路算法优化实施清单

## 📋 总览

本文档详细列出每个优化方案需要修改的文件和具体改动点。

---

## 🚀 方案 1: 路径缓存 (推荐优先实施)

### 需要修改的文件

#### 1. `src/wzry_ai/detection/model1_astar_follow.py`

**改动位置 1: 文件顶部添加缓存数据结构**
```python
# 在全局变量区域添加 (约第 60 行)

# 路径缓存相关
path_cache = {}  # 缓存字典: {(start, goal): (path, timestamp)}
CACHE_MAX_SIZE = 20  # 最大缓存数量
CACHE_EXPIRE_TIME = 2.0  # 缓存过期时间（秒）
CACHE_POSITION_THRESHOLD = 5  # 位置变化阈值（格）
```

**改动位置 2: 添加缓存辅助函数**
```python
# 在 a_star 函数之前添加 (约第 120 行)

def get_cached_path(start, goal):
    """
    从缓存获取路径
    返回: (path, is_valid) 元组
    """
    # 实现逻辑:
    # 1. 检查缓存是否存在
    # 2. 检查是否过期
    # 3. 检查起点终点是否在阈值内
    # 4. 返回路径或 None
    pass

def cache_path(start, goal, path):
    """
    缓存路径
    """
    # 实现逻辑:
    # 1. 添加到缓存字典
    # 2. 如果超过最大数量，删除最旧的
    # 3. 记录时间戳
    pass

def clear_expired_cache():
    """
    清理过期缓存
    """
    # 实现逻辑:
    # 1. 遍历缓存
    # 2. 删除过期项
    pass
```

**改动位置 3: 修改 a_star 函数调用处**
```python
# 找到所有调用 a_star 的地方，改为:

# 原代码:
path = a_star(start, goal, obstacle_map)

# 改为:
cached_path, is_valid = get_cached_path(start, goal)
if is_valid:
    path = cached_path
else:
    path = a_star(start, goal, obstacle_map)
    if path:
        cache_path(start, goal, path)
```

**预计改动量**: 
- 新增代码: ~80 行
- 修改代码: ~5 处调用点
- 难度: ⭐⭐ (简单)

---

## 🚀 方案 2: 路径平滑

### 需要修改的文件

#### 1. 新建文件: `src/wzry_ai/utils/path_smoother.py`

**文件内容结构**:
```python
"""
路径平滑工具模块
提供多种路径平滑算法
"""

import numpy as np
from typing import List, Tuple

def smooth_path_bezier(path: List[Tuple[int, int]], 
                       obstacle_map: np.ndarray) -> List[Tuple[float, float]]:
    """
    使用贝塞尔曲线平滑路径
    
    参数:
        path: 原始路径点列表
        obstacle_map: 障碍物地图（用于碰撞检测）
    
    返回:
        平滑后的路径点列表
    """
    # 实现逻辑:
    # 1. 提取关键转折点
    # 2. 在转折点之间插入贝塞尔曲线
    # 3. 碰撞检测，确保不穿过障碍物
    # 4. 返回平滑路径
    pass

def smooth_path_spline(path: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
    """
    使用样条曲线平滑路径
    """
    # 实现逻辑:
    # 1. 使用 scipy.interpolate.splprep
    # 2. 生成平滑曲线
    # 3. 采样点
    pass

def simplify_path(path: List[Tuple[int, int]], 
                  epsilon: float = 2.0) -> List[Tuple[int, int]]:
    """
    使用 Douglas-Peucker 算法简化路径
    减少路径点数量，保持形状
    """
    # 实现逻辑:
    # 1. 递归简化
    # 2. 保留关键点
    # 3. 删除冗余点
    pass

def check_line_collision(p1: Tuple[int, int], 
                         p2: Tuple[int, int],
                         obstacle_map: np.ndarray) -> bool:
    """
    检查两点连线是否碰撞障碍物
    使用 Bresenham 直线算法
    """
    # 实现逻辑:
    # 1. Bresenham 算法生成直线上的点
    # 2. 检查每个点是否是障碍物
    # 3. 返回是否碰撞
    pass
```

**预计代码量**: ~150 行

#### 2. 修改: `src/wzry_ai/detection/model1_astar_follow.py`

**改动位置: 导入平滑模块**
```python
# 在文件顶部添加
from wzry_ai.utils.path_smoother import smooth_path_bezier, simplify_path
```

**改动位置: a_star 函数返回后**
```python
# 找到 a_star 返回路径的地方

# 原代码:
path = a_star(start, goal, obstacle_map)
if path:
    # 使用路径...

# 改为:
path = a_star(start, goal, obstacle_map)
if path:
    # 先简化路径（减少点数）
    path = simplify_path(path, epsilon=2.0)
    # 再平滑路径（视觉效果）
    path = smooth_path_bezier(path, obstacle_map)
    # 使用路径...
```

**预计改动量**:
- 新增文件: 1 个
- 修改代码: ~3 处
- 难度: ⭐⭐ (简单)

---

## 🚀 方案 3: JPS (Jump Point Search) 算法

### 需要修改的文件

#### 1. 新建文件: `src/wzry_ai/detection/jps_pathfinding.py`

**文件内容结构**:
```python
"""
JPS (Jump Point Search) 寻路算法实现
比标准 A* 快 10-100 倍
"""

import numpy as np
from heapq import heappop, heappush
from typing import List, Tuple, Optional

class JPSPathfinder:
    """JPS 寻路器类"""
    
    def __init__(self, obstacle_map: np.ndarray):
        """
        初始化
        
        参数:
            obstacle_map: 障碍物地图 (0=可通行, 1=障碍)
        """
        self.obstacle_map = obstacle_map
        self.width = obstacle_map.shape[1]
        self.height = obstacle_map.shape[0]
    
    def find_path(self, start: Tuple[int, int], 
                  goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        使用 JPS 算法寻路
        
        参数:
            start: 起点坐标 (x, y)
            goal: 终点坐标 (x, y)
        
        返回:
            路径点列表，如果无法到达返回 None
        """
        # 实现逻辑:
        # 1. 初始化开放/关闭列表
        # 2. 主循环搜索跳点
        # 3. 回溯构建路径
        pass
    
    def jump(self, x: int, y: int, dx: int, dy: int, 
             goal: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        跳点搜索核心函数
        
        参数:
            x, y: 当前位置
            dx, dy: 搜索方向
            goal: 目标位置
        
        返回:
            跳点坐标，如果没有返回 None
        """
        # 实现逻辑:
        # 1. 沿方向前进
        # 2. 检查是否是跳点
        # 3. 递归搜索
        pass
    
    def identify_successors(self, node, goal):
        """
        识别后继节点（跳点）
        """
        # 实现逻辑:
        # 1. 获取自然邻居和强制邻居
        # 2. 对每个方向调用 jump
        # 3. 返回跳点列表
        pass
    
    def get_neighbors(self, x: int, y: int, 
                      parent_x: int, parent_y: int) -> List[Tuple[int, int]]:
        """
        获取邻居节点（考虑剪枝）
        """
        # 实现逻辑:
        # 1. 根据父节点方向确定搜索方向
        # 2. 应用对称性剪枝
        # 3. 返回需要探索的邻居
        pass
    
    def has_forced_neighbor(self, x: int, y: int, 
                           dx: int, dy: int) -> bool:
        """
        检查是否有强制邻居
        """
        # 实现逻辑:
        # 1. 检查垂直方向的障碍物
        # 2. 判断是否产生强制邻居
        pass
```

**预计代码量**: ~300 行

#### 2. 修改: `src/wzry_ai/detection/model1_astar_follow.py`

**改动位置 1: 文件顶部导入**
```python
# 添加导入
from wzry_ai.detection.jps_pathfinding import JPSPathfinder

# 初始化 JPS 寻路器（全局变量）
jps_pathfinder = JPSPathfinder(obstacle_map)
```

**改动位置 2: 替换 a_star 调用**
```python
# 原代码:
path = a_star(start, goal, obstacle_map)

# 改为:
path = jps_pathfinder.find_path(start, goal)
```

**改动位置 3: 添加性能对比开关**
```python
# 在配置中添加开关
USE_JPS = True  # True=使用JPS, False=使用A*

# 调用时:
if USE_JPS:
    path = jps_pathfinder.find_path(start, goal)
else:
    path = a_star(start, goal, obstacle_map)
```

**预计改动量**:
- 新增文件: 1 个
- 修改代码: ~5 处
- 难度: ⭐⭐⭐⭐ (较难)

---

## 🚀 方案 4: 动态精度调整

### 需要修改的文件

#### 1. `src/wzry_ai/config/base.py`

**改动位置: 添加多精度配置**
```python
# 在网格配置区域添加 (约第 181 行)

# ========== 多精度网格配置 ==========
# 粗网格 (远距离快速寻路)
GRID_SIZE_COARSE = 70
CELL_SIZE_COARSE = 5.0

# 中网格 (中距离平衡)
GRID_SIZE_MEDIUM = 140
CELL_SIZE_MEDIUM = 2.5

# 细网格 (近距离精确寻路)
GRID_SIZE_FINE = 210
CELL_SIZE_FINE = 5 / 3

# 距离阈值 (格)
DISTANCE_THRESHOLD_COARSE = 150  # 超过此距离用粗网格
DISTANCE_THRESHOLD_MEDIUM = 50   # 超过此距离用中网格
```

#### 2. 新建文件: `src/wzry_ai/detection/multi_resolution_pathfinding.py`

**文件内容结构**:
```python
"""
多分辨率寻路模块
根据距离自动选择合适的网格精度
"""

import numpy as np
from typing import Tuple, List, Optional
from wzry_ai.config import (
    GRID_SIZE_COARSE, GRID_SIZE_MEDIUM, GRID_SIZE_FINE,
    CELL_SIZE_COARSE, CELL_SIZE_MEDIUM, CELL_SIZE_FINE,
    DISTANCE_THRESHOLD_COARSE, DISTANCE_THRESHOLD_MEDIUM
)

class MultiResolutionPathfinder:
    """多分辨率寻路器"""
    
    def __init__(self, map_grid_path: str):
        """
        初始化，加载多个分辨率的地图
        
        参数:
            map_grid_path: 原始地图文件路径
        """
        # 加载原始地图
        self.map_fine = np.loadtxt(map_grid_path, dtype=int)
        
        # 生成粗网格地图（下采样）
        self.map_coarse = self._downsample_map(self.map_fine, 
                                                GRID_SIZE_COARSE)
        
        # 生成中网格地图
        self.map_medium = self._downsample_map(self.map_fine, 
                                                GRID_SIZE_MEDIUM)
    
    def _downsample_map(self, original_map: np.ndarray, 
                        target_size: int) -> np.ndarray:
        """
        下采样地图到目标尺寸
        
        实现逻辑:
        1. 计算采样比例
        2. 使用最大池化（保守策略：有障碍就算障碍）
        3. 返回下采样后的地图
        """
        pass
    
    def find_path(self, start: Tuple[int, int], 
                  goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        自动选择精度并寻路
        
        实现逻辑:
        1. 计算起点到终点的距离
        2. 根据距离选择合适的网格
        3. 转换坐标到对应网格
        4. 调用寻路算法
        5. 转换路径回原始坐标
        """
        # 计算距离
        distance = self._calculate_distance(start, goal)
        
        # 选择网格
        if distance > DISTANCE_THRESHOLD_COARSE:
            # 使用粗网格
            grid_map = self.map_coarse
            cell_size = CELL_SIZE_COARSE
        elif distance > DISTANCE_THRESHOLD_MEDIUM:
            # 使用中网格
            grid_map = self.map_medium
            cell_size = CELL_SIZE_MEDIUM
        else:
            # 使用细网格
            grid_map = self.map_fine
            cell_size = CELL_SIZE_FINE
        
        # 转换坐标并寻路
        # ...
        pass
    
    def _calculate_distance(self, p1: Tuple[int, int], 
                           p2: Tuple[int, int]) -> float:
        """计算两点距离"""
        pass
    
    def _convert_coordinates(self, pos: Tuple[int, int], 
                            from_size: int, to_size: int) -> Tuple[int, int]:
        """坐标系转换"""
        pass
```

**预计代码量**: ~200 行

#### 3. 修改: `src/wzry_ai/detection/model1_astar_follow.py`

**改动位置: 替换寻路器**
```python
# 原代码:
obstacle_map = np.loadtxt(map_grid_path, dtype=int)

# 改为:
from wzry_ai.detection.multi_resolution_pathfinding import MultiResolutionPathfinder
multi_res_pathfinder = MultiResolutionPathfinder(map_grid_path)

# 调用时:
path = multi_res_pathfinder.find_path(start, goal)
```

**预计改动量**:
- 新增文件: 1 个
- 修改配置: 1 处
- 修改代码: ~3 处
- 难度: ⭐⭐⭐ (中等)

---

## 🚀 方案 5: 分层寻路

### 需要修改的文件

#### 1. 新建文件: `src/wzry_ai/detection/hierarchical_pathfinding.py`

**文件内容结构**:
```python
"""
分层寻路 (HPA*) 实现
将地图分成多个区域，先在区域间寻路，再在区域内寻路
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Set

class Cluster:
    """地图区域（簇）"""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.entrances = []  # 出入口列表
    
class AbstractGraph:
    """抽象图（区域间的连接关系）"""
    def __init__(self):
        self.nodes = {}  # 节点字典
        self.edges = {}  # 边字典
    
class HierarchicalPathfinder:
    """分层寻路器"""
    
    def __init__(self, obstacle_map: np.ndarray, cluster_size: int = 30):
        """
        初始化
        
        参数:
            obstacle_map: 障碍物地图
            cluster_size: 簇大小（像素）
        """
        self.obstacle_map = obstacle_map
        self.cluster_size = cluster_size
        
        # 预处理：构建分层结构
        self.clusters = self._build_clusters()
        self.abstract_graph = self._build_abstract_graph()
    
    def _build_clusters(self) -> List[List[Cluster]]:
        """
        将地图划分为簇
        
        实现逻辑:
        1. 按 cluster_size 划分网格
        2. 为每个簇创建 Cluster 对象
        3. 识别簇之间的出入口
        """
        pass
    
    def _build_abstract_graph(self) -> AbstractGraph:
        """
        构建抽象图
        
        实现逻辑:
        1. 为每个出入口创建抽象节点
        2. 计算同一簇内出入口之间的路径
        3. 构建抽象边
        """
        pass
    
    def find_path(self, start: Tuple[int, int], 
                  goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        分层寻路
        
        实现逻辑:
        1. 将起点和终点插入抽象图
        2. 在抽象图上寻路（快速）
        3. 细化路径（在每个簇内寻路）
        4. 合并路径
        """
        pass
    
    def _insert_node(self, pos: Tuple[int, int]) -> str:
        """将节点临时插入抽象图"""
        pass
    
    def _refine_path(self, abstract_path: List[str]) -> List[Tuple[int, int]]:
        """细化抽象路径为具体路径"""
        pass
```

**预计代码量**: ~400 行

#### 2. 修改: `src/wzry_ai/detection/model1_astar_follow.py`

**改动位置: 初始化分层寻路器**
```python
# 在全局初始化区域
from wzry_ai.detection.hierarchical_pathfinding import HierarchicalPathfinder

# 初始化（只需一次，预处理）
hierarchical_pathfinder = HierarchicalPathfinder(obstacle_map, cluster_size=30)

# 使用时:
path = hierarchical_pathfinder.find_path(start, goal)
```

**预计改动量**:
- 新增文件: 1 个
- 修改代码: ~3 处
- 难度: ⭐⭐⭐⭐⭐ (困难)

---

## 📊 配置文件改动汇总

### `src/wzry_ai/config/base.py`

需要添加的配置项：

```python
# ========== 寻路优化配置 ==========

# 路径缓存
ENABLE_PATH_CACHE = True
PATH_CACHE_MAX_SIZE = 20
PATH_CACHE_EXPIRE_TIME = 2.0
PATH_CACHE_POSITION_THRESHOLD = 5

# 路径平滑
ENABLE_PATH_SMOOTHING = True
PATH_SIMPLIFY_EPSILON = 2.0

# JPS 算法
USE_JPS_ALGORITHM = False  # 默认关闭，测试后开启

# 多分辨率
ENABLE_MULTI_RESOLUTION = False
DISTANCE_THRESHOLD_COARSE = 150
DISTANCE_THRESHOLD_MEDIUM = 50

# 分层寻路
ENABLE_HIERARCHICAL = False
CLUSTER_SIZE = 30

# 性能监控
ENABLE_PATHFINDING_PROFILING = True  # 记录寻路性能
```

---

## 🧪 测试文件

### 新建: `tests/test_pathfinding.py`

```python
"""
寻路算法测试套件
"""

import time
import numpy as np
from wzry_ai.detection.model1_astar_follow import a_star
from wzry_ai.detection.jps_pathfinding import JPSPathfinder
# ... 其他导入

def test_short_distance():
    """测试短距离寻路"""
    pass

def test_long_distance():
    """测试长距离寻路"""
    pass

def test_cache_hit_rate():
    """测试缓存命中率"""
    pass

def benchmark_algorithms():
    """性能基准测试"""
    # 对比 A*, JPS, 分层等算法的性能
    pass

def test_path_quality():
    """测试路径质量"""
    # 确保优化后路径长度不会明显增加
    pass
```

---

## 📝 实施顺序建议

### 第 1 步: 路径缓存 (1 天)
- [ ] 修改 `model1_astar_follow.py` 添加缓存
- [ ] 添加配置项到 `config/base.py`
- [ ] 测试缓存命中率
- [ ] 性能对比

### 第 2 步: 路径平滑 (1 天)
- [ ] 创建 `utils/path_smoother.py`
- [ ] 集成到 `model1_astar_follow.py`
- [ ] 视觉效果测试
- [ ] 碰撞检测验证

### 第 3 步: JPS 算法 (3-5 天)
- [ ] 创建 `detection/jps_pathfinding.py`
- [ ] 实现核心 JPS 逻辑
- [ ] 单元测试
- [ ] 性能基准测试
- [ ] 集成到主流程
- [ ] A/B 测试

### 第 4 步: 动态精度 (2-3 天)
- [ ] 创建 `detection/multi_resolution_pathfinding.py`
- [ ] 实现地图下采样
- [ ] 实现自动精度选择
- [ ] 测试不同距离场景
- [ ] 集成到主流程

### 第 5 步: 分层寻路 (5-7 天)
- [ ] 创建 `detection/hierarchical_pathfinding.py`
- [ ] 实现簇划分
- [ ] 实现抽象图构建
- [ ] 实现分层寻路
- [ ] 预处理优化
- [ ] 全面测试

---

## 🔍 验证清单

每个方案实施后需要验证：

### 功能验证
- [ ] 路径正确性（起点到终点）
- [ ] 避障正确性（不穿墙）
- [ ] 边界情况处理（起点=终点等）
- [ ] 异常情况处理（无法到达等）

### 性能验证
- [ ] 短距离寻路时间
- [ ] 长距离寻路时间
- [ ] 内存占用
- [ ] 帧率影响

### 质量验证
- [ ] 路径长度（不应明显增加）
- [ ] 路径平滑度
- [ ] 视觉效果
- [ ] 用户体验

---

## 📦 依赖包

可能需要添加的依赖（在 `requirements.txt` 中）：

```txt
# 路径平滑可能需要
scipy>=1.9.0  # 用于样条插值

# 性能分析
line_profiler  # 代码性能分析
memory_profiler  # 内存分析
```

---

## 🎯 总结

### 最小改动方案（快速见效）
1. 路径缓存：修改 1 个文件，新增 ~80 行代码
2. 路径平滑：新增 1 个文件，修改 1 个文件

### 中等改动方案（显著提升）
3. JPS 算法：新增 1 个文件 (~300 行)，修改 1 个文件
4. 动态精度：新增 1 个文件 (~200 行)，修改 2 个文件

### 大型改动方案（架构升级）
5. 分层寻路：新增 1 个文件 (~400 行)，修改 1 个文件

**推荐路径**: 1 → 2 → 3，这样可以在最小风险下获得最大收益。
