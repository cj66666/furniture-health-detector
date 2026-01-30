"""分享卡片 API 路由"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict
import uuid
from datetime import datetime, timedelta
from loguru import logger
from PIL import Image, ImageDraw, ImageFont
import io

from app.models.schemas import (
    ShareCardRequest,
    ShareCardResponse,
    ShareCardData
)
from app.services.image_service import ImageService
from app.services.qwen_vl import QwenVLService

router = APIRouter(prefix="/share", tags=["分享卡片"])

# 初始化服务
image_service = ImageService()
qwen_service = QwenVLService()

# 临时存储检测报告（实际应用中应使用数据库）
reports_cache: Dict[str, dict] = {}


@router.post("/generate", response_model=ShareCardResponse)
async def generate_share_card(request: ShareCardRequest):
    """生成分享卡片

    根据检测报告生成精美的分享卡片，包含二维码。

    Args:
        request: 分享卡片生成请求

    Returns:
        ShareCardResponse: 分享卡片数据
    """
    try:
        # 从缓存中获取报告（实际应用中从数据库获取）
        report = reports_cache.get(request.report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"未找到报告 ID: {request.report_id}"
            )

        logger.info(f"开始生成分享卡片，报告 ID: {request.report_id}")

        # 1. 生成金句
        material_info = {
            'material_type': report['materials'][0]['material_type'],
            'sub_type': report['materials'][0]['sub_type']
        }
        risk_level = report['risk_assessment']['risk_level']

        catchphrase = await qwen_service.generate_catchphrase(
            material_info,
            risk_level
        )

        # 2. 生成小程序二维码
        miniprogram_path = f"/pages/report/report?id={request.report_id}"
        qr_code_url = await image_service.generate_and_upload_qr_code(
            miniprogram_path
        )

        # 3. 生成分享卡片图片
        card_image_data = await _generate_card_image(
            report,
            catchphrase,
            request.template_style
        )

        # 4. 上传卡片图片
        card_image_url = await image_service.upload_to_oss(
            card_image_data,
            f"share_card_{request.report_id}.jpg"
        )

        # 5. 创建分享卡片数据
        card_data = ShareCardData(
            card_id=str(uuid.uuid4()),
            report_id=request.report_id,
            card_image_url=card_image_url,
            qr_code_url=qr_code_url,
            catchphrase=catchphrase,
            template_style=request.template_style,
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=7)
        )

        logger.info(f"分享卡片生成完成，卡片 ID: {card_data.card_id}")

        return ShareCardResponse(
            success=True,
            data=card_data,
            error=None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"分享卡片生成失败: {e}")
        return ShareCardResponse(
            success=False,
            data=None,
            error=f"生成失败: {str(e)}"
        )


async def _generate_card_image(
    report: dict,
    catchphrase: str,
    template_style: str
) -> bytes:
    """生成分享卡片图片

    Args:
        report: 检测报告数据
        catchphrase: 金句
        template_style: 模板风格

    Returns:
        卡片图片数据
    """
    try:
        # 创建画布
        width, height = 750, 1334  # 标准分享卡片尺寸

        # 根据模板风格选择背景色
        bg_colors = {
            'modern': '#F5F7FA',
            'classic': '#FFF8E1',
            'minimal': '#FFFFFF'
        }
        bg_color = bg_colors.get(template_style, '#F5F7FA')

        # 创建图片
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # 绘制标题
        title = "家具健康检测报告"
        # 使用默认字体（实际应用中应使用自定义字体）
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            text_font = ImageFont.truetype("arial.ttf", 32)
            small_font = ImageFont.truetype("arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        # 绘制标题
        draw.text((width // 2, 100), title, fill='#333333', font=title_font, anchor='mm')

        # 绘制金句
        draw.text((width // 2, 200), catchphrase, fill='#FF6B6B', font=text_font, anchor='mm')

        # 绘制材料信息
        y_offset = 300
        materials = report.get('materials', [])
        if materials:
            material = materials[0]
            material_text = f"材料类型: {material['material_type']}"
            draw.text((100, y_offset), material_text, fill='#666666', font=text_font)

            sub_type_text = f"子类型: {material['sub_type']}"
            draw.text((100, y_offset + 60), sub_type_text, fill='#666666', font=text_font)

            confidence_text = f"置信度: {material['confidence']}%"
            draw.text((100, y_offset + 120), confidence_text, fill='#666666', font=text_font)

        # 绘制风险评估
        y_offset = 550
        risk = report.get('risk_assessment', {})
        risk_text = f"风险等级: {risk.get('risk_level', '未知')}"
        draw.text((100, y_offset), risk_text, fill='#FF6B6B', font=text_font)

        # 绘制建议
        y_offset = 650
        recommendations = risk.get('recommendations', [])
        if recommendations:
            draw.text((100, y_offset), "健康建议:", fill='#333333', font=text_font)
            for i, rec in enumerate(recommendations[:3]):  # 最多显示3条
                draw.text((100, y_offset + 60 + i * 50), f"• {rec}", fill='#666666', font=small_font)

        # 绘制底部信息
        footer_text = "扫码查看完整报告"
        draw.text((width // 2, height - 100), footer_text, fill='#999999', font=small_font, anchor='mm')

        # 转换为字节
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=90)
        return output.getvalue()

    except Exception as e:
        logger.error(f"生成卡片图片失败: {e}")
        raise
