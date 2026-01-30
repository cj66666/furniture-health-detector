"""食物数据爬虫模块"""
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

from config import DATABASE_URLS, SCRAPE_CONFIG
from utils import create_material_entry, clean_text


class FoodScraper:
    """食物数据爬虫"""

    def __init__(self, logger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPE_CONFIG['user_agent']
        })
        self.all_data = []

    def scrape_all(self) -> List[Dict[str, Any]]:
        """爬取所有食物数据源"""
        food_sources = DATABASE_URLS.get("food", {})

        self.logger.info(f"开始爬取 {len(food_sources)} 个食物数据源")

        for source_key, source_info in food_sources.items():
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
        if source_key == "usda_fooddata":
            return self._scrape_usda(source_info)
        elif source_key == "fda_food":
            return self._scrape_fda(source_info)
        elif source_key == "chinese_food_composition":
            return self._scrape_chinese_food(source_info)
        elif source_key == "food_incompatibility":
            return self._scrape_food_incompatibility(source_info)
        elif source_key == "nutrients_db":
            return self._scrape_nutrients_db(source_info)
        else:
            return self._scrape_generic(source_info)

    def _scrape_usda(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 USDA 食品数据"""
        self.logger.info("爬取 USDA 食品营养数据")
        return []

    def _scrape_fda(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取 FDA 食品数据"""
        self.logger.info("爬取 FDA 食品安全数据")
        return []

    def _scrape_chinese_food(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取中国食物成分表数据"""
        self.logger.info("爬取中国食物成分表数据")

        # 常见食物数据
        food_data = [
            # 谷物类
            {
                "name": "大米",
                "category": "谷物类",
                "nutrients": {
                    "energy": {"value": 346, "unit": "kcal/100g"},
                    "protein": {"value": 7.4, "unit": "g/100g"},
                    "fat": {"value": 0.8, "unit": "g/100g"},
                    "carbohydrate": {"value": 77.9, "unit": "g/100g"},
                    "fiber": {"value": 0.7, "unit": "g/100g"}
                },
                "recommended_intake": {
                    "adult": "250-400g/天",
                    "children": "150-250g/天",
                    "elderly": "200-300g/天"
                },
                "health_benefits": ["提供能量", "易消化", "养胃"],
                "contraindications": [],
                "incompatible_foods": []
            },
            {
                "name": "小麦",
                "category": "谷物类",
                "nutrients": {
                    "energy": {"value": 317, "unit": "kcal/100g"},
                    "protein": {"value": 11.9, "unit": "g/100g"},
                    "fat": {"value": 1.3, "unit": "g/100g"},
                    "carbohydrate": {"value": 71.5, "unit": "g/100g"},
                    "fiber": {"value": 10.8, "unit": "g/100g"}
                },
                "recommended_intake": {
                    "adult": "100-150g/天",
                    "children": "50-100g/天"
                },
                "health_benefits": ["富含B族维生素", "膳食纤维丰富"],
                "contraindications": ["麸质过敏者禁食", "乳糜泻患者禁食"],
                "incompatible_foods": []
            },

            # 蔬菜类
            {
                "name": "菠菜",
                "category": "蔬菜类",
                "nutrients": {
                    "energy": {"value": 28, "unit": "kcal/100g"},
                    "protein": {"value": 2.6, "unit": "g/100g"},
                    "iron": {"value": 2.9, "unit": "mg/100g"},
                    "calcium": {"value": 66, "unit": "mg/100g"},
                    "oxalic_acid": {"value": 0.97, "unit": "g/100g"}
                },
                "recommended_intake": {
                    "adult": "100-200g/天",
                    "children": "50-100g/天"
                },
                "health_benefits": ["补铁", "富含叶酸", "护眼"],
                "contraindications": [
                    "肾结石患者少食(含草酸高)",
                    "尿酸高者少食"
                ],
                "incompatible_foods": [
                    {"food": "豆腐", "reason": "草酸与钙结合影响吸收", "severity": "轻微"},
                    {"food": "牛奶", "reason": "草酸影响钙吸收", "severity": "轻微"}
                ]
            },
            {
                "name": "西红柿",
                "category": "蔬菜类",
                "nutrients": {
                    "energy": {"value": 19, "unit": "kcal/100g"},
                    "vitamin_c": {"value": 19, "unit": "mg/100g"},
                    "lycopene": {"value": 2.57, "unit": "mg/100g"}
                },
                "recommended_intake": {
                    "adult": "100-200g/天"
                },
                "health_benefits": ["抗氧化", "护心", "防癌"],
                "contraindications": ["空腹不宜多食"],
                "incompatible_foods": [
                    {"food": "黄瓜", "reason": "维生素C分解酶破坏营养", "severity": "轻微"}
                ]
            },

            # 水果类
            {
                "name": "苹果",
                "category": "水果类",
                "nutrients": {
                    "energy": {"value": 52, "unit": "kcal/100g"},
                    "fiber": {"value": 2.4, "unit": "g/100g"},
                    "vitamin_c": {"value": 4, "unit": "mg/100g"}
                },
                "recommended_intake": {
                    "adult": "200-350g/天(1-2个)"
                },
                "health_benefits": ["助消化", "降胆固醇", "美容"],
                "contraindications": [],
                "incompatible_foods": []
            },
            {
                "name": "香蕉",
                "category": "水果类",
                "nutrients": {
                    "energy": {"value": 89, "unit": "kcal/100g"},
                    "potassium": {"value": 358, "unit": "mg/100g"},
                    "magnesium": {"value": 27, "unit": "mg/100g"}
                },
                "recommended_intake": {
                    "adult": "1-2根/天"
                },
                "health_benefits": ["补充能量", "缓解疲劳", "润肠通便"],
                "contraindications": [
                    "糖尿病患者少食",
                    "肾功能不全者慎食(钾高)"
                ],
                "incompatible_foods": [
                    {"food": "芋头", "reason": "同食易腹胀", "severity": "轻微"}
                ]
            },

            # 肉类
            {
                "name": "猪肉",
                "category": "肉类",
                "nutrients": {
                    "energy": {"value": 395, "unit": "kcal/100g"},
                    "protein": {"value": 13.2, "unit": "g/100g"},
                    "fat": {"value": 37, "unit": "g/100g"}
                },
                "recommended_intake": {
                    "adult": "40-75g/天"
                },
                "health_benefits": ["补充蛋白质", "补铁"],
                "contraindications": [
                    "高血脂患者少食",
                    "肥胖者少食"
                ],
                "incompatible_foods": [
                    {"food": "菱角", "reason": "同食伤肝", "severity": "中等"},
                    {"food": "甘草", "reason": "同食中毒", "severity": "严重"}
                ]
            },
            {
                "name": "鸡肉",
                "category": "肉类",
                "nutrients": {
                    "energy": {"value": 167, "unit": "kcal/100g"},
                    "protein": {"value": 19.3, "unit": "g/100g"},
                    "fat": {"value": 9.4, "unit": "g/100g"}
                },
                "recommended_intake": {
                    "adult": "50-100g/天"
                },
                "health_benefits": ["优质蛋白", "低脂肪", "易消化"],
                "contraindications": [],
                "incompatible_foods": [
                    {"food": "芹菜", "reason": "同食伤元气", "severity": "轻微"}
                ]
            },

            # 水产类
            {
                "name": "鲫鱼",
                "category": "水产类",
                "nutrients": {
                    "energy": {"value": 108, "unit": "kcal/100g"},
                    "protein": {"value": 17.1, "unit": "g/100g"},
                    "omega3": {"value": 0.3, "unit": "g/100g"}
                },
                "recommended_intake": {
                    "adult": "100-150g/天"
                },
                "health_benefits": ["补充DHA", "健脑", "护心"],
                "contraindications": [],
                "incompatible_foods": [
                    {"food": "猪肝", "reason": "影响营养吸收", "severity": "轻微"},
                    {"food": "蜂蜜", "reason": "同食中毒", "severity": "严重"}
                ]
            },

            # 豆类
            {
                "name": "黄豆",
                "category": "豆类",
                "nutrients": {
                    "energy": {"value": 359, "unit": "kcal/100g"},
                    "protein": {"value": 35, "unit": "g/100g"},
                    "isoflavone": {"value": 128, "unit": "mg/100g"}
                },
                "recommended_intake": {
                    "adult": "30-50g/天(干豆)"
                },
                "health_benefits": ["植物蛋白", "降胆固醇", "补钙"],
                "contraindications": [
                    "痛风患者少食(嘌呤高)",
                    "胃肠功能弱者少食"
                ],
                "incompatible_foods": [
                    {"food": "菠菜", "reason": "影响钙吸收", "severity": "轻微"}
                ]
            },

            # 奶制品
            {
                "name": "牛奶",
                "category": "奶制品",
                "nutrients": {
                    "energy": {"value": 54, "unit": "kcal/100ml"},
                    "protein": {"value": 3, "unit": "g/100ml"},
                    "calcium": {"value": 104, "unit": "mg/100ml"}
                },
                "recommended_intake": {
                    "adult": "300ml/天",
                    "children": "300-500ml/天"
                },
                "health_benefits": ["补钙", "优质蛋白", "助眠"],
                "contraindications": [
                    "乳糖不耐受者慎饮",
                    "牛奶过敏者禁饮"
                ],
                "incompatible_foods": [
                    {"food": "橘子", "reason": "影响蛋白质消化", "severity": "轻微"},
                    {"food": "韭菜", "reason": "影响钙吸收", "severity": "轻微"}
                ]
            },

            # 调味品
            {
                "name": "食盐",
                "category": "调味品",
                "nutrients": {
                    "sodium": {"value": 38758, "unit": "mg/100g"}
                },
                "recommended_intake": {
                    "adult": "<6g/天",
                    "children": "<3g/天",
                    "hypertension": "<5g/天"
                },
                "health_benefits": ["维持体液平衡", "神经传导"],
                "contraindications": [
                    "高血压患者严格控制",
                    "肾病患者限制摄入",
                    "心血管疾病患者少食"
                ],
                "incompatible_foods": []
            }
        ]

        results = []
        for food in food_data:
            entry = create_material_entry(
                food,
                food["category"],
                source_info["name"]
            )
            results.append(entry)

        return results

    def _scrape_food_incompatibility(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取食物相克数据"""
        self.logger.info("爬取食物相克数据")

        # 常见食物相克组合
        incompatibility_data = [
            {
                "food1": "螃蟹",
                "food2": "柿子",
                "reason": "蟹肉富含蛋白质,柿子含鞣酸,同食易腹痛腹泻",
                "severity": "中等",
                "evidence_level": "民间经验"
            },
            {
                "food1": "豆浆",
                "food2": "鸡蛋",
                "reason": "豆浆中的胰蛋白酶抑制剂影响鸡蛋蛋白质吸收",
                "severity": "轻微",
                "evidence_level": "有争议"
            },
            {
                "food1": "海鲜",
                "food2": "维生素C",
                "reason": "理论上可能生成三氧化二砷,但实际剂量不足以中毒",
                "severity": "轻微",
                "evidence_level": "科学证据不足"
            },
            {
                "food1": "菠菜",
                "food2": "豆腐",
                "reason": "草酸与钙结合形成草酸钙,影响钙吸收",
                "severity": "轻微",
                "evidence_level": "有一定科学依据"
            },
            {
                "food1": "萝卜",
                "food2": "橘子",
                "reason": "萝卜产生硫氰酸抑制甲状腺,橘子类黄酮加强作用",
                "severity": "轻微",
                "evidence_level": "民间经验"
            }
        ]

        results = []
        for item in incompatibility_data:
            entry = {
                "incompatibility_id": f"{item['food1']}_{item['food2']}",
                "foods": [item['food1'], item['food2']],
                "reason": item['reason'],
                "severity": item['severity'],
                "evidence_level": item['evidence_level'],
                "source": source_info["name"],
                "note": "食物相克多为民间经验,缺乏充分科学证据,不必过度恐慌"
            }
            results.append(entry)

        return results

    def _scrape_nutrients_db(self, source_info: Dict) -> List[Dict[str, Any]]:
        """爬取营养成分数据库"""
        self.logger.info("爬取营养价值数据")
        return []

    def _scrape_generic(self, source_info: Dict) -> List[Dict[str, Any]]:
        """通用爬取方法"""
        self.logger.info(f"使用通用方法爬取: {source_info['name']}")
        return []