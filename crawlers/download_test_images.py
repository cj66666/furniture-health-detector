"""
家具材料检测和人体工学检测 - 测试图片批量下载脚本

功能：
1. 批量下载家具照片（实木、板材、皮质沙发、布艺沙发等）
2. 批量下载坐姿照片（标准坐姿、驼背、椅子高度问题等）
3. 自动分类保存到不同文件夹
4. 支持多个图片源（Bing、Unsplash等）

依赖安装：
pip install bing-image-downloader requests pillow

使用方法：
python download_test_images.py
"""

import os
import sys
from pathlib import Path

try:
    from bing_image_downloader import downloader
except ImportError:
    print("❌ 缺少依赖库！请先安装：")
    print("pip install bing-image-downloader")
    sys.exit(1)

# 配置参数
CONFIG = {
    "output_dir": "test_images",  # 输出目录
    "limit": 15,  # 每类下载数量
    "adult_filter_off": True,  # 关闭成人内容过滤
    "timeout": 60,  # 超时时间（秒）
    "verbose": True,  # 显示详细信息
}

# 家具照片搜索关键词
FURNITURE_KEYWORDS = {
    "实木桌椅": [
        "solid wood dining table clear grain",
        "wooden desk chair natural texture",
        "oak furniture wood grain pattern",
        "实木家具 木纹清晰",
    ],
    "板材家具": [
        "particle board furniture edge banding",
        "MDF furniture cabinet edge",
        "laminated furniture visible edge",
        "板材家具 封边",
    ],
    "皮质沙发": [
        "leather sofa genuine grain",
        "full grain leather couch texture",
        "top grain leather sofa close up",
        "真皮沙发 纹理",
    ],
    "布艺沙发": [
        "fabric sofa linen cotton",
        "upholstered couch textile",
        "cloth sofa material close up",
        "布艺沙发 面料",
    ],
    "劣质家具": [
        "poor quality furniture rough edge",
        "bad furniture glue overflow",
        "low quality cabinet defect",
        "劣质家具 瑕疵",
    ],
    "高质量家具": [
        "high quality furniture craftsmanship",
        "premium furniture detail",
        "luxury furniture close up",
        "高档家具 细节",
    ],
}

# 坐姿照片搜索关键词
POSTURE_KEYWORDS = {
    "标准坐姿": [
        "correct sitting posture side view",
        "proper office chair posture",
        "ergonomic sitting position profile",
        "正确坐姿 侧面",
    ],
    "驼背坐姿": [
        "slouching posture side view",
        "hunched back sitting position",
        "poor posture rounded shoulders",
        "驼背坐姿 侧面",
    ],
    "椅子过高": [
        "chair too high feet dangling",
        "sitting feet not touching floor",
        "high chair posture problem",
        "椅子过高 脚悬空",
    ],
    "椅子过低": [
        "chair too low knees bent",
        "low chair posture problem",
        "sitting knees above hips",
        "椅子过低 膝盖弯曲",
    ],
    "不同身高坐姿": [
        "different height people sitting",
        "various body types office chair",
        "tall short person sitting posture",
        "不同身高 坐姿",
    ],
}


def download_images(category, keywords, output_dir, limit):
    """
    下载指定类别的图片

    Args:
        category: 类别名称
        keywords: 搜索关键词列表
        output_dir: 输出目录
        limit: 每个关键词下载数量
    """
    print(f"\n{'='*60}")
    print(f"📥 开始下载: {category}")
    print(f"{'='*60}")

    category_dir = os.path.join(output_dir, category)

    for i, keyword in enumerate(keywords, 1):
        print(f"\n[{i}/{len(keywords)}] 搜索关键词: {keyword}")

        try:
            downloader.download(
                keyword,
                limit=limit,
                output_dir=category_dir,
                adult_filter_off=CONFIG["adult_filter_off"],
                force_replace=False,
                timeout=CONFIG["timeout"],
                verbose=CONFIG["verbose"],
            )
            print(f"✅ 完成: {keyword}")
        except Exception as e:
            print(f"❌ 失败: {keyword}")
            print(f"   错误: {str(e)}")
            continue


def main():
    """主函数"""
    print("="*60)
    print("🖼️  家具材料检测 - 测试图片批量下载工具")
    print("="*60)

    # 创建输出目录
    output_dir = CONFIG["output_dir"]
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print(f"\n📁 输出目录: {os.path.abspath(output_dir)}")
    print(f"📊 每类下载数量: {CONFIG['limit']} 张")

    # 询问用户要下载哪些类别
    print("\n请选择要下载的图片类别:")
    print("1. 家具照片")
    print("2. 坐姿照片")
    print("3. 全部下载")

    choice = input("\n请输入选项 (1/2/3，默认3): ").strip() or "3"

    download_furniture = choice in ["1", "3"]
    download_posture = choice in ["2", "3"]

    # 下载家具照片
    if download_furniture:
        print("\n" + "="*60)
        print("📦 开始下载家具照片")
        print("="*60)

        for category, keywords in FURNITURE_KEYWORDS.items():
            download_images(
                category,
                keywords,
                os.path.join(output_dir, "家具照片"),
                CONFIG["limit"]
            )

    # 下载坐姿照片
    if download_posture:
        print("\n" + "="*60)
        print("🪑 开始下载坐姿照片")
        print("="*60)

        for category, keywords in POSTURE_KEYWORDS.items():
            download_images(
                category,
                keywords,
                os.path.join(output_dir, "坐姿照片"),
                CONFIG["limit"]
            )

    # 统计下载结果
    print("\n" + "="*60)
    print("✅ 下载完成！")
    print("="*60)

    # 统计各类别图片数量
    total_images = 0
    for root, dirs, files in os.walk(output_dir):
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if image_files:
            category_name = os.path.basename(root)
            print(f"📁 {category_name}: {len(image_files)} 张")
            total_images += len(image_files)

    print(f"\n📊 总计下载: {total_images} 张图片")
    print(f"📂 保存位置: {os.path.abspath(output_dir)}")

    print("\n💡 提示:")
    print("1. 下载的图片可能需要人工筛选，删除不符合要求的图片")
    print("2. 建议检查图片质量，确保分辨率至少1080p")
    print("3. 注意图片的光线、角度和背景是否符合要求")
    print("4. 可以根据需要调整CONFIG中的limit参数增加下载数量")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断下载")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
