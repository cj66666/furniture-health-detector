from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类"""

    # 应用配置
    APP_NAME: str = "家具健康检测器"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://your-miniprogram-domain.com"
    ]

    # Qwen-VL API (通过 OpenAI SDK)
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://aiping.cn/api/v1"
    QWEN_MODEL_NAME: str = "Qwen3-VL-30B-A3B-Instruct"

    # 阿里云 OSS
    OSS_ACCESS_KEY_ID: str
    OSS_ACCESS_KEY_SECRET: str
    OSS_ENDPOINT: str = "oss-cn-hangzhou.aliyuncs.com"
    OSS_BUCKET_NAME: str = "furniture-health-detector"
    OSS_IMAGE_EXPIRE_DAYS: int = 7

    # 图片处理配置
    MAX_IMAGE_SIZE_MB: int = 10
    IMAGE_QUALITY: int = 85
    MIN_IMAGE_RESOLUTION: int = 800

    # API 调用配置
    QWEN_VL_MAX_RETRIES: int = 3
    QWEN_VL_RETRY_DELAY: float = 1.0
    QWEN_VL_TIMEOUT: int = 30

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Redis 配置 (可选)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # MongoDB 配置 (可选)
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "furniture_health"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
