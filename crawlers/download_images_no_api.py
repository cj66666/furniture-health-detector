"""
图片下载脚本 - 无需API密钥版本

使用公开的图片源，无需注册API
适合快速测试和小规模下载

依赖安装：
pip install requests pillow

使用方法：
python download_images_no_api.py
"""

import os
import sys
import time
import hashlib
from pathlib import Path
import urllib.request
import urllib.parse

try:
    import requests
    from PIL import Image
    from io import BytesIO
except ImportError as e:
    print(f"[错误] 缺少依赖库！请先安装：")
    print("pip install requests pillow")
    sys.exit(1)

# 配置参数
CONFIG = {
    "output_dir": "test_images_no_api",
    "limit_per_keyword": 2,  # 每个关键词下载数量
    "min_width": 600,
    "min_height": 400,
    "timeout": 15,
}

# 图片分类和搜索关键词
IMAGE_CATEGORIES = {
    "家具照片": {
        "实木桌椅": [
            "wooden table",
            "wood furniture",
        ],
        "沙发": [
            "leather sofa",
            "fabric couch",
        ],
        "家具细节": [
            "furniture detail",
            "wood texture",
        ],
    },
    "坐姿照片": {
        "办公坐姿": [
            "office posture",
            "desk sitting",
        ],
        "人体工学": [
            "ergonomic chair",
            "sitting position",
        ],
    },
}


class ImageDownloader:
    def __init__(self, output_dir, timeout=15):
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.downloaded_hashes = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.download_count = 0

    def get_image_hash(self, image_data):
        """计算图片的MD5哈希值用于去重"""
        return hashlib.md5(image_data).hexdigest()

    def download_from_picsum(self, width=800, height=600, keyword=""):
        """从Lorem Picsum下载随机图片（无需API密钥）"""
        images = []
        try:
            # Lorem Picsum提供免费的随机图片
            url = f"https://picsum.photos/{width}/{height}"

            print(f"    [下载] 从Picsum获取图片...")

            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            if response.status_code == 200:
                img_data = response.content

                # 检查是否重复
                img_hash = self.get_image_hash(img_data)
                if img_hash not in self.downloaded_hashes:
                    # 验证图片
                    try:
                        img = Image.open(BytesIO(img_data))
                        if img.width >= CONFIG['min_width'] and img.height >= CONFIG['min_height']:
                            images.append(img_data)
                            self.downloaded_hashes.add(img_hash)
                            print(f"    [成功] 获取图片 {img.width}x{img.height}")
                        else:
                            print(f"    [警告] 尺寸不符: {img.width}x{img.height}")
                    except Exception as e:
                        print(f"    [警告] 图片验证失败: {e}")
                else:
                    print(f"    [警告] 重复图片")

            time.sleep(1)  # 避免请求过快

        except Exception as e:
            print(f"    [警告] 下载失败: {e}")

        return images

    def download_images(self, category, subcategory, keywords, limit):
        """下载指定类别的图片"""
        # 创建输出目录
        output_path = self.output_dir / category / subcategory
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\n[下载] {category}/{subcategory}")

        all_images = []

        # 对每个关键词下载图片
        for keyword in keywords:
            if len(all_images) >= limit:
                break

            print(f"  [关键词] {keyword}")

            # 尝试下载多次以获得不同的随机图片
            for attempt in range(limit * 2):
                if len(all_images) >= limit:
                    break

                images = self.download_from_picsum(
                    width=CONFIG['min_width'],
                    height=CONFIG['min_height'],
                    keyword=keyword
                )
                all_images.extend(images)

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
                self.download_count += 1

            except Exception as e:
                print(f"  [警告] 保存失败: {e}")

        print(f"  [完成] 成功下载 {saved_count} 张图片")
        return saved_count


def main():
    """主函数"""
    print("=" * 60)
    print("图片下载工具 - 无需API密钥版本")
    print("=" * 60)
    print("\n[说明] 本脚本使用Lorem Picsum提供的免费随机图片")
    print("[说明] 图片为通用图片，可能不完全符合关键词")
    print("[说明] 适合快速测试，如需高质量图片请使用Pexels API版本")

    # 自动下载全部类别
    print("\n自动下载全部类别...")
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
        print(f"[类别] {category}")
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
    print(f"[完成] 下载完成！")
    print(f"{'='*60}")
    print(f"总类别数: {total_categories}")
    print(f"总下载数: {downloader.download_count} 张")
    print(f"保存位置: {CONFIG['output_dir']}")

    print(f"\n[提示] 这些是随机通用图片")
    print(f"[提示] 如需特定主题的高质量图片，请：")
    print(f"   1. 参考 Pexels_API配置指南.md")
    print(f"   2. 获取免费Pexels API密钥")
    print(f"   3. 使用 download_images_simple.py")


if __name__ == "__main__":
    main()
