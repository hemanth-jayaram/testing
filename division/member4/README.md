# Federated Learning for Phishing Email Detection - Cloud Edition

A cloud-enabled federated learning system for phishing email detection using AWS S3, EC2, and a modern web interface.

## Features

- **Web Interface**: Modern Bootstrap 5 UI with real-time training monitoring
- **S3 Integration**: Automatic dataset upload and model versioning
- **Federated Learning**: FedAvg algorithm with multiple clients
- **Model Versioning**: Automatic S3-based model versioning
- **Real-time Classification**: Interactive email classification with confidence scores
- **Auto-scaling**: Automatically detects and uses all CSV datasets in S3

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │   Flask App     │    │   AWS S3        │
│   (Bootstrap 5) │◄──►│   (EC2)         │◄──►│   (Storage)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Federated       │
                    │ Learning Engine │
                    └─────────────────┘
```

## Quick Start

### 1. AWS Setup

Create an S3 bucket and IAM user with S3 permissions:

```bash
# Create S3 bucket
aws s3 mb s3://your-fl-phishing-bucket

# Create folders
aws s3api put-object --bucket your-fl-phishing-bucket --key datasets/
aws s3api put-object --bucket your-fl-phishing-bucket --key models/
aws s3api put-object --bucket your-fl-phishing-bucket --key logs/
```

### 2. Local Development

```bash
# Clone and setup
git clone <repository>
cd fl-phish-cloud

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your AWS credentials

# Run application
python app.py
```

### 3. EC2 Deployment

Launch Ubuntu 22.04 EC2 instance and run:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone project
git clone <repository>
cd fl-phish-cloud

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment variables
sudo nano /etc/environment
# Add:
# AWS_ACCESS_KEY_ID="your_key"
# AWS_SECRET_ACCESS_KEY="your_secret"
# AWS_DEFAULT_REGION="us-east-1"
# S3_BUCKET_NAME="your-bucket"

# Create systemd service
sudo nano /etc/systemd/system/fl-phish.service
```

### 4. Systemd Service Configuration

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

[Install]
WantedBy=multi-user.target
```

### 5. Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. Enable Services

```bash
# Enable and start services
sudo systemctl enable fl-phish
sudo systemctl start fl-phish
sudo systemctl enable nginx
sudo systemctl start nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Usage

### 1. Upload Datasets

- Navigate to `/upload`
- Select CSV files with formats:
  - `text,label`
  - `body,label`
  - `text_combined,label`
- Files are automatically uploaded to S3 with timestamps

### 2. Train Models

- Go to `/train`
- Set number of training rounds (1-50)
- Click "Start Federated Training"
- Monitor real-time progress and accuracy charts

### 3. View Model Versions

- Visit `/models`
- See all trained model versions
- Download or test specific versions
- View training statistics

### 4. Classify Emails

- Navigate to `/classify`
- Enter email text or use sample emails
- Select model version (latest by default)
- Get phishing/legitimate prediction with confidence score

## CSV Format Support

The system automatically detects these CSV formats:

```csv
# Format 1: text,label
text,label
"Please verify your account",1
"Meeting at 3pm",0

# Format 2: body,label
body,label
"Click here to update payment",1
"Project deadline tomorrow",0

# Format 3: text_combined,label
text_combined,label
"Urgent: Confirm identity",1
"Thanks for presentation",0
```

## API Endpoints

- `POST /api/train` - Start federated training
- `GET /api/training_status` - Get training progress
- `POST /api/classify` - Classify email text
- `GET /api/download_model/<version>` - Download model

## Monitoring

### Training Logs
Real-time training logs show:
- Client initialization
- Round progress
- Accuracy improvements
- Model saving status

### Accuracy Visualization
Live Chart.js charts display:
- Per-round accuracy
- Training convergence
- Performance trends

## Security

- Environment variables for AWS credentials
- Secure file uploads with validation
- HTTPS with Let's Encrypt
- Input sanitization and validation

## Troubleshooting

### Common Issues

1. **S3 Connection Failed**
   ```bash
   # Check AWS credentials
   aws s3 ls s3://your-bucket-name
   ```

2. **No Datasets Found**
   ```bash
   # Verify S3 bucket structure
   aws s3 ls s3://your-bucket-name/datasets/
   ```

3. **Training Fails**
   ```bash
   # Check application logs
   sudo journalctl -u fl-phish -f
   ```

4. **Model Loading Error**
   ```bash
   # Verify model files in S3
   aws s3 ls s3://your-bucket-name/models/
   ```

### Performance Optimization

- Use EC2 instances with sufficient RAM (t3.medium or larger)
- Enable S3 Transfer Acceleration for faster uploads
- Use CloudFront for static assets
- Monitor CloudWatch metrics

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request