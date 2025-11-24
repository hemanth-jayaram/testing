# 🚀 Self-Sufficient Deployment Instructions

Complete deployment from S3 to EC2 - everything automated.

## 🔧 Method 1: Upload & Deploy (Recommended)

### Step 1: Upload Project to S3
```bash
# Edit upload_to_s3.py with your AWS credentials
# Update these lines:
AWS_ACCESS_KEY_ID = "YOUR_ACTUAL_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_ACTUAL_SECRET_KEY"

# Run upload
python upload_to_s3.py
```

### Step 2: Launch EC2 & Deploy
```bash
# 1. Launch Ubuntu 22.04 EC2 instance
# 2. SSH into instance
# 3. Run these commands:

# Configure AWS CLI
aws configure set aws_access_key_id YOUR_ACCESS_KEY
aws configure set aws_secret_access_key YOUR_SECRET_KEY
aws configure set default.region us-east-1

# Download and run deployment
curl -o deploy.sh https://fl-phishing-deployment.s3.amazonaws.com/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

## 🏗️ Method 2: Terraform (Fully Automated)

### Prerequisites
```bash
# Install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Configure AWS credentials
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
```

### Deploy Everything
```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="key_name=your-ec2-key-pair"

# Deploy infrastructure
terraform apply -var="key_name=your-ec2-key-pair"

# Get outputs
terraform output
```

## 🐳 Method 3: EC2 User Data (One-Click)

### Launch EC2 with User Data
```bash
# When launching EC2 instance, paste this in User Data:

#!/bin/bash
curl -sSL https://raw.githubusercontent.com/your-repo/fl-phish-cloud/main/ec2_bootstrap.sh | bash
```

## 📋 Method 4: Manual Commands

### If you prefer step-by-step:
```bash
# 1. Launch Ubuntu 22.04 EC2
# 2. SSH into instance
# 3. Run these commands:

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx git curl unzip awscli

# Configure AWS
aws configure set aws_access_key_id YOUR_KEY
aws configure set aws_secret_access_key YOUR_SECRET
aws configure set default.region us-east-1

# Download project
cd /home/ubuntu
aws s3 cp s3://fl-phishing-deployment/fl-phish-cloud-TIMESTAMP.zip project.zip
unzip project.zip -d fl-phish-cloud
cd fl-phish-cloud

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment
sudo tee /etc/environment > /dev/null <<EOF
AWS_ACCESS_KEY_ID="YOUR_KEY"
AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
AWS_DEFAULT_REGION="us-east-1"
S3_BUCKET_NAME="fl-phishing-data"
SECRET_KEY="$(openssl rand -hex 32)"
EOF

# Create service
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
server {
    listen 80;
    server_name _;
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/fl-phish /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Start services
sudo systemctl daemon-reload
sudo systemctl enable fl-phish nginx
sudo systemctl start fl-phish nginx

# Setup S3 data bucket
python3 setup_aws.py
```

## ✅ Verification

### Check Services
```bash
# Check application
sudo systemctl status fl-phish
curl http://localhost:5000

# Check Nginx
sudo systemctl status nginx

# View logs
sudo journalctl -u fl-phish -f
```

### Test Application
```bash
# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Access application
# http://YOUR_EC2_PUBLIC_IP
```

## 🔧 Troubleshooting

### Common Issues
```bash
# Service not starting
sudo journalctl -u fl-phish -n 50

# Python dependencies
source venv/bin/activate
pip install -r requirements.txt

# Permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/fl-phish-cloud

# Restart everything
sudo systemctl restart fl-phish nginx
```

## 📊 What Gets Deployed

✅ **Complete Flask Application**  
✅ **S3 Integration for datasets/models**  
✅ **Nginx reverse proxy**  
✅ **Systemd service**  
✅ **Sample data**  
✅ **All dependencies**  
✅ **Auto-start on boot**  

## 🌐 Access Your Application

After deployment, access:
- **Web Interface**: `http://YOUR_EC2_PUBLIC_IP`
- **Upload CSV**: `http://YOUR_EC2_PUBLIC_IP/upload`
- **Train Model**: `http://YOUR_EC2_PUBLIC_IP/train`
- **Classify Email**: `http://YOUR_EC2_PUBLIC_IP/classify`

🎉 **Deployment Complete!** Your federated learning system is now running in production.