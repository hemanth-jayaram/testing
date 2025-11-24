# Member 1: Backend & ML Engineer

## Role: Federated Learning Implementation & Model Development

### Your Responsibilities
- Implement federated learning algorithm (FedAvg)
- Develop and train machine learning models
- Create client-server communication logic
- Handle model training and evaluation

### Your Files
1. **server.py** - Federated server implementation
2. **client.py** - Federated client implementation
3. **model.py** - ML model definitions
4. **training_engine.py** - Training logic and logging
5. **model_stats.py** - Model statistics tracking
6. **requirements.txt** - Python dependencies

### Git Branch
```bash
git checkout -b feature/federated-learning
```

### Key Tasks
1. Implement FedAvg algorithm in server.py
2. Create client training logic in client.py
3. Define ML models (Logistic Regression, TF-IDF)
4. Add training logging and metrics
5. Implement model evaluation functions

### Testing
```bash
# Test model training
python -c "from model import FederatedModel; m = FederatedModel(); print('OK')"

# Test server initialization
python -c "from server import FederatedServer; s = FederatedServer(); print('OK')"
```

### Integration Points
- **With Member 2**: Model saving/loading from S3
- **With Member 3**: Training API endpoints, prediction API

### Commit Examples
```bash
git add server.py client.py
git commit -m "feat(ml): Implement FedAvg algorithm"

git add model.py
git commit -m "feat(ml): Add logistic regression model"

git add training_engine.py
git commit -m "feat(ml): Add training logger and metrics"
```
