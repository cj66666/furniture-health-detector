"""
专业家具材料知识库导入脚本
将扩展的知识库数据导入 ChromaDB 向量数据库
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
    name="furniture_knowledge_pro",
    metadata={"description": "专业家具材料检测知识库"}
)

# 扩展的专业知识库数据
knowledge_data = [
    # ========== 实木类 ==========
    {
        "id": "wood_001",
        "category": "实木类",
        "material_type": "橡木",
        "alternative_names": ["栎木", "Oak"],
        "visual_cues": [
            "具有比较鲜明的山形木纹",
            "纹理清晰美观",
            "木材质地均匀",
            "心材呈黄褐至红褐色",
            "表面触摸有良好的质感"
        ],
        "risk_points": [
            {
                "type": "假冒产品",
                "severity": "高",
                "description": "市场上以橡胶木代替橡木的现象普遍存在"
            },
            {
                "type": "开裂变形",
                "severity": "中",
                "description": "未脱净水制作的家具容易在一年半载后变形或开裂"
            },
            {
                "type": "虫蛀",
                "severity": "中",
                "description": "边材柔软，容易受昆虫攻击"
            }
        ],
        "health_advice": {
            "general": "环保性好，适合所有人群，需要定期保养，避免暴晒和过度干燥",
            "pregnant": "特别推荐孕妇房使用，环保安全",
            "children": "特别推荐儿童房使用，天然环保"
        },
        "advantages": "木纹美丽，韧性极好，结构牢固，使用年限长，耐腐蚀性强，档次较高",
        "disadvantages": "优质树种稀少价格昂贵，质地硬沉水分脱净比较难，边材容易受昆虫攻击",
        "price_range": "高档",
        "risk_level": "中"
    },

    {
        "id": "wood_002",
        "category": "实木类",
        "material_type": "胡桃木",
        "alternative_names": ["Walnut", "黑胡桃木"],
        "visual_cues": [
            "边材乳白色",
            "心材浅棕到深巧克力色",
            "偶尔有紫色和较暗条纹",
            "树纹一般是直的，有时有波浪形或卷曲树纹",
            "木纹精巧别致、清晰迷人"
        ],
        "risk_points": [
            {
                "type": "价格昂贵",
                "severity": "高",
                "description": "价格高昂，普通家庭难以消费"
            },
            {
                "type": "结构强度",
                "severity": "中",
                "description": "木材结构不如红木紧密，抗压抗弯曲能力只属中等"
            },
            {
                "type": "虫蛀",
                "severity": "中",
                "description": "边材易于被粉蠹破坏"
            }
        ],
        "health_advice": {
            "general": "环保性好，适合高端家居，需要注意防护和保养",
            "pregnant": "适合追求品质的孕妇房",
            "children": "适合高端儿童房，需要定期维护"
        },
        "advantages": "材色优雅，木纹精巧别致，不易开裂变形，热压能力强，心材抗腐能力强",
        "disadvantages": "价格高昂，木材结构不如红木紧密，边材易被粉蠹破坏，干燥得很慢",
        "price_range": "中高档",
        "risk_level": "中"
    },

    {
        "id": "wood_003",
        "category": "实木类",
        "material_type": "松木",
        "alternative_names": ["Pine"],
        "visual_cues": [
            "色泽天然，保持松木天然本色",
            "纹理清楚美观",
            "枝节部位留下自然生长痕迹",
            "造型朴实大方、线条饱满流畅"
        ],
        "risk_points": [
            {
                "type": "开裂变形",
                "severity": "高",
                "description": "木质软，易开裂变形，含水率高容易导致开裂"
            },
            {
                "type": "变色",
                "severity": "中",
                "description": "需要好好保养，否则容易变色，日照要严格防范"
            },
            {
                "type": "油漆变色",
                "severity": "中",
                "description": "时间一长，油漆容易变色"
            }
        ],
        "health_advice": {
            "general": "环保性较好，适合儿童家具，避免长时间日照，需要定期保养维护",
            "pregnant": "适合孕妇房，但需要注意保养",
            "children": "广泛用于儿童家具，性价比高"
        },
        "advantages": "色泽天然纹理清楚，造型朴实大方，实用性强经久耐用，弹性和透气性强，价格便宜性价比高",
        "disadvantages": "木质软易开裂变形，含水率高容易导致开裂，需要好好保养否则容易变色",
        "price_range": "60-160元/张",
        "risk_level": "中"
    },

    {
        "id": "wood_004",
        "category": "实木类",
        "material_type": "榉木",
        "alternative_names": ["Beech", "椐木", "椇木", "南榆"],
        "visual_cues": [
            "纹理清晰，木材质地均匀",
            "色调柔和，流畅",
            "木纹美丽而有光泽",
            "比多数普通硬木都重"
        ],
        "risk_points": [
            {
                "type": "开裂",
                "severity": "高",
                "description": "易开裂，在窑炉干燥和加工时易出现裂纹"
            },
            {
                "type": "干燥处理",
                "severity": "中",
                "description": "需要专业的干燥处理"
            }
        ],
        "health_advice": {
            "general": "环保性好，适合家居使用，注意防止开裂，需要控制环境湿度",
            "pregnant": "适合孕妇房使用",
            "children": "适合儿童房使用"
        },
        "advantages": "坚固耐用抗冲击性强，在蒸汽下韧性好可制作各种造型，钉子性能好，纹理清晰质地均匀",
        "disadvantages": "易开裂，在窑炉干燥和加工时易出现裂纹",
        "price_range": "中档",
        "risk_level": "中"
    },

    # ========== 皮革类 ==========
    {
        "id": "leather_001",
        "category": "皮革类",
        "material_type": "头层牛皮-全粒面革",
        "alternative_names": ["Top Grain Leather", "Full Grain Leather"],
        "visual_cues": [
            "皮面未经人工削磨除去瑕疵",
            "表面毛孔与纹理清晰可见",
            "保留牛皮更天然的皮面",
            "呈现独一无二的风貌",
            "有自然褶皱"
        ],
        "risk_points": [
            {
                "type": "价格昂贵",
                "severity": "高",
                "description": "每套需10头黄牛的牛皮，价格极高"
            },
            {
                "type": "维护成本",
                "severity": "高",
                "description": "后期维护成本高，需要专业保养"
            },
            {
                "type": "假冒产品",
                "severity": "高",
                "description": "市场上假冒产品多"
            }
        ],
        "health_advice": {
            "general": "环保性好，透气性优，适合高端家居，需要定期专业保养",
            "pregnant": "适合孕妇房，透气性好",
            "children": "适合儿童房，但需要注意保养"
        },
        "advantages": "皮革中最好的一种，更能展现动物皮的自然花纹，透气性好，耐磨性强，质感高级显档次",
        "disadvantages": "褶皱明显，价格极高，后期维护成本高",
        "price_range": "高档",
        "risk_level": "低"
    },

    {
        "id": "leather_002",
        "category": "皮革类",
        "material_type": "头层牛皮-修面革",
        "alternative_names": ["Corrected Grain Leather"],
        "visual_cues": [
            "皮面有较多瑕疵被人工磨去",
            "表面无伤残及疤痕",
            "进行涂饰、压花纹处理",
            "涂层较厚，几乎看不到原有皮革表面状态"
        ],
        "risk_points": [
            {
                "type": "透气性差",
                "severity": "中",
                "description": "涂层较厚，透气性受影响"
            },
            {
                "type": "耐磨性弱",
                "severity": "中",
                "description": "耐磨性相对弱"
            }
        ],
        "health_advice": {
            "general": "适合追求性价比的家庭，注意通风",
            "pregnant": "可以使用，但透气性不如全粒面革",
            "children": "可以使用，注意通风"
        },
        "advantages": "表面无瑕疵，不易变形，适合面积较大的产品，价格比全粒面革低",
        "disadvantages": "涂层较厚透气性受影响，耐磨性相对弱，缺乏真皮的自然质感",
        "price_range": "中档",
        "risk_level": "中"
    },

    {
        "id": "leather_003",
        "category": "皮革类",
        "material_type": "二层皮",
        "alternative_names": ["Split Leather"],
        "visual_cues": [
            "褶皱不明显",
            "质感还可以",
            "表面经过处理，看起来较平整"
        ],
        "risk_points": [
            {
                "type": "质量问题",
                "severity": "高",
                "description": "容易掉漆、开裂、覆膜软化起泡"
            },
            {
                "type": "透气性差",
                "severity": "中",
                "description": "透气性较差"
            },
            {
                "type": "使用寿命短",
                "severity": "高",
                "description": "使用寿命短"
            }
        ],
        "health_advice": {
            "general": "适合预算有限的家庭，不推荐长期使用，注意通风",
            "pregnant": "不推荐孕妇房使用",
            "children": "不推荐儿童房使用"
        },
        "advantages": "价格便宜性价比高，褶皱不明显，比人造皮革保持动物皮毛特性",
        "disadvantages": "容易掉漆开裂，覆膜软化起泡，透气性差，使用寿命短",
        "price_range": "仅是头层皮沙发的1/3",
        "risk_level": "高"
    },

    {
        "id": "leather_004",
        "category": "皮革类",
        "material_type": "PU皮",
        "alternative_names": ["PU Leather", "聚氨酯革"],
        "visual_cues": [
            "底基是平面经纬结构",
            "底基剖面顺滑",
            "摸起来像普通布料",
            "薄的PU（0.7mm）针织底，经纬纤维明显"
        ],
        "risk_points": [
            {
                "type": "掉皮开裂",
                "severity": "中",
                "description": "薄的PU容易掉皮、开裂"
            },
            {
                "type": "假冒产品",
                "severity": "高",
                "description": "市场上以PU冒充超纤皮现象普遍"
            },
            {
                "type": "透气性一般",
                "severity": "中",
                "description": "透气性一般"
            }
        ],
        "health_advice": {
            "general": "适合办公沙发和非接触面，注意通风，定期检查是否掉皮",
            "pregnant": "不推荐孕妇房使用",
            "children": "不推荐儿童房使用"
        },
        "advantages": "比PVC耐磨性好，不易脆化硬化，适用于沙发等易损耗场景，价格适中",
        "disadvantages": "薄的PU容易掉皮开裂，使用寿命不如超纤皮，透气性一般",
        "price_range": "比PVC高，比超纤皮低",
        "risk_level": "中"
    },

    {
        "id": "leather_005",
        "category": "皮革类",
        "material_type": "科技布",
        "alternative_names": ["Tech Fabric", "超细纤维皮革"],
        "visual_cues": [
            "底基纤维较为疏松",
            "更有布感而非皮感",
            "表面整齐，不易产生褶皱",
            "外观接近真皮质感"
        ],
        "risk_points": [
            {
                "type": "掉皮",
                "severity": "高",
                "description": "使用不到1年可能出现掉皮、掉渣"
            },
            {
                "type": "渗色",
                "severity": "中",
                "description": "处理不及时会渗色"
            },
            {
                "type": "清洁困难",
                "severity": "高",
                "description": "不可拆洗，清洁困难，需要专业清洗服务"
            },
            {
                "type": "不防猫抓",
                "severity": "高",
                "description": "容易被猫抓坏，拉扯和勾丝后难以修复"
            }
        ],
        "health_advice": {
            "general": "不推荐有宠物的家庭，需要小心维护，避免尖锐物品接触",
            "pregnant": "可以使用，但需要注意维护",
            "children": "不推荐有小孩的家庭（易脏且难清洁）"
        },
        "advantages": "有真皮沙发的质感价格低，防水性能好，耐磨性较好，款式多样，面料整齐观感好",
        "disadvantages": "会掉皮，会渗色，不可拆洗清洁困难，不防猫抓容易勾丝，难以修复",
        "price_range": "真皮沙发的1/2到1/3",
        "risk_level": "中高"
    },

    # ========== 布类 ==========
    {
        "id": "fabric_001",
        "category": "布类",
        "material_type": "棉麻",
        "alternative_names": ["Cotton Linen"],
        "visual_cues": [
            "粗麻：颗粒大，纹理深，面料厚",
            "细麻：颗粒小，纹理浅，更柔和舒服",
            "有自然的纹理感",
            "颜色自然柔和"
        ],
        "risk_points": [
            {
                "type": "易起皱",
                "severity": "中",
                "description": "容易起皱，需要定期清洗"
            },
            {
                "type": "易脏",
                "severity": "中",
                "description": "不防水，容易沾染污渍"
            }
        ],
        "health_advice": {
            "general": "环保性好，适合所有人群，特别适合追求自然风格的家庭，透气性好，适合夏季使用",
            "pregnant": "特别推荐孕妇房使用，天然环保",
            "children": "适合儿童房，但需要定期清洗"
        },
        "advantages": "透气性好舒适，环保天然，价格适中，可拆洗，适合多种装修风格",
        "disadvantages": "容易起皱，需要定期清洗，不防水，容易沾染污渍",
        "price_range": "中档，性价比高",
        "risk_level": "低"
    },

    {
        "id": "fabric_002",
        "category": "布类",
        "material_type": "涤纶",
        "alternative_names": ["Polyester"],
        "visual_cues": [
            "色泽绚丽",
            "可呈现丝质、麻料、绒布等多种视觉效果",
            "表面光滑"
        ],
        "risk_points": [
            {
                "type": "透气性差",
                "severity": "中",
                "description": "透气性较差，夏季使用不舒适"
            },
            {
                "type": "静电问题",
                "severity": "中",
                "description": "容易产生静电"
            },
            {
                "type": "不够环保",
                "severity": "中",
                "description": "化学纤维，不够环保"
            }
        ],
        "health_advice": {
            "general": "适合预算有限的家庭，不推荐儿童房使用，注意通风",
            "pregnant": "不推荐孕妇房使用",
            "children": "不推荐儿童房使用"
        },
        "advantages": "价格适中性价比高，耐磨耐用，不易变形，易清洁，色彩丰富",
        "disadvantages": "透气性较差，吸湿性差，容易产生静电，不够环保",
        "price_range": "经济实惠",
        "risk_level": "中"
    },

    {
        "id": "fabric_003",
        "category": "布类",
        "material_type": "绒布",
        "alternative_names": ["Velvet", "灯芯绒", "麂皮绒"],
        "visual_cues": [
            "表面有绒毛",
            "质感柔软",
            "视觉效果高级",
            "颜色饱和度高"
        ],
        "risk_points": [
            {
                "type": "易沾灰",
                "severity": "中",
                "description": "容易沾灰，需要定期清洁维护"
            },
            {
                "type": "清洁困难",
                "severity": "中",
                "description": "清洁较困难"
            },
            {
                "type": "易压痕",
                "severity": "中",
                "description": "容易压出痕迹"
            },
            {
                "type": "沾宠物毛发",
                "severity": "中",
                "description": "容易沾染宠物毛发"
            }
        ],
        "health_advice": {
            "general": "适合追求舒适感的家庭，不推荐有宠物的家庭，需要定期吸尘清洁",
            "pregnant": "适合孕妇房，舒适保暖",
            "children": "适合儿童房，但需要定期清洁"
        },
        "advantages": "坐感柔软舒适，保暖功效好，视觉效果高级，触感细腻",
        "disadvantages": "价格较高，容易沾灰，清洁较困难，容易压出痕迹",
        "price_range": "较高",
        "risk_level": "中"
    },

    {
        "id": "fabric_004",
        "category": "布类",
        "material_type": "磨砂布",
        "alternative_names": [],
        "visual_cues": [
            "表面有磨砂质感",
            "颜色柔和",
            "质感细腻"
        ],
        "risk_points": [
            {
                "type": "价格较高",
                "severity": "中",
                "description": "价格较高"
            },
            {
                "type": "款式较少",
                "severity": "低",
                "description": "款式相对较少"
            }
        ],
        "health_advice": {
            "general": "适合追求品质的家庭，环保性较好",
            "pregnant": "适合孕妇房使用",
            "children": "适合儿童房使用"
        },
        "advantages": "耐磨性好，不易起球，质感好，易清洁",
        "disadvantages": "价格较高，款式相对较少",
        "price_range": "中高档",
        "risk_level": "低"
    }
]

# 导入数据到 ChromaDB
print("开始导入专业知识库数据...")

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

print(f"\n✅ 成功导入 {len(knowledge_data)} 条专业知识库数据！")

# 测试查询
print("\n" + "="*50)
print("测试查询功能...")
print("="*50)

test_queries = [
    "橡木家具有什么特点？",
    "胡桃木适合儿童房吗？",
    "真皮沙发和科技布沙发哪个好？",
    "棉麻沙发容易清洁吗？",
    "什么材料最环保？"
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

print("\n✅ 专业知识库导入完成！可以开始使用了。")
