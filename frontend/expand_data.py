"""数据扩充脚本 - 添加更多家具、衣料和食物数据"""
import json
import sys
import os
from datetime import datetime
import hashlib

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import create_material_entry

def generate_id(name, category):
    """生成唯一ID"""
    unique_string = f"{category}_{name}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

def expand_furniture_data():
    """扩充家具材质数据"""
    new_materials = [
        # 添加更多人造板
        {
            "category": "人造板类",
            "material_type": "多层实木板",
            "chemical_components": [
                {"name": "甲醛", "cas": "50-00-0", "hazard": "低"},
                {"name": "酚醛树脂", "cas": "9003-35-4", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "低", "description": "层间胶水可能有微量甲醛"}
            ],
            "visual_cues": ["层状结构明显", "侧面可见木纹层"],
            "certifications": ["E0", "E1"]
        },
        {
            "category": "人造板类",
            "material_type": "实木指接板",
            "chemical_components": [
                {"name": "甲醛", "cas": "50-00-0", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "低", "description": "拼接处用胶少,甲醛释放量低"}
            ],
            "visual_cues": ["锯齿状拼接痕迹", "保留天然木纹"],
            "certifications": ["E0", "FSC"]
        },
        {
            "category": "人造板类",
            "material_type": "OSB定向刨花板",
            "chemical_components": [
                {"name": "甲醛", "cas": "50-00-0", "hazard": "中"},
                {"name": "MDI胶", "cas": "26447-40-5", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "甲醛", "severity": "中", "description": "使用MDI胶甲醛更低"}
            ],
            "visual_cues": ["刨片定向排列", "表面粗糙"],
            "certifications": ["E1", "CARB P2"]
        },
        # 添加更多实木
        {
            "category": "实木类",
            "material_type": "胡桃木",
            "chemical_components": [
                {"name": "天然油脂", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "假货风险", "severity": "中", "description": "市场常见贴皮仿冒"}
            ],
            "visual_cues": ["深褐色", "直纹理", "质地坚硬"],
            "certifications": ["FSC"]
        },
        {
            "category": "实木类",
            "material_type": "榉木",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [
                {"type": "霉变", "severity": "中", "description": "烘干不彻底易发霉"}
            ],
            "visual_cues": ["芝麻点", "纹理细密"],
            "certifications": ["FSC"]
        },
        {
            "category": "实木类",
            "material_type": "橡胶木",
            "chemical_components": [
                {"name": "防腐剂", "cas": "N/A", "hazard": "中"},
                {"name": "防虫剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "化学处理", "severity": "中", "description": "需大量化学处理防霉防虫"}
            ],
            "visual_cues": ["浅黄色", "质地较软"],
            "certifications": ["FSC"]
        },
        {
            "category": "实木类",
            "material_type": "水曲柳",
            "chemical_components": [{"name": "天然木质", "cas": "N/A", "hazard": "低"}],
            "risk_points": [
                {"type": "变形开裂", "severity": "中", "description": "易变形,需谨慎保养"}
            ],
            "visual_cues": ["山形纹理明显", "质地坚韧"],
            "certifications": ["FSC"]
        },
        # 添加更多皮革
        {
            "category": "皮革类",
            "material_type": "二层皮",
            "chemical_components": [
                {"name": "PU涂层", "cas": "9009-54-5", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "涂层剥落", "severity": "低", "description": "表面涂层易剥落"}
            ],
            "visual_cues": ["均匀纹理", "无明显毛孔"],
            "certifications": ["ISO 9001"]
        },
        {
            "category": "皮革类",
            "material_type": "科技布",
            "chemical_components": [
                {"name": "涤纶", "cas": "N/A", "hazard": "低"},
                {"name": "防水剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "防水涂层", "severity": "中", "description": "防水涂层可能含PFAS"}
            ],
            "visual_cues": ["布质手感", "防水防污"],
            "certifications": ["Oeko-Tex"]
        },
        # 添加布类
        {
            "category": "布类",
            "material_type": "亚麻布",
            "chemical_components": [{"name": "天然纤维", "cas": "N/A", "hazard": "低"}],
            "risk_points": [
                {"type": "染料残留", "severity": "低", "description": "劣质染料可能残留"}
            ],
            "visual_cues": ["粗糙质感", "透气"],
            "certifications": ["OEKO-TEX"]
        },
        {
            "category": "布类",
            "material_type": "绒布",
            "chemical_components": [
                {"name": "阻燃剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "阻燃剂", "severity": "中", "description": "可能添加溴化阻燃剂"}
            ],
            "visual_cues": ["绒毛丰富", "柔软"],
            "certifications": ["OEKO-TEX"]
        },
        # 添加更多金属
        {
            "category": "金属类",
            "material_type": "不锈钢",
            "chemical_components": [
                {"name": "铬", "cas": "7440-47-3", "hazard": "低"},
                {"name": "镍", "cas": "7440-02-0", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "镍过敏", "severity": "低", "description": "对镍过敏者慎用"}
            ],
            "visual_cues": ["银白光泽", "不易锈蚀"],
            "certifications": ["304", "316"]
        },
        {
            "category": "金属类",
            "material_type": "铝合金",
            "chemical_components": [{"name": "铝", "cas": "7429-90-5", "hazard": "低"}],
            "risk_points": [
                {"type": "连接件", "severity": "低", "description": "连接处尼龙件或胶水需注意"}
            ],
            "visual_cues": ["轻质", "银灰色"],
            "certifications": ["ISO 9001"]
        },
        # 添加更多塑料
        {
            "category": "高分子材料类",
            "material_type": "PE聚乙烯",
            "chemical_components": [{"name": "聚乙烯", "cas": "9002-88-4", "hazard": "低"}],
            "risk_points": [
                {"type": "安全性", "severity": "低", "description": "HDPE安全性高"}
            ],
            "visual_cues": ["柔韧", "半透明"],
            "certifications": ["FDA"]
        },
        {
            "category": "高分子材料类",
            "material_type": "ABS塑料",
            "chemical_components": [
                {"name": "ABS树脂", "cas": "9003-56-9", "hazard": "中"},
                {"name": "阻燃剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "阻燃剂", "severity": "中", "description": "可能添加溴化阻燃剂"}
            ],
            "visual_cues": ["坚硬", "不透明"],
            "certifications": ["RoHS"]
        },
        {
            "category": "高分子材料类",
            "material_type": "PC聚碳酸酯",
            "chemical_components": [
                {"name": "聚碳酸酯", "cas": "24936-68-3", "hazard": "中"},
                {"name": "双酚A", "cas": "80-05-7", "hazard": "高"}
            ],
            "risk_points": [
                {"type": "双酚A", "severity": "高", "description": "可能释放双酚A"}
            ],
            "visual_cues": ["透明", "坚硬"],
            "certifications": ["FDA(BPA-Free)"]
        },
        {
            "category": "高分子材料类",
            "material_type": "PS聚苯乙烯",
            "chemical_components": [{"name": "聚苯乙烯", "cas": "9003-53-6", "hazard": "中"}],
            "risk_points": [
                {"type": "受热释放", "severity": "中", "description": "受热释放苯乙烯"}
            ],
            "visual_cues": ["质脆", "透明"],
            "certifications": ["FDA"]
        }
    ]

    results = []
    for material in new_materials:
        entry = {
            "material_id": generate_id(material["material_type"], material["category"]),
            "category": material["category"],
            "data": material,
            "source": "数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "1.0"
        }
        results.append(entry)

    return results

def expand_textile_data():
    """扩充衣料材质数据"""
    new_textiles = [
        {
            "fabric_type": "莫代尔",
            "composition": "再生纤维素纤维",
            "chemical_treatments": [{"name": "染料", "hazard": "低"}],
            "health_risks": [
                {"type": "化学残留", "severity": "低", "description": "高品质莫代尔残留低"}
            ],
            "health_benefits": ["柔软亲肤", "吸湿性好", "不易起球"],
            "care_instructions": {
                "washing": "可机洗,30度",
                "drying": "自然晾干",
                "ironing": "低温熨烫"
            },
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "天丝",
            "composition": "莱赛尔纤维(再生纤维素)",
            "chemical_treatments": [{"name": "N-甲基吗啉-N-氧化物", "hazard": "低"}],
            "health_risks": [
                {"type": "环保工艺", "severity": "低", "description": "闭环生产,化学物回收"}
            ],
            "health_benefits": ["柔滑亲肤", "吸湿透气", "抗菌抑菌"],
            "care_instructions": {
                "washing": "手洗或机洗轻柔模式",
                "drying": "平铺晾干",
                "ironing": "低温熨烫"
            },
            "certifications": ["FSC", "OEKO-TEX"]
        },
        {
            "fabric_type": "竹纤维",
            "composition": "竹纤维(再生纤维素)",
            "chemical_treatments": [{"name": "溶剂", "hazard": "中"}],
            "health_risks": [
                {"type": "化学加工", "severity": "中", "description": "生产过程化学处理较多"}
            ],
            "health_benefits": ["天然抗菌", "吸湿透气", "环保可降解"],
            "care_instructions": {
                "washing": "可机洗",
                "drying": "自然晾干",
                "ironing": "中温熨烫"
            },
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "真丝混纺",
            "composition": "真丝+棉/聚酯纤维",
            "chemical_treatments": [{"name": "染料", "hazard": "中"}],
            "health_risks": [
                {"type": "染料残留", "severity": "中", "description": "深色真丝混纺可能有染料残留"}
            ],
            "health_benefits": ["柔滑舒适", "兼具各材质优点"],
            "care_instructions": {
                "washing": "手洗冷水",
                "drying": "阴干",
                "ironing": "低温"
            },
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "涤棉混纺",
            "composition": "涤纶+棉(常见65/35)",
            "chemical_treatments": [{"name": "染料", "hazard": "低"}],
            "health_risks": [
                {"type": "透气性", "severity": "低", "description": "涤纶成分高透气性降低"}
            ],
            "health_benefits": ["耐磨耐穿", "不易皱", "快干"],
            "care_instructions": {
                "washing": "可机洗",
                "drying": "可机烘",
                "ironing": "中温"
            },
            "certifications": ["OEKO-TEX"]
        },
        {
            "fabric_type": "棉麻混纺",
            "composition": "棉+麻(常见55/45)",
            "chemical_treatments": [{"name": "染料", "hazard": "低"}],
            "health_risks": [
                {"type": "粗糙感", "severity": "低", "description": "麻成分高可能粗糙"}
            ],
            "health_benefits": ["透气吸汗", "天然环保", "清爽舒适"],
            "care_instructions": {
                "washing": "可机洗",
                "drying": "自然晾干",
                "ironing": "高温"
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
            "source": "数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "1.0"
        }
        results.append(entry)

    return results

def expand_food_data():
    """扩充食物数据"""
    new_foods = [
        # 谷物类
        {
            "name": "糙米",
            "category": "谷物类",
            "nutrients": {
                "energy": {"value": 348, "unit": "kcal/100g"},
                "protein": {"value": 7.7, "unit": "g/100g"},
                "fiber": {"value": 3.0, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "200-300g/天"},
            "health_benefits": ["富含B族维生素", "膳食纤维高", "控血糖"],
            "contraindications": [],
            "incompatible_foods": []
        },
        {
            "name": "燕麦",
            "category": "谷物类",
            "nutrients": {
                "energy": {"value": 367, "unit": "kcal/100g"},
                "protein": {"value": 15, "unit": "g/100g"},
                "fiber": {"value": 10.1, "unit": "g/100g"},
                "beta_glucan": {"value": 4, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "40-50g/天(干重)"},
            "health_benefits": ["降胆固醇", "稳定血糖", "增加饱腹感"],
            "contraindications": ["麸质不耐受者慎用"],
            "incompatible_foods": []
        },
        # 蔬菜类
        {
            "name": "西兰花",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 34, "unit": "kcal/100g"},
                "vitamin_c": {"value": 89, "unit": "mg/100g"},
                "sulforaphane": {"value": "丰富", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "100-200g/天"},
            "health_benefits": ["抗癌", "抗氧化", "护眼"],
            "contraindications": ["甲状腺功能减退者少食"],
            "incompatible_foods": []
        },
        {
            "name": "胡萝卜",
            "category": "蔬菜类",
            "nutrients": {
                "energy": {"value": 41, "unit": "kcal/100g"},
                "carotene": {"value": 4130, "unit": "μg/100g"},
                "vitamin_a": {"value": 688, "unit": "μg/100g"}
            },
            "recommended_intake": {"adult": "50-100g/天"},
            "health_benefits": ["护眼明目", "增强免疫力", "抗衰老"],
            "contraindications": [],
            "incompatible_foods": [
                {"food": "白萝卜", "reason": "影响营养吸收", "severity": "轻微"}
            ]
        },
        # 水果类
        {
            "name": "蓝莓",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 57, "unit": "kcal/100g"},
                "anthocyanins": {"value": "高", "unit": "N/A"},
                "fiber": {"value": 2.4, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "50-100g/天"},
            "health_benefits": ["抗氧化极强", "护眼", "改善记忆力"],
            "contraindications": [],
            "incompatible_foods": []
        },
        {
            "name": "火龙果",
            "category": "水果类",
            "nutrients": {
                "energy": {"value": 51, "unit": "kcal/100g"},
                "fiber": {"value": 1.1, "unit": "g/100g"},
                "vitamin_c": {"value": 7, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "150-200g/天"},
            "health_benefits": ["润肠通便", "美容养颜", "排毒"],
            "contraindications": ["腹泻者少食", "糖尿病患者控制量"],
            "incompatible_foods": []
        },
        # 肉类
        {
            "name": "牛肉",
            "category": "肉类",
            "nutrients": {
                "energy": {"value": 125, "unit": "kcal/100g"},
                "protein": {"value": 20.2, "unit": "g/100g"},
                "iron": {"value": 3.3, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "40-75g/天"},
            "health_benefits": ["补血补铁", "增强体质", "优质蛋白"],
            "contraindications": ["高尿酸者少食"],
            "incompatible_foods": [
                {"food": "栗子", "reason": "同食不易消化", "severity": "轻微"}
            ]
        },
        {
            "name": "羊肉",
            "category": "肉类",
            "nutrients": {
                "energy": {"value": 203, "unit": "kcal/100g"},
                "protein": {"value": 19.0, "unit": "g/100g"},
                "fat": {"value": 14.1, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "50-100g/天"},
            "health_benefits": ["温补", "暖胃", "增强体质"],
            "contraindications": ["热性体质者少食", "夏季少食"],
            "incompatible_foods": [
                {"food": "西瓜", "reason": "寒热相冲", "severity": "中等"}
            ]
        },
        # 水产类
        {
            "name": "三文鱼",
            "category": "水产类",
            "nutrients": {
                "energy": {"value": 139, "unit": "kcal/100g"},
                "protein": {"value": 19.8, "unit": "g/100g"},
                "omega3": {"value": 2.5, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "100-150g/天"},
            "health_benefits": ["富含Omega-3", "护心", "健脑"],
            "contraindications": ["过敏者禁食"],
            "incompatible_foods": []
        },
        {
            "name": "虾",
            "category": "水产类",
            "nutrients": {
                "energy": {"value": 93, "unit": "kcal/100g"},
                "protein": {"value": 18.6, "unit": "g/100g"},
                "calcium": {"value": 325, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "50-100g/天"},
            "health_benefits": ["高蛋白低脂", "补钙", "提高免疫力"],
            "contraindications": ["过敏者禁食", "痛风患者少食"],
            "incompatible_foods": [
                {"food": "维生素C", "reason": "理论上生成砒霜,实际剂量不足", "severity": "轻微"}
            ]
        },
        # 豆类
        {
            "name": "黑豆",
            "category": "豆类",
            "nutrients": {
                "energy": {"value": 381, "unit": "kcal/100g"},
                "protein": {"value": 36, "unit": "g/100g"},
                "anthocyanins": {"value": "高", "unit": "N/A"}
            },
            "recommended_intake": {"adult": "30-50g/天(干豆)"},
            "health_benefits": ["补肾", "抗氧化", "黑发"],
            "contraindications": ["痛风者少食"],
            "incompatible_foods": []
        },
        {
            "name": "红豆",
            "category": "豆类",
            "nutrients": {
                "energy": {"value": 324, "unit": "kcal/100g"},
                "protein": {"value": 20.2, "unit": "g/100g"},
                "fiber": {"value": 7.7, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "30-50g/天(干豆)"},
            "health_benefits": ["利水消肿", "补血", "健脾"],
            "contraindications": [],
            "incompatible_foods": []
        },
        # 坚果类
        {
            "name": "核桃",
            "category": "坚果类",
            "nutrients": {
                "energy": {"value": 654, "unit": "kcal/100g"},
                "fat": {"value": 65.2, "unit": "g/100g"},
                "omega3": {"value": 9, "unit": "g/100g"}
            },
            "recommended_intake": {"adult": "25-35g/天(约2-3个)"},
            "health_benefits": ["健脑", "护心", "抗衰老"],
            "contraindications": ["腹泻者少食", "高血脂者控制量"],
            "incompatible_foods": [
                {"food": "白酒", "reason": "热性食物同食易上火", "severity": "轻微"}
            ]
        },
        {
            "name": "杏仁",
            "category": "坚果类",
            "nutrients": {
                "energy": {"value": 578, "unit": "kcal/100g"},
                "protein": {"value": 21.3, "unit": "g/100g"},
                "vitamin_e": {"value": 25, "unit": "mg/100g"}
            },
            "recommended_intake": {"adult": "10-15g/天"},
            "health_benefits": ["美容养颜", "润肠", "护心"],
            "contraindications": ["苦杏仁有毒需煮熟"],
            "incompatible_foods": []
        }
    ]

    results = []
    for food in new_foods:
        entry = {
            "material_id": generate_id(food["name"], food["category"]),
            "category": food["category"],
            "data": food,
            "source": "数据扩充",
            "last_updated": datetime.now().isoformat(),
            "version": "1.0"
        }
        results.append(entry)

    return results

def main():
    """主函数"""
    base_dir = r"D:\Users\86198\WeChatProjects\数据库\processed"

    print("开始扩充数据...")

    # 扩充家具数据
    print("\n1. 扩充家具材质数据...")
    furniture_file = os.path.join(base_dir, "furniture.json")
    with open(furniture_file, 'r', encoding='utf-8') as f:
        existing_furniture = json.load(f)

    new_furniture = expand_furniture_data()
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

    new_textile = expand_textile_data()
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

    new_food = expand_food_data()
    all_food = existing_food + new_food

    with open(food_file, 'w', encoding='utf-8') as f:
        json.dump(all_food, f, ensure_ascii=False, indent=2)
    print(f"   原有: {len(existing_food)} 条")
    print(f"   新增: {len(new_food)} 条")
    print(f"   总计: {len(all_food)} 条")

    # 总结
    print("\n" + "="*60)
    print("数据扩充完成!")
    print("="*60)
    print(f"家具材质: {len(all_furniture)} 条 (+{len(new_furniture)})")
    print(f"衣料材质: {len(all_textile)} 条 (+{len(new_textile)})")
    print(f"食物数据: {len(all_food)} 条 (+{len(new_food)})")
    print(f"\n总计: {len(all_furniture) + len(all_textile) + len(all_food)} 条数据")
    print("="*60)

if __name__ == "__main__":
    main()