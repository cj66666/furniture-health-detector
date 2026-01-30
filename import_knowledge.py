"""
家具材料知识库导入脚本
将知识库数据导入 ChromaDB 向量数据库
"""

import chromadb
from chromadb.config import Settings
import json

# 初始化 ChromaDB 客户端
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"  # 数据持久化目录
))

# 创建或获取集合
collection = client.get_or_create_collection(
    name="furniture_knowledge",
    metadata={"description": "家具材料检测知识库"}
)

# 知识库数据
knowledge_data = [
    # 刨花板知识
    {
        "id": "material_001",
        "category": "刨花板",
        "material_type": "人造板材",
        "risk_points": [
            "封边不严容易释放甲醛",
            "遇水易膨胀变形",
            "承重能力有限"
        ],
        "visual_cues": [
            "侧面有颗粒感",
            "边缘粗糙",
            "非激光封边会有明显黑线",
            "切面呈颗粒状"
        ],
        "health_advice": "建议查看商家是否具备ENF级证书，卧室慎用，孕妇儿童房避免使用",
        "risk_level": "中",
        "price_range": "60-160元/张",
        "advantages": "价格便宜，握钉力好，横向承重力好，甲醛含量比大芯板低",
        "disadvantages": "质量差异大不易辨别，抗弯性和抗拉性较差，密度疏松易松动"
    },

    # 密度板知识
    {
        "id": "material_002",
        "category": "密度板",
        "material_type": "人造板材",
        "risk_points": [
            "握钉力差，螺丝易松动",
            "用胶量大，甲醛风险高",
            "不适合承重部位",
            "螺丝在同一位置紧固两次会失去紧固力"
        ],
        "visual_cues": [
            "表面极其平整光滑",
            "切面呈粉末状",
            "重量较重",
            "无明显纹理"
        ],
        "health_advice": "必须查看环保检测报告，避免用于儿童房，确保六面封边良好，选择E0级以上",
        "risk_level": "中高",
        "price_range": "60-150元/张",
        "advantages": "结构致密表面平整，加工简单，不易受潮变形，质软耐冲击易再加工",
        "disadvantages": "握钉力不强是致命缺陷，密度越高用胶越多"
    },

    # 大芯板知识
    {
        "id": "material_003",
        "category": "大芯板",
        "material_type": "人造板材",
        "alternative_names": ["细木工板", "木工板"],
        "risk_points": [
            "手拼板质量差易变形",
            "劣质板材甲醛超标",
            "泡桐材质易干裂",
            "怕潮湿不适合厨卫"
        ],
        "visual_cues": [
            "芯条排列不均匀",
            "有明显缝隙对光透白",
            "有刺鼻气味",
            "敲击声音有变化说明有空洞"
        ],
        "health_advice": "选择机拼板，选择杨木桦木材质，避免用于潮湿环境，查看环保检测报告",
        "risk_level": "中",
        "price_range": "80-200元/张",
        "advantages": "握螺钉力好强度高，质坚吸声绝热，含水率10-13%适中",
        "disadvantages": "怕潮湿，手拼板质量差，劣质材料甲醛超标"
    },

    # 实木拼板知识
    {
        "id": "material_004",
        "category": "实木拼板",
        "material_type": "实木类",
        "risk_points": [
            "价格较高",
            "需要定期保养"
        ],
        "visual_cues": [
            "有自然木纹",
            "纹理规则整齐",
            "表面平整无高低差",
            "有木材香味",
            "重量适中"
        ],
        "health_advice": "环保首选，适合所有人群，特别推荐儿童房和孕妇房使用",
        "risk_level": "低",
        "price_range": "200-500元/张",
        "advantages": "板材表面不易翘曲开裂，纹理色泽整体感好，物理性能稳定，木材利用率高，甲醛挥发量低更环保",
        "disadvantages": "价格较高，需要定期保养"
    },

    # 环保等级知识
    {
        "id": "standard_001",
        "category": "环保标准",
        "material_type": "通用标准",
        "content": "ENF级甲醛释放量≤0.025mg/m³是欧洲最新最严格标准，E0级≤0.050mg/m³是高端环保标准，E1级≤0.124mg/m³是基本环保标准",
        "health_advice": "优先选择ENF级或E0级，儿童房孕妇房必须ENF级，避免选择E1级以下产品",
        "risk_level": "标准参考"
    },

    # 选购技巧
    {
        "id": "tips_001",
        "category": "选购技巧",
        "material_type": "通用技巧",
        "content": "查看环保认证要求商家出示权威机构检测报告，闻气味优质板材仅有轻微木香刺鼻或辣眼说明甲醛超标，看封边六面都要封边良好激光封边优于普通封边，检查结构芯条排列均匀整齐无腐朽断裂虫孔，敲击测试声音均匀一致声音有变化说明内部有空洞",
        "health_advice": "不要轻信口头承诺，必须查看书面检测报告，封边不严会导致甲醛持续释放",
        "risk_level": "防坑指南"
    },

    # 使用场景推荐
    {
        "id": "scene_001",
        "category": "使用场景",
        "material_type": "场景推荐",
        "content": "潮湿环境如厨房卫生间推荐多层板防潮板避免大芯板密度板，承重部位如书架衣柜推荐颗粒板OSB板实木拼板避免密度板，造型需求如门板装饰面推荐密度板但必须选E0级以上，儿童房孕妇房推荐ENF级实木拼板避免所有低等级人造板",
        "health_advice": "根据使用场景选择合适板材，潮湿环境避免易受潮板材，儿童房必须选择最高环保等级",
        "risk_level": "场景指南"
    }
]

# 导入数据到 ChromaDB
print("开始导入知识库数据...")

for item in knowledge_data:
    # 构建文档内容
    document = f"""
    材料类别: {item['category']}
    材料类型: {item['material_type']}
    """

    if 'risk_points' in item:
        document += f"\n风险点: {', '.join(item['risk_points'])}"

    if 'visual_cues' in item:
        document += f"\n视觉特征: {', '.join(item['visual_cues'])}"

    if 'health_advice' in item:
        document += f"\n健康建议: {item['health_advice']}"

    if 'advantages' in item:
        document += f"\n优点: {item['advantages']}"

    if 'disadvantages' in item:
        document += f"\n缺点: {item['disadvantages']}"

    if 'content' in item:
        document += f"\n内容: {item['content']}"

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

    print(f"✓ 已导入: {item['category']}")

print(f"\n✅ 成功导入 {len(knowledge_data)} 条知识库数据！")

# 测试查询
print("\n" + "="*50)
print("测试查询功能...")
print("="*50)

test_queries = [
    "这个柜子是刨花板的，安全吗？",
    "密度板有什么问题？",
    "儿童房用什么板材好？",
    "如何识别劣质板材？"
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

print("\n✅ 知识库导入完成！可以开始使用了。")
