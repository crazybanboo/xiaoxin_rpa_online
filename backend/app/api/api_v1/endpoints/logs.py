from typing import Any
import os
import json
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


class FrontendLogEntry(BaseModel):
    timestamp: str
    level: str
    logger: str
    message: str
    data: Any = None
    stack: str = None
    url: str = None
    userAgent: str = None
    logLine: str


class FrontendLogger:
    """前端日志文件管理器"""
    
    def __init__(self):
        # 创建前端日志目录
        self.log_dir = Path("frontend/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置文件处理器
        self.setup_file_handlers()
    
    def setup_file_handlers(self):
        """设置文件处理器"""
        # 应用日志文件处理器
        self.app_handler = RotatingFileHandler(
            filename=self.log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # 错误日志文件处理器
        self.error_handler = RotatingFileHandler(
            filename=self.log_dir / "error.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=3,
            encoding='utf-8'
        )
        
        # 每日日志文件处理器
        from logging.handlers import TimedRotatingFileHandler
        self.daily_handler = TimedRotatingFileHandler(
            filename=self.log_dir / "daily.log",
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8'
        )
    
    def write_log(self, log_entry: FrontendLogEntry):
        """写入日志到文件"""
        try:
            # 写入应用日志
            with open(self.log_dir / "app.log", "a", encoding='utf-8') as f:
                f.write(log_entry.logLine + "\n")
            
            # 如果是错误级别，也写入错误日志
            if log_entry.level.upper() == "ERROR":
                with open(self.log_dir / "error.log", "a", encoding='utf-8') as f:
                    f.write(log_entry.logLine + "\n")
            
            # 写入每日日志
            with open(self.log_dir / "daily.log", "a", encoding='utf-8') as f:
                f.write(log_entry.logLine + "\n")
                
        except Exception as e:
            logger.error(f"Failed to write frontend log to file: {e}")
            raise


# 全局前端日志管理器实例
frontend_logger = FrontendLogger()


@router.post("/frontend")
async def save_frontend_log(log_entry: FrontendLogEntry):
    """
    保存前端日志到文件
    """
    try:
        # 记录后端接收到前端日志的信息
        logger.debug(f"Received frontend log: {log_entry.level} - {log_entry.message}")
        
        # 写入前端日志文件
        frontend_logger.write_log(log_entry)
        
        return {"status": "success", "message": "Log saved successfully"}
        
    except Exception as e:
        logger.error(f"Failed to save frontend log: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save log: {str(e)}")


@router.get("/frontend/stats")
async def get_frontend_log_stats():
    """
    获取前端日志统计信息
    """
    try:
        log_dir = Path("frontend/logs")
        
        stats = {
            "files": {},
            "total_size": 0
        }
        
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                file_stats = log_file.stat()
                stats["files"][log_file.name] = {
                    "size": file_stats.st_size,
                    "modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                    "lines": sum(1 for _ in open(log_file, 'r', encoding='utf-8', errors='ignore'))
                }
                stats["total_size"] += file_stats.st_size
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get frontend log stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get log stats: {str(e)}")


@router.get("/frontend/{filename}")
async def get_frontend_log_file(filename: str, lines: int = 100):
    """
    获取前端日志文件内容
    """
    try:
        log_file = Path("frontend/logs") / filename
        
        if not log_file.exists():
            raise HTTPException(status_code=404, detail="Log file not found")
        
        # 读取最后N行
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return {
            "filename": filename,
            "total_lines": len(all_lines),
            "returned_lines": len(recent_lines),
            "content": "".join(recent_lines)
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Log file not found")
    except Exception as e:
        logger.error(f"Failed to read frontend log file {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read log file: {str(e)}")