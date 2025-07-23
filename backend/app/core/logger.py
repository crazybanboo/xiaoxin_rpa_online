import logging
import logging.config
import os
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

from app.core.config import settings


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[35m',   # 紫色
        'RESET': '\033[0m'        # 重置颜色
    }
    
    def format(self, record):
        # 添加颜色
        levelname = record.levelname
        if levelname in self.COLORS:
            colored_levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
            record.levelname = colored_levelname
        
        # 格式化日志
        formatted = super().format(record)
        
        # 恢复原始levelname，避免影响其他处理器
        record.levelname = levelname
        
        return formatted


class LoggerManager:
    """日志管理器"""
    
    def __init__(self):
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志配置"""
        # 日志级别
        log_level = getattr(settings, 'LOG_LEVEL', 'INFO').upper()
        
        # 创建根日志器
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level))
        
        # 清除已有的处理器
        root_logger.handlers.clear()
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level))
        
        # 控制台格式化器（带颜色）
        console_formatter = ColoredFormatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # 文件处理器 - 按大小滚动
        file_handler = RotatingFileHandler(
            filename=self.log_dir / "app.log",
            maxBytes=getattr(settings, 'LOG_FILE_MAX_SIZE', 10 * 1024 * 1024),
            backupCount=getattr(settings, 'LOG_FILE_BACKUP_COUNT', 5),
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, log_level))
        
        # 文件格式化器（不带颜色）
        file_formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # 错误日志处理器 - 单独记录ERROR及以上级别
        error_handler = RotatingFileHandler(
            filename=self.log_dir / "error.log",
            maxBytes=getattr(settings, 'LOG_FILE_MAX_SIZE', 10 * 1024 * 1024),
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        
        # 按时间滚动的处理器 - 每日一个文件
        daily_handler = TimedRotatingFileHandler(
            filename=self.log_dir / "daily.log",
            when='midnight',
            interval=1,
            backupCount=getattr(settings, 'LOG_DAILY_BACKUP_COUNT', 30),
            encoding='utf-8'
        )
        daily_handler.setLevel(getattr(logging, log_level))
        daily_handler.setFormatter(file_formatter)
        
        # 添加处理器到根日志器
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(daily_handler)
        
        # 设置第三方库的日志级别
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
        
    def get_logger(self, name: str) -> logging.Logger:
        """获取指定名称的日志器"""
        return logging.getLogger(name)
    
    def set_level(self, level: str):
        """动态设置日志级别"""
        level_obj = getattr(logging, level.upper())
        root_logger = logging.getLogger()
        root_logger.setLevel(level_obj)
        
        # 更新所有处理器的级别（除了错误处理器）
        for handler in root_logger.handlers:
            if not isinstance(handler, type(root_logger.handlers[2])):  # 不是error_handler
                handler.setLevel(level_obj)


# 全局日志管理器实例
logger_manager = LoggerManager()

# 便捷函数
def get_logger(name: str = None) -> logging.Logger:
    """获取日志器"""
    if name is None:
        # 获取调用者的模块名
        import inspect
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', 'unknown')
    
    return logger_manager.get_logger(name)


# 导出常用的日志器
app_logger = get_logger('app')
api_logger = get_logger('api')
db_logger = get_logger('database')
auth_logger = get_logger('auth')
websocket_logger = get_logger('websocket')
monitoring_logger = get_logger('monitoring')