"""配置文件"""
import os
from datetime import datetime

# Firecrawl API 配置
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY', '')

# 数据目录
BASE_DIR = r"D:\Users\86198\WeChatProjects\数据库"
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "processed")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# 数据源配置
DATABASE_URLS = {
    # 家具材质数据源
    "furniture": {
        "echa_scip": {
            "name": "ECHA SCIP Database",
            "url": "https://echa.europa.eu/scip",
            "description": "欧洲化学品管理局 - 高度关注物质数据库"
        },
        "cpid": {
            "name": "Consumer Product Information Database",
            "url": "https://www.cpid.org/",
            "description": "消费者产品信息数据库"
        },
        "pubchem": {
            "name": "PubChem",
            "url": "https://pubchem.ncbi.nlm.nih.gov/",
            "description": "化学物质数据库"
        },
        "bifma": {
            "name": "BIFMA",
            "url": "https://www.bifma.org/",
            "description": "办公家具行业标准"
        },
        "greenguard": {
            "name": "Greenguard",
            "url": "https://www.ul.com/resources/greenguard-certification-program",
            "description": "低排放产品认证"
        },
        "oeko_tex": {
            "name": "OEKO-TEX",
            "url": "https://www.oeko-tex.com/",
            "description": "纺织品有害物质检测标准"
        },
        "healthy_materials_lab": {
            "name": "Healthy Materials Lab",
            "url": "https://healthymaterialslab.org/",
            "description": "健康材料实验室"
        },
        "ewg": {
            "name": "Environmental Working Group",
            "url": "https://www.ewg.org/",
            "description": "环境工作组"
        }
    },

    # 衣料材质数据源
    "textile": {
        "oeko_tex": {
            "name": "OEKO-TEX Standard 100",
            "url": "https://www.oeko-tex.com/en/our-standards/standard-100-by-oeko-tex",
            "description": "纺织品有害物质检测"
        },
        "gots": {
            "name": "Global Organic Textile Standard",
            "url": "https://www.global-standard.org/",
            "description": "全球有机纺织品标准"
        },
        "textile_exchange": {
            "name": "Textile Exchange",
            "url": "https://textileexchange.org/",
            "description": "纺织品交易所"
        },
        "epa_textile": {
            "name": "EPA TextileInfo",
            "url": "https://www.epa.gov/",
            "description": "美国环保署纺织品信息"
        },
        "made_safe": {
            "name": "Made Safe",
            "url": "https://www.madesafe.org/",
            "description": "安全产品认证"
        }
    },

    # 食物数据源
    "food": {
        "usda_fooddata": {
            "name": "USDA FoodData Central",
            "url": "https://fdc.nal.usda.gov/",
            "description": "美国农业部食品数据中心"
        },
        "fda_food": {
            "name": "FDA Food Database",
            "url": "https://www.fda.gov/food",
            "description": "FDA 食品数据库"
        },
        "chinese_food_composition": {
            "name": "中国食物成分表",
            "url": "http://yingyang.sbr.net.cn/",
            "description": "中国疾病预防控制中心营养与健康所"
        },
        "food_incompatibility": {
            "name": "食物相克数据",
            "url": "https://www.meishij.net/",
            "description": "食物相克数据库"
        },
        "nutrients_db": {
            "name": "营养成分数据库",
            "url": "https://www.nutritionvalue.org/",
            "description": "营养价值数据库"
        }
    },

    # GitHub 公开数据库
    "github": {
        "furniture_materials": {
            "name": "Furniture Materials Database",
            "url": "https://github.com/search?q=furniture+materials+database",
            "description": "家具材质开源数据"
        },
        "textile_data": {
            "name": "Textile Material Database",
            "url": "https://github.com/search?q=textile+materials+data",
            "description": "纺织品材质数据"
        },
        "food_composition": {
            "name": "Food Composition Database",
            "url": "https://github.com/search?q=food+composition+database",
            "description": "食物成分数据库"
        }
    }
}

# 爬取配置
SCRAPE_CONFIG = {
    "max_pages": 100,  # 每个数据源最多爬取页数
    "timeout": 30,  # 请求超时时间(秒)
    "retry_times": 3,  # 失败重试次数
    "delay": 2,  # 请求间隔(秒)
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 日志配置
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": os.path.join(LOGS_DIR, f"scraper_{datetime.now().strftime('%Y%m%d')}.log")
}

# 数据验证规则
VALIDATION_RULES = {
    "furniture": {
        "required_fields": ["material_id", "category", "material_type"],
        "categories": ["人造板类", "实木类", "皮革类", "布类", "金属类", "高分子材料类"]
    },
    "textile": {
        "required_fields": ["material_id", "fabric_type"],
        "fabric_types": ["棉", "麻", "丝", "羊毛", "涤纶", "尼龙", "氨纶", "粘胶纤维"]
    },
    "food": {
        "required_fields": ["food_id", "name", "category"],
        "categories": ["谷物类", "蔬菜类", "水果类", "肉类", "水产类", "豆类", "奶制品", "调味品"]
    }
}