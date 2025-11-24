# 🚀 Deployment Guide - Federated Learning Phishing Detection

Complete deployment instructions for AWS EC2 with S3 integration.

## 📋 Prerequisites

- AWS Account with S3 and EC2 access
- Domain name (optional, for HTTPS)
- Basic knowledge of Linux/Ubuntu

## 🔧 Step 1: AWS Setup

### Create S3 Bucket

```bash
# Using AWS CLI
aws s3 mb s3://your-fl-phishing-bucket
aws s3api put-bucket-versioning --bucket your-fl-phishing-bucket --versioning-configuration Status=Enabled

# Create folder structure
aws s3api put-object --bucket your-fl-phishing-bucket --key datasets/
aws s3api put-object --bucket your-fl-phishing-bucket --key models/
aws s3api put-object --bucket your-fl-phishing-bucket --key logs/
aws s3api put-object --bucket your-fl-phishing-bucket --key plots/
```

### Create IAM User

1. Go to AWS IAM Console
2. Create new user: `fl-phishing-user`
3. Attach policy: `AmazonS3FullAccess`
4. Save Access Key ID and Secret Access Key

## 🖥️ Step 2: Launch EC2 Instance

### Instance Configuration

- **AMI**: Ubuntu Server 22.04 LTS
- **Instance Type**: t3.medium (minimum) or t3.large (recommended)
- **Storage**: 20 GB GP3
- **Security Group**: Allow HTTP (80), HTTPS (443), SSH (22)

### Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

## ⚡ Step 3: Automated Deployment

### Option A: One-Command Deployment

```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
export S3_BUCKET_NAME="your-fl-phishing-bucket"
export DOMAIN_NAME="your-domain.com"  # Optional

# Download and run deployment script
curl -sSL https://raw.githubusercontent.com/your-repo/fl-phish-cloud/main/deploy.sh | bash
```

### Option B: Manual Deployment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Clone repository
git clone https://github.com/your-repo/fl-phish-cloud.git
cd fl-phish-cloud

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
sudo nano /etc/environment
# Add your AWS credentials:
AWS_ACCESS_KEY_ID="your_access_key"
AWS_SECRET_ACCESS_KEY="your_secret_key"
AWS_DEFAULT_REGION="us-east-1"
S3_BUCKET_NAME="your-fl-phishing-bucket"

# Setup systemd service
sudo cp deploy/fl-phish.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable fl-phish
sudo systemctl start fl-phish

# Configure Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/fl-phish
sudo ln -s /etc/nginx/sites-available/fl-phish /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

## 🔒 Step 4: SSL Certificate (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already configured)
sudo systemctl status certbot.timer
```

## 🐳 Step 5: Docker Deployment (Alternative)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy with Docker
git clone https://github.com/your-repo/fl-phish-cloud.git
cd fl-phish-cloud

# Create .env file
cp .env.example .env
nano .env  # Add your AWS credentials

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## 📊 Step 6: Verification

### Check Services

```bash
# Check application status
sudo systemctl status fl-phish
curl http://localhost:5000

# Check Nginx status
sudo systemctl status nginx
curl http://your-domain.com

# Check logs
sudo journalctl -u fl-phish -f
sudo tail -f /var/log/nginx/access.log
```

### Test S3 Integration

```bash
# Run AWS setup script
cd fl-phish-cloud
python3 setup_aws.py

# Upload sample data
python3 -c "
from s3_helper import S3Helper
s3 = S3Helper()
print('S3 Connection:', 'OK' if s3.list_files('') is not None else 'Failed')
"
```

## 🔧 Step 7: Configuration

### Environment Variables

```bash
# Edit environment file
sudo nano /etc/environment

# Required variables:
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="..."
AWS_DEFAULT_REGION="us-east-1"
S3_BUCKET_NAME="your-bucket-name"
SECRET_KEY="your-flask-secret-key"
```

### Application Settings

```bash
# Edit config file
nano fl-phish-cloud/config.py

# Adjust settings:
# - MAX_CONTENT_LENGTH (file upload size)
# - AWS region
# - S3 bucket name
```

## 📈 Step 8: Monitoring & Maintenance

### Log Monitoring

```bash
# Application logs
sudo journalctl -u fl-phish -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System resources
htop
df -h
free -h
```

### Backup Strategy

```bash
# S3 versioning is enabled automatically
# Create backup script for EC2 instance
sudo nano /etc/cron.daily/backup-fl-phish

#!/bin/bash
# Backup application files
tar -czf /tmp/fl-phish-backup-$(date +%Y%m%d).tar.gz /home/ubuntu/fl-phish-cloud
aws s3 cp /tmp/fl-phish-backup-$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
rm /tmp/fl-phish-backup-*.tar.gz
```

### Updates

```bash
# Update application
cd fl-phish-cloud
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart fl-phish
```

## 🚨 Troubleshooting

### Common Issues

1. **S3 Connection Failed**
   ```bash
   # Check AWS credentials
   aws s3 ls s3://your-bucket-name
   
   # Verify IAM permissions
   aws iam get-user
   ```

2. **Application Won't Start**
   ```bash
   # Check logs
   sudo journalctl -u fl-phish -n 50
   
   # Test manually
   cd fl-phish-cloud
   source venv/bin/activate
   python3 app.py
   ```

3. **Nginx 502 Error**
   ```bash
   # Check if app is running
   sudo systemctl status fl-phish
   
   # Check Nginx config
   sudo nginx -t
   
   # Restart services
   sudo systemctl restart fl-phish nginx
   ```

4. **File Upload Issues**
   ```bash
   # Check disk space
   df -h
   
   # Check permissions
   ls -la temp_uploads/
   
   # Check Nginx client_max_body_size
   sudo nano /etc/nginx/sites-available/fl-phish
   ```

### Performance Optimization

```bash
# Increase worker processes
sudo nano /etc/systemd/system/fl-phish.service
# Change: --workers 3 to --workers 4

# Enable Nginx gzip compression
sudo nano /etc/nginx/nginx.conf
# Add gzip configuration

# Monitor resource usage
sudo apt install htop iotop
htop
```

## 📞 Support

- **Documentation**: Check README.md for detailed usage
- **Logs**: Always check application and system logs first
- **AWS Console**: Monitor S3 bucket and EC2 instance
- **GitHub Issues**: Report bugs and feature requests

## 🔐 Security Checklist

- ✅ AWS credentials stored securely
- ✅ HTTPS enabled with valid certificate
- ✅ Firewall configured (UFW or Security Groups)
- ✅ Regular security updates
- ✅ S3 bucket permissions reviewed
- ✅ Application logs monitored

## 📊 Scaling Considerations

### Horizontal Scaling

- Use Application Load Balancer
- Deploy multiple EC2 instances
- Shared S3 storage for models/datasets
- Redis for session management

### Vertical Scaling

- Upgrade to larger EC2 instance types
- Increase storage capacity
- Optimize database queries
- Enable CloudFront CDN

---

🎉 **Deployment Complete!** Your federated learning system is now running in production.