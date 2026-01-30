# Pexels API 配置指南

## 问题说明

当前脚本下载0张图片的原因：
- Pexels API密钥无效（401未授权错误）
- 脚本中的密钥是示例密钥，需要替换为真实的API密钥

## 解决方案：获取免费Pexels API密钥

### 步骤1：注册Pexels账号

1. 访问 https://www.pexels.com/
2. 点击右上角 "Join" 或 "Sign up" 注册账号
3. 可以使用邮箱注册，或使用Google/Facebook账号快速登录

### 步骤2：申请API密钥

1. 登录后，访问 https://www.pexels.com/api/
2. 点击 "Get Started" 或 "Your API Key"
3. 填写简单的申请表单：
   - Application Name: 填写 "Furniture Material Detection" 或任意名称
   - Application Description: 填写 "Download test images for AI project"
   - 同意服务条款
4. 提交后会立即获得API密钥

### 步骤3：复制API密钥

注册成功后，你会看到类似这样的密钥：
```
563492ad6f917000010000abcdef1234567890abcdef1234567890
```

**重要**：这是你的私密密钥，不要分享给他人！

### 步骤4：更新脚本

1. 打开文件：`download_images_simple.py`
2. 找到第44行：
   ```python
   PEXELS_API_KEY = "563492ad6f91700001000001c9ae6c8e4e5d4e5f8b5c8f5e5e5e5e5e"
   ```
3. 将引号内的内容替换为你的真实API密钥：
   ```python
   PEXELS_API_KEY = "你的真实API密钥"
   ```
4. 保存文件

### 步骤5：运行脚本

```bash
cd C:\Users\cj783\Desktop\材料项目
python download_images_simple.py
```

## Pexels API 限制

- 免费账号：每月5000次请求
- 每次请求最多返回80张图片
- 对于本项目完全够用

## 预期结果

配置正确后，你应该看到：
```
[API] 响应状态: 200
[图片] 找到 X 张图片
[下载] 下载: https://...
[尺寸] 1920x1080
[成功] 成功添加
[成功] 成功下载 3 张图片
```

## 如果仍然失败

### 检查清单：
1. API密钥是否正确复制（没有多余空格）
2. 网络连接是否正常
3. 是否能访问 https://www.pexels.com/

### 备用方案：
如果Pexels API仍然无法使用，可以考虑：
1. 使用Unsplash API（需要另外注册）
2. 手动下载图片到指定文件夹
3. 使用其他免费图片API

## 常见问题

**Q: 注册需要付费吗？**
A: 不需要，Pexels API完全免费

**Q: 需要信用卡吗？**
A: 不需要

**Q: API密钥会过期吗？**
A: 不会，除非你主动删除

**Q: 每月5000次够用吗？**
A: 够用。本脚本每次运行大约使用10-20次请求

## 技术支持

如果遇到问题，可以：
1. 查看Pexels API文档：https://www.pexels.com/api/documentation/
2. 检查脚本输出的错误信息
3. 确认API密钥格式正确
