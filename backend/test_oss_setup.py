"""Test and Setup OSS Bucket"""
import oss2
from app.core.config import get_settings


def test_oss_connection():
    """Test OSS connection and bucket"""
    print("=" * 60)
    print("Testing OSS Configuration")
    print("=" * 60)

    settings = get_settings()

    print(f"\nOSS Configuration:")
    print(f"  - Access Key ID: {settings.OSS_ACCESS_KEY_ID[:10]}...")
    print(f"  - Endpoint: {settings.OSS_ENDPOINT}")
    print(f"  - Bucket Name: {settings.OSS_BUCKET_NAME}")

    # Initialize OSS client
    auth = oss2.Auth(
        settings.OSS_ACCESS_KEY_ID,
        settings.OSS_ACCESS_KEY_SECRET
    )

    # Test connection by listing buckets
    print("\nTesting connection...")
    try:
        service = oss2.Service(auth, settings.OSS_ENDPOINT)
        buckets = [b.name for b in oss2.BucketIterator(service)]
        print(f"Connection successful!")
        print(f"Found {len(buckets)} bucket(s) in your account:")
        for bucket_name in buckets:
            print(f"  - {bucket_name}")

        # Check if our bucket exists
        if settings.OSS_BUCKET_NAME in buckets:
            print(f"\n[OK] Bucket '{settings.OSS_BUCKET_NAME}' exists!")
            return True
        else:
            print(f"\n[ERROR] Bucket '{settings.OSS_BUCKET_NAME}' does NOT exist!")
            print("\nTo create the bucket, you have two options:")
            print("\n1. Create via Aliyun Console:")
            print("   - Visit: https://oss.console.aliyun.com/bucket")
            print(f"   - Click 'Create Bucket'")
            print(f"   - Bucket Name: {settings.OSS_BUCKET_NAME}")
            print(f"   - Region: cn-hangzhou")
            print(f"   - Storage Class: Standard")
            print(f"   - Access Control: Private")
            print("\n2. Create programmatically (run this script with --create):")
            print(f"   python test_oss_setup.py --create")
            return False

    except Exception as e:
        print(f"Connection failed: {e}")
        print("\nPlease check:")
        print("  1. Access Key ID and Secret are correct")
        print("  2. Network connection is available")
        print("  3. Endpoint is correct for your region")
        return False


def create_bucket():
    """Create OSS bucket"""
    print("=" * 60)
    print("Creating OSS Bucket")
    print("=" * 60)

    settings = get_settings()

    auth = oss2.Auth(
        settings.OSS_ACCESS_KEY_ID,
        settings.OSS_ACCESS_KEY_SECRET
    )

    bucket = oss2.Bucket(
        auth,
        settings.OSS_ENDPOINT,
        settings.OSS_BUCKET_NAME
    )

    try:
        # Create bucket with private ACL
        bucket.create_bucket(
            oss2.models.BUCKET_ACL_PRIVATE,
            oss2.models.BucketCreateConfig(
                oss2.BUCKET_STORAGE_CLASS_STANDARD
            )
        )
        print(f"[OK] Bucket '{settings.OSS_BUCKET_NAME}' created successfully!")

        # Set CORS rules for web access
        rule = oss2.models.CorsRule(
            allowed_origins=['*'],
            allowed_methods=['GET', 'POST', 'PUT'],
            allowed_headers=['*'],
            max_age_seconds=3600
        )
        bucket.put_bucket_cors(oss2.models.BucketCors([rule]))
        print("[OK] CORS rules configured")

        return True

    except oss2.exceptions.OssError as e:
        if e.code == 'BucketAlreadyOwnedByYou':
            print(f"Bucket '{settings.OSS_BUCKET_NAME}' already exists and owned by you!")
            return True
        else:
            print(f"Failed to create bucket: {e}")
            return False
    except Exception as e:
        print(f"Failed to create bucket: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        success = create_bucket()
        if success:
            print("\n" + "=" * 60)
            print("Bucket created! Now you can run the full workflow test:")
            print("python test_full_workflow.py")
            print("=" * 60)
    else:
        test_oss_connection()
