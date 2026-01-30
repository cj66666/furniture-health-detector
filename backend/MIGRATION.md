# 迁移指南：从 DashScope SDK 到 OpenAI SDK

## 概述

本项目已从阿里云 DashScope SDK 迁移到 OpenAI SDK，以使用 aiping.cn 提供的 Qwen3-VL-30B 模型。

## 主要变更

### 1. 依赖变更

**之前 (requirements.txt):**
```
dashscope==1.14.1
```

**现在 (requirements.txt):**
```
openai==1.12.0
```

### 2. 环境变量变更

**之前 (.env):**
```env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

**现在 (.env):**
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://www.aiping.cn/api/v1
QWEN_MODEL_NAME=Qwen3-VL-30B-A3B-Instruct
```

### 3. 配置类变更

**之前 (app/core/config.py):**
```python
# 阿里云 DashScope (Qwen-VL)
DASHSCOPE_API_KEY: str
```

**现在 (app/core/config.py):**
```python
# Qwen-VL API (通过 OpenAI SDK)
OPENAI_API_KEY: str
OPENAI_BASE_URL: str = "https://www.aiping.cn/api/v1"
QWEN_MODEL_NAME: str = "Qwen3-VL-30B-A3B-Instruct"
```

### 4. QwenVLService 实现变更

**之前 (app/services/qwen_vl.py):**
```python
import dashscope
from dashscope import MultiModalConversation

class QwenVLService:
    def __init__(self):
        self.settings = get_settings()
        dashscope.api_key = self.settings.DASHSCOPE_API_KEY

    async def analyze_furniture(self, image_url: str, additional_context: Optional[str] = None) -> Dict:
        messages = [
            {'role': 'system', 'content': [{'text': self._build_system_prompt()}]},
            {'role': 'user', 'content': [{'image': image_url}, {'text': additional_context or '请分析这张家具图片的材料'}]}
        ]

        response = MultiModalConversation.call(
            model='qwen-vl-plus',
            messages=messages
        )
```

**现在 (app/services/qwen_vl.py):**
```python
from openai import OpenAI

class QwenVLService:
    def __init__(self):
        self.settings = get_settings()
        self.client = OpenAI(
            api_key=self.settings.OPENAI_API_KEY,
            base_url=self.settings.OPENAI_BASE_URL
        )
        self.model = self.settings.QWEN_MODEL_NAME

    async def analyze_furniture(self, image_url: str, additional_context: Optional[str] = None) -> Dict:
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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
            temperature=0.7,
            max_tokens=2000
        )
```

## 迁移步骤

### 步骤 1: 更新依赖

```bash
cd backend
pip3 uninstall dashscope
pip3 install openai==1.12.0
```

或者直接重新安装所有依赖：

```bash
pip3 install -r requirements.txt
```

### 步骤 2: 更新环境变量

1. 编辑 `.env` 文件
2. 删除或注释掉 `DASHSCOPE_API_KEY`
3. 添加新的配置：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://www.aiping.cn/api/v1
QWEN_MODEL_NAME=Qwen3-VL-30B-A3B-Instruct
```

### 步骤 3: 获取 API Key

1. 访问 [aiping.cn](https://www.aiping.cn)
2. 注册账号并获取 API Key
3. 将 API Key 填入 `.env` 文件的 `OPENAI_API_KEY` 字段

### 步骤 4: 测试服务

```bash
# 启动服务器
python3 main.py

# 在另一个终端测试健康检查
curl http://localhost:8000/api/v1/health
```

预期输出：
```json
{
  "status": "healthy",
  "services": {
    "api": "ok",
    "knowledge_base": "ok",
    "qwen_vl": "ok",
    "oss": "ok"
  }
}
```

### 步骤 5: 测试家具检测 API

```bash
python3 test_api.py
```

或使用 Swagger UI 测试：http://localhost:8000/api/v1/docs

## 功能对比

| 功能 | DashScope SDK | OpenAI SDK |
|------|---------------|------------|
| 模型 | qwen-vl-plus | Qwen3-VL-30B-A3B-Instruct |
| API 提供商 | 阿里云 DashScope | aiping.cn |
| 图片输入格式 | `{'image': url}` | `{'type': 'image_url', 'image_url': {'url': url}}` |
| 响应格式 | `response.output.choices[0].message.content[0]['text']` | `response.choices[0].message.content` |
| 流式响应 | 支持 | 支持 |
| 重试机制 | ✅ 保留 | ✅ 保留 |
| 错误处理 | ✅ 保留 | ✅ 保留 |

## 优势

### 使用 OpenAI SDK 的优势：

1. **标准化接口**: OpenAI SDK 是业界标准，更容易集成和维护
2. **更好的文档**: OpenAI SDK 有完善的文档和社区支持
3. **灵活性**: 可以轻松切换到其他兼容 OpenAI API 的服务
4. **更强大的模型**: Qwen3-VL-30B 比 qwen-vl-plus 更强大

### 保留的功能：

- ✅ 重试机制（指数退避）
- ✅ 图片质量验证
- ✅ 错误处理和日志记录
- ✅ 金句生成功能
- ✅ 所有业务逻辑保持不变

## 常见问题

### Q1: 为什么要迁移？

A: 为了使用更强大的 Qwen3-VL-30B 模型，并通过 aiping.cn 提供的服务获得更好的性能和稳定性。

### Q2: 旧的 API Key 还能用吗？

A: 不能。需要从 aiping.cn 获取新的 API Key。

### Q3: 迁移后性能有变化吗？

A: Qwen3-VL-30B 模型更强大，识别准确度更高，但响应时间可能略有增加。

### Q4: 如何回退到旧版本？

A: 如果需要回退，可以：
1. 恢复 `requirements.txt` 中的 `dashscope==1.14.1`
2. 恢复旧的 `qwen_vl.py` 文件
3. 恢复 `.env` 中的 `DASHSCOPE_API_KEY`

### Q5: 是否影响前端？

A: 不影响。API 接口保持不变，前端无需修改。

## 技术支持

如有问题，请：
1. 查看 [README.md](README.md)
2. 查看 API 文档: http://localhost:8000/api/v1/docs
3. 提交 Issue

## 更新日志

- **2026-01-30**: 完成从 DashScope SDK 到 OpenAI SDK 的迁移
  - 更新依赖：dashscope → openai
  - 更新配置：DASHSCOPE_API_KEY → OPENAI_API_KEY
  - 更新模型：qwen-vl-plus → Qwen3-VL-30B-A3B-Instruct
  - 保留所有核心功能和业务逻辑
