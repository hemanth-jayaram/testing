# Terraform deployment for FL Phishing Detection

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.medium"
}

variable "key_name" {
  description = "EC2 Key Pair name"
  type        = string
}

# S3 bucket for deployment
resource "aws_s3_bucket" "deployment" {
  bucket = "fl-phishing-deployment-${random_string.suffix.result}"
}

resource "aws_s3_bucket" "data" {
  bucket = "fl-phishing-data-${random_string.suffix.result}"
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_versioning" "data_versioning" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Security group
resource "aws_security_group" "fl_phish" {
  name_prefix = "fl-phish-"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# IAM role for EC2
resource "aws_iam_role" "fl_phish_role" {
  name = "fl-phish-ec2-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "fl_phish_policy" {
  name = "fl-phish-s3-policy"
  role = aws_iam_role.fl_phish_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.deployment.arn,
          "${aws_s3_bucket.deployment.arn}/*",
          aws_s3_bucket.data.arn,
          "${aws_s3_bucket.data.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_instance_profile" "fl_phish_profile" {
  name = "fl-phish-profile"
  role = aws_iam_role.fl_phish_role.name
}

# EC2 instance
resource "aws_instance" "fl_phish" {
  ami                    = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS
  instance_type          = var.instance_type
  key_name              = var.key_name
  vpc_security_group_ids = [aws_security_group.fl_phish.id]
  iam_instance_profile   = aws_iam_instance_profile.fl_phish_profile.name
  
  user_data = base64encode(templatefile("${path.module}/ec2_bootstrap.sh", {
    deployment_bucket = aws_s3_bucket.deployment.bucket
    data_bucket      = aws_s3_bucket.data.bucket
  }))
  
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }
  
  tags = {
    Name = "FL-Phishing-Detection"
  }
}

# Outputs
output "instance_public_ip" {
  value = aws_instance.fl_phish.public_ip
}

output "instance_public_dns" {
  value = aws_instance.fl_phish.public_dns
}

output "deployment_bucket" {
  value = aws_s3_bucket.deployment.bucket
}

output "data_bucket" {
  value = aws_s3_bucket.data.bucket
}

output "application_url" {
  value = "http://${aws_instance.fl_phish.public_ip}"
}