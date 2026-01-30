"""家具检测 API 路由"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
import uuid
from datetime import datetime
from loguru import logger

from app.models.schemas import (
    FurnitureDetectionResponse,
    FurnitureDetectionReport,
    MaterialData,
    RiskAssessment,
    VisualCue,
    MaterialType,
    RiskLevel
)
from app.services.image_service import ImageService
from app.services.qwen_vl import QwenVLService
from app.services.knowledge_base import KnowledgeBaseService

router = APIRouter(prefix="/furniture", tags=["家具检测"])

# 初始化服务
image_service = ImageService()
qwen_service = QwenVLService()
knowledge_service = KnowledgeBaseService()


@router.post("/detect", response_model=FurnitureDetectionResponse)
async def detect_furniture(
    image: UploadFile = File(..., description="家具图片"),
    disclaimer_accepted: bool = Form(..., description="是否接受免责声明")
):
    """家具材料检测端点

    上传家具图片，返回材料识别和健康风险评估结果。

    Args:
        image: 上传的图片文件
        disclaimer_accepted: 用户是否已接受免责声明

    Returns:
        FurnitureDetectionResponse: 检测结果
    """
    try:
        # 验证免责声明
        if not disclaimer_accepted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请先接受免责声明"
            )

        # 读取图片数据
        image_data = await image.read()

        # 验证图片质量
        # 先保存临时文件用于验证
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(image_data)
            temp_path = temp_file.name

        is_valid, error_msg = qwen_service.validate_image_quality(temp_path)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"图片质量不符合要求: {error_msg}"
            )

        logger.info(f"开始处理图片: {image.filename}")

        # 1. 压缩并上传图片到 OSS
        compressed_data = image_service.compress_image(image_data)
        image_url = await image_service.upload_to_oss(
            compressed_data,
            image.filename or "furniture.jpg"
        )

        # 2. 调用 Qwen-VL 分析图片
        logger.info("调用 Qwen-VL 分析图片...")
        analysis_result = await qwen_service.analyze_furniture(image_url)

        # 3. 解析分析结果
        furniture_type = analysis_result.get('furniture_type', '未知家具')
        materials_data = analysis_result.get('materials', [])

        if not materials_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无法识别图片中的材料，请上传更清晰的家具图片"
            )

        # 4. 构建材料数据列表
        materials = []
        for mat in materials_data:
            material_type = mat.get('material_type')
            sub_type = mat.get('sub_type')
            confidence = mat.get('confidence', 0)
            visual_cues = mat.get('visual_cues', {})

            # 创建 MaterialData 对象
            material = MaterialData(
                material_type=MaterialType(material_type),
                sub_type=sub_type,
                confidence=confidence,
                visual_cues=VisualCue(
                    texture=visual_cues.get('texture', ''),
                    color=visual_cues.get('color', ''),
                    pattern=visual_cues.get('pattern', '')
                )
            )
            materials.append(material)

        # 5. 查询知识库获取风险评估
        logger.info("查询知识库获取风险评估...")
        risk_data = None
        for mat in materials_data:
            sub_type = mat.get('sub_type')
            kb_material = knowledge_service.search_by_sub_type(sub_type)
            if kb_material:
                risk_data = kb_material.get('risk_assessment')
                break

        # 如果知识库中没有找到，使用默认风险评估
        if not risk_data:
            risk_data = {
                'risk_level': '中风险',
                'risk_score': 50,
                'harmful_substances': ['未知'],
                'sensitive_groups': ['婴幼儿', '孕妇', '呼吸道敏感人群'],
                'health_impacts': ['建议咨询专业人士'],
                'recommendations': ['定期通风', '保持室内空气流通']
            }

        # 6. 创建风险评估对象
        risk_assessment = RiskAssessment(
            risk_level=RiskLevel(risk_data['risk_level']),
            risk_score=risk_data['risk_score'],
            harmful_substances=risk_data.get('harmful_substances', []),
            sensitive_groups=risk_data.get('sensitive_groups', []),
            health_impacts=risk_data.get('health_impacts', []),
            recommendations=risk_data.get('recommendations', [])
        )

        # 7. 生成检测报告
        report = FurnitureDetectionReport(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            image_url=image_url,
            furniture_type=furniture_type,
            materials=materials,
            risk_assessment=risk_assessment,
            disclaimer_accepted=disclaimer_accepted
        )

        logger.info(f"检测完成，报告 ID: {report.report_id}")

        return FurnitureDetectionResponse(
            success=True,
            data=report,
            error=None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"家具检测失败: {e}")
        return FurnitureDetectionResponse(
            success=False,
            data=None,
            error=f"检测失败: {str(e)}"
        )
