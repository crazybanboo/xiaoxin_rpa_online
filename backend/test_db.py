#!/usr/bin/env python3
"""
数据库测试脚本
验证数据库模型和CRUD操作是否正常工作
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


def test_database():
    """测试数据库操作"""
    print("开始测试数据库...")
    
    # 初始化数据库
    init_db()
    print("数据库初始化完成")
    
    db = SessionLocal()
    try:
        # 测试管理员CRUD
        print("\n测试管理员CRUD操作...")
        admin_data = AdminCreate(
            username="test_admin",
            email="test@example.com",
            password="test123"
        )
        created_admin = admin.create_with_password(db, obj_in=admin_data)
        print(f"创建管理员: {created_admin}")
        
        # 测试客户端CRUD
        print("\n测试客户端CRUD操作...")
        client_data = ClientCreate(
            name="测试客户端",
            ip_address="192.168.1.100",
            version="1.0.0",
            status="online"
        )
        created_client = client.create(db, obj_in=client_data)
        print(f"创建客户端: {created_client}")
        
        # 测试升级包CRUD
        print("\n测试升级包CRUD操作...")
        package_data = UpgradePackageCreate(
            name="测试升级包",
            version="2.0.0",
            file_path="/path/to/package.zip",
            file_size=1024000
        )
        created_package = upgrade_package.create(db, obj_in=package_data)
        print(f"创建升级包: {created_package}")
        
        # 测试升级任务CRUD
        print("\n测试升级任务CRUD操作...")
        task_data = UpgradeTaskCreate(
            client_id=created_client.id,
            package_id=created_package.id,
            status="pending"
        )
        created_task = upgrade_task.create(db, obj_in=task_data)
        print(f"创建升级任务: {created_task}")
        
        # 测试查询操作
        print("\n测试查询操作...")
        all_clients = client.get_multi(db)
        print(f"所有客户端: {len(all_clients)} 个")
        
        client_by_ip = client.get_by_ip(db, ip_address="192.168.1.100")
        print(f"IP查询客户端: {client_by_ip}")
        
        client_tasks = upgrade_task.get_by_client(db, client_id=created_client.id)
        print(f"客户端任务: {len(client_tasks)} 个")
        
        print("\n数据库测试完成！所有操作正常。")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_database()