from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate


class CRUDAdmin(CRUDBase[Admin, AdminCreate, AdminUpdate]):
    """管理员CRUD操作"""
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[Admin]:
        """根据用户名获取管理员"""
        return db.query(Admin).filter(Admin.username == username).first()
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[Admin]:
        """根据邮箱获取管理员"""
        return db.query(Admin).filter(Admin.email == email).first()
    
    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[Admin]:
        """验证管理员账号密码"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        admin = self.get_by_username(db, username=username)
        if not admin:
            return None
        if not pwd_context.verify(password, admin.password_hash):
            return None
        return admin
    
    def create_with_password(self, db: Session, *, obj_in: AdminCreate) -> Admin:
        """创建管理员（加密密码）"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        hashed_password = pwd_context.hash(obj_in.password)
        db_obj = Admin(
            username=obj_in.username,
            email=obj_in.email,
            password_hash=hashed_password
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


admin = CRUDAdmin(Admin)