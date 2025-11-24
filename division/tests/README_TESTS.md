# Testing Suite - FL Phishing Detection

## Test Organization

### Unit Tests
**Assigned to: Member 1 (ML) & Member 3 (Web)**

- `test_unit_model.py` - Model function tests (Member 1)
- `test_unit_client.py` - Client function tests (Member 1)
- `test_unit_api.py` - API endpoint tests (Member 3)

### Integration Tests
**Assigned to: Member 1 & Member 2**

- `test_integration_s3.py` - S3 operations (Member 2)
- `test_integration_federated.py` - Federated workflow (Member 1 & 2)

### ML-Specific Tests
**Assigned to: Member 1 & Member 4**

- `test_ml_accuracy.py` - Model accuracy tests (Member 1)
- `test_ml_data_validation.py` - Data validation (Member 4)

---

## Test Assignment by Member

### Member 1: Backend & ML Engineer
**Branch**: `feature/federated-learning`
**Tests**:
- test_unit_model.py
- test_unit_client.py
- test_integration_federated.py
- test_ml_accuracy.py

### Member 2: Cloud Infrastructure & DevOps
**Branch**: `feature/cloud-infrastructure`
**Tests**:
- test_integration_s3.py
- test_integration_federated.py (collaborate with Member 1)

### Member 3: Frontend & Web Development
**Branch**: `feature/web-interface`
**Tests**:
- test_unit_api.py

### Member 4: Data & Documentation
**Branch**: `feature/data-documentation`
**Tests**:
- test_ml_data_validation.py

---

## Running Tests

### Install Testing Dependencies
```bash
pip install pytest pytest-cov pytest-flask
```

### Run All Tests
```bash
cd division/tests
pytest -v
```

### Run Specific Test File
```bash
pytest test_unit_model.py -v
```

### Run Tests with Coverage
```bash
pytest --cov=../../ --cov-report=html
```

### Run Tests by Member
```bash
# Member 1
pytest test_unit_model.py test_unit_client.py test_ml_accuracy.py -v

# Member 2
pytest test_integration_s3.py -v

# Member 3
pytest test_unit_api.py -v

# Member 4
pytest test_ml_data_validation.py -v
```

---

## Test Descriptions

### Unit Tests

**test_unit_model.py**
- Model initialization
- Training functionality
- Prediction accuracy
- Weight get/set operations

**test_unit_client.py**
- Client initialization
- Data loading
- Local training
- Data size retrieval

**test_unit_api.py**
- Page loading (home, upload, train, etc.)
- API endpoints functionality
- Error handling
- Response validation

### Integration Tests

**test_integration_s3.py**
- S3 connection
- File upload/download
- Model versioning
- Bucket operations

**test_integration_federated.py**
- Server-client communication
- Federated averaging
- Model save/load
- Training workflow

### ML-Specific Tests

**test_ml_accuracy.py**
- Minimum accuracy threshold
- Prediction consistency
- FedAvg convergence
- Overfitting detection
- Probability validation

**test_ml_data_validation.py**
- CSV format validation
- Label correctness
- Missing value detection
- Dataset balance
- Text field validation

---

## Test Coverage Goals

- **Unit Tests**: 80% coverage
- **Integration Tests**: 70% coverage
- **ML Tests**: 90% coverage
- **Overall**: 75% coverage

---

## Continuous Integration

Add to `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          cd division/tests
          pytest --cov=../../ --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Before Merging Checklist

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] ML accuracy tests pass
- [ ] Code coverage > 75%
- [ ] No failing tests
- [ ] Tests documented

---

## Writing New Tests

### Template for Unit Test
```python
def test_function_name():
    """Test description"""
    # Arrange
    input_data = ...
    
    # Act
    result = function(input_data)
    
    # Assert
    assert result == expected
```

### Template for Integration Test
```python
def test_integration_scenario():
    """Test integration between components"""
    # Setup
    component1 = Component1()
    component2 = Component2()
    
    # Execute workflow
    result = component1.process()
    output = component2.use(result)
    
    # Verify
    assert output is not None
```

---

## Common Issues

### Import Errors
```bash
# Add parent directory to Python path
export PYTHONPATH="${PYTHONPATH}:../.."
```

### AWS Credentials for Tests
```bash
# Use mock or test credentials
export AWS_ACCESS_KEY_ID="test"
export AWS_SECRET_ACCESS_KEY="test"
```

### Temporary Files
```python
# Always clean up
import tempfile
temp = tempfile.NamedTemporaryFile(delete=False)
try:
    # Use temp file
finally:
    os.unlink(temp.name)
```

---

## Test Results

Track test results in each PR:
- Number of tests: X
- Passed: Y
- Failed: Z
- Coverage: W%
