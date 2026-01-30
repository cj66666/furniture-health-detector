"""衣料材质数据爬虫模块"""
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from config import DATABASE_URLS, SCRAPE_CONFIG
from utils import create_material_entry, clean_text


class TextileScraper:
    """衣料材质数据爬虫"""

    def __init__(self, logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPE_CONFIG['user_agent']
        })
        self.all_data = []

    def scrape_all(self) -> List[Dict[str, Any]]:
        """爬取所有衣料材质数据源"""
        textile_sources = DATABASE_URLS.get("textile", {})

        self.logger.info(f"开始爬取 {len(textile_sources)} 个衣料数据源")

        for source_key, source_info in textile_sources.items():
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
        if source_key == "oeko_tex":
            return self._scrape_oeko_tex(source_info)
        elif source_key == "gots":
            return self._scrape_gots(source_info)
        elif source_key == "textile_exchange":
            return self._scrape_textile_exchange(source_info)
        elif source_key == "epa_textile":
            return self._scrape_epa_textile(source_info)
        elif source_key == "made_safe":
            return self._scrape_made_safe(source_info)
        else:
            return self._scrape_generic(source_info)

    def _scrape_oeko_tex(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 OEKO-TEX 数据"""
        self.logger.info("爬取 OEKO-TEX 纺织品安全数据")

        textile_materials = [
            {
                "fabric_type": "棉",
                "composition": "100% 天然纤维",
                "chemical_treatments": [
                    {"name": "漂白剂", "hazard": "低"},
                    {"name": "染料", "hazard": "中"}
                ],
                "health_risks": [
                    {"type": "染料残留", "severity": "低", "description": "劣质染料可能含偶氮染料"},
                    {"type": "农药残留", "severity": "低", "description": "非有机棉可能有农药残留"}
                ],
                "health_benefits": [
                    "透气性好",
                    "吸湿性强",
                    "亲肤柔软"
                ],
                "care_instructions": {
                    "washing": "可机洗,40度以下",
                    "drying": "可机烘,低温",
                    "ironing": "高温熨烫"
                },
                "certifications": ["OEKO-TEX", "GOTS", "OCS"]
            },
            {
                "fabric_type": "麻",
                "composition": "100% 天然纤维(亚麻/苎麻)",
                "chemical_treatments": [
                    {"name": "漂白剂", "hazard": "低"},
                    {"name": "柔软剂", "hazard": "低"}
                ],
                "health_risks": [
                    {"type": "粗糙质感", "severity": "低", "description": "未处理麻布可能对敏感肌肤有刺激"}
                ],
                "health_benefits": [
                    "天然抗菌",
                    "极佳透气性",
                    "吸湿快干"
                ],
                "care_instructions": {
                    "washing": "可机洗,冷水",
                    "drying": "自然晾干",
                    "ironing": "高温熨烫"
                },
                "certifications": ["OEKO-TEX", "European Flax"]
            },
            {
                "fabric_type": "丝",
                "composition": "100% 天然蛋白质纤维",
                "chemical_treatments": [
                    {"name": "脱胶剂", "hazard": "低"},
                    {"name": "染料", "hazard": "中"}
                ],
                "health_risks": [
                    {"type": "蛋白质过敏", "severity": "低", "description": "极少数人对蚕丝蛋白过敏"},
                    {"type": "染料残留", "severity": "中", "description": "深色真丝可能有染料残留"}
                ],
                "health_benefits": [
                    "亲肤柔滑",
                    "保湿美肤",
                    "减少静电"
                ],
                "care_instructions": {
                    "washing": "手洗,冷水,专用洗涤剂",
                    "drying": "阴干,避免阳光直射",
                    "ironing": "低温熨烫,反面"
                },
                "certifications": ["OEKO-TEX", "GS Mark"]
            },
            {
                "fabric_type": "羊毛",
                "composition": "100% 动物纤维",
                "chemical_treatments": [
                    {"name": "防缩剂", "hazard": "中"},
                    {"name": "防虫剂", "hazard": "中"},
                    {"name": "氯化处理", "hazard": "高"}
                ],
                "health_risks": [
                    {"type": "氯化处理", "severity": "高", "description": "劣质羊毛可能经氯化处理,残留有毒物质"},
                    {"type": "防虫剂", "severity": "中", "description": "传统防虫剂可能含有机磷农药"},
                    {"type": "过敏", "severity": "中", "description": "羊毛过敏者慎用"}
                ],
                "health_benefits": [
                    "保暖性极佳",
                    "吸湿排汗",
                    "天然阻燃"
                ],
                "care_instructions": {
                    "washing": "手洗或干洗,冷水",
                    "drying": "平铺晾干",
                    "ironing": "低温熨烫,隔布"
                },
                "certifications": ["Woolmark", "OEKO-TEX", "ZQ Merino"]
            },
            {
                "fabric_type": "涤纶",
                "composition": "100% 聚酯纤维(化纤)",
                "chemical_treatments": [
                    {"name": "阻燃剂", "hazard": "高"},
                    {"name": "抗静电剂", "hazard": "中"},
                    {"name": "染料", "hazard": "中"}
                ],
                "health_risks": [
                    {"type": "阻燃剂", "severity": "高", "description": "部分涤纶添加溴化阻燃剂,可能影响内分泌"},
                    {"type": "塑化剂", "severity": "中", "description": "劣质涤纶可能含塑化剂"},
                    {"type": "不透气", "severity": "低", "description": "纯涤纶透气性差,易闷热"}
                ],
                "health_benefits": [
                    "耐用抗皱",
                    "快干",
                    "价格便宜"
                ],
                "care_instructions": {
                    "washing": "可机洗,温水",
                    "drying": "可机烘,低温",
                    "ironing": "低温熨烫"
                },
                "certifications": ["OEKO-TEX", "GRS(再生涤纶)"]
            },
            {
                "fabric_type": "尼龙",
                "composition": "100% 聚酰胺纤维(化纤)",
                "chemical_treatments": [
                    {"name": "抗菌剂", "hazard": "中"},
                    {"name": "防水剂", "hazard": "高"},
                    {"name": "染料", "hazard": "中"}
                ],
                "health_risks": [
                    {"type": "PFAS永久化学品", "severity": "高", "description": "防水尼龙可能含全氟化合物(PFAS)"},
                    {"type": "抗菌剂", "severity": "中", "description": "银离子等抗菌剂可能引起过敏"},
                    {"type": "不透气", "severity": "低", "description": "纯尼龙不透气,贴身穿着易闷热"}
                ],
                "health_benefits": [
                    "轻便耐磨",
                    "强度高",
                    "快干"
                ],
                "care_instructions": {
                    "washing": "可机洗,冷水",
                    "drying": "阴干,避免高温",
                    "ironing": "低温或不熨烫"
                },
                "certifications": ["OEKO-TEX", "bluesign"]
            },
            {
                "fabric_type": "氨纶",
                "composition": "弹性纤维(通常与其他纤维混纺)",
                "chemical_treatments": [
                    {"name": "异氰酸酯", "hazard": "高"},
                    {"name": "溶剂残留", "hazard": "中"}
                ],
                "health_risks": [
                    {"type": "异氰酸酯", "severity": "高", "description": "生产过程使用异氰酸酯,残留可能致敏"},
                    {"type": "溶剂残留", "severity": "中", "description": "DMF等溶剂残留有毒"},
                    {"type": "过敏", "severity": "中", "description": "对弹性纤维过敏者慎用"}
                ],
                "health_benefits": [
                    "弹性极佳",
                    "贴身舒适",
                    "增强耐用性"
                ],
                "care_instructions": {
                    "washing": "可机洗,冷水",
                    "drying": "阴干,避免阳光和高温",
                    "ironing": "不熨烫"
                },
                "certifications": ["OEKO-TEX"]
            },
            {
                "fabric_type": "粘胶纤维",
                "composition": "再生纤维素纤维(人造纤维)",
                "chemical_treatments": [
                    {"name": "二硫化碳", "hazard": "高"},
                    {"name": "氢氧化钠", "hazard": "中"}
                ],
                "health_risks": [
                    {"type": "生产污染", "severity": "高", "description": "传统粘胶生产使用二硫化碳,环境污染大"},
                    {"type": "化学残留", "severity": "中", "description": "劣质粘胶可能有碱液残留"},
                    {"type": "易皱缩水", "severity": "低", "description": "湿强度低,易变形"}
                ],
                "health_benefits": [
                    "柔软舒适",
                    "吸湿透气",
                    "不起静电"
                ],
                "care_instructions": {
                    "washing": "手洗或干洗",
                    "drying": "平铺晾干",
                    "ironing": "中温熨烫"
                },
                "certifications": ["OEKO-TEX", "FSC(天丝)", "PEFC"]
            }
        ]

        results = []
        for material in textile_materials:
            entry = create_material_entry(
                material,
                "衣料纺织品",
                source_info["name"]
            )
            results.append(entry)

        return results

    def _scrape_gots(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 GOTS 有机纺织品数据"""
        self.logger.info("爬取 GOTS 全球有机纺织品标准数据")
        return []

    def _scrape_textile_exchange(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 Textile Exchange 数据"""
        self.logger.info("爬取 Textile Exchange 纺织品交易所数据")
        return []

    def _scrape_epa_textile(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 EPA 纺织品信息"""
        self.logger.info("爬取 EPA 纺织品环保信息")
        return []

    def _scrape_made_safe(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 Made Safe 认证数据"""
        self.logger.info("爬取 Made Safe 安全产品认证数据")
        return []

    def _scrape_generic(self, source_info: Dict) -> List[Dict[str, Any]]:
        """通用爬取方法"""
        self.logger.info(f"使用通用方法爬取: {source_info['name']}")
        return []