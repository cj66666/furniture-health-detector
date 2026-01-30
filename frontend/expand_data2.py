"""第二轮数据扩充脚本 - 继续添加更多数据"""
import json
import sys
import os
from datetime import datetime
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_id(name, category):
    """生成唯一ID"""
    unique_string = f"{category}_{name}_{datetime.now().isoformat()}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

def expand_furniture_more():
    """继续扩充家具材质数据"""
    new_materials = [
        # 新型环保材质
        {
            "category": "人造板类",
            "material_type": "秸秆板",
            "chemical_components": [
                {"name": "MDI胶", "cas": "26447-40-5", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "环保材质", "severity": "低", "description": "农作物秸秆制成,零甲醛"}
            ],
            "visual_cues": ["秸秆纹理", "黄褐色", "轻质"],
            "certifications": ["环保认证"]
        },
        {
            "category": "人造板类",
            "material_type": "禾香板",
            "chemical_components": [
                {"name": "MDI生态胶", "cas": "26447-40-5", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "零甲醛", "severity": "低", "description": "稻麦秸秆为原料,无醛添加"}
            ],
            "visual_cues": ["稻草纤维可见", "环保标识"],
            "certifications": ["NAF", "CARB P2"]
        },
        # 实木类扩充
        {
            "category": "实木类",
            "material_type": "樱桃木",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [
                {"type": "价格高", "severity": "低", "description": "名贵硬木,价格昂贵"}
            ],
            "visual_cues": ["红褐色", "细腻纹理", "质地温润"],
            "certifications": ["FSC"]
        },
        {
            "category": "实木类",
            "material_type": "白蜡木",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [
                {"type": "开裂风险", "severity": "中", "description": "含水率高易开裂"}
            ],
            "visual_cues": ["浅白色", "山形纹理", "质地坚韧"],
            "certifications": ["FSC"]
        },
        {
            "category": "实木类",
            "material_type": "柚木",
            "chemical_components": [
                {"name": "天然油脂", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "假货多", "severity": "中", "description": "市场假冒柚木多"}
            ],
            "visual_cues": ["金黄色", "油性光泽", "防水性强"],
            "certifications": ["FSC"]
        },
        # 复合材质
        {
            "category": "复合材质",
            "material_type": "木塑复合材料",
            "chemical_components": [
                {"name": "木粉+PE/PP", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "耐候性", "severity": "低", "description": "户外使用需防紫外线"}
            ],
            "visual_cues": ["仿木纹理", "防水防腐"],
            "certifications": ["环保认证"]
        },
        {
            "category": "复合材质",
            "material_type": "碳纤维复合材料",
            "chemical_components": [
                {"name": "碳纤维+树脂", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "价格极高", "severity": "低", "description": "高端材质价格昂贵"}
            ],
            "visual_cues": ["黑色编织纹理", "轻质高强"],
            "certifications": ["ISO 9001"]
        },
        # 玻璃类
        {
            "category": "玻璃类",
            "material_type": "钢化玻璃",
            "chemical_components": [
                {"name": "二氧化硅", "cas": "7631-86-9", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "自爆风险", "severity": "低", "description": "千分之三自爆率"}
            ],
            "visual_cues": ["透明", "边角有CCC标识"],
            "certifications": ["3C认证"]
        },
        {
            "category": "玻璃类",
            "material_type": "夹层玻璃",
            "chemical_components": [
                {"name": "PVB胶片", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "安全性高", "severity": "低", "description": "破碎不飞溅"}
            ],
            "visual_cues": ["多层结构", "安全玻璃"],
            "certifications": ["3C认证"]
        },
        # 石材类
        {
            "category": "石材类",
            "material_type": "天然大理石",
            "chemical_components": [
                {"name": "碳酸钙", "cas": "471-34-1", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "放射性", "severity": "中", "description": "部分大理石有微量放射性"}
            ],
            "visual_cues": ["天然纹理", "冷触感", "重量大"],
            "certifications": ["放射性检测"]
        },
        {
            "category": "石材类",
            "material_type": "人造石英石",
            "chemical_components": [
                {"name": "石英砂+树脂", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "树脂气味", "severity": "低", "description": "新品可能有轻微树脂味"}
            ],
            "visual_cues": ["均匀花纹", "硬度高"],
            "certifications": ["NSF认证"]
        },
        # 藤编类
        {
            "category": "天然材质",
            "material_type": "藤编",
            "chemical_components": [
                {"name": "天然藤条", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "虫蛀风险", "severity": "中", "description": "需防虫防潮"}
            ],
            "visual_cues": ["编织纹理", "天然色泽"],
            "certifications": ["FSC"]
        },
        {
            "category": "天然材质",
            "material_type": "竹材",
            "chemical_components": [
                {"name": "天然竹纤维", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "开裂风险", "severity": "中", "description": "需防干燥开裂"}
            ],
            "visual_cues": ["竹节纹理", "清香"],
            "certifications": ["FSC"]
        }
    ]

    results = []
    for material in new_materials:
        entry = {
            "material_id": generate_id(material["material_type"], material["category"]),
            "category": material["category"],
            "data": material,
            "source": "第二轮数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "2.0"
        }
        results.append(entry)

    return results

def expand_textile_more():
    """继续扩充衣料材质数据"""
    new_textiles = [
        # 功能性面料
        {
            "fabric_type": "防晒面料",
            "composition": "涤纶+防晒助剂",
            "chemical_treatments": [
                {"name": "紫外线吸收剂", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "化学助剂", "severity": "低", "description": "防晒助剂残留极少"}
            ],
            "health_benefits": ["UPF50+防晒", "防紫外线"],
            "care_instructions": {
                "washing": "轻柔洗涤",
                "drying": "阴干",
                "ironing": "不熨烫"
            },
            "certifications": ["UPF认证"]
        },
        {
            "fabric_type": "速干面料",
            "composition": "聚酯纤维速干纤维",
            "chemical_treatments": [
                {"name": "吸湿排汗整理", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "静电", "severity": "低", "description": "易产生静电"}
            ],
            "health_benefits": ["快速排汗", "速干透气"],
            "care_instructions": {
                "washing": "可机洗",
                "drying": "快速风干",
                "ironing": "低温"
            },
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "抗菌面料",
            "composition": "棉/涤纶+银离子",
            "chemical_treatments": [
                {"name": "银离子抗菌剂", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "银离子过敏", "severity": "低", "description": "极少数人对银过敏"}
            ],
            "health_benefits": ["抗菌抑菌", "防臭"],
            "care_instructions": {
                "washing": "温和洗涤",
                "drying": "自然晾干",
                "ironing": "中温"
            },
            "certifications": ["抗菌检测"]
        },
        # 户外面料
        {
            "fabric_type": "冲锋衣面料",
            "composition": "尼龙+PTFE薄膜",
            "chemical_treatments": [
                {"name": "防水透湿涂层", "hazard": "中"},
                {"name": "DWR拒水剂", "hazard": "中"}
            ],
            "health_risks": [
                {"type": "PFAS", "severity": "中", "description": "传统DWR含全氟化合物"}
            ],
            "health_benefits": ["防水透气", "防风"],
            "care_instructions": {
                "washing": "专用洗涤剂",
                "drying": "低温烘干恢复防水",
                "ironing": "不熨烫"
            },
            "certifications": ["bluesign"]
        },
        {
            "fabric_type": "羽绒",
            "composition": "鹅绒/鸭绒",
            "chemical_treatments": [
                {"name": "清洗消毒", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "过敏", "severity": "中", "description": "羽绒过敏者禁用"}
            ],
            "health_benefits": ["保暖性极佳", "轻盈"],
            "care_instructions": {
                "washing": "专业清洗",
                "drying": "低温烘干拍打",
                "ironing": "不熨烫"
            },
            "certifications": ["RDS负责任羽绒"]
        },
        # 特殊工艺
        {
            "fabric_type": "水洗棉",
            "composition": "100%棉水洗工艺",
            "chemical_treatments": [
                {"name": "柔软剂", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "缩水", "severity": "低", "description": "预缩水处理"}
            ],
            "health_benefits": ["柔软舒适", "透气吸汗"],
            "care_instructions": {
                "washing": "可机洗",
                "drying": "自然晾干",
                "ironing": "中高温"
            },
            "certifications": ["GOTS"]
        },
        {
            "fabric_type": "双面羊绒",
            "composition": "100%羊绒双层编织",
            "chemical_treatments": [
                {"name": "防缩处理", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "价格昂贵", "severity": "低", "description": "名贵面料"}
            ],
            "health_benefits": ["极致保暖", "奢华手感"],
            "care_instructions": {
                "washing": "干洗",
                "drying": "平铺晾干",
                "ironing": "蒸汽低温"
            },
            "certifications": ["Woolmark"]
        },
        {
            "fabric_type": "牛仔布",
            "composition": "棉+少量弹力纤维",
            "chemical_treatments": [
                {"name": "靛蓝染料", "hazard": "低"},
                {"name": "水洗加工", "hazard": "低"}
            ],
            "health_risks": [
                {"type": "掉色", "severity": "低", "description": "初期可能掉色"}
            ],
            "health_benefits": ["耐磨耐穿", "经典时尚"],
            "care_instructions": {
                "washing": "翻面洗涤",
                "drying": "自然晾干",
                "ironing": "中温"
            },
            "certifications": ["OEKO-TEX"]
        }
    ]

    results = []
    for textile in new_textiles:
        entry = {
            "material_id": generate_id(textile["fabric_type"], "衣料纺织品"),
            "category": "衣料纺织品",
            "data": textile,
            "source": "第二轮数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "2.0"
        }
        results.append(entry)

    return results

def expand_food_more():
    """继续扩充食物数据"""
    new_foods = [
        # 更多蔬菜
        {
            "name": "芹菜",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 14, "unit": "kcal/100g"},
                "fiber": {"value": 1.2, "unit": "g/100g"},
                "potassium": {"value": 206, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "50-100g/天"},
            "health_benefits": ["降血压", "利尿", "清热"],
            "contraindications": ["低血压者慎食"],
            "incompatible_foods": []
        },
        {
            "name": "黄瓜",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 15, "unit": "kcal/100g"},
                "water": {"value": 96, "unit": "%"},
                "vitamin_c": {"value": 9, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["补水", "美容", "减肥"],
            "contraindications": [],
            "incompatible_foods": [
                {"food": "西红柿", "reason": "维生素C分解酶", "severity": "轻微"}
            ]
        },
        {
            "name": "土豆",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 81, "unit": "kcal/100g"},
                "starch": {"value": 17.2, "unit": "g/100g"},
                "vitamin_c": {"value": 27, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "150-250g/天"},
            "health_benefits": ["饱腹感强", "补充维C", "养胃"],
            "contraindications": ["发芽土豆有毒禁食", "糖尿病患者控制量"],
            "incompatible_foods": []
        },
        # 更多水果
        {
            "name": "葡萄",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 43, "unit": "kcal/100g"},
                "resveratrol": {"value": "丰富", "unit": "N/A"},
                "glucose": {"value": 10.3, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["抗氧化", "护心", "美容"],
            "contraindications": ["糖尿病患者少食"],
            "incompatible_foods": []
        },
        {
            "name": "橙子",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 47, "unit": "kcal/100g"},
                "vitamin_c": {"value": 33, "unit": "mg/100g"},
                "folate": {"value": 30, "unit": "μg/100g"}
            },
            "recommended_intake": {"adult": "1-2个/天"},
            "health_benefits": ["补充维C", "增强免疫", "美白"],
            "contraindications": ["空腹不宜多食"],
            "incompatible_foods": [
                {"food": "牛奶", "reason": "影响蛋白质消化", "severity": "轻微"}
            ]
        },
        {
            "name": "柚子",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 41, "unit": "kcal/100g"},
                "vitamin_c": {"value": 61, "unit": "mg/100g"},
                "naringin": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["降血糖", "降血脂", "助消化"],
            "contraindications": ["服药期间慎食(影响药效)"],
            "incompatible_foods": []
        },
        # 菌菇类
        {
            "name": "香菇",
            "category": "菌菇类",
            "nutrients": {
                "energy": {"value": 19, "unit": "kcal/100g"},
                "protein": {"value": 2.2, "unit": "g/100g"},
                "polysaccharide": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "50-100g/天"},
            "health_benefits": ["增强免疫", "抗癌", "降胆固醇"],
            "contraindications": ["痛风患者少食"],
            "incompatible_foods": []
        },
        {
            "name": "木耳",
            "category": "菌菇类",
            "nutrients": {
                "energy": {"value": 27, "unit": "kcal/100g"},
                "iron": {"value": 97.4, "unit": "mg/100g"},
                "fiber": {"value": 2.6, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "30-50g/天(干品)"},
            "health_benefits": ["补血", "清肺", "通便"],
            "contraindications": ["鲜木耳有毒需煮熟", "泡发时间不超过4小时"],
            "incompatible_foods": []
        },
        # 海产品
        {
            "name": "海带",
            "category": "水产类",
            "nutrients": {
                "energy": {"value": 13, "unit": "kcal/100g"},
                "iodine": {"value": 36240, "unit": "μg/100g"},
                "calcium": {"value": 348, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "15-30g/天(干品)"},
            "health_benefits": ["补碘", "降血脂", "防辐射"],
            "contraindications": ["甲亢患者禁食", "碘摄入过量风险"],
            "incompatible_foods": []
        },
        {
            "name": "紫菜",
            "category": "水产类",
            "nutrients": {
                "energy": {"value": 207, "unit": "kcal/100g"},
                "protein": {"value": 26.7, "unit": "g/100g"},
                "iodine": {"value": 4323, "unit": "μg/100g"}
            },
            "recommended_intake": {"adult": "5-10g/天(干品)"},
            "health_benefits": ["补碘", "高蛋白", "护眼"],
            "contraindications": ["甲亢患者少食"],
            "incompatible_foods": []
        },
        # 调味品
        {
            "name": "酱油",
            "category": "调味品",
            "nutrients": {
                "sodium": {"value": 5586, "unit": "mg/100ml"},
                "protein": {"value": 8.3, "unit": "g/100ml"}
            },
            "recommended_intake": {"adult": "<10ml/天"},
            "health_benefits": ["增加食欲", "提供鲜味"],
            "contraindications": ["高血压患者严格限制", "肾病患者少食"],
            "incompatible_foods": []
        },
        {
            "name": "醋",
            "category": "调味品",
            "nutrients": {
                "acetic_acid": {"value": 3.5, "unit": "g/100ml"}
            },
            "recommended_intake": {"adult": "10-15ml/天"},
            "health_benefits": ["助消化", "软化血管", "杀菌"],
            "contraindications": ["胃酸过多者少食"],
            "incompatible_foods": []
        },
        {
            "name": "姜",
            "category": "调味品",
            "nutrients": {
                "gingerol": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "3-5g/天"},
            "health_benefits": ["驱寒", "止呕", "发汗"],
            "contraindications": ["阴虚火旺者慎食", "晚上不宜多食"],
            "incompatible_foods": []
        },
        {
            "name": "蒜",
            "category": "调味品",
            "nutrients": {
                "allicin": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "2-3瓣/天"},
            "health_benefits": ["杀菌", "抗癌", "降血脂"],
            "contraindications": ["眼病患者慎食", "肝病患者少食"],
            "incompatible_foods": []
        },
        # 饮品
        {
            "name": "绿茶",
            "category": "饮品类",
            "nutrients": {
                "tea_polyphenols": {"value": "高", "unit": "N/A"},
                "caffeine": {"value": 20, "unit": "mg/杯"}
            },
            "recommended_intake": {"adult": "2-3杯/天"},
            "health_benefits": ["抗氧化", "提神", "减肥"],
            "contraindications": ["失眠者晚上不宜", "贫血患者少饮"],
            "incompatible_foods": []
        },
        {
            "name": "蜂蜜",
            "category": "甜品类",
            "nutrients": {
                "energy": {"value": 321, "unit": "kcal/100g"},
                "fructose": {"value": 40, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "20-30g/天"},
            "health_benefits": ["润肠", "美容", "润肺"],
            "contraindications": ["1岁以下婴儿禁食", "糖尿病患者慎食"],
            "incompatible_foods": [
                {"food": "豆腐", "reason": "同食易腹泻", "severity": "轻微"}
            ]
        }
    ]

    results = []
    for food in new_foods:
        entry = {
            "material_id": generate_id(food["name"], food["category"]),
            "category": food["category"],
            "data": food,
            "source": "第二轮数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "2.0"
        }
        results.append(entry)

    return results

def main():
    """主函数"""
    base_dir = r"D:\Users\86198\WeChatProjects\数据库\processed"

    print("\n" + "="*60)
    print("第二轮数据扩充开始...")
    print("="*60)

    # 扩充家具数据
    print("\n1. 扩充家具材质数据...")
    furniture_file = os.path.join(base_dir, "furniture.json")
    with open(furniture_file, 'r', encoding='utf-8') as f:
        existing_furniture = json.load(f)

    new_furniture = expand_furniture_more()
    all_furniture = existing_furniture + new_furniture

    with open(furniture_file, 'w', encoding='utf-8') as f:
        json.dump(all_furniture, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_furniture)} 条")
    print(f"   新增: {len(new_furniture)} 条")
    print(f"   总计: {len(all_furniture)} 条")

    # 扩充衣料数据
    print("\n2. 扩充衣料材质数据...")
    textile_file = os.path.join(base_dir, "textile.json")
    with open(textile_file, 'r', encoding='utf-8') as f:
        existing_textile = json.load(f)

    new_textile = expand_textile_more()
    all_textile = existing_textile + new_textile

    with open(textile_file, 'w', encoding='utf-8') as f:
        json.dump(all_textile, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_textile)} 条")
    print(f"   新增: {len(new_textile)} 条")
    print(f"   总计: {len(all_textile)} 条")

    # 扩充食物数据
    print("\n3. 扩充食物数据...")
    food_file = os.path.join(base_dir, "food.json")
    with open(food_file, 'r', encoding='utf-8') as f:
        existing_food = json.load(f)

    new_food = expand_food_more()
    all_food = existing_food + new_food

    with open(food_file, 'w', encoding='utf-8') as f:
        json.dump(all_food, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_food)} 条")
    print(f"   新增: {len(new_food)} 条")
    print(f"   总计: {len(all_food)} 条")

    # 总结
    print("\n" + "="*60)
    print("第二轮数据扩充完成!")
    print("="*60)
    print(f"家具材质: {len(all_furniture)} 条 (+{len(new_furniture)})")
    print(f"衣料材质: {len(all_textile)} 条 (+{len(new_textile)})")
    print(f"食物数据: {len(all_food)} 条 (+{len(new_food)})")
    total = len(all_furniture) + len(all_textile) + len(all_food)
    new_total = len(new_furniture) + len(new_textile) + len(new_food)
    print(f"\n总计: {total} 条数据 (本轮新增 {new_total} 条)")
    print("="*60)

if __name__ == "__main__":
    main()