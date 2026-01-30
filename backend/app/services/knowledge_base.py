"""材料知识库服务"""
import json
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
from app.models.schemas import MaterialType, RiskLevel


class KnowledgeBaseService:
    """材料知识库服务类"""

    def __init__(self, knowledge_base_path: str = "app/data/knowledge_base.json"):
        """初始化知识库服务

        Args:
            knowledge_base_path: 知识库文件路径
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.materials: List[Dict] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        """加载知识库数据"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.materials = data.get('materials', [])
            logger.info(f"成功加载知识库，共 {len(self.materials)} 条材料数据")
        except FileNotFoundError:
            logger.error(f"知识库文件不存在: {self.knowledge_base_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"知识库文件格式错误: {e}")
            raise

    def query_by_material_type(self, material_type: str) -> List[Dict]:
        """根据材料类型查询

        Args:
            material_type: 材料类型（实木类、人造板类、皮革类、布类）

        Returns:
            匹配的材料列表
        """
        results = [
            m for m in self.materials
            if m.get('material_type') == material_type
        ]
        logger.debug(f"查询材料类型 '{material_type}'，找到 {len(results)} 条结果")
        return results

    def query_by_visual_cues(
        self,
        texture: Optional[str] = None,
        color: Optional[str] = None,
        pattern: Optional[str] = None
    ) -> List[Dict]:
        """根据视觉特征查询（语义匹配）

        Args:
            texture: 纹理描述
            color: 颜色描述
            pattern: 图案描述

        Returns:
            匹配的材料列表
        """
        results = []

        for material in self.materials:
            visual_cues = material.get('visual_cues', {})
            score = 0

            # 简单的关键词匹配（实际应用中可以使用更复杂的语义匹配）
            if texture and texture in visual_cues.get('texture', ''):
                score += 1
            if color and color in visual_cues.get('color', ''):
                score += 1
            if pattern and pattern in visual_cues.get('pattern', ''):
                score += 1

            if score > 0:
                results.append({
                    'material': material,
                    'match_score': score
                })

        # 按匹配分数排序
        results.sort(key=lambda x: x['match_score'], reverse=True)
        logger.debug(f"视觉特征查询找到 {len(results)} 条结果")

        return [r['material'] for r in results]

    def get_risk_assessment(self, material_id: str) -> Optional[Dict]:
        """获取材料的风险评估

        Args:
            material_id: 材料 ID

        Returns:
            风险评估数据，如果未找到则返回 None
        """
        for material in self.materials:
            if material.get('id') == material_id:
                return material.get('risk_assessment')

        logger.warning(f"未找到材料 ID: {material_id}")
        return None

    def validate_material_data(self, material: Dict) -> bool:
        """验证材料数据结构完整性

        Args:
            material: 材料数据字典

        Returns:
            是否验证通过
        """
        required_fields = [
            'id', 'material_type', 'sub_type',
            'description', 'visual_cues', 'risk_assessment'
        ]

        for field in required_fields:
            if field not in material:
                logger.error(f"材料数据缺少必需字段: {field}")
                return False

        # 验证 visual_cues 结构
        visual_cues = material.get('visual_cues', {})
        if not all(k in visual_cues for k in ['texture', 'color', 'pattern']):
            logger.error("visual_cues 缺少必需字段")
            return False

        # 验证 risk_assessment 结构
        risk = material.get('risk_assessment', {})
        required_risk_fields = [
            'risk_level', 'risk_score',
            'harmful_substances', 'health_impacts', 'recommendations'
        ]
        if not all(k in risk for k in required_risk_fields):
            logger.error("risk_assessment 缺少必需字段")
            return False

        return True

    def get_all_materials(self) -> List[Dict]:
        """获取所有材料数据

        Returns:
            所有材料列表
        """
        return self.materials

    def search_by_sub_type(self, sub_type: str) -> Optional[Dict]:
        """根据材料子类型精确查询

        Args:
            sub_type: 材料子类型

        Returns:
            匹配的材料，如果未找到则返回 None
        """
        for material in self.materials:
            if material.get('sub_type') == sub_type:
                return material

        logger.debug(f"未找到材料子类型: {sub_type}")
        return None
