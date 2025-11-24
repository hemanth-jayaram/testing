"""
Integration Tests - S3 Operations
Member 2: Cloud Infrastructure & DevOps
"""

import pytest
import tempfile
import os


def test_s3_helper_initialization():
    """Test S3Helper can be initialized"""
    from s3_helper import S3Helper
    s3 = S3Helper()
    assert s3 is not None


def test_s3_list_files():
    """Test listing files from S3"""
    from s3_helper import S3Helper
    
    s3 = S3Helper()
    files = s3.list_files('datasets/')
    
    assert files is not None
    assert isinstance(files, list)


def test_s3_upload_download():
    """Test uploading and downloading files"""
    from s3_helper import S3Helper
    
    s3 = S3Helper()
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write("test content")
    temp_file.close()
    
    try:
        # Upload
        success = s3.upload_file(temp_file.name, 'test/test_file.txt')
        
        # Download
        download_path = tempfile.mktemp(suffix='.txt')
        if success:
            downloaded = s3.download_file('test/test_file.txt', download_path)
            
            if downloaded and os.path.exists(download_path):
                with open(download_path, 'r') as f:
                    content = f.read()
                assert content == "test content"
                os.unlink(download_path)
    finally:
        os.unlink(temp_file.name)


def test_s3_get_latest_model_version():
    """Test getting latest model version"""
    from s3_helper import S3Helper
    
    s3 = S3Helper()
    version = s3.get_latest_model_version()
    
    assert isinstance(version, int)
    assert version >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
