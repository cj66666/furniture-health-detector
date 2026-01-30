"""Test Qwen-VL API Connection"""
import asyncio
from app.services.qwen_vl import QwenVLService


async def test_api_connection():
    """Test API connection"""
    print("Testing Qwen-VL API connection...")

    try:
        service = QwenVLService()
        print("Service initialized successfully")
        print(f"  - API Base URL: {service.settings.OPENAI_BASE_URL}")
        print(f"  - Model: {service.model}")
        print(f"  - API Key: {service.settings.OPENAI_API_KEY[:10]}...")

        # Test simple text generation (no image required)
        print("\nTesting API call...")
        result = await service.generate_catchphrase(
            material_info={'material_type': 'solid_wood', 'sub_type': 'solid_wood_board'},
            risk_level='low_risk'
        )

        print("API call successful!")
        print(f"  Generated catchphrase: {result}")

        return True

    except Exception as e:
        print(f"API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_api_connection())

    print("\n" + "="*50)
    if success:
        print("SUCCESS: Qwen-VL API is configured correctly!")
    else:
        print("FAILED: Please check API Key and network connection")
    print("="*50)
