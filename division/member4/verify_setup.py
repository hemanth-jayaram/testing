#!/usr/bin/env python3
"""
Setup Verification Script
Checks if all required files and dependencies are present
"""

import os
import sys
import importlib

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[X] {description}: {filepath} - MISSING")
        return False

def check_import(module_name, description):
    """Check if a Python module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"[OK] {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"[X] {description}: {module_name} - {str(e)}")
        return False

def check_security():
    """Check for security issues"""
    issues = []
    
    # Check for private keys
    if os.path.exists('devops-key.pem'):
        issues.append("[!] SECURITY RISK: devops-key.pem found - DELETE IMMEDIATELY!")
    
    # Check for .env with credentials
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'AKIA' in content or 'aws_access_key' in content.lower():
                issues.append("[!] WARNING: .env contains AWS credentials - ensure it's in .gitignore")
    
    return issues

def main():
    print("=" * 60)
    print("Federated Learning Project - Setup Verification")
    print("=" * 60)
    print()
    
    all_checks = []
    
    # Check core application files
    print("[Core Application Files]")
    all_checks.append(check_file('app.py', 'Main application'))
    all_checks.append(check_file('config.py', 'Configuration'))
    all_checks.append(check_file('model.py', 'Model definition'))
    all_checks.append(check_file('server.py', 'Federated server'))
    all_checks.append(check_file('client.py', 'Federated client'))
    all_checks.append(check_file('s3_helper.py', 'S3 integration'))
    all_checks.append(check_file('training_engine.py', 'Training engine'))
    all_checks.append(check_file('model_stats.py', 'Model statistics'))
    print()
    
    # Check configuration files
    print("[Configuration Files]")
    all_checks.append(check_file('requirements.txt', 'Python dependencies'))
    all_checks.append(check_file('.env.example', 'Environment template'))
    all_checks.append(check_file('.gitignore', 'Git ignore rules'))
    print()
    
    # Check deployment files
    print("[Deployment Files]")
    all_checks.append(check_file('deploy.sh', 'Deployment script'))
    all_checks.append(check_file('ec2_bootstrap.sh', 'EC2 bootstrap'))
    all_checks.append(check_file('docker-compose.yml', 'Docker Compose'))
    all_checks.append(check_file('Dockerfile', 'Docker image'))
    all_checks.append(check_file('nginx.conf', 'Nginx config'))
    print()
    
    # Check documentation
    print("[Documentation]")
    all_checks.append(check_file('README.md', 'Main documentation'))
    all_checks.append(check_file('DEPLOYMENT_GUIDE.md', 'Deployment guide'))
    print()
    
    # Check templates
    print("[Templates]")
    all_checks.append(check_file('templates/base.html', 'Base template'))
    all_checks.append(check_file('templates/home.html', 'Home page'))
    all_checks.append(check_file('templates/upload.html', 'Upload page'))
    all_checks.append(check_file('templates/train.html', 'Training page'))
    all_checks.append(check_file('templates/models.html', 'Models page'))
    all_checks.append(check_file('templates/classify.html', 'Classify page'))
    print()
    
    # Check Python dependencies
    print("[Python Dependencies]")
    all_checks.append(check_import('flask', 'Flask framework'))
    all_checks.append(check_import('boto3', 'AWS SDK'))
    all_checks.append(check_import('pandas', 'Data processing'))
    all_checks.append(check_import('sklearn', 'Machine learning'))
    all_checks.append(check_import('numpy', 'Numerical computing'))
    print()
    
    # Check for security issues
    print("[Security Check]")
    security_issues = check_security()
    if security_issues:
        for issue in security_issues:
            print(issue)
            all_checks.append(False)
    else:
        print("[OK] No security issues found")
        all_checks.append(True)
    print()
    
    # Check for unnecessary files
    print("[Cleanup Check]")
    unnecessary_files = [
        'DEPLOY_INSTRUCTIONS.md',
        'DEPLOYMENT.md',
        'run_local.py',
        'devops-key.pem'
    ]
    
    found_unnecessary = []
    for filename in unnecessary_files:
        if os.path.exists(filename):
            found_unnecessary.append(filename)
    
    if found_unnecessary:
        print("[!] Unnecessary files found (should be removed):")
        for filename in found_unnecessary:
            print(f"   - {filename}")
        all_checks.append(False)
    else:
        print("[OK] No unnecessary files found")
        all_checks.append(True)
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(all_checks)
    total = len(all_checks)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("[SUCCESS] All checks passed! Your setup is ready.")
        return 0
    else:
        print("[WARNING] Some checks failed. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
