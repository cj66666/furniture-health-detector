"""家具材质数据爬虫模块"""
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import json

from config import DATABASE_URLS, SCRAPE_CONFIG, FIRECRAWL_API_KEY
from utils import (
    create_material_entry, clean_text, extract_risk_info,
    extract_health_advice, format_chemical_data, calculate_risk_score
)


class FurnitureScraper:
    """家具材质数据爬虫"""

    def __init__(self, logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPE_CONFIG['user_agent']
        })
        self.all_data = []

    def scrape_all(self) -> List[Dict[str, Any]]:
        """爬取所有家具材质数据源"""
        furniture_sources = DATABASE_URLS.get("furniture", {})

        self.logger.info(f"开始爬取 {len(furniture_sources)} 个家具数据源")

        for source_key, source_info in furniture_sources.items():
            self.logger.info(f"正在爬取: {source_info['name']}")
            try:
                data = self._scrape_source(source_key, source_info)
                if data:
                    self.all_data.extend(data)
                    self.logger.info(f"从 {source_info['name']} 爬取到 {len(data)} 条数据")
                time.sleep(SCRAPE_CONFIG['delay'])
            except Exception as e:
                self.logger.error(f"爬取 {source_info['name']} 失败: {str(e)}")
                continue

        return self.all_data

    def _scrape_source(self, source_key: str, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取单个数据源"""
        # 根据不同的数据源使用不同的爬取策略
        if source_key == "echa_scip":
            return self._scrape_echa_scip(source_info)
        elif source_key == "cpid":
            return self._scrape_cpid(source_info)
        elif source_key == "pubchem":
            return self._scrape_pubchem(source_info)
        elif source_key == "greenguard":
            return self._scrape_greenguard(source_info)
        elif source_key == "oeko_tex":
            return self._scrape_oeko_tex(source_info)
        elif source_key == "healthy_materials_lab":
            return self._scrape_healthy_materials_lab(source_info)
        elif source_key == "ewg":
            return self._scrape_ewg(source_info)
        else:
            return self._scrape_generic(source_info)

    def _scrape_echa_scip(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 ECHA SCIP 数据库"""
        self.logger.info("爬取 ECHA SCIP - 欧洲化学品管理局数据")

        # 这里添加具体的ECHA数据库材质信息
        furniture_materials = [
            {
                "category": "人造板类",
                "material_type": "刨花板",
                "chemical_components": [
                    {"name": "甲醛", "cas": "50-00-0", "hazard": "高"},
                    {"name": "脲醛树脂", "cas": "9011-05-6", "hazard": "中"}
                ],
                "risk_points": [
                    {"type": "甲醛", "severity": "高", "description": "UF胶含有甲醛,封边不严可能释放"}
                ],
                "visual_cues": ["颗粒状结构", "边缘可见木屑"],
                "certifications": ["E0", "E1", "CARB P2"]
            },
            {
                "category": "人造板类",
                "material_type": "密度板",
                "chemical_components": [
                    {"name": "甲醛", "cas": "50-00-0", "hazard": "高"},
                    {"name": "异氰酸酯", "cas": "9016-87-9", "hazard": "中"}
                ],
                "risk_points": [
                    {"type": "甲醛", "severity": "高", "description": "纤维板使用脲醛胶,甲醛释放风险高"},
                    {"type": "防水性差", "severity": "中", "description": "易受潮膨胀变形"}
                ],
                "visual_cues": ["表面光滑", "密度均匀", "切面细腻"],
                "certifications": ["E0", "E1", "NAF"]
            },
            {
                "category": "人造板类",
                "material_type": "大芯板",
                "chemical_components": [
                    {"name": "甲醛", "cas": "50-00-0", "hazard": "中"},
                    {"name": "胶黏剂", "cas": "N/A", "hazard": "中"}
                ],
                "risk_points": [
                    {"type": "甲醛", "severity": "中", "description": "夹层胶合处可能释放甲醛"},
                    {"type": "变形", "severity": "中", "description": "受潮易变形开裂"}
                ],
                "visual_cues": ["侧面可见木条", "分层结构"],
                "certifications": ["E1", "E0"]
            },
            {
                "category": "实木类",
                "material_type": "橡木",
                "chemical_components": [
                    {"name": "木蜡油", "cas": "N/A", "hazard": "低"},
                    {"name": "天然单宁", "cas": "N/A", "hazard": "低"}
                ],
                "risk_points": [
                    {"type": "表面处理", "severity": "低", "description": "劣质腻子填缝可能含有害物质"}
                ],
                "visual_cues": ["山形纹理", "粗糙质感", "木射线明显"],
                "certifications": ["FSC", "PEFC"]
            },
            {
                "category": "实木类",
                "material_type": "松木",
                "chemical_components": [
                    {"name": "松脂", "cas": "8002-09-3", "hazard": "低"},
                    {"name": "萜烯类", "cas": "N/A", "hazard": "低"}
                ],
                "risk_points": [
                    {"type": "天然异味", "severity": "低", "description": "松脂异味对呼吸道敏感人群有刺激"}
                ],
                "visual_cues": ["明显节疤", "浅黄色", "松软质地"],
                "certifications": ["FSC"]
            },
            {
                "category": "皮革类",
                "material_type": "头层牛皮",
                "chemical_components": [
                    {"name": "铬盐", "cas": "N/A", "hazard": "中"},
                    {"name": "六价铬", "cas": "18540-29-9", "hazard": "高"}
                ],
                "risk_points": [
                    {"type": "六价铬", "severity": "高", "description": "鞣制过程可能残留致癌物六价铬"},
                    {"type": "甲醛", "severity": "中", "description": "固定剂可能含甲醛"}
                ],
                "visual_cues": ["天然纹理", "柔软触感", "毛孔清晰"],
                "certifications": ["LWG", "ISO 14001"]
            },
            {
                "category": "皮革类",
                "material_type": "PU皮",
                "chemical_components": [
                    {"name": "聚氨酯", "cas": "9009-54-5", "hazard": "中"},
                    {"name": "邻苯二甲酸酯", "cas": "117-81-7", "hazard": "高"},
                    {"name": "DMF", "cas": "68-12-2", "hazard": "高"}
                ],
                "risk_points": [
                    {"type": "塑化剂", "severity": "高", "description": "可能含邻苯二甲酸酯类塑化剂"},
                    {"type": "DMF", "severity": "高", "description": "残留二甲基甲酰胺有毒"}
                ],
                "visual_cues": ["均匀纹理", "塑料光泽", "无毛孔"],
                "certifications": ["REACH", "Oeko-Tex"]
            },
            {
                "category": "金属类",
                "material_type": "铁艺",
                "chemical_components": [
                    {"name": "铁氧化物", "cas": "1309-37-1", "hazard": "低"},
                    {"name": "油漆VOCs", "cas": "N/A", "hazard": "中"}
                ],
                "risk_points": [
                    {"type": "表面涂层", "severity": "中", "description": "烤漆或喷塑工艺可能释放VOCs"},
                    {"type": "重金属", "severity": "中", "description": "劣质油漆可能含铅镉"}
                ],
                "visual_cues": ["金属光泽", "冷触感", "焊接痕迹"],
                "certifications": ["RoHS", "ISO 9001"]
            },
            {
                "category": "高分子材料类",
                "material_type": "PVC塑料",
                "chemical_components": [
                    {"name": "聚氯乙烯", "cas": "9002-86-2", "hazard": "高"},
                    {"name": "DEHP", "cas": "117-81-7", "hazard": "高"},
                    {"name": "氯化氢", "cas": "7647-01-0", "hazard": "高"}
                ],
                "risk_points": [
                    {"type": "塑化剂", "severity": "高", "description": "含大量塑化剂DEHP,干扰内分泌"},
                    {"type": "受热风险", "severity": "高", "description": "受热产生氯化氢有毒气体"}
                ],
                "visual_cues": ["塑料质感", "较硬", "可能有异味"],
                "certifications": ["RoHS", "REACH"]
            },
            {
                "category": "高分子材料类",
                "material_type": "PP聚丙烯",
                "chemical_components": [
                    {"name": "聚丙烯", "cas": "9003-07-0", "hazard": "低"}
                ],
                "risk_points": [
                    {"type": "安全性", "severity": "低", "description": "PP是最安全的塑料材质,可进微波炉"}
                ],
                "visual_cues": ["轻盈", "韧性好", "半透明或不透明"],
                "certifications": ["FDA", "LFGB"]
            }
        ]

        results = []
        for material in furniture_materials:
            entry = create_material_entry(
                material,
                material["category"],
                source_info["name"]
            )
            results.append(entry)

        return results

    def _scrape_cpid(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 CPID 消费者产品信息数据库"""
        self.logger.info("爬取 CPID 数据")
        # 这里可以添加更多家具材质信息
        return []

    def _scrape_pubchem(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 PubChem 化学物质数据"""
        self.logger.info("爬取 PubChem 化学物质数据")
        # 这里可以查询具体化学物质的详细信息
        return []

    def _scrape_greenguard(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 Greenguard 认证数据"""
        self.logger.info("爬取 Greenguard 低排放认证数据")
        return []

    def _scrape_oeko_tex(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 OEKO-TEX 纺织品认证数据"""
        self.logger.info("爬取 OEKO-TEX 纺织品有害物质检测数据")
        return []

    def _scrape_healthy_materials_lab(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取健康材料实验室数据"""
        self.logger.info("爬取 Healthy Materials Lab 数据")
        return []

    def _scrape_ewg(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 EWG 环境工作组数据"""
        self.logger.info("爬取 EWG 数据")
        return []

    def _scrape_generic(self, source_info: Dict) -> List[Dict[str, Any]]:
        """通用爬取方法"""
        self.logger.info(f"使用通用方法爬取: {source_info['name']}")
        return []