from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "小新RPA在线平台"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = "sqlite:///./xiaoxin_rpa.db"

    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Client Monitoring
    HEARTBEAT_TIMEOUT_SECONDS: int = 60  # 客户端心跳超时时间（秒）
    HEARTBEAT_CHECK_INTERVAL_SECONDS: int = 30  # 心跳检查间隔（秒）
    
    # Logging
    LOG_LEVEL: str = "INFO"  # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE_MAX_SIZE: int = 10 * 1024 * 1024  # 日志文件最大大小（字节）
    LOG_FILE_BACKUP_COUNT: int = 5  # 保留的日志文件数量
    LOG_DAILY_BACKUP_COUNT: int = 30  # 每日日志保留天数

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()