"""Qwen-VL API 集成服务 (通过 OpenAI SDK)"""
import asyncio
from typing import Dict, Optional
from loguru import logger
from openai import OpenAI
from app.core.config import get_settings


class QwenVLService:
    """Qwen-VL 视觉语言模型服务类"""

    def __init__(self):
        """初始化 Qwen-VL 服务"""
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.OPENAI_API_KEY,
            base_url=self.settings.OPENAI_BASE_URL
        )
        self.model = self.settings.QWEN_MODEL_NAME
        self.max_retries = self.settings.QWEN_VL_MAX_RETRIES
        self.retry_delay = self.settings.QWEN_VL_RETRY_DELAY
        self.timeout = self.settings.QWEN_VL_TIMEOUT

    def _build_system_prompt(self) -> str:
        """构建结构化的思维链 System Prompt"""
        return """你是一个专业的家具材料识别专家。请按照以下步骤分析图片中的家具材料：

1. **观察阶段**：仔细观察图片中的家具，识别其类型（如椅子、沙发、桌子等）

2. **材料识别**：
   - 观察表面纹理、颜色、光泽度
   - 识别材料类型：实木类、人造板类、皮革类、布类
   - 确定具体子类型（如实木拼板、密度板、刨花板、真皮、布艺等）
   - 评估识别置信度（0-100）

3. **视觉特征提取**：
   - 纹理描述（如"自然木纹"、"表面平整光滑"、"有编织纹理"）
   - 颜色描述（如"木材原色"、"深棕色"、"米白色"）
   - 图案描述（如"天然纹路"、"无明显纹理"、"编织图案"）

4. **输出格式**：
请以 JSON 格式输出结果：
{
  "furniture_type": "家具类型",
  "materials": [
    {
      "material_type": "材料大类（实木类/人造板类/皮革类/布类）",
      "sub_type": "具体子类型",
      "confidence": 85,
      "visual_cues": {
        "texture": "纹理描述",
        "color": "颜色描述",
        "pattern": "图案描述"
      }
    }
  ]
}

注意：
- 置信度必须在 0-100 之间
- 材料类型必须是四大类之一
- 如果无法识别，请说明原因"""

    async def analyze_furniture(
        self,
        image_url: str,
        additional_context: Optional[str] = None
    ) -> Dict:
        """分析家具图片

        Args:
            image_url: 图片 URL
            additional_context: 额外的上下文信息

        Returns:
            分析结果字典

        Raises:
            Exception: API 调用失败
        """
        messages = [
            {
                "role": "system",
                "content": self._build_system_prompt()
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    },
                    {
                        "type": "text",
                        "text": additional_context or "请分析这张家具图片的材料"
                    }
                ]
            }
        ]

        # 实现重试机制
        for attempt in range(self.max_retries):
            try:
                logger.info(f"调用 Qwen-VL API (尝试 {attempt + 1}/{self.max_retries})")

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    stream=False,
                    temperature=0.7,
                    max_tokens=2000
                )

                if response.choices and len(response.choices) > 0:
                    result = response.choices[0].message.content
                    logger.info("Qwen-VL API 调用成功")
                    return self._parse_response(result)
                else:
                    logger.error("API 返回空响应")

            except Exception as e:
                logger.error(f"API 调用异常 (尝试 {attempt + 1}): {e}")

                if attempt < self.max_retries - 1:
                    # 指数退避
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    await asyncio.sleep(wait_time)
                else:
                    raise Exception(f"Qwen-VL API 调用失败，已重试 {self.max_retries} 次")

        raise Exception("Qwen-VL API 调用失败")

    def _parse_response(self, response_text: str) -> Dict:
        """解析 API 响应

        Args:
            response_text: API 返回的文本

        Returns:
            解析后的字典
        """
        import json
        import re

        try:
            # 尝试提取 JSON 部分
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                logger.warning("响应中未找到 JSON 格式，返回原始文本")
                return {"raw_response": response_text}
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            return {"raw_response": response_text, "parse_error": str(e)}

    def validate_image_quality(
        self,
        image_path: str,
        min_resolution: int = 800
    ) -> tuple[bool, Optional[str]]:
        """验证图片质量

        Args:
            image_path: 图片路径
            min_resolution: 最小分辨率要求

        Returns:
            (是否通过验证, 错误信息)
        """
        try:
            from PIL import Image

            with Image.open(image_path) as img:
                width, height = img.size

                # 检查分辨率
                if width < min_resolution or height < min_resolution:
                    return False, f"图片分辨率过低，至少需要 {min_resolution}x{min_resolution}"

                # 检查图片格式
                if img.format not in ['JPEG', 'PNG', 'JPG']:
                    return False, f"不支持的图片格式: {img.format}，请使用 JPEG 或 PNG"

                # 检查图片大小
                file_size_mb = len(img.tobytes()) / (1024 * 1024)
                max_size = self.settings.MAX_IMAGE_SIZE_MB
                if file_size_mb > max_size:
                    return False, f"图片文件过大，最大支持 {max_size}MB"

                return True, None

        except Exception as e:
            logger.error(f"图片质量验证失败: {e}")
            return False, f"图片验证失败: {str(e)}"

    async def generate_catchphrase(
        self,
        material_info: Dict,
        risk_level: str
    ) -> str:
        """生成分享卡片金句

        Args:
            material_info: 材料信息
            risk_level: 风险等级

        Returns:
            生成的金句
        """
        prompt = f"""基于以下家具材料信息，生成一句简短、有趣、易记的金句（不超过20字）：

材料类型：{material_info.get('material_type')}
子类型：{material_info.get('sub_type')}
风险等级：{risk_level}

要求：
1. 简洁有力，朗朗上口
2. 突出材料特点或健康提示
3. 适合社交分享
4. 不超过20字

只返回金句本身，不要其他内容。"""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
                temperature=0.9,
                max_tokens=100
            )

            if response.choices and len(response.choices) > 0:
                catchphrase = response.choices[0].message.content
                return catchphrase.strip()
            else:
                logger.error("金句生成失败: 空响应")
                return "健康家居，从材料开始"

        except Exception as e:
            logger.error(f"金句生成异常: {e}")
            return "健康家居，从材料开始"

