import asyncio
from datetime import datetime, timedelta
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud.crud_client import client as client_crud
from app.websocket.websocket_manager import WebSocketManager, MessageType
from app.core.config import settings
from app.core.logger import monitoring_logger


class ClientMonitoringService:
    """Service for monitoring client heartbeats and updating their status"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.ws_manager = WebSocketManager()
        self.heartbeat_timeout = getattr(settings, 'HEARTBEAT_TIMEOUT_SECONDS', 60)
        self.check_interval = getattr(settings, 'HEARTBEAT_CHECK_INTERVAL_SECONDS', 30)
        
    async def check_client_heartbeats(self):
        """Check all clients for heartbeat timeout and update their status"""
        # Run synchronous database operations in a thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._check_heartbeats_sync)
    
    def _check_heartbeats_sync(self):
        """Synchronous method to check heartbeats"""
        db = SessionLocal()
        try:
            # Get all online clients
            online_clients = client_crud.get_by_status(db, status="online")
            
            # Current time
            now = datetime.utcnow()
            timeout_threshold = now - timedelta(seconds=self.heartbeat_timeout)
            
            # Check each client
            for client in online_clients:
                if client.last_heartbeat and client.last_heartbeat < timeout_threshold:
                    # Mark client as offline
                    self._mark_client_offline_sync(db, client.id)
                    monitoring_monitoring_logger.info(f"Client {client.id} marked as offline due to heartbeat timeout")
                    
        except Exception as e:
            monitoring_logger.error(f"Error during heartbeat monitoring: {str(e)}")
        finally:
            db.close()
    
    def _mark_client_offline_sync(self, db: Session, client_id: int):
        """Mark a client as offline synchronously"""
        try:
            # Get the client
            client = client_crud.get(db, client_id)
            if not client:
                return
            
            # Update client status in database
            updated_client = client_crud.update(
                db, 
                db_obj=client,
                obj_in={"status": "offline"}
            )
            
            # Send WebSocket notification (async)
            asyncio.create_task(self._send_offline_notification(updated_client))
                
        except Exception as e:
            monitoring_logger.error(f"Error marking client {client_id} as offline: {str(e)}")
    
    async def _send_offline_notification(self, client):
        """Send WebSocket notification for offline client"""
        try:
            await self.ws_manager.broadcast_to_topic(
                "client_status",
                {
                    "type": MessageType.CLIENT_STATUS_UPDATE.value,
                    "data": {
                        "client_id": client.id,
                        "name": client.name,
                        "status": "offline",
                        "last_heartbeat": client.last_heartbeat.isoformat() if client.last_heartbeat else None,
                        "reason": "heartbeat_timeout"
                    }
                }
            )
        except Exception as e:
            monitoring_logger.error(f"Error sending offline notification for client {client.id}: {str(e)}")
    
    def start(self):
        """Start the monitoring service"""
        try:
            # Add the heartbeat check job
            self.scheduler.add_job(
                self.check_client_heartbeats,
                trigger=IntervalTrigger(seconds=self.check_interval),
                id="heartbeat_monitor",
                name="Client Heartbeat Monitor",
                replace_existing=True
            )
            
            # Start the scheduler
            self.scheduler.start()
            monitoring_logger.info(f"Client monitoring service started (interval: {self.check_interval}s, timeout: {self.heartbeat_timeout}s)")
            
        except Exception as e:
            monitoring_logger.error(f"Failed to start monitoring service: {str(e)}")
            raise
    
    def stop(self):
        """Stop the monitoring service"""
        try:
            self.scheduler.shutdown(wait=True)
            monitoring_logger.info("Client monitoring service stopped")
        except Exception as e:
            monitoring_logger.error(f"Error stopping monitoring service: {str(e)}")


# Global instance
monitoring_service = ClientMonitoringService()