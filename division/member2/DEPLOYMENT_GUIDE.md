# 🚀 Complete Deployment Guide

Comprehensive deployment instructions for Federated Learning Phishing Detection on AWS.

## 📋 Prerequisites

- AWS Account with S3 and EC2 access
- AWS CLI configured or access keys ready
- EC2 Key Pair created
- Domain name (optional, for HTTPS)

---

## 🔧 Quick Deployment Methods

### Method 1: Automated Script (Recommended)

```bash
# 1. Launch Ubuntu 22.04 EC2 instance (t3.medium or larger)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 3. Run deployment script
curl -sSL https://raw.githubusercontent.com/your-repo/fl-phish-cloud/main/deploy.sh | bash

# 4. Follow prompts to enter AWS credentials
```

### Method 2: EC2 User Data (One-Click)

When launching EC2 instance, paste this in User Data section:

```bash
#!/bin/bash
curl -sSL https://raw.githubusercontent.com/your-repo/fl-phish-cloud/main/ec2_bootstrap.sh | bash
```

### Method 3: Terraform (Infrastructure as Code)

```bash
# Install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Configure AWS credentials
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"

# Deploy
terraform init
terraform plan -var="key_name=your-ec2-key-pair"
terraform apply -var="key_name=your-ec2-key-pair"

# Get outputs
terraform output
```

---

## 📝 Manual Step-by-Step Deployment

### Step 1: AWS S3 Setup

```bash
# Create S3 bucket for data
aws s3 mb s3://your-fl-phishing-bucket

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket your-fl-phishing-bucket \
  --versioning-configuration Status=Enabled

# Create folder structure
aws s3api put-object --bucket your-fl-phishing-bucket --key datasets/
aws s3api put-object --bucket your-fl-phishing-bucket --key models/
aws s3api put-object --bucket your-fl-phishing-bucket --key logs/
aws s3api put-object --bucket your-fl-phishing-bucket --key plots/
```

### Step 2: Launch EC2 Instance

**Instance Configuration:**
- AMI: Ubuntu Server 22.04 LTS
- Instance Type: t3.medium (minimum) or t3.large (recommended)
- Storage: 20 GB GP3
- Security Group: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)

### Step 3: Connect and Install Dependencies

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx git curl unzip awscli
```

### Step 4: Clone and Setup Application

```bash
# Clone repository
cd /home/ubuntu
git clone https://github.com/your-repo/fl-phish-cloud.git
cd fl-phish-cloud

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

```bash
# Create environment file
sudo nano /etc/environment

# Add these variables:
AWS_ACCESS_KEY_ID="your_access_key"
AWS_SECRET_ACCESS_KEY="your_secret_key"
AWS_DEFAULT_REGION="us-east-1"
S3_BUCKET_NAME="your-fl-phishing-bucket"
SECRET_KEY="$(openssl rand -hex 32)"

# Save and reload
source /etc/environment
```

### Step 6: Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/fl-phish.service
```

Paste this configuration:

```ini
[Unit]
Description=Federated Learning Phishing Detection
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/fl-phish-cloud
Environment=PATH=/home/ubuntu/fl-phish-cloud/venv/bin
EnvironmentFile=/etc/environment
ExecStart=/home/ubuntu/fl-phish-cloud/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 7: Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/fl-phish
```

Paste this configuration:

```nginx
server {
    listen 80;
    server_name _;
    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/ubuntu/fl-phish-cloud/static;
        expires 30d;
    }
}
```

Enable the site:

```bash
sudo ln -sf /etc/nginx/sites-available/fl-phish /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
```

### Step 8: Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable fl-phish
sudo systemctl enable nginx

# Start services
sudo systemctl start fl-phish
sudo systemctl start nginx

# Check status
sudo systemctl status fl-phish
sudo systemctl status nginx
```

### Step 9: Setup SSL (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Auto-renewal is configured automatically
sudo systemctl status certbot.timer
```

---

## 🐳 Docker Deployment (Alternative)

### Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Deploy with Docker

```bash
# Clone repository
git clone https://github.com/your-repo/fl-phish-cloud.git
cd fl-phish-cloud

# Create .env file
cp .env.example .env
nano .env  # Add your AWS credentials

# Start services
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

---

## ✅ Verification & Testing

### Check Services

```bash
# Check application
sudo systemctl status fl-phish
curl http://localhost:5000

# Check Nginx
sudo systemctl status nginx
curl http://localhost

# View logs
sudo journalctl -u fl-phish -f
sudo tail -f /var/log/nginx/access.log
```

### Test S3 Integration

```bash
# Test S3 connection
cd /home/ubuntu/fl-phish-cloud
source venv/bin/activate
python3 setup_aws.py

# Verify bucket structure
aws s3 ls s3://your-fl-phishing-bucket/
```

### Access Application

```bash
# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Access in browser
# http://YOUR_EC2_PUBLIC_IP
```

---

## 🔧 Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u fl-phish -n 50 --no-pager

# Test manually
cd /home/ubuntu/fl-phish-cloud
source venv/bin/activate
python3 app.py
```

### S3 Connection Failed

```bash
# Verify AWS credentials
aws s3 ls s3://your-bucket-name

# Check IAM permissions
aws iam get-user

# Test from Python
python3 -c "from s3_helper import S3Helper; s3 = S3Helper(); print(s3.list_files(''))"
```

### Nginx 502 Error

```bash
# Check if app is running
sudo systemctl status fl-phish
curl http://localhost:5000

# Check Nginx config
sudo nginx -t

# Restart services
sudo systemctl restart fl-phish nginx
```

### File Upload Issues

```bash
# Check disk space
df -h

# Check permissions
ls -la /home/ubuntu/fl-phish-cloud/temp_uploads/

# Create directory if missing
mkdir -p /home/ubuntu/fl-phish-cloud/temp_uploads
chmod 755 /home/ubuntu/fl-phish-cloud/temp_uploads
```

---

## 📊 Monitoring & Maintenance

### View Logs

```bash
# Application logs
sudo journalctl -u fl-phish -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# System resources
htop
df -h
free -h
```

### Backup Strategy

```bash
# S3 versioning is enabled automatically

# Backup application files
tar -czf /tmp/fl-phish-backup-$(date +%Y%m%d).tar.gz /home/ubuntu/fl-phish-cloud
aws s3 cp /tmp/fl-phish-backup-$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
rm /tmp/fl-phish-backup-*.tar.gz
```

### Update Application

```bash
cd /home/ubuntu/fl-phish-cloud
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart fl-phish
```

---

## 🔐 Security Checklist

- ✅ AWS credentials stored in environment variables (not in code)
- ✅ HTTPS enabled with valid SSL certificate
- ✅ Security groups configured (only necessary ports open)
- ✅ Regular security updates applied
- ✅ S3 bucket permissions reviewed
- ✅ Application logs monitored
- ✅ Private keys never committed to repository

---

## 📈 Performance Optimization

### Increase Workers

```bash
# Edit service file
sudo nano /etc/systemd/system/fl-phish.service

# Change: --workers 3 to --workers 4
# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart fl-phish
```

### Enable Nginx Caching

```bash
# Edit Nginx config
sudo nano /etc/nginx/sites-available/fl-phish

# Add caching directives
location /static {
    alias /home/ubuntu/fl-phish-cloud/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

---

## 🌐 Access Your Application

After successful deployment:

- **Home**: `http://YOUR_EC2_IP/`
- **Upload Datasets**: `http://YOUR_EC2_IP/upload`
- **Train Model**: `http://YOUR_EC2_IP/train`
- **View Models**: `http://YOUR_EC2_IP/models`
- **Classify Emails**: `http://YOUR_EC2_IP/classify`

---

## 📞 Support

- Check application logs: `sudo journalctl -u fl-phish -f`
- Review README.md for usage instructions
- Monitor AWS CloudWatch for metrics
- Check S3 bucket for stored data

🎉 **Deployment Complete!** Your federated learning system is now running in production.
