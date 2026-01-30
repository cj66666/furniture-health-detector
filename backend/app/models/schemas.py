"""数据模型定义"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum


class MaterialType(str, Enum):
    """材料类型枚举"""
    SOLID_WOOD = "实木类"
    ENGINEERED_WOOD = "人造板类"
    LEATHER = "皮革类"
    FABRIC = "布类"


class RiskLevel(str, Enum):
    """风险等级枚举"""
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"


class VisualCue(BaseModel):
    """视觉特征"""
    texture: str = Field(..., description="纹理描述")
    color: str = Field(..., description="颜色描述")
    pattern: str = Field(..., description="图案描述")


class MaterialData(BaseModel):
    """材料数据模型"""
    material_type: MaterialType = Field(..., description="材料类型")
    sub_type: str = Field(..., description="材料子类型，如'橡木'、'密度板'")
    confidence: float = Field(..., ge=0, le=100, description="识别置信度 (0-100)")
    visual_cues: VisualCue = Field(..., description="视觉特征")

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """验证置信度范围"""
        if not 0 <= v <= 100:
            raise ValueError("置信度必须在 0-100 范围内")
        return v


class RiskAssessment(BaseModel):
    """风险评估"""
    risk_level: RiskLevel = Field(..., description="风险等级")
    risk_score: float = Field(..., ge=0, le=100, description="风险评分 (0-100)")
    harmful_substances: List[str] = Field(
        default_factory=list,
        description="可能含有的有害物质列表"
    )
    health_impacts: List[str] = Field(
        default_factory=list,
        description="健康影响列表"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="建议措施"
    )


class FurnitureDetectionReport(BaseModel):
    """家具检测报告"""
    report_id: str = Field(..., description="报告唯一标识")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="检测时间"
    )
    image_url: str = Field(..., description="原始图片 URL")
    furniture_type: str = Field(..., description="家具类型，如'椅子'、'沙发'")
    materials: List[MaterialData] = Field(..., description="检测到的材料列表")
    risk_assessment: RiskAssessment = Field(..., description="风险评估")
    disclaimer_accepted: bool = Field(
        default=False,
        description="用户是否已接受免责声明"
    )

    @field_validator("materials")
    @classmethod
    def validate_materials(cls, v: List[MaterialData]) -> List[MaterialData]:
        """验证材料列表不为空"""
        if not v:
            raise ValueError("材料列表不能为空")
        return v


class ShareCardData(BaseModel):
    """分享卡片数据"""
    card_id: str = Field(..., description="卡片唯一标识")
    report_id: str = Field(..., description="关联的报告 ID")
    card_image_url: str = Field(..., description="卡片图片 URL")
    qr_code_url: str = Field(..., description="小程序二维码 URL")
    catchphrase: str = Field(..., description="AI 生成的金句")
    template_style: Literal["modern", "classic", "minimal"] = Field(
        default="modern",
        description="卡片模板风格"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="创建时间"
    )
    expires_at: Optional[datetime] = Field(
        None,
        description="过期时间（7天后）"
    )


# API 请求/响应模型

class FurnitureDetectionRequest(BaseModel):
    """家具检测请求"""
    disclaimer_accepted: bool = Field(..., description="用户是否已接受免责声明")


class FurnitureDetectionResponse(BaseModel):
    """家具检测响应"""
    success: bool = Field(..., description="是否成功")
    data: Optional[FurnitureDetectionReport] = Field(None, description="检测报告")
    error: Optional[str] = Field(None, description="错误信息")


class ShareCardRequest(BaseModel):
    """分享卡片生成请求"""
    report_id: str = Field(..., description="报告 ID")
    template_style: Literal["modern", "classic", "minimal"] = Field(
        default="modern",
        description="卡片模板风格"
    )


class ShareCardResponse(BaseModel):
    """分享卡片生成响应"""
    success: bool = Field(..., description="是否成功")
    data: Optional[ShareCardData] = Field(None, description="分享卡片数据")
    error: Optional[str] = Field(None, description="错误信息")
