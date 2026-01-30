"""
高分子材料知识库导入脚本
将高分子材料知识库数据导入 ChromaDB 向量数据库
"""

import chromadb
from chromadb.config import Settings
import json

# 初始化 ChromaDB 客户端
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

# 创建或获取集合
collection = client.get_or_create_collection(
    name="furniture_knowledge_polymer",
    metadata={"description": "家具高分子材料检测知识库"}
)

# 高分子材料知识库数据
knowledge_data = [
    # ========== ABS塑料 ==========
    {
        "id": "polymer_001",
        "category": "高分子材料类",
        "material_type": "ABS塑料",
        "alternative_names": ["丙烯腈-丁二烯-苯乙烯共聚物", "ABS树脂", "Acrylonitrile Butadiene Styrene"],
        "visual_cues": [
            "外观呈半透明或透明颗粒",
            "无毒无味",
            "表面光泽度好",
            "可表面镀铬、喷漆处理",
            "颜色多样"
        ],
        "risk_points": [
            {
                "type": "热变形",
                "severity": "中",
                "description": "热变形温度较低，不适合高温环境"
            },
            {
                "type": "可燃性",
                "severity": "中",
                "description": "可燃，需要注意防火"
            },
            {
                "type": "耐候性差",
                "severity": "中",
                "description": "长期暴露在阳光下会老化"
            }
        ],
        "health_advice": {
            "general": "无毒无味，适合家居使用，注意防火和防晒",
            "pregnant": "适合孕妇房使用",
            "children": "适合儿童房使用"
        },
        "advantages": "综合性能优良，冲击强度极好，尺寸稳定性好，耐磨性好，抗化学药品性强，染色性好，成型加工容易，价格便宜用途广泛",
        "disadvantages": "热变形温度较低，可燃，耐候性较差，不溶于大部分醇类和烃类溶剂",
        "price_range": "中档，性价比高",
        "risk_level": "低"
    },

    # ========== PP塑料 ==========
    {
        "id": "polymer_002",
        "category": "高分子材料类",
        "material_type": "PP塑料",
        "alternative_names": ["聚丙烯", "百折胶", "Polypropylene"],
        "visual_cues": [
            "原料外观透明而轻",
            "无毒无味",
            "密度较小",
            "表面光滑",
            "可染色"
        ],
        "risk_points": [
            {
                "type": "低温脆化",
                "severity": "中",
                "description": "低温时变脆"
            },
            {
                "type": "不耐磨",
                "severity": "低",
                "description": "不耐磨，易老化"
            },
            {
                "type": "再生制品风险",
                "severity": "高",
                "description": "禁止用再生制品盛装食品"
            }
        ],
        "health_advice": {
            "general": "无毒无味，适合所有人群，特别适合食品接触用途，可用于微波炉加热",
            "pregnant": "特别推荐孕妇房使用，安全环保",
            "children": "特别推荐儿童房使用，可用于食具"
        },
        "advantages": "无毒无味可用于食具，强度刚度硬度耐热性均优于低压聚乙烯，可在100度左右使用，具有良好的电性能和高频绝缘性，耐化学物质耐碰撞，能放入微波炉加热",
        "disadvantages": "低温时变脆，不耐磨易老化，禁止用再生制品盛装食品",
        "price_range": "经济实惠",
        "risk_level": "低"
    },

    # ========== PE塑料 ==========
    {
        "id": "polymer_003",
        "category": "高分子材料类",
        "material_type": "PE塑料",
        "alternative_names": ["聚乙烯", "Polyethylene", "HDPE高密度聚乙烯", "LDPE低密度聚乙烯"],
        "visual_cues": [
            "聚乙烯无臭无毒",
            "手感似蜡",
            "HDPE呈白色",
            "LDPE呈乳白色",
            "透明性好（LDPE）"
        ],
        "risk_points": [
            {
                "type": "耐热性差",
                "severity": "高",
                "description": "LDPE超过110℃会热熔释放有毒物质"
            },
            {
                "type": "环境应力敏感",
                "severity": "中",
                "description": "对环境应力敏感，耐热老化性差"
            },
            {
                "type": "难清洗",
                "severity": "中",
                "description": "难清洗干净，不要循环使用"
            }
        ],
        "health_advice": {
            "general": "无毒无味，适合食品包装，LDPE不适合高温使用，不建议循环使用",
            "pregnant": "适合孕妇房，但避免高温使用",
            "children": "适合儿童房，但避免用于热食包装"
        },
        "advantages": "无毒无味安全性好，耐低温性能优良，化学稳定性好耐酸碱，电绝缘性能优良，吸水性小，价格便宜",
        "disadvantages": "对环境应力敏感，耐热老化性差，HDPE抗老化性能差，LDPE耐热性不好超过110℃会热熔释放有毒物质，难清洗干净不要循环使用",
        "price_range": "经济实惠",
        "risk_level": "中"
    },

    # ========== PS塑料 ==========
    {
        "id": "polymer_004",
        "category": "高分子材料类",
        "material_type": "PS塑料",
        "alternative_names": ["聚苯乙烯", "硬胶", "Polystyrene"],
        "visual_cues": [
            "原料透光度高",
            "无色无味",
            "染色容易",
            "硬度比PP高一点",
            "表面光滑"
        ],
        "risk_points": [
            {
                "type": "高温释放有害物质",
                "severity": "高",
                "description": "温度超过70℃就会释放有害物质"
            },
            {
                "type": "韧性差",
                "severity": "中",
                "description": "韧性较差，容易脆"
            },
            {
                "type": "环保性差",
                "severity": "高",
                "description": "不容易回收利用，环境污染严重"
            }
        ],
        "health_advice": {
            "general": "不推荐长期使用，不适合热食包装，避免用于儿童用品，逐渐被纸类材料替代",
            "pregnant": "不推荐孕妇房使用",
            "children": "不推荐儿童房使用"
        },
        "advantages": "透光度高，染色容易，价格便宜，加工简单",
        "disadvantages": "韧性较差容易脆，温度超过70℃就会释放有害物质，不容易回收利用，环保性差",
        "price_range": "低档",
        "risk_level": "高"
    },

    # ========== PVC塑料 ==========
    {
        "id": "polymer_005",
        "category": "高分子材料类",
        "material_type": "PVC塑料",
        "alternative_names": ["聚氯乙烯", "附胶膜", "Polyvinyl Chloride"],
        "visual_cues": [
            "本色为微黄色半透明状",
            "有光泽",
            "透明度胜于聚乙烯、聚苯烯",
            "分为软、硬聚氯乙烯",
            "软制品柔而韧，手感粘",
            "硬制品硬度高，在屈折处会出现白化现象"
        ],
        "risk_points": [
            {
                "type": "毒性",
                "severity": "高",
                "description": "硬质PVC有毒性，添加增塑剂、防老剂后有毒"
            },
            {
                "type": "食品接触风险",
                "severity": "高",
                "description": "不适合食品接触"
            },
            {
                "type": "燃烧有害",
                "severity": "中",
                "description": "燃烧后难软化，有刺激性酸味"
            }
        ],
        "health_advice": {
            "general": "软质PVC相对安全，硬质PVC不适合食品接触，不推荐用于儿童用品，注意通风",
            "pregnant": "不推荐孕妇房使用",
            "children": "不推荐儿童房使用"
        },
        "advantages": "高强度，柔性好，不易脆，价格适中，用途广泛",
        "disadvantages": "PVC本身没有毒性但添加增塑剂防老剂后有毒，软质PVC没有毒性硬质PVC有毒性，不易燃烧离开火源就熄灭，燃烧后难软化有刺激性酸味",
        "price_range": "中低档",
        "risk_level": "中高"
    },

    # ========== PA塑料 ==========
    {
        "id": "polymer_006",
        "category": "高分子材料类",
        "material_type": "PA塑料",
        "alternative_names": ["聚酰胺", "尼龙", "Polyamide"],
        "visual_cues": [
            "原料无毒无臭",
            "坚韧性能好",
            "表面光滑",
            "可染色"
        ],
        "risk_points": [
            {
                "type": "酸碱接触",
                "severity": "中",
                "description": "不可长期与酸碱接触"
            },
            {
                "type": "价格较高",
                "severity": "低",
                "description": "价格较高"
            }
        ],
        "health_advice": {
            "general": "无毒无臭，适合所有人群，适合家居用品，适合儿童用品（梳子、牙刷等）",
            "pregnant": "适合孕妇房使用",
            "children": "特别适合儿童用品"
        },
        "advantages": "无毒无臭，坚韧性能好，耐磨耐热耐化学品，品种繁多，通过混入各种纤维材料性能显著提高，已经取代了部分金属",
        "disadvantages": "不可长期与酸碱接触，不易燃烧离开火源就熄灭，燃烧后起泡滴落有羊皮指甲气味",
        "price_range": "中高档",
        "risk_level": "低"
    },

    # ========== PC塑料 ==========
    {
        "id": "polymer_007",
        "category": "高分子材料类",
        "material_type": "PC塑料",
        "alternative_names": ["聚碳酸酯", "Polycarbonate"],
        "visual_cues": [
            "无色透明",
            "有光泽",
            "表面光滑",
            "可染色"
        ],
        "risk_points": [
            {
                "type": "双酚A",
                "severity": "高",
                "description": "可能释放双酚A（BPA），对婴幼儿健康造成伤害"
            },
            {
                "type": "高温风险",
                "severity": "高",
                "description": "不能在微波炉加热，不能高温消毒，不能直晒"
            },
            {
                "type": "耐磨性差",
                "severity": "中",
                "description": "耐磨性差，易磨损的用途需要对表面进行特殊处理"
            }
        ],
        "health_advice": {
            "general": "可能释放双酚A，不推荐用于婴幼儿奶瓶水瓶，不适合孕妇房儿童房，避免高温使用",
            "pregnant": "不推荐孕妇房使用",
            "children": "不推荐儿童房使用，特别是婴幼儿用品"
        },
        "advantages": "无色透明，耐热抗冲击阻燃，在普通使用温度内都有良好的机械性能，折射率高加工性能好",
        "disadvantages": "耐磨性差易磨损的用途需要对表面进行特殊处理，可能释放双酚A，不能在微波炉加热不能高温消毒不能直晒",
        "price_range": "中高档",
        "risk_level": "中高"
    },

    # ========== PET塑料 ==========
    {
        "id": "polymer_008",
        "category": "高分子材料类",
        "material_type": "PET塑料",
        "alternative_names": ["聚对苯二甲酸乙二醇酯", "涤纶树脂", "Polyethylene Terephthalate"],
        "visual_cues": [
            "原料呈乳白色或浅黄色",
            "透明性好",
            "无毒",
            "表面光滑"
        ],
        "risk_points": [
            {
                "type": "高温释放有害物质",
                "severity": "高",
                "description": "超过65℃容易释放有害物质"
            },
            {
                "type": "不耐热水",
                "severity": "中",
                "description": "不耐热水侵泡，不耐碱"
            },
            {
                "type": "不能反复使用",
                "severity": "中",
                "description": "不能长时间反复使用"
            }
        ],
        "health_advice": {
            "general": "无毒，适合一次性使用，不适合反复使用，不适合热水，避免高温环境",
            "pregnant": "适合孕妇房，但一次性使用",
            "children": "适合儿童房，但一次性使用"
        },
        "advantages": "透明性好，无毒，密度高硬度高，耐磨损，价格适中",
        "disadvantages": "不耐热水侵泡，不耐碱，超过65℃容易释放有害物质，不能长时间反复使用",
        "price_range": "中档",
        "risk_level": "中"
    }
]

# 导入数据到 ChromaDB
print("开始导入高分子材料知识库数据...")

for item in knowledge_data:
    # 构建文档内容
    document = f"""
    材料类别: {item['category']}
    材料类型: {item['material_type']}
    """

    if 'alternative_names' in item and item['alternative_names']:
        document += f"\n别名: {', '.join(item['alternative_names'])}"

    if 'visual_cues' in item:
        document += f"\n视觉特征: {', '.join(item['visual_cues'])}"

    if 'risk_points' in item:
        risk_descriptions = [f"{r['type']}({r['severity']}): {r['description']}" for r in item['risk_points']]
        document += f"\n风险点: {'; '.join(risk_descriptions)}"

    if 'health_advice' in item:
        if isinstance(item['health_advice'], dict):
            document += f"\n健康建议-通用: {item['health_advice']['general']}"
            document += f"\n健康建议-孕妇: {item['health_advice']['pregnant']}"
            document += f"\n健康建议-儿童: {item['health_advice']['children']}"
        else:
            document += f"\n健康建议: {item['health_advice']}"

    if 'advantages' in item:
        document += f"\n优点: {item['advantages']}"

    if 'disadvantages' in item:
        document += f"\n缺点: {item['disadvantages']}"

    if 'price_range' in item:
        document += f"\n价格区间: {item['price_range']}"

    # 构建元数据
    metadata = {
        "category": item['category'],
        "material_type": item['material_type'],
        "risk_level": item.get('risk_level', 'unknown')
    }

    # 添加到集合
    collection.add(
        ids=[item['id']],
        documents=[document],
        metadatas=[metadata]
    )

    print(f"✓ 已导入: {item['category']} - {item['material_type']}")

print(f"\n✅ 成功导入 {len(knowledge_data)} 条高分子材料知识库数据！")

# 测试查询
print("\n" + "="*50)
print("测试查询功能...")
print("="*50)

test_queries = [
    "ABS塑料有什么特点？",
    "PP塑料适合儿童房吗？",
    "哪些塑料可以用于食品包装？",
    "PC塑料有什么风险？",
    "什么塑料可以放微波炉？"
]

for query in test_queries:
    print(f"\n查询: {query}")
    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    print("相关知识:")
    for i, doc in enumerate(results['documents'][0], 1):
        print(f"{i}. {doc[:200]}...")
    print("-" * 50)

print("\n✅ 高分子材料知识库导入完成！可以开始使用了。")
