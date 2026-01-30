"""第四轮数据扩充脚本 - 添加房屋建材数据"""
import json
import sys
import os
from datetime import datetime
import hashlib

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_id(name, category):
    unique_string = f"{category}_{name}_{datetime.now().isoformat()}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]

def expand_building_materials():
    """第四轮房屋建材数据扩充"""
    new_materials = [
        # 水泥类
        {
            "category": "水泥类",
            "material_type": "普通硅酸盐水泥",
            "chemical_components": [
                {"name": "硅酸钙", "cas": "1344-95-2", "hazard": "低"},
                {"name": "铝酸钙", "cas": "12042-68-1", "hazard": "低"},
                {"name": "六价铬", "cas": "18540-29-9", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "碱性灼伤", "severity": "中", "description": "湿水泥pH>12,皮肤接触易灼伤"},
                {"type": "六价铬过敏", "severity": "中", "description": "部分人群对六价铬过敏"}
            ],
            "visual_cues": ["灰色粉末", "遇水凝固", "硬化后坚固"],
            "certifications": ["GB 175"]
        },
        {
            "category": "水泥类",
            "material_type": "白水泥",
            "chemical_components": [
                {"name": "硅酸钙", "cas": "1344-95-2", "hazard": "低"},
                {"name": "氧化铝", "cas": "1344-28-1", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "碱性", "severity": "中", "description": "碱性强,施工需戴手套"}
            ],
            "visual_cues": ["白色粉末", "装饰性强"],
            "certifications": ["GB 2015"]
        },
        # 砖类
        {
            "category": "砖类",
            "material_type": "红砖",
            "chemical_components": [
                {"name": "黏土烧结", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "放射性", "severity": "低", "description": "天然黏土微量放射性,符合标准"}
            ],
            "visual_cues": ["红褐色", "多孔结构", "吸水性强"],
            "certifications": ["GB 5101"]
        },
        {
            "category": "砖类",
            "material_type": "加气混凝土砌块",
            "chemical_components": [
                {"name": "硅酸盐", "cas": "N/A", "hazard": "低"},
                {"name": "铝粉", "cas": "7429-90-5", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "轻质易碎", "severity": "低", "description": "强度较低需注意承重"}
            ],
            "visual_cues": ["灰白色", "重量轻", "多孔"],
            "certifications": ["GB 11968"]
        },
        {
            "category": "砖类",
            "material_type": "页岩砖",
            "chemical_components": [
                {"name": "页岩烧结", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "环保型", "severity": "低", "description": "替代红砖的环保产品"}
            ],
            "visual_cues": ["深灰色", "质地坚硬"],
            "certifications": ["GB 5101"]
        },
        # 管材类
        {
            "category": "管材类",
            "material_type": "PPR水管",
            "chemical_components": [
                {"name": "无规共聚聚丙烯", "cas": "25085-53-4", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "耐高温", "severity": "低", "description": "长期耐温70℃,瞬间95℃"}
            ],
            "visual_cues": ["白色或灰色", "光滑表面", "热熔连接"],
            "certifications": ["GB/T 18742"]
        },
        {
            "category": "管材类",
            "material_type": "PVC排水管",
            "chemical_components": [
                {"name": "聚氯乙烯", "cas": "9002-86-2", "hazard": "中"},
                {"name": "增塑剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "塑化剂", "severity": "中", "description": "仅用于排水,不可饮用水管"},
                {"type": "燃烧有毒", "severity": "高", "description": "燃烧释放氯化氢"}
            ],
            "visual_cues": ["灰色", "PVC标识"],
            "certifications": ["GB/T 5836"]
        },
        {
            "category": "管材类",
            "material_type": "铜管",
            "chemical_components": [
                {"name": "纯铜", "cas": "7440-50-8", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "价格高", "severity": "低", "description": "材料成本高"}
            ],
            "visual_cues": ["红铜色", "金属光泽", "抗菌性强"],
            "certifications": ["GB/T 18033"]
        },
        {
            "category": "管材类",
            "material_type": "不锈钢水管",
            "chemical_components": [
                {"name": "304不锈钢", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "安全性高", "severity": "低", "description": "食品级材质,最安全"}
            ],
            "visual_cues": ["银白色", "金属质感", "卡压连接"],
            "certifications": ["GB/T 19228"]
        },
        # 门窗材料
        {
            "category": "门窗类",
            "material_type": "断桥铝门窗",
            "chemical_components": [
                {"name": "铝合金型材", "cas": "N/A", "hazard": "低"},
                {"name": "PA66隔热条", "cas": "32131-17-2", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "假冒隔热条", "severity": "中", "description": "PVC冒充PA66隔热条"}
            ],
            "visual_cues": ["中间黑色隔热条", "型材厚"],
            "certifications": ["GB/T 8478"]
        },
        {
            "category": "门窗类",
            "material_type": "塑钢门窗",
            "chemical_components": [
                {"name": "PVC型材", "cas": "9002-86-2", "hazard": "中"},
                {"name": "钢衬", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "铅稳定剂", "severity": "中", "description": "老式塑钢含铅,选环保型"}
            ],
            "visual_cues": ["白色塑料外观", "内有钢衬"],
            "certifications": ["GB/T 8814"]
        },
        {
            "category": "门窗类",
            "material_type": "实木门",
            "chemical_components": [
                {"name": "天然木材", "cas": "N/A", "hazard": "低"},
                {"name": "木器漆", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "油漆VOCs", "severity": "中", "description": "传统油漆含VOCs,选水性漆"}
            ],
            "visual_cues": ["天然木纹", "质感厚重"],
            "certifications": ["GB 18584"]
        },
        # 吊顶材料
        {
            "category": "吊顶类",
            "material_type": "石膏板",
            "chemical_components": [
                {"name": "天然石膏", "cas": "13397-24-5", "hazard": "低"},
                {"name": "纸面护层", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "防水性差", "severity": "中", "description": "普通石膏板怕水"}
            ],
            "visual_cues": ["白色板材", "纸面覆盖"],
            "certifications": ["GB/T 9775"]
        },
        {
            "category": "吊顶类",
            "material_type": "铝扣板",
            "chemical_components": [
                {"name": "铝合金", "cas": "N/A", "hazard": "低"},
                {"name": "表面涂层", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "涂层脱落", "severity": "低", "description": "劣质产品涂层易脱落"}
            ],
            "visual_cues": ["金属光泽", "可拆卸", "防水防潮"],
            "certifications": ["GB/T 23443"]
        },
        {
            "category": "吊顶类",
            "material_type": "集成吊顶",
            "chemical_components": [
                {"name": "铝镁合金", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "电器安全", "severity": "中", "description": "注意电器3C认证"}
            ],
            "visual_cues": ["模块化设计", "集成照明通风"],
            "certifications": ["GB/T 23443"]
        },
        # 保温材料
        {
            "category": "保温类",
            "material_type": "岩棉",
            "chemical_components": [
                {"name": "玄武岩纤维", "cas": "N/A", "hazard": "中"},
                {"name": "酚醛树脂", "cas": "9003-35-4", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "纤维刺激", "severity": "中", "description": "施工时纤维刺激皮肤"},
                {"type": "酚醛异味", "severity": "中", "description": "新品可能有异味"}
            ],
            "visual_cues": ["黄褐色", "纤维状", "防火A级"],
            "certifications": ["GB/T 25975"]
        },
        {
            "category": "保温类",
            "material_type": "挤塑板(XPS)",
            "chemical_components": [
                {"name": "聚苯乙烯", "cas": "9003-53-6", "hazard": "中"},
                {"name": "阻燃剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "阻燃剂", "severity": "中", "description": "含溴系阻燃剂HBCD"},
                {"type": "防火等级低", "severity": "中", "description": "B1级阻燃"}
            ],
            "visual_cues": ["蓝色或粉色", "闭孔结构", "硬质"],
            "certifications": ["GB/T 10801"]
        },
        {
            "category": "保温类",
            "material_type": "聚氨酯保温板",
            "chemical_components": [
                {"name": "聚氨酯", "cas": "9009-54-5", "hazard": "中"},
                {"name": "异氰酸酯", "cas": "N/A", "hazard": "高"}
            ],
            "risk_points": [
                {"type": "异氰酸酯残留", "severity": "高", "description": "未固化完全有毒性"},
                {"type": "燃烧剧毒", "severity": "高", "description": "燃烧产生氰化氢"}
            ],
            "visual_cues": ["黄色或白色", "闭孔泡沫"],
            "certifications": ["GB/T 21558"]
        },
        # 防水材料
        {
            "category": "防水类",
            "material_type": "聚合物水泥防水涂料",
            "chemical_components": [
                {"name": "丙烯酸酯", "cas": "N/A", "hazard": "低"},
                {"name": "水泥", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "环保型", "severity": "低", "description": "水性涂料环保无毒"}
            ],
            "visual_cues": ["双组份", "涂刷型"],
            "certifications": ["GB/T 23445"]
        },
        {
            "category": "防水类",
            "material_type": "SBS改性沥青防水卷材",
            "chemical_components": [
                {"name": "SBS橡胶", "cas": "9003-55-8", "hazard": "低"},
                {"name": "沥青", "cas": "8052-42-4", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "沥青气味", "severity": "中", "description": "热熔施工有沥青烟"},
                {"type": "多环芳烃", "severity": "中", "description": "沥青含PAHs"}
            ],
            "visual_cues": ["黑色卷材", "柔韧性好"],
            "certifications": ["GB 18242"]
        },
        {
            "category": "防水类",
            "material_type": "聚氨酯防水涂料",
            "chemical_components": [
                {"name": "聚氨酯", "cas": "9009-54-5", "hazard": "中"},
                {"name": "溶剂", "cas": "N/A", "hazard": "高"}
            ],
            "risk_points": [
                {"type": "溶剂型有毒", "severity": "高", "description": "含甲苯二甲苯等溶剂"},
                {"type": "选水性", "severity": "低", "description": "水性聚氨酯更环保"}
            ],
            "visual_cues": ["黑色或绿色", "涂膜厚"],
            "certifications": ["GB/T 19250"]
        },
        # 瓷砖类
        {
            "category": "瓷砖类",
            "material_type": "抛光砖",
            "chemical_components": [
                {"name": "瓷土", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "放射性", "severity": "低", "description": "天然石材A类放射性合格"}
            ],
            "visual_cues": ["表面光亮", "耐磨"],
            "certifications": ["GB 6566"]
        },
        {
            "category": "瓷砖类",
            "material_type": "釉面砖",
            "chemical_components": [
                {"name": "陶土+釉料", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "釉面铅镉", "severity": "中", "description": "劣质釉面含铅镉"}
            ],
            "visual_cues": ["釉面光滑", "花色丰富"],
            "certifications": ["GB/T 4100"]
        },
        {
            "category": "瓷砖类",
            "material_type": "全抛釉瓷砖",
            "chemical_components": [
                {"name": "瓷土+透明釉", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "耐磨性", "severity": "低", "description": "釉面硬度不如抛光砖"}
            ],
            "visual_cues": ["亮度高", "花纹细腻"],
            "certifications": ["GB/T 4100"]
        },
        # 胶类材料
        {
            "category": "胶类",
            "material_type": "瓷砖胶",
            "chemical_components": [
                {"name": "水泥基+聚合物", "cas": "N/A", "hazard": "低"}
            ],
            "risk_points": [
                {"type": "环保型", "severity": "低", "description": "替代水泥砂浆更环保"}
            ],
            "visual_cues": ["灰色粉末", "加水搅拌"],
            "certifications": ["JC/T 547"]
        },
        {
            "category": "胶类",
            "material_type": "结构胶",
            "chemical_components": [
                {"name": "硅酮胶", "cas": "N/A", "hazard": "中"},
                {"name": "醇类溶剂", "cas": "N/A", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "固化气味", "severity": "中", "description": "固化期释放醇类"}
            ],
            "visual_cues": ["高强度", "耐候性好"],
            "certifications": ["GB 16776"]
        },
        {
            "category": "胶类",
            "material_type": "美缝剂",
            "chemical_components": [
                {"name": "环氧树脂", "cas": "25068-38-6", "hazard": "中"}
            ],
            "risk_points": [
                {"type": "环氧树脂过敏", "severity": "中", "description": "未固化时皮肤过敏风险"}
            ],
            "visual_cues": ["双组份", "颜色丰富", "表面光滑"],
            "certifications": ["JC/T 1004"]
        }
    ]

    results = []
    for material in new_materials:
        entry = {
            "material_id": generate_id(material["material_type"], material["category"]),
            "category": material["category"],
            "data": material,
            "source": "第四轮数据扩充-房屋建材",
            "last_updated": datetime.now().isoformat(),
            "version": "4.0"
        }
        results.append(entry)
    return results

def main():
    base_dir = r"D:\Users\86198\WeChatProjects\数据库\processed"

    print("\n" + "="*60)
    print("第四轮数据扩充开始 - 房屋建材类别")
    print("="*60)

    # 房屋建材数据添加到家具材质文件
    print("\n添加房屋建材数据...")
    furniture_file = os.path.join(base_dir, "furniture.json")
    with open(furniture_file, 'r', encoding='utf-8') as f:
        existing_furniture = json.load(f)

    new_materials = expand_building_materials()
    all_furniture = existing_furniture + new_materials

    with open(furniture_file, 'w', encoding='utf-8') as f:
        json.dump(all_furniture, f, ensure_ascii=False, indent=2)

    print(f"   原有: {len(existing_furniture)} 条")
    print(f"   新增: {len(new_materials)} 条")
    print(f"   总计: {len(all_furniture)} 条")

    # 统计各类别
    categories = {}
    for item in all_furniture:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1

    print("\n各类别统计:")
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count}条")

    # 总结
    print("\n" + "="*60)
    print("第四轮数据扩充完成!")
    print("="*60)
    print(f"家具及建材总数: {len(all_furniture)} 条 (+{len(new_materials)})")
    print("\n新增建材类别:")
    print("  - 水泥类 (2种): 普通硅酸盐水泥、白水泥")
    print("  - 砖类 (3种): 红砖、加气混凝土砌块、页岩砖")
    print("  - 管材类 (4种): PPR水管、PVC排水管、铜管、不锈钢水管")
    print("  - 门窗类 (3种): 断桥铝门窗、塑钢门窗、实木门")
    print("  - 吊顶类 (3种): 石膏板、铝扣板、集成吊顶")
    print("  - 保温类 (3种): 岩棉、挤塑板、聚氨酯保温板")
    print("  - 防水类 (3种): 聚合物水泥防水涂料、SBS防水卷材、聚氨酯防水涂料")
    print("  - 瓷砖类 (3种): 抛光砖、釉面砖、全抛釉瓷砖")
    print("  - 胶类 (3种): 瓷砖胶、结构胶、美缝剂")
    print("="*60)

if __name__ == "__main__":
    main()
