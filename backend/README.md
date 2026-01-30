# 家具健康检测器 - 后端 API

基于 FastAPI 的家具材料健康检测后端服务。

## 功能特性

- 🔍 家具材料识别（基于 Qwen3-VL-30B）
- 📊 材料健康风险评估
- 🎨 分享卡片生成
- 🧘 坐姿分析（v2.0 规划中）

## 核心功能

### 1. 家具材料检测
- 上传家具图片
- AI 自动识别材料类型（实木类、人造板类、皮革类、布类）
- 评估材料置信度（0-100）
- 提取视觉特征（纹理、颜色、图案）

### 2. 健康风险评估
- 查询材料知识库
- 评估风险等级（低风险、中风险、高风险）
- 识别有害物质（甲醛、脲醛树脂等）
- 提供健康建议

### 3. 分享卡片生成
- AI 生成金句
- 三种模板风格（modern、classic、minimal）
- 自动生成小程序二维码
- 7天自动过期

## 快速开始

### 1. 安装依赖

**Linux/Mac:**
```bash
cd backend
./setup.sh
```

**Windows:**
```cmd
cd backend
setup.bat
```

**手动安装:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip3 install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

**必需配置:**
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://www.aiping.cn/api/v1
QWEN_MODEL_NAME=Qwen3-VL-30B-A3B-Instruct
OSS_ACCESS_KEY_ID=your_oss_access_key_id
OSS_ACCESS_KEY_SECRET=your_oss_access_key_secret
```

### 3. 运行开发服务器

```bash
python3 main.py
```

访问 API 文档：http://localhost:8000/api/v1/docs

### 4. 测试 API

```bash
python3 test_api.py
```

## 项目结构

```
backend/
├── app/
│   ├── api/v1/          # API 路由
│   │   ├── furniture.py # 家具检测 API
│   │   └── share.py     # 分享卡片 API
│   ├── core/            # 核心配置
│   │   ├── config.py    # 配置管理
│   │   └── middleware.py # 中间件
│   ├── data/            # 数据文件
│   │   └── knowledge_base.json # 材料知识库
│   ├── models/          # 数据模型
│   │   └── schemas.py   # Pydantic 模型
│   ├── services/        # 业务服务
│   │   ├── knowledge_base.py  # 知识库服务
│   │   ├── qwen_vl.py         # Qwen-VL 服务
│   │   └── image_service.py   # 图片处理服务
│   └── utils/           # 工具函数
├── tests/               # 测试
├── main.py              # 应用入口
├── requirements.txt     # 依赖列表
├── .env.example         # 环境变量示例
├── setup.sh / setup.bat # 快速启动脚本
├── test_api.py          # API 测试脚本
├── README.md            # 项目说明
├── PROGRESS.md          # 开发进度报告
└── SUMMARY.md           # 完成总结
```

## API 端点

### 核心端点

- `GET /` - 根路径
- `GET /api/v1/health` - 健康检查
- `POST /api/v1/furniture/detect` - 家具检测
- `POST /api/v1/share/generate` - 生成分享卡片

### 详细文档

访问 http://localhost:8000/api/v1/docs 查看完整的 Swagger UI 文档。

## 使用示例

### 家具检测

```python
import requests

with open('furniture.jpg', 'rb') as f:
    files = {'image': f}
    data = {'disclaimer_accepted': 'true'}
    response = requests.post(
        'http://localhost:8000/api/v1/furniture/detect',
        files=files,
        data=data
    )
    result = response.json()
    print(result)
```

### 生成分享卡片

```python
import requests

data = {
    'report_id': 'your-report-id',
    'template_style': 'modern'
}
response = requests.post(
    'http://localhost:8000/api/v1/share/generate',
    json=data
)
card = response.json()
print(card)
```

## 技术栈

- **框架**: FastAPI 0.109.0
- **数据验证**: Pydantic 2.5.3
- **AI 服务**: Qwen3-VL-30B (通过 OpenAI SDK)
- **图片处理**: Pillow 10.2.0
- **云存储**: 阿里云 OSS
- **日志**: Loguru 0.7.2

## 开发进度

- [x] 项目初始化和基础架构
- [x] 数据模型定义
- [x] 材料知识库实现
- [x] Qwen-VL API 集成
- [x] 图片处理服务
- [x] 家具检测 API 端点
- [x] 分享卡片生成功能
- [x] 健康检查和监控

**MVP v1.0 核心功能已全部完成！** ✅

详细进度请查看 [PROGRESS.md](PROGRESS.md)。

## 注意事项

### API Key 配置
- 需要在 `.env` 文件中配置 `OPENAI_API_KEY`（用于 Qwen3-VL API）
- 需要配置阿里云 OSS 的 Access Key 和 Secret Key

### 成本控制
- Qwen3-VL API 调用有成本，开发阶段注意控制调用次数
- OSS 存储设置 7 天自动过期

### 安全
- 不要将 API Key 提交到代码仓库
- 使用环境变量管理敏感配置
- 建议添加请求速率限制（防止滥用）

## 故障排除

### 1. 无法连接到服务器
```bash
# 检查服务是否启动
python3 main.py
```

### 2. API Key 错误
```bash
# 检查 .env 文件中的配置
cat .env
```

### 3. 依赖安装失败
```bash
# 升级 pip
pip3 install --upgrade pip
# 重新安装依赖
pip3 install -r requirements.txt
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请查看：
- [PROGRESS.md](PROGRESS.md) - 详细开发进度
- [SUMMARY.md](SUMMARY.md) - 完成总结
- API 文档: http://localhost:8000/api/v1/docs
