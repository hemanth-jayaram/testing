#!/bin/bash

# Federated Learning Phishing Detection - EC2 Deployment Script
# Run this script on Ubuntu 22.04 EC2 instance

set -e

echo "🚀 Starting FL Phishing Detection Deployment..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing Python, Nginx, and dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# Create application directory
echo "📁 Setting up application directory..."
cd /home/ubuntu
git clone https://github.com/your-repo/fl-phish-cloud.git || echo "Repository already exists"
cd fl-phish-cloud

# Setup Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
echo "⚙️ Configuring environment variables..."
sudo tee /etc/environment > /dev/null <<EOF
AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION"
S3_BUCKET_NAME="$S3_BUCKET_NAME"
EOF

# Create systemd service
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/fl-phish.service > /dev/null <<EOF
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
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/fl-phish > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static {
        alias /home/ubuntu/fl-phish-cloud/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/fl-phish /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Create temp directories
mkdir -p temp_uploads

# Set permissions
sudo chown -R ubuntu:ubuntu /home/ubuntu/fl-phish-cloud

# Reload systemd and start services
echo "🔄 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable fl-phish
sudo systemctl start fl-phish
sudo systemctl enable nginx
sudo systemctl restart nginx

# Install SSL certificate (optional)
if [ ! -z "$DOMAIN_NAME" ]; then
    echo "🔒 Setting up SSL certificate..."
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME
fi

# Check service status
echo "✅ Checking service status..."
sudo systemctl status fl-phish --no-pager
sudo systemctl status nginx --no-pager

# Display final information
echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📊 Service Status:"
echo "  - Flask App: $(sudo systemctl is-active fl-phish)"
echo "  - Nginx: $(sudo systemctl is-active nginx)"
echo ""
echo "🌐 Access your application:"
if [ ! -z "$DOMAIN_NAME" ]; then
    echo "  - HTTPS: https://$DOMAIN_NAME"
    echo "  - HTTP: http://$DOMAIN_NAME"
else
    echo "  - HTTP: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
fi
echo ""
echo "📝 Useful commands:"
echo "  - View logs: sudo journalctl -u fl-phish -f"
echo "  - Restart app: sudo systemctl restart fl-phish"
echo "  - Check status: sudo systemctl status fl-phish"
echo ""
echo "⚠️  Remember to:"
echo "  1. Configure your AWS credentials in /etc/environment"
echo "  2. Create S3 bucket with datasets/ and models/ folders"
echo "  3. Upload CSV datasets to S3 bucket"
echo ""