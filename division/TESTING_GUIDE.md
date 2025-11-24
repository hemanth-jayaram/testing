# Testing Guide - FL Phishing Detection

## Testing Responsibilities by Member

### Member 1 (ML Engineer) - ML & Algorithm Testing
**Focus**: Model accuracy, federated learning correctness

**Tests**:
- Model training produces valid weights
- FedAvg aggregation is mathematically correct
- Predictions are consistent
- Model accuracy improves over rounds
- TF-IDF vectorization works correctly

### Member 2 (DevOps) - Infrastructure & Integration Testing
**Focus**: AWS, deployment, system integration

**Tests**:
- S3 upload/download works
- Deployment scripts execute successfully
- Docker containers build and run
- Nginx routes traffic correctly
- EC2 instance setup completes

### Member 3 (Frontend) - API & UI Testing
**Focus**: Web functionality, user experience

**Tests**:
- All API endpoints return correct responses
- Forms validate input properly
- File uploads work
- Real-time updates display correctly
- Error messages show appropriately

### Member 4 (Documentation) - End-to-End & Acceptance Testing
**Focus**: Complete workflows, user scenarios

**Tests**:
- Full workflow: upload → train → classify
- Documentation accuracy
- Setup instructions work
- Sample data is valid
- User can complete all tasks

---

## Test Types

### 1. Unit Tests
```python
# test_model.py
def test_model_training():
    model = FederatedModel()
    X_train = [[1, 2, 3], [4, 5, 6]]
    y_train = [0, 1]
    model.train(X_train, y_train)
    assert model.weights is not None

def test_prediction():
    model = FederatedModel()
    # Load trained model
    prediction = model.predict([[1, 2, 3]])
    assert prediction in [0, 1]
```

### 2. Integration Tests
```python
# test_integration.py
def test_s3_model_storage():
    # Train model
    server = FederatedServer()
    server.train_round(1)
    
    # Save to S3
    version = server.save_model_to_s3()
    
    # Load from S3
    loaded_model = load_model_from_s3(version)
    assert loaded_model is not None
```

### 3. API Tests
```python
# test_api.py
def test_train_endpoint():
    response = client.post('/api/train', data={'rounds': 5})
    assert response.status_code == 200
    assert response.json['success'] == True

def test_classify_endpoint():
    response = client.post('/api/classify', 
                          data={'email_text': 'Test email'})
    assert 'prediction' in response.json
```

### 4. ML Accuracy Tests
```python
# test_ml_accuracy.py
def test_model_accuracy():
    # Load test dataset
    X_test, y_test = load_test_data()
    
    # Load trained model
    model = load_latest_model()
    
    # Evaluate
    accuracy = model.evaluate(X_test, y_test)
    assert accuracy > 0.7  # Minimum 70% accuracy
```

### 5. Security Tests
```python
# test_security.py
def test_file_upload_validation():
    # Try uploading non-CSV file
    response = client.post('/upload', 
                          files={'file': 'malicious.exe'})
    assert response.status_code == 400

def test_sql_injection():
    response = client.post('/api/classify',
                          data={'email_text': "'; DROP TABLE--"})
    assert response.status_code == 200  # Should handle safely
```

### 6. Performance Tests
```python
# test_performance.py
def test_training_time():
    import time
    start = time.time()
    
    server = FederatedServer()
    server.train_round(1)
    
    duration = time.time() - start
    assert duration < 60  # Should complete in under 60 seconds
```

---

## Test Files to Create

```
tests/
├── test_model.py              # Member 1
├── test_federated.py          # Member 1
├── test_s3_integration.py     # Member 2
├── test_deployment.py         # Member 2
├── test_api.py                # Member 3
├── test_ui.py                 # Member 3
├── test_end_to_end.py         # Member 4
└── test_data_validation.py    # Member 4
```

---

## Running Tests

```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-flask

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_model.py

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_model.py::test_model_training
```

---

## Test Checklist

### Before Merging PR
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] No security vulnerabilities
- [ ] Code coverage > 70%
- [ ] Manual testing completed

### Before Deployment
- [ ] All tests pass on main branch
- [ ] Performance tests acceptable
- [ ] Security scan completed
- [ ] End-to-end workflow tested
- [ ] Documentation updated

---

## Continuous Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
```
