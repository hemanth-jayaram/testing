# Project Division - Federated Learning Phishing Detection

## Team Structure (4 Members)

### Member 1: Backend & ML Engineer (Core Logic)
**Role**: Federated Learning Implementation & Model Development
**Branch**: `feature/federated-learning`

**Responsibilities**:
- Federated learning algorithm implementation
- Model training and evaluation
- Client-server communication logic
- Machine learning model development

**Files**:
- `server.py` - Federated server implementation
- `client.py` - Federated client implementation
- `model.py` - ML model definitions
- `training_engine.py` - Training logic
- `model_stats.py` - Model statistics tracking
- `requirements.txt` - Python dependencies

---

### Member 2: Cloud Infrastructure & DevOps
**Role**: AWS Integration & Deployment
**Branch**: `feature/cloud-infrastructure`

**Responsibilities**:
- AWS S3 integration
- EC2 deployment automation
- Infrastructure as Code (Terraform)
- CI/CD and deployment scripts

**Files**:
- `s3_helper.py` - S3 integration
- `setup_aws.py` - AWS setup automation
- `upload_to_s3.py` - S3 upload utilities
- `deploy.sh` - Deployment script
- `ec2_bootstrap.sh` - EC2 initialization
- `terraform_deploy.tf` - Terraform configuration
- `docker-compose.yml` - Docker orchestration
- `Dockerfile` - Container definition
- `nginx.conf` - Web server configuration
- `DEPLOYMENT_GUIDE.md` - Deployment documentation

---

### Member 3: Frontend & Web Development
**Role**: User Interface & Web Application
**Branch**: `feature/web-interface`

**Responsibilities**:
- Flask web application
- HTML/CSS/JavaScript frontend
- API endpoints
- User interface design

**Files**:
- `app.py` - Flask application
- `config.py` - Application configuration
- `templates/` - All HTML templates
  - `base.html`
  - `home.html`
  - `upload.html`
  - `train.html`
  - `models.html`
  - `classify.html`
- `static/` - CSS and JavaScript
  - `style.css`
  - `app.js`

---

### Member 4: Data & Documentation
**Role**: Dataset Management & Project Documentation
**Branch**: `feature/data-documentation`

**Responsibilities**:
- Sample data preparation
- Project documentation
- Testing and validation
- User guides and README

**Files**:
- `sample_data/` - Sample datasets
  - `sample_phishing.csv`
- `README.md` - Main documentation
- `.env.example` - Environment template
- `.gitignore` - Git ignore rules
- `verify_setup.py` - Setup verification
- `cleanup.bat` - Cleanup automation
- `CLEANUP_SUMMARY.md` - Cleanup documentation
- `FINAL_CLEANUP_REPORT.md` - Status report

---

## Git Workflow

### Initial Setup
```bash
# Clone repository
git clone <repository-url>
cd fl-phish-cloud

# Each member creates their branch
git checkout -b feature/federated-learning    # Member 1
git checkout -b feature/cloud-infrastructure  # Member 2
git checkout -b feature/web-interface         # Member 3
git checkout -b feature/data-documentation    # Member 4
```

### Development Workflow
```bash
# Work on your files
git add <your-files>
git commit -m "Descriptive commit message"
git push origin <your-branch>

# Create Pull Request on GitHub
# Request code review from team members
```

### Integration
```bash
# Merge to main branch after review
git checkout main
git merge feature/<branch-name>
git push origin main
```

---

## Commit Message Convention

```
<type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Testing
- chore: Maintenance

Examples:
- feat(ml): Implement FedAvg algorithm
- feat(cloud): Add S3 integration
- feat(ui): Create training dashboard
- docs(readme): Add installation guide
```

---

## Collaboration Points

### Member 1 ↔ Member 2
- Model saving/loading from S3
- Training data retrieval from S3

### Member 1 ↔ Member 3
- Training API endpoints
- Model prediction API

### Member 2 ↔ Member 3
- File upload to S3
- Environment configuration

### Member 3 ↔ Member 4
- UI/UX documentation
- Sample data integration

---

## Testing Responsibilities

### Unit Tests
- **Member 1**: test_unit_model.py, test_unit_client.py
- **Member 3**: test_unit_api.py

### Integration Tests
- **Member 1 & Member 2**: test_integration_federated.py
- **Member 2**: test_integration_s3.py

### ML-Specific Tests
- **Member 1**: test_ml_accuracy.py
- **Member 4**: test_ml_data_validation.py

**Test Location**: `division/tests/`
**See**: `division/tests/README_TESTS.md` for details

---

## Timeline Suggestion

### Week 1: Individual Development
- Each member works on their assigned files
- Daily standups to sync progress

### Week 2: Integration
- Merge branches incrementally
- Resolve conflicts together
- Integration testing

### Week 3: Testing & Documentation
- Complete testing
- Finalize documentation
- Prepare presentation

---

## Communication

- **Daily Standups**: 15 min sync
- **Code Reviews**: Required for all PRs
- **Documentation**: Update as you code
- **Issues**: Use GitHub Issues for bugs/features

---

## Success Criteria

✅ All branches merged successfully  
✅ Application runs without errors  
✅ All features working as expected  
✅ Complete documentation  
✅ Successful AWS deployment  
✅ Demo-ready presentation
