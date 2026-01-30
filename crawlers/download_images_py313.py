"""
家具材料检测和人体工学检测 - 测试图片批量下载脚本 (Python 3.13兼容版)

功能：
1. 批量下载家具照片（实木、板材、皮质沙发、布艺沙发等）
2. 批量下载坐姿照片（标准坐姿、驼背、椅子高度问题等）
3. 自动分类保存到不同文件夹
4. 使用Unsplash和Pexels API（免费）

依赖安装：
pip install requests pillow tqdm

使用方法：
python download_images_py313.py
"""

import os
import sys
import time
import hashlib
from pathlib import Path
from urllib.parse import urlencode

try:
    import requests
    from PIL import Image
    from io import BytesIO
    from tqdm import tqdm
except ImportError as e:
    print(f"❌ 缺少依赖库！请先安装：")
    print("pip install requests pillow tqdm")
    sys.exit(1)

# 配置参数
CONFIG = {
    "output_dir": "test_images_py313",  # 输出目录
    "limit_per_keyword": 5,  # 每个关键词下载数量
    "min_width": 1280,  # 最小宽度
    "min_height": 720,  # 最小高度
    "timeout": 30,  # 超时时间（秒）
}

# Unsplash API配置（免费，无需注册也可使用搜索）
UNSPLASH_API = "https://unsplash.com/napi/search/photos"

# Pexels API配置（需要注册获取API key，这里使用公开搜索）
PEXELS_SEARCH = "https://www.pexels.com/search"

# 图片分类和搜索关键词
IMAGE_CATEGORIES = {
    "家具照片": {
        "实木桌椅": [
            "solid wood dining table",
            "wooden desk natural grain",
            "oak furniture texture",
        ],
        "板材家具": [
            "particle board furniture",
            "laminated cabinet",
            "MDF furniture",
        ],
        "皮质沙发_真皮": [
            "genuine leather sofa",
            "full grain leather couch",
            "top grain leather furniture",
        ],
        "皮质沙发_PU皮": [
            "PU leather sofa",
            "faux leather couch",
            "synthetic leather furniture",
        ],
        "皮质沙发_科技布": [
            "tech fabric sofa",
            "microfiber couch",
            "performance fabric furniture",
        ],
        "布艺沙发_棉麻": [
            "linen sofa",
            "cotton linen couch",
            "natural fabric furniture",
        ],
        "布艺沙发_绒布": [
            "velvet sofa",
            "plush couch",
            "velour furniture",
        ],
        "劣质家具": [
            "poor quality furniture defects",
            "furniture damage peeling",
            "bad furniture edge",
        ],
        "高质量家具": [
            "high quality furniture craftsmanship",
            "luxury furniture detail",
            "premium furniture finish",
        ],
    },
    "坐姿照片": {
        "标准坐姿": [
            "correct sitting posture side view",
            "proper desk posture ergonomic",
            "good sitting position office",
        ],
        "驼背坐姿": [
            "slouching posture bad",
            "hunched back sitting",
            "poor posture desk",
        ],
        "椅子过高": [
            "chair too high feet dangling",
            "high chair posture problem",
            "elevated seat posture",
        ],
        "椅子过低": [
            "chair too low knees bent",
            "low seat posture issue",
            "sitting low chair",
        ],
        "不同身高": [
            "different heights sitting",
            "tall short people chairs",
            "various body types seating",
        ],
    },
}


class ImageDownloader:
    def __init__(self, output_dir, timeout=30):
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.downloaded_hashes = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_image_hash(self, image_data):
        """计算图片的MD5哈希值用于去重"""
        return hashlib.md5(image_data).hexdigest()

    def download_from_unsplash(self, query, limit=5):
        """从Unsplash下载图片"""
        images = []
        try:
            params = {
                'query': query,
                'per_page': limit * 2,  # 多下载一些以防过滤后不够
                'orientation': 'landscape'
            }

            response = self.session.get(
                UNSPLASH_API,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])

                for item in results[:limit * 2]:
                    try:
                        # 获取常规尺寸的图片URL
                        img_url = item.get('urls', {}).get('regular')
                        if not img_url:
                            continue

                        # 下载图片
                        img_response = self.session.get(img_url, timeout=self.timeout)
                        if img_response.status_code == 200:
                            img_data = img_response.content

                            # 检查是否重复
                            img_hash = self.get_image_hash(img_data)
                            if img_hash in self.downloaded_hashes:
                                continue

                            # 检查图片尺寸
                            try:
                                img = Image.open(BytesIO(img_data))
                                if img.width >= CONFIG['min_width'] and img.height >= CONFIG['min_height']:
                                    images.append(img_data)
                                    self.downloaded_hashes.add(img_hash)

                                    if len(images) >= limit:
                                        break
                            except Exception:
                                continue

                        time.sleep(0.5)  # 避免请求过快

                    except Exception as e:
                        continue

        except Exception as e:
            print(f"  ⚠️ Unsplash搜索失败: {e}")

        return images

    def download_images(self, category, subcategory, keywords, limit):
        """下载指定类别的图片"""
        # 创建输出目录
        output_path = self.output_dir / category / subcategory
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\n📥 下载 {category}/{subcategory}")

        all_images = []

        # 对每个关键词进行搜索
        for keyword in keywords:
            if len(all_images) >= limit:
                break

            print(f"  🔍 搜索: {keyword}")

            # 从Unsplash下载
            images = self.download_from_unsplash(keyword, limit=limit - len(all_images))
            all_images.extend(images)

            if len(all_images) >= limit:
                break

        # 保存图片
        saved_count = 0
        for idx, img_data in enumerate(all_images[:limit], 1):
            try:
                # 生成文件名
                filename = f"{subcategory.replace('/', '_')}_{idx:03d}.jpg"
                filepath = output_path / filename

                # 保存图片
                with open(filepath, 'wb') as f:
                    f.write(img_data)

                saved_count += 1

            except Exception as e:
                print(f"  ⚠️ 保存失败: {e}")

        print(f"  ✅ 成功下载 {saved_count} 张图片")
        return saved_count


def main():
    """主函数"""
    print("=" * 60)
    print("家具材料检测和人体工学检测 - 测试图片下载工具 (Python 3.13)")
    print("=" * 60)

    # 选择下载类别
    print("\n请选择下载类别：")
    print("1. 仅下载家具照片")
    print("2. 仅下载坐姿照片")
    print("3. 下载全部（默认）")

    choice = input("\n请输入选项 (1/2/3，直接回车选择3): ").strip()

    categories_to_download = []
    if choice == "1":
        categories_to_download = ["家具照片"]
    elif choice == "2":
        categories_to_download = ["坐姿照片"]
    else:
        categories_to_download = ["家具照片", "坐姿照片"]

    # 创建下载器
    downloader = ImageDownloader(
        output_dir=CONFIG["output_dir"],
        timeout=CONFIG["timeout"]
    )

    # 统计信息
    total_downloaded = 0
    total_categories = 0

    # 开始下载
    print(f"\n开始下载到目录: {CONFIG['output_dir']}")
    print(f"每个类别下载: {CONFIG['limit_per_keyword']} 张")
    print(f"最小分辨率: {CONFIG['min_width']}x{CONFIG['min_height']}")

    for category in categories_to_download:
        if category not in IMAGE_CATEGORIES:
            continue

        print(f"\n{'='*60}")
        print(f"📂 {category}")
        print(f"{'='*60}")

        for subcategory, keywords in IMAGE_CATEGORIES[category].items():
            count = downloader.download_images(
                category=category,
                subcategory=subcategory,
                keywords=keywords,
                limit=CONFIG["limit_per_keyword"]
            )
            total_downloaded += count
            total_categories += 1

    # 显示统计信息
    print(f"\n{'='*60}")
    print(f"✅ 下载完成！")
    print(f"{'='*60}")
    print(f"总类别数: {total_categories}")
    print(f"总下载数: {total_downloaded} 张")
    print(f"保存位置: {CONFIG['output_dir']}")
    print(f"\n💡 提示: 下载的图片已按类别整理，可以直接用于测试")


if __name__ == "__main__":
    main()
