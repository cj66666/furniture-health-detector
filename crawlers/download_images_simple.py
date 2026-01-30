"""
家具材料检测和人体工学检测 - 测试图片批量下载脚本 (简化版)

功能：
1. 使用Pexels API批量下载高质量图片
2. 自动分类保存到不同文件夹
3. 支持去重和质量过滤

依赖安装：
pip install requests pillow tqdm

使用方法：
python download_images_simple.py
"""

import os
import sys
import time
import hashlib
from pathlib import Path
import json

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
    "output_dir": "test_images_simple",  # 输出目录
    "limit_per_keyword": 3,  # 每个关键词下载数量（降低以提高成功率）
    "min_width": 800,  # 降低最小宽度要求
    "min_height": 600,  # 降低最小高度要求
    "timeout": 30,  # 超时时间（秒）
}

# Pexels API - 免费，每月5000次请求
# 注册地址: https://www.pexels.com/api/
PEXELS_API_KEY = "wDIq8pvgdx3B5rOveYDr2K2wzfJqsMPYzq7hrdymo1DERtwr94E03M7h"  # 真实API密钥
PEXELS_API = "https://api.pexels.com/v1/search"

# 图片分类和搜索关键词（简化版，使用更通用的关键词）
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
    def __init__(self, output_dir, timeout=30):
        self.output_dir = Path(output_dir)
        self.timeout = timeout
        self.downloaded_hashes = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Authorization': PEXELS_API_KEY
        })
        self.download_count = 0

    def get_image_hash(self, image_data):
        """计算图片的MD5哈希值用于去重"""
        return hashlib.md5(image_data).hexdigest()

    def download_from_pexels(self, query, limit=3):
        """从Pexels下载图片"""
        images = []
        try:
            print(f"    [搜索] Pexels搜索: {query}")

            params = {
                'query': query,
                'per_page': limit * 2,
                'orientation': 'landscape'
            }

            response = self.session.get(
                PEXELS_API,
                params=params,
                timeout=self.timeout
            )

            print(f"    [API] 响应状态: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                photos = data.get('photos', [])

                print(f"    [图片] 找到 {len(photos)} 张图片")

                for photo in photos[:limit * 2]:
                    try:
                        # 获取中等尺寸的图片URL
                        img_url = photo.get('src', {}).get('large')
                        if not img_url:
                            continue

                        print(f"    [下载]  下载: {img_url[:50]}...")

                        # 下载图片
                        img_response = self.session.get(img_url, timeout=self.timeout)
                        if img_response.status_code == 200:
                            img_data = img_response.content

                            # 检查是否重复
                            img_hash = self.get_image_hash(img_data)
                            if img_hash in self.downloaded_hashes:
                                print(f"    [警告]  重复图片，跳过")
                                continue

                            # 检查图片尺寸
                            try:
                                img = Image.open(BytesIO(img_data))
                                print(f"    [尺寸] {img.width}x{img.height}")

                                if img.width >= CONFIG['min_width'] and img.height >= CONFIG['min_height']:
                                    images.append(img_data)
                                    self.downloaded_hashes.add(img_hash)
                                    print(f"    [成功] 成功添加")

                                    if len(images) >= limit:
                                        break
                                else:
                                    print(f"    [警告]  尺寸不符合要求")
                            except Exception as e:
                                print(f"    [警告]  图片处理失败: {e}")
                                continue

                        time.sleep(1)  # 避免请求过快

                    except Exception as e:
                        print(f"    [警告]  下载失败: {e}")
                        continue

            elif response.status_code == 403:
                print(f"    [警告]  API认证失败，请检查API Key")
            else:
                print(f"    [警告]  API请求失败: {response.text[:100]}")

        except Exception as e:
            print(f"    [警告]  Pexels搜索失败: {e}")

        return images

    def download_from_placeholder(self, width=800, height=600, text="Test"):
        """使用占位图片服务（备用方案）"""
        images = []
        try:
            # 使用 placeholder.com 服务
            url = f"https://via.placeholder.com/{width}x{height}.jpg?text={text}"

            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                img_data = response.content
                img_hash = self.get_image_hash(img_data)

                if img_hash not in self.downloaded_hashes:
                    images.append(img_data)
                    self.downloaded_hashes.add(img_hash)
                    print(f"    [成功] 使用占位图片")

        except Exception as e:
            print(f"    [警告]  占位图片下载失败: {e}")

        return images

    def download_images(self, category, subcategory, keywords, limit):
        """下载指定类别的图片"""
        # 创建输出目录
        output_path = self.output_dir / category / subcategory
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"\n[下载] {category}/{subcategory}")

        all_images = []

        # 对每个关键词进行搜索
        for keyword in keywords:
            if len(all_images) >= limit:
                break

            print(f"  [搜索] 关键词: {keyword}")

            # 从Pexels下载
            images = self.download_from_pexels(keyword, limit=limit - len(all_images))
            all_images.extend(images)

            # 如果Pexels没有结果，使用占位图片
            if len(images) == 0:
                print(f"  [警告]  Pexels无结果，使用占位图片")
                placeholder_images = self.download_from_placeholder(
                    width=CONFIG['min_width'],
                    height=CONFIG['min_height'],
                    text=keyword.replace(' ', '+')
                )
                all_images.extend(placeholder_images)

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
                self.download_count += 1

            except Exception as e:
                print(f"  [警告]  保存失败: {e}")

        print(f"  [成功] 成功下载 {saved_count} 张图片")
        return saved_count


def main():
    """主函数"""
    print("=" * 60)
    print("家具材料检测和人体工学检测 - 测试图片下载工具 (简化版)")
    print("=" * 60)

    # 自动下载全部类别（无需用户输入）
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
    print(f"\n[提示] 如果Pexels API失败，会自动使用占位图片")

    for category in categories_to_download:
        if category not in IMAGE_CATEGORIES:
            continue

        print(f"\n{'='*60}")
        print(f"[文件夹] {category}")
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
    print(f"[成功] 下载完成！")
    print(f"{'='*60}")
    print(f"总类别数: {total_categories}")
    print(f"总下载数: {downloader.download_count} 张")
    print(f"保存位置: {CONFIG['output_dir']}")
    print(f"\n[提示] 如需更多图片，可以：")
    print(f"   1. 注册Pexels API获取免费API Key")
    print(f"   2. 访问 https://www.pexels.com/api/")
    print(f"   3. 替换脚本中的 PEXELS_API_KEY")


if __name__ == "__main__":
    main()
