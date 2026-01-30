from app import create_app
from app.core.config import get_settings
from app.api.v1 import furniture, share

app = create_app()
settings = get_settings()

# 注册路由
app.include_router(furniture.router, prefix="/api/v1")
app.include_router(share.router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/api/v1/health")
async def health_check():
    """健康检查端点"""
    from app.services.knowledge_base import KnowledgeBaseService
    from app.services.qwen_vl import QwenVLService
    from app.services.image_service import ImageService

    services_status = {
        "api": "ok",
        "knowledge_base": "unknown",
        "qwen_vl": "unknown",
        "oss": "unknown"
    }

    # 检查知识库
    try:
        kb_service = KnowledgeBaseService()
        materials = kb_service.get_all_materials()
        services_status["knowledge_base"] = "ok" if materials else "error"
    except Exception as e:
        services_status["knowledge_base"] = f"error: {str(e)}"

    # 检查 Qwen-VL（简单检查配置）
    try:
        qwen_service = QwenVLService()
        services_status["qwen_vl"] = "ok" if qwen_service.settings.OPENAI_API_KEY else "not_configured"
    except Exception as e:
        services_status["qwen_vl"] = f"error: {str(e)}"

    # 检查 OSS（简单检查配置）
    try:
        image_service = ImageService()
        services_status["oss"] = "ok" if image_service.bucket else "not_configured"
    except Exception as e:
        services_status["oss"] = f"error: {str(e)}"

    return {
        "status": "healthy",
        "services": services_status
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
