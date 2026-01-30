"""API 测试脚本

用于快速测试后端 API 是否正常工作。
"""
import requests
import json


def test_root():
    """测试根路径"""
    print("测试根路径...")
    response = requests.get("http://localhost:8000/")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    response = requests.get("http://localhost:8000/api/v1/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()


def test_furniture_detect():
    """测试家具检测（需要提供图片文件）"""
    print("测试家具检测...")
    print("注意：此测试需要提供图片文件路径")
    print("示例代码：")
    print("""
    with open('test_image.jpg', 'rb') as f:
        files = {'image': f}
        data = {'disclaimer_accepted': 'true'}
        response = requests.post(
            'http://localhost:8000/api/v1/furniture/detect',
            files=files,
            data=data
        )
        print(response.json())
    """)
    print()


def test_api_docs():
    """测试 API 文档"""
    print("API 文档地址:")
    print("- Swagger UI: http://localhost:8000/api/v1/docs")
    print("- ReDoc: http://localhost:8000/api/v1/redoc")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("家具健康检测器 - API 测试")
    print("=" * 60)
    print()

    try:
        test_root()
        test_health()
        test_furniture_detect()
        test_api_docs()

        print("=" * 60)
        print("✅ 基础测试完成！")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("❌ 错误: 无法连接到服务器")
        print("请确保后端服务已启动: python main.py")
    except Exception as e:
        print(f"❌ 错误: {e}")
