#!/usr/bin/env python3

"""
测试后端日志系统
"""

import sys
import os
import time

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.core.logger import app_logger, api_logger, auth_logger, monitoring_logger

def test_backend_logging():
    """测试后端日志系统"""
    print("🧪 Testing Backend Logging System...")
    print("=" * 50)
    
    # 测试不同级别的日志
    app_logger.debug("This is a DEBUG message")
    app_logger.info("This is an INFO message")
    app_logger.warn("This is a WARN message")
    app_logger.error("This is an ERROR message")
    
    # 测试不同模块的日志
    api_logger.info("API module test message")
    auth_logger.info("Auth module test message")  
    monitoring_logger.info("Monitoring module test message")
    
    # 测试带数据的日志
    app_logger.info("Test with data", extra={'test_data': {'key': 'value', 'number': 123}})
    
    # 测试错误日志（带异常）
    try:
        raise ValueError("This is a test exception")
    except Exception as e:
        app_logger.error("Test exception logging", exc_info=True)
    
    print("\n✅ Backend logging test completed!")
    print("Check the following log files:")
    print("- backend/logs/app.log")
    print("- backend/logs/error.log") 
    print("- backend/logs/daily.log")

if __name__ == "__main__":
    test_backend_logging()