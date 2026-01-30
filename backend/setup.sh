#!/bin/bash

echo "========================================="
echo "家具健康检测器 - 后端开发环境设置"
echo "========================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python3 --version

if [ $? -ne 0 ]; then
    echo "错误: 未找到 Python 3，请先安装 Python 3.9+"
    exit 1
fi

# 创建虚拟环境
echo ""
echo "创建 Python 虚拟环境..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "错误: 虚拟环境创建失败"
    exit 1
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "安装项目依赖..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "错误: 依赖安装失败"
    exit 1
fi

# 复制环境变量文件
if [ ! -f .env ]; then
    echo ""
    echo "创建 .env 文件..."
    cp .env.example .env
    echo "请编辑 .env 文件，填入你的 API Key"
fi

# 创建日志目录
echo ""
echo "创建日志目录..."
mkdir -p logs

echo ""
echo "========================================="
echo "✅ 环境设置完成！"
echo "========================================="
echo ""
echo "下一步："
echo "1. 编辑 .env 文件，填入你的 API Key"
echo "2. 运行开发服务器: python3 main.py"
echo "3. 访问 API 文档: http://localhost:8000/api/v1/docs"
echo ""
