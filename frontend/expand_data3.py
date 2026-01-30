"""第三轮数据扩充脚本 - 继续大幅度扩充数据"""
import json
import sys
import os
from datetime import datetime
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_id(name, category):
    unique_string = f"{category}_{name}_{datetime.now().isoformat()}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

def expand_furniture_round3():
    """第三轮家具材质扩充"""
    new_materials = [
        # 更多实木
        {
            "category": "实木类",
            "material_type": "红木",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [{"type": "价格昂贵", "severity": "低", "description": "名贵红木价格极高"}],
            "visual_cues": ["红褐色", "质地坚硬", "纹理华美"],
            "certifications": ["CITES"]
        },
        {
            "category": "实木类",
            "material_type": "桦木",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [{"type": "易开裂", "severity": "中", "description": "干燥地区易开裂"}],
            "visual_cues": ["浅黄白色", "纹理细腻"],
            "certifications": ["FSC"]
        },
        {
            "category": "实木类",
            "material_type": "枫木",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [{"type": "硬度高", "severity": "低", "description": "加工难度大"}],
            "visual_cues": ["白中略带红", "致密纹理"],
            "certifications": ["FSC"]
        },
        # 软装材质
        {
            "category": "软装材质",
            "material_type": "海绵",
            "chemical_components": [
                {"name": "聚氨酯", "cas": "9009-54-5", "hazard": "中"},
                {"name": "TDI/MDI", "cas": "584-84-9", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "VOCs释放", "severity": "中", "description": "新海绵可能释放异味"}
            ],
            "visual_cues": ["多孔结构", "弹性好"],
            "certifications": ["CertiPUR-US"]
        },
        {
            "category": "软装材质",
            "material_type": "乳胶",
            "chemical_components": [
                {"name": "天然乳胶", "cas": "9006-04-6", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "乳胶过敏", "severity": "中", "description": "对乳胶过敏者不适用"}
            ],
            "visual_cues": ["乳白色", "弹性极佳", "蜂窝结构"],
            "certifications": ["LGA", "ECO"]
        },
        {
            "category": "软装材质",
            "material_type": "记忆棉",
            "chemical_components": [
                {"name": "慢回弹聚氨酯", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "化学气味", "severity": "中", "description": "新品可能有异味"}
            ],
            "visual_cues": ["慢回弹", "贴合身体"],
            "certifications": ["CertiPUR-US"]
        },
        # 装饰材料
        {
            "category": "装饰材料",
            "material_type": "壁纸",
            "chemical_components": [
                {"name": "PVC", "cas": "9002-86-2", "hazard": "中"},
                {"name": "胶水", "cas": "N/A", "hazard": "高"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "高", "description": "胶水可能含甲醛"},
                {"type": "塑化剂", "severity": "中", "description": "PVC壁纸含塑化剂"}
            ],
            "visual_cues": ["表面印花", "可擦洗"],
            "certifications": ["十环认证"]
        },
        {
            "category": "装饰材料",
            "material_type": "乳胶漆",
            "chemical_components": [
                {"name": "丙烯酸乳液", "cas": "N/A", "hazard": "低"},
                {"name": "VOCs", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "VOCs", "severity": "中", "description": "施工期释放VOCs"}
            ],
            "visual_cues": ["液体涂料", "遮盖力强"],
            "certifications": ["十环认证", "绿色之星"]
        },
        {
            "category": "装饰材料",
            "material_type": "硅藻泥",
            "chemical_components": [
                {"name": "硅藻土", "cas": "61790-53-2", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "吸湿性强", "severity": "低", "description": "潮湿地区需注意"}
            ],
            "visual_cues": ["粗糙质感", "无光泽"],
            "certifications": ["JC/T 2177"]
        },
        # 地板材质
        {
            "category": "地板类",
            "material_type": "强���地板",
            "chemical_components": [
                {"name": "高密度板基材", "cas": "N/A", "hazard": "中"},
                {"name": "三聚氰胺", "cas": "108-78-1", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "中", "description": "基材可能释放甲醛"}
            ],
            "visual_cues": ["耐磨层", "仿木纹"],
            "certifications": ["E0", "E1"]
        },
        {
            "category": "地板类",
            "material_type": "实木复合地板",
            "chemical_components": [
                {"name": "实木+胶合板", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "低", "description": "胶水用量少"}
            ],
            "visual_cues": ["表层实木", "稳定性好"],
            "certifications": ["E0", "FSC"]
        },
        {
            "category": "地板类",
            "material_type": "SPC地板",
            "chemical_components": [
                {"name": "石塑复合材料", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "零甲醛", "severity": "低", "description": "无胶水零甲醛"}
            ],
            "visual_cues": ["坚硬", "防水", "锁扣式"],
            "certifications": ["FloorScore"]
        },
        # 胶粘剂
        {
            "category": "辅材类",
            "material_type": "白乳胶",
            "chemical_components": [
                {"name": "聚醋酸乙烯", "cas": "9003-20-7", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "低", "description": "环保白乳胶甲醛低"}
            ],
            "visual_cues": ["乳白色", "水溶性"],
            "certifications": ["十环认证"]
        },
        {
            "category": "辅材类",
            "material_type": "玻璃胶",
            "chemical_components": [
                {"name": "硅酮", "cas": "N/A", "hazard": "中"},
                {"name": "醋酸", "cas": "64-19-7", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "酸味刺激", "severity": "中", "description": "固化时释放醋酸"}
            ],
            "visual_cues": ["透明或白色", "柔韧性好"],
            "certifications": ["十环认证"]
        }
    ]

    results = []
    for material in new_materials:
        entry = {
            "material_id": generate_id(material["material_type"], material["category"]),
            "category": material["category"],
            "data": material,
            "source": "第三轮数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "3.0"
        }
        results.append(entry)
    return results

def expand_textile_round3():
    """第三轮衣料材质扩充"""
    new_textiles = [
        # 特种面料
        {
            "fabric_type": "防静电面料",
            "composition": "涤纶+导电纤维",
            "chemical_treatments": [{"name": "导电纤维植入", "hazard": "低"}],
            "health_risks": [{"type": "无特殊风险", "severity": "低", "description": "安全性高"}],
            "health_benefits": ["防静电", "防尘"],
            "care_instructions": {"washing": "可机洗", "drying": "低温烘干", "ironing": "不熨烫"},
            "certifications": ["GB 12014"]
        },
        {
            "fabric_type": "阻燃面料",
            "composition": "阻燃纤维",
            "chemical_treatments": [{"name": "阻燃剂", "hazard": "中"}],
            "health_risks": [{"type": "阻燃剂残留", "severity": "中", "description": "部分阻燃剂有毒性"}],
            "health_benefits": ["防火安全"],
            "care_instructions": {"washing": "专业清洗", "drying": "自然晾干", "ironing": "不熨烫"},
            "certifications": ["GB 8965"]
        },
        {
            "fabric_type": "保暖内衣面料",
            "composition": "莫代尔+氨纶",
            "chemical_treatments": [{"name": "柔软整理", "hazard": "低"}],
            "health_risks": [{"type": "过紧影响血液循环", "severity": "低", "description": "选择合适尺码"}],
            "health_benefits": ["保暖透气", "柔软贴身"],
            "care_instructions": {"washing": "手洗", "drying": "平铺晾干", "ironing": "不熨烫"},
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "冰丝",
            "composition": "改性纤维素纤维",
            "chemical_treatments": [{"name": "凉感整理", "hazard": "低"}],
            "health_risks": [{"type": "易起球", "severity": "低", "description": "质量差的易起球"}],
            "health_benefits": ["凉感", "透气", "顺滑"],
            "care_instructions": {"washing": "轻柔洗", "drying": "阴干", "ironing": "低温"},
            "certifications": ["OEKO-TEX"]
        },
        # 传统面料
        {
            "fabric_type": "棉绒",
            "composition": "100%棉起绒工艺",
            "chemical_treatments": [{"name": "起绒处理", "hazard": "低"}],
            "health_risks": [{"type": "掉毛", "severity": "低", "description": "初次使用可能掉毛"}],
            "health_benefits": ["保暖", "柔软", "吸湿"],
            "care_instructions": {"washing": "单独洗", "drying": "晾干", "ironing": "不熨烫"},
            "certifications": ["GOTS"]
        },
        {
            "fabric_type": "帆布",
            "composition": "纯棉或棉麻",
            "chemical_treatments": [{"name": "上浆", "hazard": "低"}],
            "health_risks": [{"type": "较硬", "severity": "低", "description": "新品较硬需软化"}],
            "health_benefits": ["耐磨", "透气", "环保"],
            "care_instructions": {"washing": "可机洗", "drying": "晾干", "ironing": "高温"},
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "雪纺",
            "composition": "涤纶或真丝",
            "chemical_treatments": [{"name": "柔软整理", "hazard": "低"}],
            "health_risks": [{"type": "易钩丝", "severity": "低", "description": "需小心穿着"}],
            "health_benefits": ["轻薄", "飘逸", "透气"],
            "care_instructions": {"washing": "手洗", "drying": "阴干", "ironing": "低温隔布"},
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "针织棉",
            "composition": "100%棉针织",
            "chemical_treatments": [{"name": "柔软整理", "hazard": "低"}],
            "health_risks": [{"type": "易变形", "severity": "低", "description": "需平铺晾干"}],
            "health_benefits": ["弹性好", "舒适", "透气"],
            "care_instructions": {"washing": "可机洗", "drying": "平铺晾干", "ironing": "中温"},
            "certifications": ["GOTS"]
        },
        {
            "fabric_type": "法兰绒",
            "composition": "涤纶或羊毛",
            "chemical_treatments": [{"name": "拉毛整理", "hazard": "低"}],
            "health_risks": [{"type": "掉毛", "severity": "低", "description": "初次使用掉毛"}],
            "health_benefits": ["保暖", "柔软", "舒适"],
            "care_instructions": {"washing": "轻柔洗", "drying": "晾干", "ironing": "不熨烫"},
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "珊瑚绒",
            "composition": "涤纶超细纤维",
            "chemical_treatments": [{"name": "柔软剂", "hazard": "低"}],
            "health_risks": [{"type": "静电", "severity": "低", "description": "易产生静电"}],
            "health_benefits": ["超柔软", "保暖", "不掉毛"],
            "care_instructions": {"washing": "可机洗", "drying": "低温烘干", "ironing": "不熨烫"},
            "certifications": ["OEKO-TEX"]
        }
    ]

    results = []
    for textile in new_textiles:
        entry = {
            "material_id": generate_id(textile["fabric_type"], "衣料纺织品"),
            "category": "衣料纺织品",
            "data": textile,
            "source": "第三轮数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "3.0"
        }
        results.append(entry)
    return results

def expand_food_round3():
    """第三轮食物数据扩充"""
    new_foods = [
        # 更多谷物
        {
            "name": "玉米",
            "category": "谷物类",
            "nutrients": {
                "energy": {"value": 112, "unit": "kcal/100g"},
                "fiber": {"value": 2.9, "unit": "g/100g"},
                "lutein": {"value": "丰富", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["护眼", "通便", "抗衰老"],
            "contraindications": [],
            "incompatible_foods": []
        },
        {
            "name": "紫薯",
            "category": "谷物类",
            "nutrients": {
                "energy": {"value": 82, "unit": "kcal/100g"},
                "anthocyanins": {"value": "极高", "unit": "N/A"},
                "fiber": {"value": 1.6, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "100-150g/天"},
            "health_benefits": ["抗氧化", "护肝", "通便"],
            "contraindications": ["糖尿病患者控制量"],
            "incompatible_foods": []
        },
        # 更多蔬菜
        {
            "name": "白菜",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 17, "unit": "kcal/100g"},
                "vitamin_c": {"value": 31, "unit": "mg/100g"},
                "calcium": {"value": 50, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["清热", "通便", "补钙"],
            "contraindications": [],
            "incompatible_foods": []
        },
        {
            "name": "茄子",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 21, "unit": "kcal/100g"},
                "anthocyanins": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "100-150g/天"},
            "health_benefits": ["保护心血管", "抗衰老"],
            "contraindications": ["生食有毒"],
            "incompatible_foods": []
        },
        {
            "name": "南瓜",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 26, "unit": "kcal/100g"},
                "carotene": {"value": 3100, "unit": "μg/100g"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["护眼", "降血糖", "通便"],
            "contraindications": ["湿热体质少食"],
            "incompatible_foods": []
        },
        # 更多水果
        {
            "name": "草莓",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 32, "unit": "kcal/100g"},
                "vitamin_c": {"value": 47, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "100-150g/天"},
            "health_benefits": ["美白", "抗氧化", "助消化"],
            "contraindications": ["农药残留需清洗干净"],
            "incompatible_foods": []
        },
        {
            "name": "猕猴桃",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 56, "unit": "kcal/100g"},
                "vitamin_c": {"value": 62, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "1-2个/天"},
            "health_benefits": ["维C之王", "通便", "美容"],
            "contraindications": ["脾胃虚寒者少食"],
            "incompatible_foods": [{"food": "牛奶", "reason": "影响消化", "severity": "轻微"}]
        },
        {
            "name": "西瓜",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 26, "unit": "kcal/100g"},
                "lycopene": {"value": 4868, "unit": "μg/100g"}
            },
            "recommended_intake": {"adult": "200-300g/天"},
            "health_benefits": ["清热解暑", "利尿", "补水"],
            "contraindications": ["糖尿病患者少食", "脾胃虚寒少食"],
            "incompatible_foods": [{"food": "羊肉", "reason": "寒热相冲", "severity": "中等"}]
        },
        # 药食同源
        {
            "name": "枸杞",
            "category": "药食同源",
            "nutrients": {
                "energy": {"value": 258, "unit": "kcal/100g"},
                "carotene": {"value": "极高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "10-15g/天"},
            "health_benefits": ["明目", "养肝", "抗衰老"],
            "contraindications": ["感冒发烧期间不宜", "腹泻者慎食"],
            "incompatible_foods": []
        },
        {
            "name": "红枣",
            "category": "药食同源",
            "nutrients": {
                "energy": {"value": 122, "unit": "kcal/100g"},
                "iron": {"value": 2.3, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "3-5颗/天"},
            "health_benefits": ["补血", "养颜", "安神"],
            "contraindications": ["糖尿病患者少食", "湿热体质少食"],
            "incompatible_foods": []
        },
        {
            "name": "山药",
            "category": "药食同源",
            "nutrients": {
                "energy": {"value": 57, "unit": "kcal/100g"},
                "mucilage": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["健脾", "养胃", "补肾"],
            "contraindications": ["便秘者慎食"],
            "incompatible_foods": []
        },
        # 干果
        {
            "name": "葡萄干",
            "category": "干果类",
            "nutrients": {
                "energy": {"value": 299, "unit": "kcal/100g"},
                "iron": {"value": 9.1, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "30-50g/天"},
            "health_benefits": ["补血", "抗疲劳"],
            "contraindications": ["糖尿病患者慎食"],
            "incompatible_foods": []
        },
        {
            "name": "桂圆",
            "category": "干果类",
            "nutrients": {
                "energy": {"value": 273, "unit": "kcal/100g"},
                "iron": {"value": 3.9, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "5-10颗/天"},
            "health_benefits": ["补血", "安神", "益智"],
            "contraindications": ["上火体质少食", "孕妇慎食"],
            "incompatible_foods": []
        },
        # 更多调味品
        {
            "name": "花椒",
            "category": "调味品",
            "nutrients": {},
            "recommended_intake": {"adult": "1-2g/天"},
            "health_benefits": ["驱寒", "除湿", "止痛"],
            "contraindications": ["阴虚火旺者慎用", "孕妇慎用"],
            "incompatible_foods": []
        },
        {
            "name": "八角",
            "category": "调味品",
            "nutrients": {},
            "recommended_intake": {"adult": "1-2个/天"},
            "health_benefits": ["温阳散寒", "理气止痛"],
            "contraindications": ["热性体质慎用"],
            "incompatible_foods": []
        },
        # 饮品
        {
            "name": "红茶",
            "category": "饮品类",
            "nutrients": {
                "tea_polyphenols": {"value": "中", "unit": "N/A"},
                "caffeine": {"value": 25, "unit": "mg/杯"}
            },
            "recommended_intake": {"adult": "2-3杯/天"},
            "health_benefits": ["暖胃", "提神", "助消化"],
            "contraindications": ["神经衰弱者慎饮"],
            "incompatible_foods": []
        },
        {
            "name": "菊花茶",
            "category": "饮品类",
            "nutrients": {},
            "recommended_intake": {"adult": "1-2杯/天"},
            "health_benefits": ["清热", "明目", "降火"],
            "contraindications": ["脾胃虚寒者慎饮"],
            "incompatible_foods": []
        },
        # 油脂
        {
            "name": "橄榄油",
            "category": "油脂类",
            "nutrients": {
                "energy": {"value": 899, "unit": "kcal/100g"},
                "monounsaturated_fat": {"value": 73, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "25-30g/天"},
            "health_benefits": ["护心", "抗氧化", "润肠"],
            "contraindications": [],
            "incompatible_foods": []
        },
        {
            "name": "花生油",
            "category": "油脂类",
            "nutrients": {
                "energy": {"value": 899, "unit": "kcal/100g"},
                "vitamin_e": {"value": 42, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "25-30g/天"},
            "health_benefits": ["补充维E", "降胆固醇"],
            "contraindications": ["高血脂者控制量"],
            "incompatible_foods": []
        }
    ]

    results = []
    for food in new_foods:
        entry = {
            "material_id": generate_id(food["name"], food["category"]),
            "category": food["category"],
            "data": food,
            "source": "第三轮数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "3.0"
        }
        results.append(entry)
    return results

def main():
    base_dir = r"D:\Users\86198\WeChatProjects\数据库\processed"

    print("\n" + "="*60)
    print("第三轮数据扩充开始...")
    print("="*60)

    # 家具
    print("\n1. 扩充家具材质数据...")
    furniture_file = os.path.join(base_dir, "furniture.json")
    with open(furniture_file, 'r', encoding='utf-8') as f:
        existing_furniture = json.load(f)
    new_furniture = expand_furniture_round3()
    all_furniture = existing_furniture + new_furniture
    with open(furniture_file, 'w', encoding='utf-8') as f:
        json.dump(all_furniture, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_furniture)} 条")
    print(f"   新增: {len(new_furniture)} 条")
    print(f"   总计: {len(all_furniture)} 条")

    # 衣料
    print("\n2. 扩充衣料材质数据...")
    textile_file = os.path.join(base_dir, "textile.json")
    with open(textile_file, 'r', encoding='utf-8') as f:
        existing_textile = json.load(f)
    new_textile = expand_textile_round3()
    all_textile = existing_textile + new_textile
    with open(textile_file, 'w', encoding='utf-8') as f:
        json.dump(all_textile, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_textile)} 条")
    print(f"   新增: {len(new_textile)} 条")
    print(f"   总计: {len(all_textile)} 条")

    # 食物
    print("\n3. 扩充食物数据...")
    food_file = os.path.join(base_dir, "food.json")
    with open(food_file, 'r', encoding='utf-8') as f:
        existing_food = json.load(f)
    new_food = expand_food_round3()
    all_food = existing_food + new_food
    with open(food_file, 'w', encoding='utf-8') as f:
        json.dump(all_food, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_food)} 条")
    print(f"   新增: {len(new_food)} 条")
    print(f"   总计: {len(all_food)} 条")

    # 总结
    print("\n" + "="*60)
    print("第三轮数据扩充完成!")
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