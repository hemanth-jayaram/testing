# Team Collaboration Guide

## Project: Federated Learning for Phishing Email Detection

---

## Quick Start for Each Member

### Member 1 (Backend & ML)
```bash
cd division/member1
# Review README_MEMBER1.md
# Work on: server.py, client.py, model.py, training_engine.py, model_stats.py
```

### Member 2 (Cloud & DevOps)
```bash
cd division/member2
# Review README_MEMBER2.md
# Work on: s3_helper.py, deploy.sh, terraform_deploy.tf, docker files
```

### Member 3 (Frontend & Web)
```bash
cd division/member3
# Review README_MEMBER3.md
# Work on: app.py, templates/, static/
```

### Member 4 (Data & Docs)
```bash
cd division/member4
# Review README_MEMBER4.md
# Work on: README.md, sample_data/, verify_setup.py
```

---

## GitHub Repository Setup

### 1. Create Repository
```bash
# On GitHub, create new repository: fl-phish-cloud
# Initialize with README
```

### 2. Clone and Setup
```bash
git clone https://github.com/your-team/fl-phish-cloud.git
cd fl-phish-cloud

# Copy all original files to repository
# (Not from division folders - those are for reference)
```

### 3. Each Member Creates Branch
```bash
# Member 1
git checkout -b feature/federated-learning

# Member 2
git checkout -b feature/cloud-infrastructure

# Member 3
git checkout -b feature/web-interface

# Member 4
git checkout -b feature/data-documentation
```

---

## Development Workflow

### Step 1: Work on Your Files
```bash
# Edit your assigned files
# Test locally
# Make sure code works
```

### Step 2: Commit Changes
```bash
git add <your-files>
git commit -m "feat(scope): description"
git push origin <your-branch>
```

### Step 3: Create Pull Request
1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Add description of changes
5. Request review from team members

### Step 4: Code Review
- At least 1 team member must review
- Address feedback
- Get approval

### Step 5: Merge to Main
```bash
# After approval
git checkout main
git merge <your-branch>
git push origin main
```

---

## Commit Message Format

```
<type>(<scope>): <subject>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Testing

Scopes:
- ml: Machine learning
- cloud: Cloud infrastructure
- web: Web application
- ui: User interface
- data: Data/datasets
- docs: Documentation

Examples:
feat(ml): Implement FedAvg algorithm
feat(cloud): Add S3 integration
feat(web): Create training dashboard
docs(readme): Add installation guide
fix(ui): Fix training progress display
```

---

## Integration Timeline

### Week 1: Individual Development
**Days 1-2**: Setup and initial implementation
- Each member works on their files
- Daily 15-min standup

**Days 3-5**: Complete core features
- Finish main functionality
- Write basic tests
- Document your code

**Days 6-7**: Testing and refinement
- Test your components
- Fix bugs
- Prepare for integration

### Week 2: Integration
**Days 8-9**: First integration
- Member 1 + Member 2: ML with S3
- Member 3 + Member 4: Web with docs

**Days 10-11**: Full integration
- Merge all branches
- Resolve conflicts
- Integration testing

**Days 12-14**: Testing and polish
- End-to-end testing
- Bug fixes
- Performance optimization

### Week 3: Deployment and Presentation
**Days 15-17**: Deployment
- Deploy to AWS EC2
- Final testing in production
- Documentation updates

**Days 18-21**: Presentation prep
- Create demo
- Prepare slides
- Practice presentation

---

## Communication

### Daily Standup (15 min)
- What did you do yesterday?
- What will you do today?
- Any blockers?

### Code Review Guidelines
- Review within 24 hours
- Be constructive and respectful
- Test the code before approving
- Check for security issues

### Conflict Resolution
1. Try to resolve together first
2. If stuck, discuss as team
3. Vote if needed (majority wins)
4. Document decision

---

## Testing Responsibilities

### Member 1: ML Testing
```python
# Test model training
# Test FedAvg algorithm
# Test prediction accuracy
```

### Member 2: Infrastructure Testing
```bash
# Test S3 upload/download
# Test deployment scripts
# Test Docker containers
```

### Member 3: Web Testing
```python
# Test API endpoints
# Test UI functionality
# Test form validation
```

### Member 4: Integration Testing
```python
# Test end-to-end workflow
# Test with sample data
# Verify documentation accuracy
```

---

## File Dependencies

```
app.py (Member 3)
├── server.py (Member 1)
├── client.py (Member 1)
├── model.py (Member 1)
├── training_engine.py (Member 1)
├── model_stats.py (Member 1)
├── s3_helper.py (Member 2)
├── config.py (Member 3)
└── templates/ (Member 3)

s3_helper.py (Member 2)
└── Used by: server.py, app.py

sample_data/ (Member 4)
└── Used by: app.py, testing
```

---

## Common Issues and Solutions

### Merge Conflicts
```bash
# Update your branch with main
git checkout main
git pull
git checkout <your-branch>
git merge main
# Resolve conflicts
git add .
git commit -m "fix: Resolve merge conflicts"
```

### Import Errors
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### AWS Credentials
```bash
# Never commit credentials!
# Use .env file (in .gitignore)
# Set environment variables
```

---

## Success Metrics

- [ ] All 4 branches created
- [ ] Each member has 5+ commits
- [ ] All branches merged to main
- [ ] Application runs without errors
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Successfully deployed to AWS
- [ ] Demo presentation ready

---

## Emergency Contacts

- **Technical Issues**: Discuss in team chat
- **Git Problems**: Ask Member 2 (DevOps)
- **Code Questions**: Ask relevant member
- **Deadline Issues**: Notify team immediately

---

## Final Checklist

### Before Merging
- [ ] Code works locally
- [ ] Tests pass
- [ ] No console errors
- [ ] Code is documented
- [ ] Commit messages are clear
- [ ] No sensitive data in code

### Before Deployment
- [ ] All branches merged
- [ ] Integration tests pass
- [ ] AWS credentials configured
- [ ] Environment variables set
- [ ] Documentation updated
- [ ] Demo data prepared

### Before Presentation
- [ ] Application deployed
- [ ] Demo script prepared
- [ ] Slides ready
- [ ] Each member knows their part
- [ ] Backup plan ready

---

## Resources

- **Git Tutorial**: https://git-scm.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **AWS S3 Docs**: https://docs.aws.amazon.com/s3/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **Scikit-learn**: https://scikit-learn.org/

---

**Remember**: Communication is key! Ask questions, help each other, and work as a team.

Good luck! 🚀
