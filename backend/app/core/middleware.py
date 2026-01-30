from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
import time
from typing import Callable


def setup_cors(app: FastAPI, origins: list) -> None:
    """配置 CORS 中间件"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_logging_middleware(app: FastAPI) -> None:
    """配置日志中间件"""

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID", "unknown")
        start_time = time.time()

        logger.info(
            f"Request started: {request.method} {request.url.path} "
            f"[RequestID: {request_id}]"
        )

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"[Status: {response.status_code}] "
            f"[Duration: {process_time:.3f}s] "
            f"[RequestID: {request_id}]"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response


def setup_exception_handlers(app: FastAPI) -> None:
    """配置全局异常处理"""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """处理请求验证错误"""
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "请求参数验证失败",
                "details": exc.errors(),
                "message": "请检查您的请求参数是否正确"
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理通用异常"""
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "服务器内部错误",
                "message": "抱歉，服务器遇到了问题，请稍后重试"
            }
        )
