"""
Unit Tests - Model Functions
Member 1: Backend & ML Engineer
"""

import pytest
import numpy as np
from sklearn.linear_model import LogisticRegression


def test_model_initialization():
    """Test model can be initialized"""
    from model import FederatedModel
    model = FederatedModel()
    assert model is not None


def test_model_training():
    """Test model training with sample data"""
    from model import FederatedModel
    
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    y_train = np.array([0, 1, 0])
    
    model.train(X_train, y_train)
    assert model.model is not None


def test_model_prediction():
    """Test model prediction"""
    from model import FederatedModel
    
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6]])
    y_train = np.array([0, 1])
    
    model.train(X_train, y_train)
    prediction = model.predict([[2, 3, 4]])
    
    assert prediction is not None
    assert prediction[0] in [0, 1]


def test_get_weights():
    """Test getting model weights"""
    from model import FederatedModel
    
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6]])
    y_train = np.array([0, 1])
    
    model.train(X_train, y_train)
    weights = model.get_weights()
    
    assert weights is not None
    assert len(weights) > 0


def test_set_weights():
    """Test setting model weights"""
    from model import FederatedModel
    
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6]])
    y_train = np.array([0, 1])
    
    model.train(X_train, y_train)
    original_weights = model.get_weights()
    
    # Set new weights
    new_weights = [w * 1.1 for w in original_weights]
    model.set_weights(new_weights)
    
    updated_weights = model.get_weights()
    assert not np.array_equal(original_weights, updated_weights)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
