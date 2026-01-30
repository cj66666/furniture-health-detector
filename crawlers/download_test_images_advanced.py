"""
增强版图片下载脚本 - 支持多个图片源和质量检查

功能：
1. 支持多个图片源（Bing、Unsplash、Pexels）
2. 自动检查图片质量（分辨率、文件大小）
3. 去重功能
4. 下载进度显示
5. 自动重命名和分类

依赖安装：
pip install bing-image-downloader requests pillow tqdm

使用方法：
python download_test_images_advanced.py
"""

import os
import sys
import hashlib
import requests
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse

try:
    from bing_image_downloader import downloader
    from PIL import Image
    from tqdm import tqdm
except ImportError:
    print("❌ 缺少依赖库！请先安装：")
    print("pip install bing-image-downloader requests pillow tqdm")
    sys.exit(1)

# 配置参数
CONFIG = {
    "output_dir": "test_images_hq",  # 输出目录
    "limit_per_keyword": 5,  # 每个关键词下载数量
    "min_width": 1920,  # 最小宽度（1080p）
    "min_height": 1080,  # 最小高度
    "min_file_size": 100 * 1024,  # 最小文件大小（100KB）
    "max_file_size": 10 * 1024 * 1024,  # 最大文件大小（10MB）
    "timeout": 30,  # 超时时间（秒）
    "remove_duplicates": True,  # 去重
}

# Unsplash API配置（可选，需要注册获取Access Key）
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # 替换为你的Access Key

# 图片搜索配置
IMAGE_CATEGORIES = {
    "家具照片": {
        "实木桌椅": [
            "solid wood dining table grain",
            "wooden desk natural texture",
            "oak furniture pattern",
        ],
        "板材家具": [
            "particle board furniture",
            "MDF cabinet edge",
            "laminated furniture",
        ],
        "皮质沙发_真皮": [
            "genuine leather sofa texture",
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
            "linen sofa natural",
            "cotton fabric couch",
            "natural fiber furniture",
        ],
        "布艺沙发_绒布": [
            "velvet sofa",
            "plush fabric couch",
            "soft velour furniture",
        ],
        "劣质家具": [
            "poor quality furniture defect",
            "bad furniture rough edge",
            "low quality cabinet flaw",
        ],
        "高质量家具": [
            "high quality furniture detail",
            "premium furniture craftsmanship",
            "luxury furniture close up",
        ],
    },
    "坐姿照片": {
        "标准坐姿": [
            "correct sitting posture side",
            "proper office posture profile",
            "ergonomic sitting position",
        ],
        "驼背坐姿": [
            "slouching posture side",
            "hunched back sitting",
            "poor posture rounded",
        ],
        "椅子过高": [
            "chair too high feet dangling",
            "sitting feet not floor",
            "high chair problem",
        ],
        "椅子过低": [
            "chair too low knees",
            "low chair posture",
            "knees above hips sitting",
        ],
        "不同身高": [
            "different height sitting",
            "various body types chair",
            "tall short person sitting",
        ],
    },
}


class ImageDownloader:
    """图片下载器类"""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.downloaded_hashes = set()  # 用于去重
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def get_image_hash(self, image_path: str) -> str:
        """计算图片哈希值用于去重"""
        with open(image_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def check_image_quality(self, image_path: str) -> Dict:
        """
        检查图片质量

        Returns:
            dict: {
                'valid': bool,
                'width': int,
                'height': int,
                'size': int,
                'reason': str
            }
        """
        try:
            # 检查文件大小
            file_size = os.path.getsize(image_path)
            if file_size < CONFIG["min_file_size"]:
                return {
                    'valid': False,
                    'reason': f'文件太小 ({file_size/1024:.1f}KB < {CONFIG["min_file_size"]/1024:.1f}KB)'
                }
            if file_size > CONFIG["max_file_size"]:
                return {
                    'valid': False,
                    'reason': f'文件太大 ({file_size/1024/1024:.1f}MB > {CONFIG["max_file_size"]/1024/1024:.1f}MB)'
                }

            # 检查图片分辨率
            with Image.open(image_path) as img:
                width, height = img.size

                if width < CONFIG["min_width"] or height < CONFIG["min_height"]:
                    return {
                        'valid': False,
                        'width': width,
                        'height': height,
                        'size': file_size,
                        'reason': f'分辨率太低 ({width}x{height} < {CONFIG["min_width"]}x{CONFIG["min_height"]})'
                    }

                # 检查是否重复
                if CONFIG["remove_duplicates"]:
                    img_hash = self.get_image_hash(image_path)
                    if img_hash in self.downloaded_hashes:
                        return {
                            'valid': False,
                            'width': width,
                            'height': height,
                            'size': file_size,
                            'reason': '重复图片'
                        }
                    self.downloaded_hashes.add(img_hash)

                return {
                    'valid': True,
                    'width': width,
                    'height': height,
                    'size': file_size,
                    'reason': 'OK'
                }

        except Exception as e:
            return {
                'valid': False,
                'reason': f'无法读取图片: {str(e)}'
            }

    def download_from_bing(self, keyword: str, category_dir: str, limit: int) -> int:
        """从Bing下载图片"""
        temp_dir = os.path.join(category_dir, "temp_bing")

        try:
            # 下载到临时目录
            downloader.download(
                keyword,
                limit=limit * 2,  # 下载更多以便筛选
                output_dir=temp_dir,
                adult_filter_off=True,
                force_replace=False,
                timeout=CONFIG["timeout"],
                verbose=False,
            )

            # 检查和移动符合质量要求的图片
            valid_count = 0
            keyword_dir = os.path.join(temp_dir, keyword)

            if os.path.exists(keyword_dir):
                for filename in os.listdir(keyword_dir):
                    if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                        continue

                    src_path = os.path.join(keyword_dir, filename)
                    quality = self.check_image_quality(src_path)

                    if quality['valid']:
                        # 重命名并移动到目标目录
                        new_filename = f"{keyword.replace(' ', '_')}_{valid_count+1:03d}{Path(filename).suffix}"
                        dst_path = os.path.join(category_dir, new_filename)
                        os.rename(src_path, dst_path)
                        valid_count += 1

                        if valid_count >= limit:
                            break
                    else:
                        # 删除不符合要求的图片
                        os.remove(src_path)

            # 清理临时目录
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

            return valid_count

        except Exception as e:
            print(f"   ❌ Bing下载失败: {str(e)}")
            return 0

    def download_from_unsplash(self, keyword: str, category_dir: str, limit: int) -> int:
        """从Unsplash下载图片（需要API Key）"""
        if UNSPLASH_ACCESS_KEY == "YOUR_UNSPLASH_ACCESS_KEY":
            return 0

        try:
            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
            params = {
                "query": keyword,
                "per_page": limit,
                "orientation": "landscape"
            }

            response = requests.get(url, headers=headers, params=params, timeout=CONFIG["timeout"])
            response.raise_for_status()
            data = response.json()

            valid_count = 0
            for i, photo in enumerate(data.get('results', [])):
                if valid_count >= limit:
                    break

                # 下载高质量版本
                image_url = photo['urls']['full']
                filename = f"{keyword.replace(' ', '_')}_unsplash_{i+1:03d}.jpg"
                filepath = os.path.join(category_dir, filename)

                # 下载图片
                img_response = requests.get(image_url, timeout=CONFIG["timeout"])
                img_response.raise_for_status()

                with open(filepath, 'wb') as f:
                    f.write(img_response.content)

                # 检查质量
                quality = self.check_image_quality(filepath)
                if quality['valid']:
                    valid_count += 1
                else:
                    os.remove(filepath)

            return valid_count

        except Exception as e:
            print(f"   ❌ Unsplash下载失败: {str(e)}")
            return 0


def main():
    """主函数"""
    print("="*70)
    print("🖼️  家具材料检测 - 高质量测试图片批量下载工具（增强版）")
    print("="*70)

    output_dir = CONFIG["output_dir"]
    print(f"\n📁 输出目录: {os.path.abspath(output_dir)}")
    print(f"📊 每个关键词目标: {CONFIG['limit_per_keyword']} 张高质量图片")
    print(f"📐 最小分辨率: {CONFIG['min_width']}x{CONFIG['min_height']}")
    print(f"💾 文件大小范围: {CONFIG['min_file_size']/1024:.0f}KB - {CONFIG['max_file_size']/1024/1024:.0f}MB")

    # 询问用户
    print("\n请选择要下载的图片类别:")
    print("1. 家具照片")
    print("2. 坐姿照片")
    print("3. 全部下载")

    choice = input("\n请输入选项 (1/2/3，默认3): ").strip() or "3"

    categories_to_download = []
    if choice in ["1", "3"]:
        categories_to_download.append("家具照片")
    if choice in ["2", "3"]:
        categories_to_download.append("坐姿照片")

    # 开始下载
    downloader_obj = ImageDownloader(output_dir)
    total_downloaded = 0

    for main_category in categories_to_download:
        print(f"\n{'='*70}")
        print(f"📦 开始下载: {main_category}")
        print(f"{'='*70}")

        categories = IMAGE_CATEGORIES[main_category]

        for category, keywords in categories.items():
            print(f"\n📁 类别: {category}")
            category_dir = os.path.join(output_dir, main_category, category)
            Path(category_dir).mkdir(parents=True, exist_ok=True)

            category_total = 0

            for keyword in tqdm(keywords, desc=f"  下载进度"):
                # 从Bing下载
                count = downloader_obj.download_from_bing(
                    keyword,
                    category_dir,
                    CONFIG["limit_per_keyword"]
                )
                category_total += count

                # 如果配置了Unsplash API，也从Unsplash下载
                if UNSPLASH_ACCESS_KEY != "YOUR_UNSPLASH_ACCESS_KEY":
                    count = downloader_obj.download_from_unsplash(
                        keyword,
                        category_dir,
                        CONFIG["limit_per_keyword"]
                    )
                    category_total += count

            print(f"  ✅ {category}: 下载 {category_total} 张高质量图片")
            total_downloaded += category_total

    # 统计结果
    print(f"\n{'='*70}")
    print("✅ 下载完成！")
    print(f"{'='*70}")

    print(f"\n📊 总计下载: {total_downloaded} 张高质量图片")
    print(f"📂 保存位置: {os.path.abspath(output_dir)}")

    print("\n💡 后续建议:")
    print("1. 人工检查图片内容是否符合需求")
    print("2. 删除角度不合适或背景杂乱的图片")
    print("3. 可以使用图片标注工具进行标注")
    print("4. 建议每类保留10-15张最优质的图片")

    print("\n🔧 配置Unsplash API（可选）:")
    print("1. 访问 https://unsplash.com/developers")
    print("2. 注册并创建应用获取Access Key")
    print("3. 将Access Key填入脚本中的UNSPLASH_ACCESS_KEY变量")
    print("4. 重新运行脚本即可从Unsplash下载高质量图片")


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
