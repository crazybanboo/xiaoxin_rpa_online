#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表和初始数据
"""

from app.core.database import init_db, SessionLocal
from app.crud import admin
from app.schemas.admin import AdminCreate


def create_initial_admin():
    """创建初始管理员账号"""
    db = SessionLocal()
    try:
        # 检查是否已有管理员
        existing_admin = admin.get_by_username(db, username="admin")
        if existing_admin:
            print("初始管理员已存在，跳过创建")
            return
        
        # 创建默认管理员
        admin_in = AdminCreate(
            username="admin",
            email="admin@xiaoxin-rpa.com",
            password="admin123"  # 生产环境应该使用强密码
        )
        
        created_admin = admin.create_with_password(db, obj_in=admin_in)
        print(f"创建初始管理员成功: {created_admin.username}")
        
    except Exception as e:
        print(f"创建初始管理员失败: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """主函数"""
    print("开始初始化数据库...")
    
    # 创建所有表
    init_db()
    print("数据库表创建完成")
    
    # 创建初始数据
    create_initial_admin()
    
    print("数据库初始化完成！")


if __name__ == "__main__":
    main()