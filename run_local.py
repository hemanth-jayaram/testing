#!/usr/bin/env python3
"""
Local Development Runner for Federated Learning Phishing Detection
Use this script to run the application locally with sample data.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import flask
        import boto3
        import pandas
        import sklearn
        import numpy
        import matplotlib
        import seaborn
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_environment():
    """Check environment variables"""
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'S3_BUCKET_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nCreate a .env file or set these variables:")
        print("export AWS_ACCESS_KEY_ID='your_key'")
        print("export AWS_SECRET_ACCESS_KEY='your_secret'")
        print("export S3_BUCKET_NAME='your-bucket'")
        return False
    
    print("✅ Environment variables configured")
    return True

def setup_directories():
    """Create necessary directories"""
    directories = ['temp_uploads', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_aws_setup():
    """Run AWS S3 setup"""
    print("\n🔧 Setting up AWS S3 bucket...")
    try:
        result = subprocess.run([sys.executable, 'setup_aws.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ AWS setup completed")
            return True
        else:
            print(f"❌ AWS setup failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running AWS setup: {e}")
        return False

def start_flask_app():
    """Start the Flask application"""
    print("\n🚀 Starting Flask application...")
    print("📊 Access the application at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        os.system(f"{sys.executable} app.py")
    except KeyboardInterrupt:
        print("\n👋 Application stopped")

def main():
    """Main function"""
    print("🔥 Federated Learning Phishing Detection - Local Runner")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n💡 Tip: Copy .env.example to .env and fill in your AWS credentials")
        sys.exit(1)
    
    # Setup directories
    print("\n📁 Setting up directories...")
    setup_directories()
    
    # Setup AWS (optional for local development)
    setup_aws = input("\n🤔 Do you want to setup AWS S3 bucket? (y/n): ").lower().strip()
    if setup_aws == 'y':
        if not run_aws_setup():
            print("⚠️  AWS setup failed, but you can still run locally")
    
    # Start Flask app
    start_flask_app()

if __name__ == "__main__":
    main()