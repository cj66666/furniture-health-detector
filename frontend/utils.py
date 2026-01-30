"""工具函数模块"""
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any
import hashlib


def setup_logger(log_file: str, level: str = "INFO") -> logging.Logger:
    """设置日志记录器"""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger("scraper")
    logger.setLevel(getattr(logging, level))

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(getattr(logging, level))

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level))

    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def generate_material_id(data: Dict[str, Any], category: str) -> str:
    """生成材料唯一ID"""
    unique_string = f"{category}_{data.get('name', '')}_{data.get('type', '')}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:16]


def save_json(data: Any, file_path: str) -> None:
    """保存 JSON 数据"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(file_path: str) -> Any:
    """加载 JSON 数据"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_data(old_data: List[Dict], new_data: List[Dict], key: str = "material_id") -> List[Dict]:
    """合并新旧数据"""
    merged = {item[key]: item for item in old_data}
    for item in new_data:
        merged[item[key]] = item
    return list(merged.values())


def validate_data(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """验证数据完整性"""
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    return True


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    # 移除多余空白
    text = ' '.join(text.split())
    # 移除特殊字符
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return text.strip()


def create_material_entry(data: Dict[str, Any], category: str, source: str) -> Dict[str, Any]:
    """创建标准化的材料条目"""
    return {
        "material_id": generate_material_id(data, category),
        "category": category,
        "data": data,
        "source": source,
        "last_updated": datetime.now().isoformat(),
        "version": "1.0"
    }


def format_chemical_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """格式化化学物质数据"""
    return {
        "chemical_name": raw_data.get("name", ""),
        "cas_number": raw_data.get("cas", ""),
        "hazard_level": raw_data.get("hazard", "unknown"),
        "health_effects": raw_data.get("effects", []),
        "exposure_limit": raw_data.get("limit", "")
    }


def format_certification_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """格式化认证数据"""
    return {
        "certification_name": raw_data.get("name", ""),
        "issuing_body": raw_data.get("issuer", ""),
        "standard_level": raw_data.get("level", ""),
        "valid_until": raw_data.get("valid_until", ""),
        "scope": raw_data.get("scope", "")
    }


def extract_risk_info(text: str) -> List[Dict[str, Any]]:
    """从文本中提取风险信息"""
    risks = []

    # 关键词映射
    risk_keywords = {
        "甲醛": {"severity": "高", "category": "化学物质"},
        "VOCs": {"severity": "中", "category": "挥发性有机物"},
        "重金属": {"severity": "高", "category": "重金属"},
        "塑化剂": {"severity": "中", "category": "添加剂"},
        "致癌": {"severity": "高", "category": "健康风险"},
        "过敏": {"severity": "中", "category": "健康风险"}
    }

    for keyword, info in risk_keywords.items():
        if keyword in text:
            risks.append({
                "type": keyword,
                "severity": info["severity"],
                "category": info["category"],
                "description": f"可能含有{keyword}"
            })

    return risks


def extract_health_advice(text: str) -> Dict[str, Any]:
    """从文本中提取健康建议"""
    advice = {
        "general": [],
        "pregnant": [],
        "children": [],
        "elderly": []
    }

    # 通用建议关键词
    if "通风" in text or "ventilation" in text.lower():
        advice["general"].append("保持室内通风")
    if "避免" in text or "avoid" in text.lower():
        advice["general"].append("避免长时间接触")

    # 特殊人群建议
    if "孕妇" in text or "pregnant" in text.lower():
        advice["pregnant"].append("孕妇应谨慎使用")
    if "儿童" in text or "children" in text.lower():
        advice["children"].append("儿童应避免接触")
    if "老人" in text or "elderly" in text.lower():
        advice["elderly"].append("老年人应注意防护")

    return advice


def calculate_risk_score(risk_points: List[Dict[str, Any]]) -> int:
    """计算风险评分 (0-100)"""
    if not risk_points:
        return 0

    severity_scores = {
        "低": 20,
        "中": 50,
        "高": 80,
        "极高": 100
    }

    total_score = sum(severity_scores.get(risk.get("severity", "低"), 20) for risk in risk_points)
    return min(total_score // len(risk_points), 100)


def format_food_nutrition(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """格式化食物营养数据"""
    return {
        "energy": raw_data.get("energy", 0),
        "protein": raw_data.get("protein", 0),
        "fat": raw_data.get("fat", 0),
        "carbohydrate": raw_data.get("carb", 0),
        "fiber": raw_data.get("fiber", 0),
        "vitamins": raw_data.get("vitamins", {}),
        "minerals": raw_data.get("minerals", {})
    }


def detect_food_incompatibility(food1: str, food2: str, incompatibility_data: Dict) -> bool:
    """检测食物相克"""
    key1 = f"{food1}_{food2}"
    key2 = f"{food2}_{food1}"
    return key1 in incompatibility_data or key2 in incompatibility_data