@echo off
chcp 65001 >nul
echo =========================================
echo 家具健康检测器 - 后端开发环境设置
echo =========================================
echo.

REM 检查 Python 版本
echo 检查 Python 版本...
python --version
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

REM 创建虚拟环境
echo.
echo 创建 Python 虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo 错误: 虚拟环境创建失败
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo.
echo 安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: 依赖安装失败
    pause
    exit /b 1
)

REM 复制环境变量文件
if not exist .env (
    echo.
    echo 创建 .env 文件...
    copy .env.example .env
    echo 请编辑 .env 文件，填入你的 API Key
)

REM 创建日志目录
echo.
echo 创建日志目录...
if not exist logs mkdir logs

echo.
echo =========================================
echo ✅ 环境设置完成！
echo =========================================
echo.
echo 下一步：
echo 1. 编辑 .env 文件，填入你的 API Key
echo 2. 运行开发服务器: python main.py
echo 3. 访问 API 文档: http://localhost:8000/api/v1/docs
echo.
pause
