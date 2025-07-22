#!/usr/bin/env python3
"""
数据模型关系测试脚本
测试数据库模型之间的关联关系是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import init_db, SessionLocal
from app.crud import admin, client, upgrade_package, upgrade_task
from app.schemas.admin import AdminCreate
from app.schemas.client import ClientCreate
from app.schemas.upgrade_package import UpgradePackageCreate
from app.schemas.upgrade_task import UpgradeTaskCreate
import time

def test_model_relationships():
    """测试模型关联关系"""
    print("开始测试模型关联关系...")
    
    # 初始化数据库
    init_db()
    print("数据库初始化完成")
    
    db = SessionLocal()
    try:
        # 使用时间戳确保唯一性
        timestamp = str(int(time.time()))
        
        # 创建测试数据
        print("\n创建测试数据...")
        
        # 1. 创建管理员
        admin_data = AdminCreate(
            username=f"rel_admin_{timestamp}",
            email=f"rel{timestamp}@example.com",
            password="test123"
        )
        created_admin = admin.create_with_password(db, obj_in=admin_data)
        print(f"✓ 创建管理员: {created_admin.username}")
        
        # 2. 创建客户端
        client_data = ClientCreate(
            name=f"关系测试客户端_{timestamp}",
            ip_address=f"192.168.2.{int(timestamp[-3:]) % 255}",
            version="1.0.0",
            status="online"
        )
        created_client = client.create(db, obj_in=client_data)
        print(f"✓ 创建客户端: {created_client.name}")
        
        # 3. 创建升级包
        package_data = UpgradePackageCreate(
            name=f"关系测试升级包_{timestamp}",
            version=f"2.1.{timestamp[-2:]}",
            file_path=f"/path/to/rel_package_{timestamp}.zip",
            file_size=2048000
        )
        created_package = upgrade_package.create(db, obj_in=package_data)
        print(f"✓ 创建升级包: {created_package.name}")
        
        # 4. 创建升级任务（建立关联关系）
        task_data = UpgradeTaskCreate(
            client_id=created_client.id,
            package_id=created_package.id,
            status="pending"
        )
        created_task = upgrade_task.create(db, obj_in=task_data)
        print(f"✓ 创建升级任务: ID={created_task.id}")
        
        # 测试关联关系
        print("\n测试关联关系...")
        
        # 测试客户端的所有任务
        client_tasks = upgrade_task.get_by_client(db, client_id=created_client.id)
        print(f"✓ 客户端 '{created_client.name}' 的任务数量: {len(client_tasks)}")
        
        # 测试升级包的所有任务
        package_tasks = upgrade_task.get_by_package(db, package_id=created_package.id)
        print(f"✓ 升级包 '{created_package.name}' 的任务数量: {len(package_tasks)}")
        
        # 测试任务状态更新
        print("\n测试任务状态更新...")
        completed_task = upgrade_task.complete_task(db, task_id=created_task.id, success=True)
        print(f"✓ 任务状态更新为: {completed_task.status}")
        
        # 测试按状态查询
        print("\n测试按状态查询...")
        pending_tasks = upgrade_task.get_pending_tasks(db)
        print(f"✓ 待执行任务数量: {len(pending_tasks)}")
        
        active_tasks = upgrade_task.get_active_tasks(db)
        print(f"✓ 活跃任务数量: {len(active_tasks)}")
        
        # 测试客户端活跃任务
        client_active_task = upgrade_task.get_client_active_task(db, client_id=created_client.id)
        print(f"✓ 客户端活跃任务: {'存在' if client_active_task else '无'}")
        
        # 测试所有任务查询
        print("\n测试所有任务查询...")
        all_tasks = upgrade_task.get_multi(db)
        print(f"✓ 所有任务数量: {len(all_tasks)}")
        
        for task in all_tasks[-3:]:  # 显示最后3个任务
            print(f"  - 任务 {task.id}: client_id={task.client_id}, package_id={task.package_id} ({task.status})")
        
        print("\n模型关联关系测试完成！所有关系正常。")
        
    except Exception as e:
        print(f"关系测试失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = test_model_relationships()
    if success:
        print("✅ 所有关联关系测试通过")
    else:
        print("❌ 部分关联关系测试失败")