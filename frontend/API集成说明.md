# 家居健康小助手 - 前端 API 集成说明

## 项目定位
全方位家居健康管理小程序，涵盖家具材料、食物营养、衣物材质、房屋建材四大健康检测模块。

## 集成完成时间
2026-01-30

## 已完成的集成工作 (Phase 1: 家具模块)

### 1. 创建 API 工具类
**文件：** `frontend/utils/api.js`

**功能：**
- 封装所有后端 API 调用
- 统一错误处理
- 图片大小验证
- 请求超时控制

**导出方法：**
- `detectFurniture(imagePath, disclaimerAccepted)` - 家具检测
- `generateShareCard(reportData)` - 生成分享卡片
- `healthCheck()` - 健康检查
- `handleError(error)` - 错误处理

### 2. 更新家具检测页面
**文件：** `frontend/pages/furniture-detect/detect.js`

**新增功能：**
- ✅ 调用后端 `/api/v1/furniture/detect` 接口
- ✅ 上传图片到后端
- ✅ 接收并展示检测结果
- ✅ 错误处理和用户提示
- ✅ 防止重复提交
- ✅ 查看详细报告
- ✅ 生成分享卡片
- ✅ 重新检测

**数据结构：**
```javascript
{
  hasResult: false,          // 是否有检测结果
  imagePath: '',             // 图片路径
  detectionResult: null,     // 检测结果对象
  isAnalyzing: false         // 是否正在分析
}
```

### 3. 更新分享卡片页面
**文件：** `frontend/pages/share-card/share.js`

**新增功能：**
- ✅ 调用后端 `/api/v1/share/generate` 接口
- ✅ 生成分享卡片
- ✅ 选择模板（modern/classic/minimal）
- ✅ 保存卡片到相册
- ✅ 分享到微信好友/朋友圈
- ✅ 重新生成卡片

**数据结构：**
```javascript
{
  reportId: '',              // 报告ID
  reportData: null,          // 报告数据
  shareCardUrl: '',          // 分享卡片URL
  isGenerating: false,       // 是否正在生成
  selectedTemplate: 'modern' // 选中的模板
}
```

## API 配置

### 开发环境配置
在 `frontend/utils/api.js` 中修改 `BASE_URL`：

```javascript
const CONFIG = {
  BASE_URL: 'http://localhost:8000/api/v1',  // 本地开发
  TIMEOUT: 30000,
  MAX_IMAGE_SIZE: 10
};
```

### 生产环境配置
部署时需要修改为实际的服务器地址：

```javascript
const CONFIG = {
  BASE_URL: 'https://your-domain.com/api/v1',  // 生产环境
  TIMEOUT: 30000,
  MAX_IMAGE_SIZE: 10
};
```

## 测试步骤

### 本地测试
1. **启动后端服务**
   ```bash
   cd backend
   python3 main.py
   ```
   后端将在 `http://localhost:8000` 运行

2. **配置微信开发者工具**
   - 打开微信开发者工具
   - 导入前端项目（frontend 目录）
   - 点击右上角"详情"
   - 勾选"不校验合法域名、web-view（业务域名）、TLS 版本以及 HTTPS 证书"

3. **测试家具检测功能**
   - 进入"家具检测"页面
   - 点击"拍照识别"或"从相册选择"
   - 选择一张家具图片
   - 等待识别结果
   - 查看检测报告

4. **测试分享卡片功能**
   - 在检测结果页面点击"生成分享卡片"
   - 选择模板样式
   - 等待卡片生成
   - 测试保存到相册功能

### 生产环境测试
1. **部署后端到服务器**
   - 配置 HTTPS（微信小程序要求）
   - 配置域名
   - 启动后端服务

2. **配置小程序服务器域名**
   - 登录微信公众平台
   - 进入"开发" → "开发管理" → "开发设置"
   - 在"服务器域名"中添加：
     - request 合法域名：`https://your-domain.com`
     - uploadFile 合法域名：`https://your-domain.com`
     - downloadFile 合法域名：`https://your-domain.com`（用于下载分享卡片）

3. **更新前端配置**
   - 修改 `frontend/utils/api.js` 中的 `BASE_URL`
   - 上传代码到微信小程序后台
   - 提交审核

## API 接口说明

### 1. 家具检测接口
**端点：** `POST /api/v1/furniture/detect`

**请求参数：**
- `image`: 图片文件（multipart/form-data）
- `disclaimer_accepted`: 是否接受免责声明（boolean）

**响应示例：**
```json
{
  "report_id": "uuid",
  "furniture_type": "沙发",
  "materials": [
    {
      "material_type": "实木类",
      "sub_type": "橡木",
      "confidence": 85,
      "risk_assessment": {
        "risk_level": "低风险",
        "harmful_substances": [],
        "health_advice": "..."
      }
    }
  ]
}
```

### 2. 生成分享卡片接口
**端点：** `POST /api/v1/share/generate`

**请求参数：**
```json
{
  "report_id": "uuid",
  "furniture_type": "沙发",
  "materials": [...],
  "template": "modern"
}
```

**响应示例：**
```json
{
  "card_url": "https://oss.../share_card.jpg",
  "qr_code_url": "https://oss.../qr_code.jpg",
  "expires_at": "2026-02-06T00:00:00Z"
}
```

## 错误处理

### 常见错误及处理

1. **网络连接失败**
   - 错误码：-1
   - 提示：网络连接失败，请检查网络
   - 处理：检查网络连接，重试

2. **图片大小超限**
   - 错误码：-2
   - 提示：图片大小超过限制（10MB）
   - 处理：压缩图片或选择其他图片

3. **请求参数错误**
   - 错误码：400
   - 提示：请求参数错误
   - 处理：检查请求参数格式

4. **服务器错误**
   - 错误码：500
   - 提示：服务器错误
   - 处理：稍后重试或联系管理员

## 注意事项

### 1. 图片上传
- 最大图片大小：10MB
- 支持格式：JPG、PNG
- 建议分辨率：800px 以上

### 2. 请求超时
- 默认超时时间：30秒
- 图片上传可能需要较长时间，请耐心等待

### 3. 微信小程序限制
- 必须使用 HTTPS
- 需要配置服务器域名白名单
- 本地调试需要关闭域名校验

### 4. 用户体验
- 添加了加载提示（wx.showLoading）
- 添加了错误提示（wx.showModal）
- 防止重复提交（isAnalyzing 标志）
- 提供重试机制

## 规划中的模块 (Phase 2-4)

### Phase 2: 食物健康分析模块
**预计时间**: 4周

#### 待开发功能
- [ ] 食物识别与营养分析页面
- [ ] 食物相克检测页面
- [ ] 每日摄入量追踪页面
- [ ] 营养报告可视化
- [ ] 个性化饮食建议

#### API 端点
- `POST /api/v1/food/analyze` - 食物识别与营养分析
- `POST /api/v1/food/check-conflict` - 食物相克检测
- `POST /api/v1/food/track-intake` - 记录每日摄入
- `GET /api/v1/food/daily-report` - 每日营养报告

#### 页面设计
```
pages/food-analyze/        # 食物分析
├── analyze.wxml
├── analyze.wxss
├── analyze.js
└── analyze.json

pages/food-conflict/       # 食物相克检测
├── conflict.wxml
├── conflict.wxss
├── conflict.js
└── conflict.json

pages/food-tracking/       # 摄入量追踪
├── tracking.wxml
├── tracking.wxss
├── tracking.js
└── tracking.json
```

### Phase 3: 衣物材质检测模块
**预计时间**: 3周

#### 待开发功能
- [ ] 衣物材质识别页面
- [ ] 过敏原检测结果展示
- [ ] 舒适度评估展示
- [ ] 护理建议页面

#### API 端点
- `POST /api/v1/clothing/detect` - 衣物材质检测

#### 页面设计
```
pages/clothing-detect/     # 衣物检测
├── detect.wxml
├── detect.wxss
├── detect.js
└── detect.json
```

### Phase 4: 房屋建材安全模块
**预计时间**: 3周

#### 待开发功能
- [ ] 建材识别页面
- [ ] 有害物质检测结果展示
- [ ] 安全风险评估展示
- [ ] 改善建议页面

#### API 端点
- `POST /api/v1/building/detect` - 建材安全检测

#### 页面设计
```
pages/building-detect/     # 建材检测
├── detect.wxml
├── detect.wxss
├── detect.js
└── detect.json
```

## 通用功能开发计划

### 短期任务 (2周)
- [ ] 完善 UI 展示（显示检测结果的详细信息）
- [ ] 添加加载进度提示
- [ ] 优化错误提示文案
- [ ] 添加用户引导
- [ ] 实现首页四大模块入口

### 中期任务 (4周)
- [ ] 实现历史记录功能（支持四大模块）
- [ ] 添加用户反馈功能
- [ ] 优化图片压缩算法
- [ ] 添加离线缓存
- [ ] 实现健康档案功能
- [ ] 添加知识库浏览

### 长期任务 (持续)
- [ ] 添加数据统计和分析
- [ ] 实现用户账号系统
- [ ] 添加社交分享功能
- [ ] 实现提醒功能
- [ ] 会员系统开发
- [ ] 增值服务开发

## 联系方式

如有问题，请联系：
- 后端仓库：https://github.com/cj66666/furniture-health-detector
- 前端仓库：https://github.com/XIXIrodrian/health-tool

---

**集成完成时间：** 2026-01-30
**集成人员：** Claude Sonnet 4.5
