"""Test Full Furniture Detection Workflow"""
import asyncio
import os
from pathlib import Path
from PIL import Image
import io

from app.services.image_service import ImageService
from app.services.qwen_vl import QwenVLService
from app.core.config import get_settings


async def test_oss_upload():
    """Test OSS image upload"""
    print("=" * 60)
    print("Testing OSS Upload Service...")
    print("=" * 60)

    try:
        image_service = ImageService()
        print("Image Service initialized successfully")
        print(f"  - Bucket: {image_service.bucket.bucket_name}")
        print(f"  - Endpoint: {image_service.settings.OSS_ENDPOINT}")

        # Create a test image
        print("\nCreating test image...")
        img = Image.new('RGB', (800, 600), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        # Upload test image
        print("Uploading test image to OSS...")
        image_url = await image_service.upload_to_oss(
            img_bytes.getvalue(),
            "test_furniture.jpg"
        )

        print(f"Upload successful!")
        print(f"  - Image URL: {image_url}")

        return image_url

    except Exception as e:
        print(f"OSS test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_qwen_analysis(image_url: str):
    """Test Qwen-VL analysis with image"""
    print("\n" + "=" * 60)
    print("Testing Qwen-VL Analysis Service...")
    print("=" * 60)

    try:
        qwen_service = QwenVLService()
        print("Qwen-VL Service initialized successfully")
        print(f"  - Model: {qwen_service.model}")
        print(f"  - API Base URL: {qwen_service.settings.OPENAI_BASE_URL}")

        # Analyze the uploaded image
        print(f"\nAnalyzing image: {image_url}")
        result = await qwen_service.analyze_furniture(
            image_url=image_url,
            additional_context="This is a test image. Please analyze it."
        )

        print("Analysis successful!")
        print(f"  - Material Type: {result.get('material_type')}")
        print(f"  - Sub Type: {result.get('sub_type')}")
        print(f"  - Risk Level: {result.get('risk_level')}")
        print(f"  - Confidence: {result.get('confidence')}")
        print(f"  - Description: {result.get('description', '')[:100]}...")

        return result

    except Exception as e:
        print(f"Qwen-VL analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_full_workflow():
    """Test complete workflow: Upload + Analysis"""
    print("\n" + "=" * 60)
    print("FULL WORKFLOW TEST")
    print("=" * 60)

    # Step 1: Upload image to OSS
    image_url = await test_oss_upload()
    if not image_url:
        print("\nWorkflow failed at OSS upload step")
        return False

    # Step 2: Analyze with Qwen-VL
    result = await test_qwen_analysis(image_url)
    if not result:
        print("\nWorkflow failed at Qwen-VL analysis step")
        return False

    print("\n" + "=" * 60)
    print("SUCCESS: Full workflow completed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    print("Starting Full Workflow Test...")
    print("This will test: OSS Upload + Qwen-VL Analysis\n")

    success = asyncio.run(test_full_workflow())

    print("\n" + "=" * 60)
    if success:
        print("ALL TESTS PASSED!")
    else:
        print("TESTS FAILED - Please check configuration")
    print("=" * 60)
