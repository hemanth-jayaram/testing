import boto3
import os
from datetime import datetime
from config import Config

class S3Helper:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION
        )
        self.bucket_name = Config.S3_BUCKET_NAME

    def upload_file(self, local_file_path, s3_key):
        try:
            self.s3_client.upload_file(local_file_path, self.bucket_name, s3_key)
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False

    def download_file(self, s3_key, local_file_path):
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_file_path)
            return True
        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

    def list_files(self, prefix=''):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def get_latest_model_version(self):
        models = self.list_files('models/')
        if not models:
            return 0
        versions = []
        for model in models:
            if model.startswith('models/model_v') and model.endswith('.pkl'):
                try:
                    version = int(model.split('model_v')[1].split('.pkl')[0])
                    versions.append(version)
                except:
                    continue
        return max(versions) if versions else 0

    def upload_csv_dataset(self, file_path, filename):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        s3_key = f"datasets/client_{timestamp}_{filename}"
        return self.upload_file(file_path, s3_key), s3_key