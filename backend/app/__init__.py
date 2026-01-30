"""应用初始化模块"""
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.middleware import (
    setup_cors,
    setup_logging_middleware,
    setup_exception_handlers
)
from loguru import logger
import sys


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例"""
    settings = get_settings()

    # 配置日志
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
               "<level>{message}</level>"
    )
    logger.add(
        settings.LOG_FILE,
        rotation="500 MB",
        retention="10 days",
        level=settings.LOG_LEVEL
    )

    # 创建应用
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json"
    )

    # 配置中间件
    setup_cors(app, settings.CORS_ORIGINS)
    setup_logging_middleware(app)
    setup_exception_handlers(app)

    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} 初始化完成")

    return app
