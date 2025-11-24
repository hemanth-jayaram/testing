#!/usr/bin/env python3
"""
AWS S3 Bucket Setup Script for Federated Learning Phishing Detection
Run this script to create and configure the required S3 bucket structure.
"""

import boto3
import sys
from config import Config

def create_s3_bucket():
    """Create S3 bucket and folder structure"""
    
    if not all([Config.AWS_ACCESS_KEY_ID, Config.AWS_SECRET_ACCESS_KEY, Config.S3_BUCKET_NAME]):
        print("❌ Error: AWS credentials or bucket name not configured")
        print("Please set the following environment variables:")
        print("- AWS_ACCESS_KEY_ID")
        print("- AWS_SECRET_ACCESS_KEY") 
        print("- S3_BUCKET_NAME")
        return False
    
    try:
        # Initialize S3 client
        s3_client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION
        )
        
        bucket_name = Config.S3_BUCKET_NAME or 'fl-phishing-data'
        
        print(f"🚀 Setting up S3 bucket: {bucket_name}")
        
        # Create bucket
        try:
            if Config.AWS_DEFAULT_REGION == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': Config.AWS_DEFAULT_REGION}
                )
            print(f"✅ Created S3 bucket: {bucket_name}")
        except s3_client.exceptions.BucketAlreadyOwnedByYou:
            print(f"✅ S3 bucket already exists: {bucket_name}")
        except Exception as e:
            print(f"❌ Error creating bucket: {e}")
            return False
        
        # Create folder structure
        folders = ['datasets/', 'models/', 'logs/', 'plots/']
        
        for folder in folders:
            try:
                s3_client.put_object(Bucket=bucket_name, Key=folder)
                print(f"✅ Created folder: {folder}")
            except Exception as e:
                print(f"❌ Error creating folder {folder}: {e}")
        
        # Enable versioning
        try:
            s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            print("✅ Enabled S3 versioning")
        except Exception as e:
            print(f"⚠️  Warning: Could not enable versioning: {e}")
        
        # Set CORS configuration for web access
        cors_configuration = {
            'CORSRules': [
                {
                    'AllowedHeaders': ['*'],
                    'AllowedMethods': ['GET', 'PUT', 'POST'],
                    'AllowedOrigins': ['*'],
                    'ExposeHeaders': ['ETag'],
                    'MaxAgeSeconds': 3000
                }
            ]
        }
        
        try:
            s3_client.put_bucket_cors(
                Bucket=bucket_name,
                CORSConfiguration=cors_configuration
            )
            print("✅ Configured CORS settings")
        except Exception as e:
            print(f"⚠️  Warning: Could not set CORS: {e}")
        
        print(f"\n🎉 S3 bucket setup completed successfully!")
        print(f"📊 Bucket: {bucket_name}")
        print(f"🌍 Region: {Config.AWS_DEFAULT_REGION}")
        print(f"📁 Folders created: {', '.join(folders)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up S3 bucket: {e}")
        return False

def upload_sample_data():
    """Upload sample dataset to S3"""
    try:
        from s3_helper import S3Helper
        
        s3_helper = S3Helper()
        sample_file = 'sample_data/sample_phishing.csv'
        
        if not os.path.exists(sample_file):
            print(f"⚠️  Sample file not found: {sample_file}")
            # Create sample data if not exists
            os.makedirs('sample_data', exist_ok=True)
            with open(sample_file, 'w') as f:
                f.write('text,label\n')
                f.write('"Please verify your account",1\n')
                f.write('"Meeting at 3pm",0\n')
                f.write('"Click here to win",1\n')
                f.write('"Project update",0\n')
            print(f"✅ Created sample file: {sample_file}")
        
        success, s3_key = s3_helper.upload_csv_dataset(sample_file, 'sample_phishing.csv')
        
        if success:
            print(f"✅ Uploaded sample dataset: {s3_key}")
            return True
        else:
            print("❌ Failed to upload sample dataset")
            return False
            
    except Exception as e:
        print(f"❌ Error uploading sample data: {e}")
        return False

def verify_setup():
    """Verify the S3 setup is working"""
    try:
        from s3_helper import S3Helper
        
        s3_helper = S3Helper()
        
        # Test listing files
        datasets = s3_helper.list_files('datasets/')
        models = s3_helper.list_files('models/')
        
        print(f"\n🔍 Verification Results:")
        print(f"📁 Datasets folder: {len(datasets)} files")
        print(f"🤖 Models folder: {len(models)} files")
        
        # Test model versioning
        latest_version = s3_helper.get_latest_model_version()
        print(f"📊 Latest model version: {latest_version}")
        
        print("✅ S3 setup verification completed")
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    import os
    
    print("🔧 AWS S3 Setup for Federated Learning Phishing Detection")
    print("=" * 60)
    
    # Create bucket and folders
    if create_s3_bucket():
        
        # Upload sample data if available
        if os.path.exists('sample_data/sample_phishing.csv'):
            print("\n📤 Uploading sample dataset...")
            upload_sample_data()
        
        # Verify setup
        print("\n🔍 Verifying setup...")
        verify_setup()
        
        print("\n🎉 Setup completed! You can now:")
        print("1. Upload CSV datasets via the web interface")
        print("2. Run federated training")
        print("3. View model versions and results")
        
    else:
        print("\n❌ Setup failed. Please check your AWS credentials and try again.")
        sys.exit(1)