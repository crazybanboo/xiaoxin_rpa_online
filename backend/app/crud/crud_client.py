from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    """客户端CRUD操作"""
    
    def get_by_ip(self, db: Session, *, ip_address: str) -> Optional[Client]:
        """根据IP地址获取客户端"""
        return db.query(Client).filter(Client.ip_address == ip_address).first()
    
    def get_by_status(self, db: Session, *, status: str) -> List[Client]:
        """根据状态获取客户端列表"""
        return db.query(Client).filter(Client.status == status).all()
    
    def get_online_clients(self, db: Session) -> List[Client]:
        """获取在线客户端列表"""
        return self.get_by_status(db, status="online")
    
    def get_recent_heartbeat(self, db: Session, *, limit: int = 10) -> List[Client]:
        """获取最近心跳的客户端"""
        return (
            db.query(Client)
            .filter(Client.last_heartbeat.isnot(None))
            .order_by(desc(Client.last_heartbeat))
            .limit(limit)
            .all()
        )
    
    def update_heartbeat(self, db: Session, *, client_id: int) -> Optional[Client]:
        """更新客户端心跳时间"""
        from datetime import datetime
        
        client = self.get(db, client_id)
        if client:
            client.last_heartbeat = datetime.utcnow()
            client.status = "online"
            db.add(client)
            db.commit()
            db.refresh(client)
        return client


client = CRUDClient(Client)