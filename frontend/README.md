# 健康风险数据爬取系统

## 项目结构

```
D:\Users\86198\WeChatProjects\数据库\
├── raw/              # 原始爬取数据
│   ├── furniture/    # 家具材质数据
│   ├── textile/      # 衣料材质数据
│   └── food/         # 食物数据
├── processed/        # 处理后的数据
│   ├── furniture.json
│   ├── textile.json
│   └── food.json
├── logs/             # 日志文件
├── scrapers/         # 爬虫模块
│   ├── furniture_scraper.py
│   ├── textile_scraper.py
│   └── food_scraper.py
├── config.py         # 配置文件
├── main.py           # 主程序
└── README.md         # 本文件
```

## 数据源

### 家具材质
- ECHA SCIP Database (欧洲化学品管理局)
- CPID (Consumer Product Information Database)
- PubChem/TOXNET
- BIFMA, Greenguard, OEKO-TEX
- Healthy Materials Lab
- EWG

### 衣料材质
- OEKO-TEX Standard 100
- GOTS (Global Organic Textile Standard)
- Textile Exchange
- EPA TextileInfo

### 食物
- USDA FoodData Central
- FDA Food Database
- 中国食物成分表
- 食物相克数据库

## 使用方法

1. 配置 Firecrawl API Key:
```bash
export FIRECRAWL_API_KEY="your_api_key"
```

2. 运行爬虫:
```bash
python main.py --category all
# 或单独爬取
python main.py --category furniture
python main.py --category textile
python main.py --category food
```

## 数据格式

### 家具材质数据
```json
{
  "material_id": "unique_id",
  "category": "人造板类",
  "material_type": "刨花板",
  "chemical_components": [],
  "risk_points": [],
  "health_advice": {},
  "visual_cues": [],
  "certifications": [],
  "source": "database_name",
  "last_updated": "2026-01-30"
}
```

### 衣料材质数据
```json
{
  "material_id": "unique_id",
  "fabric_type": "棉",
  "composition": "100% Cotton",
  "chemical_treatments": [],
  "health_risks": [],
  "certifications": [],
  "care_instructions": {},
  "source": "database_name",
  "last_updated": "2026-01-30"
}
```

### 食物数据
```json
{
  "food_id": "unique_id",
  "name": "食物名称",
  "category": "蔬菜类",
  "nutrients": {},
  "recommended_intake": {},
  "contraindications": [],
  "incompatible_foods": [],
  "health_benefits": [],
  "source": "database_name",
  "last_updated": "2026-01-30"
}
```