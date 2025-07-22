#!/usr/bin/env python3
"""
任务2测试总结脚本
对数据库模型和数据层设计的完整测试和验证
"""

import asyncio
import sys
import os
import subprocess
sys.path.insert(0, os.path.dirname(__file__))

def run_test_script(script_name, description):
    """运行测试脚本并返回结果"""
    print(f"\n{'='*60}")
    print(f"运行 {description}")
    print(f"{'='*60}")
    
    try:
        # 激活虚拟环境并运行脚本
        cmd = f"source .env/bin/activate && python {script_name}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print("警告/错误信息:")
            print(result.stderr)
        
        success = result.returncode == 0
        return success
        
    except subprocess.TimeoutExpired:
        print(f"❌ {description} 超时")
        return False
    except Exception as e:
        print(f"❌ {description} 执行失败: {e}")
        return False

def main():
    """运行所有Task 2相关的测试"""
    print("🚀 开始Task 2 - 数据库模型和数据层设计的综合测试")
    print("测试包括：数据库连接、模型定义、CRUD操作、关系映射、API端点")
    
    test_results = {}
    
    # 1. 基础数据库和CRUD测试
    test_results['基础数据库CRUD测试'] = run_test_script(
        'test_db.py', 
        '基础数据库CRUD测试 (test_db.py)'
    )
    
    # 2. 模型关系测试
    test_results['模型关系测试'] = run_test_script(
        'test_relationships.py', 
        '模型关系测试 (test_relationships.py)'
    )
    
    # 3. API端点测试
    test_results['API端点测试'] = run_test_script(
        'test_api.py', 
        'API端点测试 (test_api.py)'
    )
    
    # 总结测试结果
    print(f"\n{'='*60}")
    print("Task 2 测试结果总结")
    print(f"{'='*60}")
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, success in test_results.items():
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        if success:
            passed_tests += 1
    
    print(f"\n总体结果: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("\n🎉 Task 2 - 数据库模型和数据层设计 - 全部测试通过！")
        print("\n✅ 已验证的功能：")
        print("   • SQLAlchemy ORM模型定义正确")
        print("   • 数据库连接和会话管理正常")
        print("   • 所有模型的CRUD操作工作正常") 
        print("   • 模型之间的关联关系正确")
        print("   • 数据验证和约束生效")
        print("   • API接口基础框架工作正常")
        print("   • 数据库初始化和表创建成功")
        
        print("\n📋 Task 2 实现的组件：")
        print("   • 管理员模型 (Admin) - 用户认证")
        print("   • 客户端模型 (Client) - 设备管理")
        print("   • 升级包模型 (UpgradePackage) - 版本管理")
        print("   • 升级任务模型 (UpgradeTask) - 任务跟踪")
        print("   • 完整的CRUD操作层")
        print("   • Pydantic Schema验证")
        print("   • FastAPI基础框架")
        
        return True
    else:
        print(f"\n⚠️  Task 2 测试未全部通过，有 {total_tests - passed_tests} 项失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)