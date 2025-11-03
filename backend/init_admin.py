#!/usr/bin/env python
"""初始化管理员用户"""

from app.database import SessionLocal
from app.models.user import User
from app.utils.password import hash_password

def init_admin():
    """创建初始管理员用户"""
    db = SessionLocal()
    
    try:
        # 检查是否已存在管理员
        admin = db.query(User).filter(User.is_admin == True).first()
        if admin:
            print(f"✅ 管理员已存在: {admin.username} ({admin.email})")
            return
        
        # 创建管理员用户
        admin_user = User(
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("admin123456"),
            is_active=True,
            is_admin=True,
            role="superadmin",
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ 管理员用户创建成功")
        print(f"   用户名: admin")
        print(f"   邮箱: admin@example.com")
        print(f"   密码: admin123456")
        print(f"   角色: superadmin")
        
    except Exception as e:
        print(f"❌ 创建管理员失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_admin()

