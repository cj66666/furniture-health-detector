"""图片处理服务"""
import io
import os
from typing import Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from PIL import Image
import qrcode
import oss2
from app.core.config import get_settings


class ImageService:
    """图片处理服务类"""

    def __init__(self):
        """初始化图片服务"""
        self.settings = get_settings()

        # 初始化 OSS 客户端
        auth = oss2.Auth(
            self.settings.OSS_ACCESS_KEY_ID,
            self.settings.OSS_ACCESS_KEY_SECRET
        )
        self.bucket = oss2.Bucket(
            auth,
            self.settings.OSS_ENDPOINT,
            self.settings.OSS_BUCKET_NAME
        )

        logger.info("图片服务初始化完成")

    async def upload_to_oss(
        self,
        file_data: bytes,
        file_name: str,
        content_type: str = "image/jpeg",
        expire_days: Optional[int] = None
    ) -> str:
        """上传图片到阿里云 OSS

        Args:
            file_data: 图片二进制数据
            file_name: 文件名
            content_type: 内容类型
            expire_days: 过期天数，默认使用配置中的值

        Returns:
            图片 URL
        """
        try:
            # 生成唯一的文件路径
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_name = f"furniture/{timestamp}_{file_name}"

            # 设置过期时间
            if expire_days is None:
                expire_days = self.settings.OSS_IMAGE_EXPIRE_DAYS

            # 上传文件
            result = self.bucket.put_object(
                object_name,
                file_data,
                headers={
                    'Content-Type': content_type
                }
            )

            if result.status == 200:
                # 生成带签名的访问 URL (有效期为配置的过期天数)
                expire_seconds = expire_days * 24 * 3600
                url = self.bucket.sign_url('GET', object_name, expire_seconds)
                logger.info(f"图片上传成功: {object_name}")

                # 设置生命周期规则（7天后自动删除）
                self._set_lifecycle_rule(expire_days)

                return url
            else:
                raise Exception(f"上传失败，状态码: {result.status}")

        except Exception as e:
            logger.error(f"图片上传到 OSS 失败: {e}")
            raise

    def _set_lifecycle_rule(self, expire_days: int) -> None:
        """设置 OSS 生命周期规则

        Args:
            expire_days: 过期天数
        """
        try:
            # 检查是否已存在规则
            lifecycle = self.bucket.get_bucket_lifecycle()
            rule_exists = any(
                rule.id == 'auto-delete-furniture-images'
                for rule in lifecycle.rules
            )

            if not rule_exists:
                # 创建生命周期规则
                rule = oss2.models.LifecycleRule(
                    'auto-delete-furniture-images',
                    'furniture/',
                    status=oss2.models.LifecycleRule.ENABLED,
                    expiration=oss2.models.LifecycleExpiration(days=expire_days)
                )
                lifecycle = oss2.models.BucketLifecycle([rule])
                self.bucket.put_bucket_lifecycle(lifecycle)
                logger.info(f"已设置 OSS 生命周期规则: {expire_days} 天后自动删除")
        except oss2.exceptions.NoSuchLifecycle:
            # 如果没有生命周期规则，创建新的
            rule = oss2.models.LifecycleRule(
                'auto-delete-furniture-images',
                'furniture/',
                status=oss2.models.LifecycleRule.ENABLED,
                expiration=oss2.models.LifecycleExpiration(days=expire_days)
            )
            lifecycle = oss2.models.BucketLifecycle([rule])
            self.bucket.put_bucket_lifecycle(lifecycle)
            logger.info(f"已创建 OSS 生命周期规则: {expire_days} 天后自动删除")
        except Exception as e:
            logger.warning(f"设置生命周期规则失败: {e}")

    def compress_image(
        self,
        image_data: bytes,
        quality: Optional[int] = None,
        max_size: Optional[Tuple[int, int]] = None
    ) -> bytes:
        """压缩图片

        Args:
            image_data: 原始图片数据
            quality: 压缩质量 (1-100)，默认使用配置中的值
            max_size: 最大尺寸 (width, height)，如果提供则会等比例缩放

        Returns:
            压缩后的图片数据
        """
        try:
            if quality is None:
                quality = self.settings.IMAGE_QUALITY

            # 打开图片
            img = Image.open(io.BytesIO(image_data))

            # 转换为 RGB 模式（如果是 RGBA 或其他模式）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 如果指定了最大尺寸，进行等比例缩放
            if max_size:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

            # 压缩图片
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_data = output.getvalue()

            # 计算压缩率
            original_size = len(image_data)
            compressed_size = len(compressed_data)
            compression_ratio = (1 - compressed_size / original_size) * 100

            logger.info(
                f"图片压缩完成: {original_size / 1024:.2f}KB -> "
                f"{compressed_size / 1024:.2f}KB (压缩率: {compression_ratio:.1f}%)"
            )

            return compressed_data

        except Exception as e:
            logger.error(f"图片压缩失败: {e}")
            raise

    def generate_qr_code(
        self,
        data: str,
        size: int = 300,
        border: int = 2
    ) -> bytes:
        """生成二维码

        Args:
            data: 二维码数据（通常是小程序路径）
            size: 二维码尺寸（像素）
            border: 边框宽度

        Returns:
            二维码图片数据
        """
        try:
            # 创建二维码
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # 生成图片
            img = qr.make_image(fill_color="black", back_color="white")

            # 调整尺寸
            img = img.resize((size, size), Image.Resampling.LANCZOS)

            # 转换为字节
            output = io.BytesIO()
            img.save(output, format='PNG')
            qr_data = output.getvalue()

            logger.info(f"二维码生成成功，尺寸: {size}x{size}")

            return qr_data

        except Exception as e:
            logger.error(f"二维码生成失败: {e}")
            raise

    async def upload_image_file(
        self,
        file_path: str,
        compress: bool = True
    ) -> str:
        """上传本地图片文件到 OSS

        Args:
            file_path: 本地文件路径
            compress: 是否压缩

        Returns:
            图片 URL
        """
        try:
            # 读取文件
            with open(file_path, 'rb') as f:
                image_data = f.read()

            # 压缩图片
            if compress:
                image_data = self.compress_image(image_data)

            # 获取文件名
            file_name = Path(file_path).name

            # 上传到 OSS
            url = await self.upload_to_oss(image_data, file_name)

            return url

        except Exception as e:
            logger.error(f"上传图片文件失败: {e}")
            raise

    async def generate_and_upload_qr_code(
        self,
        miniprogram_path: str,
        size: int = 300
    ) -> str:
        """生成二维码并上传到 OSS

        Args:
            miniprogram_path: 小程序路径
            size: 二维码尺寸

        Returns:
            二维码图片 URL
        """
        try:
            # 生成二维码
            qr_data = self.generate_qr_code(miniprogram_path, size)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"qrcode_{timestamp}.png"

            # 上传到 OSS
            url = await self.upload_to_oss(
                qr_data,
                file_name,
                content_type="image/png"
            )

            return url

        except Exception as e:
            logger.error(f"生成并上传二维码失败: {e}")
            raise
