#!/usr/bin/env python
"""测试运行脚本 - 提供多种测试运行选项"""

import sys
import subprocess
from pathlib import Path


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("运行所有测试...")
    print("=" * 60)
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
    return result.returncode


def run_unit_tests():
    """只运行单元测试"""
    print("=" * 60)
    print("运行单元测试...")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests/", 
        "-v", "-m", "unit"
    ])
    return result.returncode


def run_integration_tests():
    """只运行集成测试"""
    print("=" * 60)
    print("运行集成测试...")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests/", 
        "-v", "-m", "integration"
    ])
    return result.returncode


def run_with_coverage():
    """运行测试并生成覆盖率报告"""
    print("=" * 60)
    print("运行测试并生成覆盖率报告...")
    print("=" * 60)
    
    # 检查pytest-cov是否安装
    try:
        import pytest_cov
    except ImportError:
        print("警告: pytest-cov未安装，无法生成覆盖率报告")
        print("请运行: pip install pytest-cov")
        return 1
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests/",
        "--cov=src/wzry_ai",
        "--cov-report=html",
        "--cov-report=term-missing",
        "-v"
    ])
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("覆盖率报告已生成: htmlcov/index.html")
        print("=" * 60)
    
    return result.returncode


def run_specific_test(test_path):
    """运行特定测试文件或测试函数"""
    print("=" * 60)
    print(f"运行测试: {test_path}")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, "-m", "pytest", test_path, "-v"
    ])
    return result.returncode


def run_fast_tests():
    """运行快速测试（排除慢速测试）"""
    print("=" * 60)
    print("运行快速测试（排除慢速测试）...")
    print("=" * 60)
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests/",
        "-v", "-m", "not slow"
    ])
    return result.returncode


def show_help():
    """显示帮助信息"""
    print("""
测试运行脚本使用说明
==================

用法: python run_tests.py [选项]

选项:
  all           运行所有测试（默认）
  unit          只运行单元测试
  integration   只运行集成测试
  coverage      运行测试并生成覆盖率报告
  fast          运行快速测试（排除慢速测试）
  <test_path>   运行特定测试文件或函数
  help          显示此帮助信息

示例:
  python run_tests.py                          # 运行所有测试
  python run_tests.py unit                     # 只运行单元测试
  python run_tests.py coverage                 # 生成覆盖率报告
  python run_tests.py tests/test_config.py     # 运行特定测试文件
  python run_tests.py tests/test_config.py::TestConfigConstants::test_grid_size  # 运行特定测试

注意:
  - 确保已安装pytest: pip install pytest
  - 覆盖率报告需要pytest-cov: pip install pytest-cov
  - 测试前会自动设置PYTHONPATH
""")


def main():
    """主函数"""
    # 设置PYTHONPATH
    project_root = Path(__file__).parent
    src_path = project_root / "src"
    import os
    os.environ["PYTHONPATH"] = str(src_path)
    
    # 解析命令行参数
    if len(sys.argv) == 1:
        # 默认运行所有测试
        return run_all_tests()
    
    command = sys.argv[1].lower()
    
    if command == "all":
        return run_all_tests()
    elif command == "unit":
        return run_unit_tests()
    elif command == "integration":
        return run_integration_tests()
    elif command == "coverage":
        return run_with_coverage()
    elif command == "fast":
        return run_fast_tests()
    elif command == "help" or command == "-h" or command == "--help":
        show_help()
        return 0
    else:
        # 假设是测试路径
        return run_specific_test(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
