#!/usr/bin/env python3
"""Upload entire project to S3 for EC2 deployment"""

import boto3
import os
import zipfile
import tempfile
from datetime import datetime

# AWS Configuration - USE ENVIRONMENT VARIABLES
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'YOUR_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'YOUR_SECRET_KEY')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
S3_BUCKET = os.getenv('S3_BUCKET_NAME', 'fl-phishing-deployment')

def create_project_zip():
    """Create zip file of entire project"""
    zip_path = tempfile.mktemp(suffix='.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Skip unnecessary directories
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'node_modules']]
            
            for file in files:
                if not file.endswith(('.pyc', '.pyo', '.log')):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, '.')
                    zipf.write(file_path, arcname)
    
    print(f"Project zipped: {zip_path}")
    return zip_path

def upload_to_s3():
    """Upload project and create deployment script"""
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    # Create bucket if not exists
    try:
        s3_client.create_bucket(Bucket=S3_BUCKET)
        print(f"Created bucket: {S3_BUCKET}")
    except:
        print(f"Bucket exists: {S3_BUCKET}")
    
    # Upload project zip
    zip_path = create_project_zip()
    s3_key = f"deployments/fl-phish-cloud-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    s3_client.upload_file(zip_path, S3_BUCKET, s3_key)
    print(f"Uploaded project: s3://{S3_BUCKET}/{s3_key}")
    
    # Create deployment script
    deploy_script = f"""#!/bin/bash
# Auto-generated deployment script

set -e

echo "FL Phishing Detection - Auto Deployment"
echo "=========================================="

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx git curl unzip awscli

# Download project from S3
cd /home/ubuntu
aws s3 cp s3://{S3_BUCKET}/{s3_key} fl-phish-cloud.zip
unzip -o fl-phish-cloud.zip -d fl-phish-cloud
cd fl-phish-cloud

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt

# Set environment variables
sudo tee /etc/environment > /dev/null <<EOF
AWS_ACCESS_KEY_ID="{AWS_ACCESS_KEY_ID}"
AWS_SECRET_ACCESS_KEY="{AWS_SECRET_ACCESS_KEY}"
AWS_DEFAULT_REGION="{AWS_REGION}"
S3_BUCKET_NAME="fl-phishing-data"
SECRET_KEY="$(openssl rand -hex 32)"
EOF

# Create systemd service
sudo tee /etc/systemd/system/fl-phish.service > /dev/null <<EOF
[Unit]
Description=FL Phishing Detection
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/fl-phish-cloud
Environment=PATH=/home/ubuntu/fl-phish-cloud/venv/bin
EnvironmentFile=/etc/environment
ExecStart=/home/ubuntu/fl-phish-cloud/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
sudo tee /etc/nginx/sites-available/fl-phish > /dev/null <<EOF
server {{
    listen 80;
    server_name _;
    client_max_body_size 20M;

    location / {{
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \\$host;
        proxy_set_header X-Real-IP \\$remote_addr;
        proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\$scheme;
    }}

    location /static {{
        alias /home/ubuntu/fl-phish-cloud/static;
        expires 1y;
    }}
}}
EOF

sudo ln -sf /etc/nginx/sites-available/fl-phish /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

# Create directories
mkdir -p temp_uploads

# Set permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/fl-phish-cloud

# Start services
sudo systemctl daemon-reload
sudo systemctl enable fl-phish
sudo systemctl start fl-phish
sudo systemctl enable nginx
sudo systemctl restart nginx

# Setup S3 bucket for data
python3 setup_aws.py

echo ""
echo "Deployment completed!"
echo "Access: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "Logs: sudo journalctl -u fl-phish -f"
echo ""
"""
    
    # Upload deployment script
    script_path = tempfile.mktemp(suffix='.sh')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(deploy_script)
    
    script_key = "deploy.sh"
    s3_client.upload_file(script_path, S3_BUCKET, script_key)
    print(f"Uploaded deploy script: s3://{S3_BUCKET}/{script_key}")
    
    # Cleanup
    os.unlink(zip_path)
    os.unlink(script_path)
    
    return S3_BUCKET, script_key

if __name__ == "__main__":
    print("Uploading FL Phishing Detection to S3...")
    
    # Update credentials before running
    if AWS_ACCESS_KEY_ID == "YOUR_ACCESS_KEY":
        print("Please update AWS credentials in this script first!")
        exit(1)
    
    bucket, script_key = upload_to_s3()
    
    print(f"""
Upload completed!

EC2 Deployment Commands:
1. Launch Ubuntu 22.04 EC2 instance
2. SSH into instance
3. Run these commands:

# Configure AWS CLI
aws configure set aws_access_key_id {AWS_ACCESS_KEY_ID}
aws configure set aws_secret_access_key {AWS_SECRET_ACCESS_KEY}
aws configure set default.region {AWS_REGION}

# Download and run deployment
curl -o deploy.sh https://{bucket}.s3.amazonaws.com/{script_key}
chmod +x deploy.sh
./deploy.sh

Your app will be available at: http://YOUR_EC2_PUBLIC_IP
""")