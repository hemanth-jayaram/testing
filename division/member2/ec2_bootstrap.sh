#!/bin/bash
# EC2 User Data Script - Self-sufficient deployment

set -e

# Configuration
S3_BUCKET="fl-phishing-deployment"
AWS_REGION="us-east-1"

echo "🚀 FL Phishing Detection - Bootstrap Deployment"
echo "=============================================="

# Update system
apt update && apt upgrade -y

# Install dependencies
apt install -y python3 python3-pip python3-venv nginx git curl unzip awscli

# Create ubuntu user if not exists (for some AMIs)
if ! id "ubuntu" &>/dev/null; then
    useradd -m -s /bin/bash ubuntu
    usermod -aG sudo ubuntu
fi

# Switch to ubuntu user directory
cd /home/ubuntu

# Download latest deployment
aws s3 cp s3://$S3_BUCKET/deploy.sh deploy.sh --no-sign-request || {
    echo "❌ Failed to download deployment script"
    exit 1
}

chmod +x deploy.sh

# Run deployment as ubuntu user
sudo -u ubuntu ./deploy.sh

echo "🎉 Bootstrap completed!"
echo "📊 Service status:"
systemctl status fl-phish --no-pager
systemctl status nginx --no-pager