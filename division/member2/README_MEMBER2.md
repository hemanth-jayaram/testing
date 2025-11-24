# Member 2: Cloud Infrastructure & DevOps

## Role: AWS Integration & Deployment Automation

### Your Responsibilities
- Implement AWS S3 integration
- Create deployment automation scripts
- Configure Docker and Terraform
- Setup Nginx and EC2 infrastructure

### Your Files
1. **s3_helper.py** - S3 integration utilities
2. **setup_aws.py** - AWS setup automation
3. **upload_to_s3.py** - S3 upload utilities
4. **deploy.sh** - Deployment script
5. **ec2_bootstrap.sh** - EC2 initialization
6. **terraform_deploy.tf** - Infrastructure as Code
7. **docker-compose.yml** - Docker orchestration
8. **Dockerfile** - Container definition
9. **nginx.conf** - Web server configuration
10. **DEPLOYMENT_GUIDE.md** - Deployment documentation

### Git Branch
```bash
git checkout -b feature/cloud-infrastructure
```

### Key Tasks
1. Implement S3 file upload/download in s3_helper.py
2. Create AWS bucket setup automation
3. Write deployment scripts for EC2
4. Configure Docker containers
5. Setup Terraform infrastructure
6. Configure Nginx reverse proxy

### Testing
```bash
# Test S3 connection
python -c "from s3_helper import S3Helper; s = S3Helper(); print('OK')"

# Test AWS setup
python setup_aws.py

# Test Docker build
docker build -t fl-phish .
```

### Integration Points
- **With Member 1**: Model storage in S3, training data retrieval
- **With Member 3**: File uploads, environment configuration

### Commit Examples
```bash
git add s3_helper.py
git commit -m "feat(cloud): Implement S3 integration"

git add deploy.sh ec2_bootstrap.sh
git commit -m "feat(devops): Add deployment automation"

git add terraform_deploy.tf
git commit -m "feat(infra): Add Terraform configuration"
```
