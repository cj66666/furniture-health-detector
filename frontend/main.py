"""主数据爬取程序"""
import os
import argparse
import sys
from datetime import datetime

from config import (
    BASE_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, LOGS_DIR,
    DATABASE_URLS, SCRAPE_CONFIG, LOG_CONFIG, FIRECRAWL_API_KEY
)
from utils import setup_logger, save_json, load_json, merge_data


def create_directories():
    """创建必要的目录结构"""
    dirs = [
        os.path.join(RAW_DATA_DIR, "furniture"),
        os.path.join(RAW_DATA_DIR, "textile"),
        os.path.join(RAW_DATA_DIR, "food"),
        PROCESSED_DATA_DIR,
        LOGS_DIR
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def check_firecrawl_setup():
    """检查 Firecrawl 配置"""
    if not FIRECRAWL_API_KEY:
        print("警告: 未设置 FIRECRAWL_API_KEY 环境变量")
        print("部分功能可能无法使用。请设置 API Key:")
        print("export FIRECRAWL_API_KEY='your_api_key'")
        return False
    return True


def scrape_furniture_data(logger):
    """爬取家具材质数据"""
    logger.info("开始爬取家具材质数据...")

    # 导入家具爬虫
    try:
        from scrapers.furniture_scraper import FurnitureScraper
        scraper = FurnitureScraper(logger)
        data = scraper.scrape_all()
        logger.info(f"成功爬取 {len(data)} 条家具材质数据")
        return data
    except Exception as e:
        logger.error(f"家具数据爬取失败: {str(e)}")
        return []


def scrape_textile_data(logger):
    """爬取衣料材质数据"""
    logger.info("开始爬取衣料材质数据...")

    # 导入衣料爬虫
    try:
        from scrapers.textile_scraper import TextileScraper
        scraper = TextileScraper(logger)
        data = scraper.scrape_all()
        logger.info(f"成功爬取 {len(data)} 条衣料材质数据")
        return data
    except Exception as e:
        logger.error(f"衣料数据爬取失败: {str(e)}")
        return []


def scrape_food_data(logger):
    """爬取食物数据"""
    logger.info("开始爬取食物数据...")

    # 导入食物爬虫
    try:
        from scrapers.food_scraper import FoodScraper
        scraper = FoodScraper(logger)
        data = scraper.scrape_all()
        logger.info(f"成功爬取 {len(data)} 条食物数据")
        return data
    except Exception as e:
        logger.error(f"食物数据爬取失败: {str(e)}")
        return []


def process_and_save_data(category: str, data: list, logger):
    """处理并保存数据"""
    if not data:
        logger.warning(f"{category} 数据为空,跳过保存")
        return

    # 保存原始数据
    raw_file = os.path.join(RAW_DATA_DIR, category, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    save_json(data, raw_file)
    logger.info(f"原始数据已保存到: {raw_file}")

    # 加载已有的处理数据
    processed_file = os.path.join(PROCESSED_DATA_DIR, f"{category}.json")
    existing_data = load_json(processed_file)

    if existing_data:
        # 合并数据
        merged_data = merge_data(existing_data, data)
        logger.info(f"合并后共 {len(merged_data)} 条 {category} 数据")
    else:
        merged_data = data

    # 保存处理后的数据
    save_json(merged_data, processed_file)
    logger.info(f"处理后数据已保存到: {processed_file}")


def print_summary(furniture_count, textile_count, food_count):
    """打印爬取摘要"""
    print("\n" + "="*60)
    print("数据爬取完成!")
    print("="*60)
    print(f"家具材质数据: {furniture_count} 条")
    print(f"衣料材质数据: {textile_count} 条")
    print(f"食物数据: {food_count} 条")
    print(f"总计: {furniture_count + textile_count + food_count} 条")
    print("="*60)
    print(f"\n数据保存位置: {PROCESSED_DATA_DIR}")
    print("\n数据文件:")
    print(f"  - furniture.json (家具材质)")
    print(f"  - textile.json (衣料材质)")
    print(f"  - food.json (食物)")
    print("\n" + "="*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="健康风险数据爬取系统")
    parser.add_argument(
        "--category",
        type=str,
        choices=["all", "furniture", "textile", "food"],
        default="all",
        help="要爬取的数据类别 (默认: all)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="显示详细日志"
    )

    args = parser.parse_args()

    # 创建目录
    create_directories()

    # 设置日志
    log_level = "DEBUG" if args.verbose else LOG_CONFIG["level"]
    logger = setup_logger(LOG_CONFIG["file"], log_level)

    # 检查 Firecrawl 配置
    check_firecrawl_setup()

    logger.info("="*60)
    logger.info("健康风险数据爬取系统启动")
    logger.info(f"爬取类别: {args.category}")
    logger.info("="*60)

    furniture_count = 0
    textile_count = 0
    food_count = 0

    try:
        if args.category in ["all", "furniture"]:
            furniture_data = scrape_furniture_data(logger)
            process_and_save_data("furniture", furniture_data, logger)
            furniture_count = len(furniture_data)

        if args.category in ["all", "textile"]:
            textile_data = scrape_textile_data(logger)
            process_and_save_data("textile", textile_data, logger)
            textile_count = len(textile_data)

        if args.category in ["all", "food"]:
            food_data = scrape_food_data(logger)
            process_and_save_data("food", food_data, logger)
            food_count = len(food_data)

        print_summary(furniture_count, textile_count, food_count)

    except KeyboardInterrupt:
        logger.info("用户中断爬取")
        sys.exit(0)
    except Exception as e:
        logger.error(f"爬取过程发生错误: {str(e)}", exc_info=True)
        sys.exit(1)

    logger.info("爬取任务完成")


if __name__ == "__main__":
    main()