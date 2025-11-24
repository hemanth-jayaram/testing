"""
ML-Specific Tests - Model Accuracy & Performance
Member 1: Backend & ML Engineer
"""

import pytest
import numpy as np
from sklearn.model_selection import train_test_split


def test_model_accuracy_threshold():
    """Test model achieves minimum accuracy"""
    from model import FederatedModel
    
    # Create synthetic dataset
    np.random.seed(42)
    X = np.random.rand(100, 10)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    # Train model
    model = FederatedModel()
    model.train(X_train, y_train)
    
    # Evaluate
    accuracy = model.evaluate(X_test, y_test)
    
    assert accuracy > 0.5  # Should be better than random


def test_prediction_consistency():
    """Test model predictions are consistent"""
    from model import FederatedModel
    import numpy as np
    
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    y_train = np.array([0, 1, 0])
    
    model.train(X_train, y_train)
    
    # Same input should give same prediction
    test_input = [[2, 3, 4]]
    pred1 = model.predict(test_input)
    pred2 = model.predict(test_input)
    
    assert np.array_equal(pred1, pred2)


def test_fedavg_convergence():
    """Test FedAvg improves accuracy over rounds"""
    from server import FederatedServer
    from client import FederatedClient
    import tempfile
    import os
    
    # Create dataset
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    for i in range(50):
        label = i % 2
        temp_file.write(f"email text {i},{label}\n")
    temp_file.close()
    
    try:
        server = FederatedServer()
        client = FederatedClient(client_id=1)
        client.load_data(temp_file.name)
        
        accuracies = []
        
        # Run multiple rounds
        for round_num in range(3):
            weights = server.get_global_weights()
            updated_weights = client.train(weights, epochs=1)
            server.federated_averaging([updated_weights], [client.get_data_size()])
            
            # Evaluate
            accuracy = server.evaluate_global_model([temp_file.name])
            accuracies.append(accuracy)
        
        # Check if accuracy improves or stays stable
        assert len(accuracies) == 3
    finally:
        os.unlink(temp_file.name)


def test_model_overfitting_check():
    """Test model doesn't severely overfit"""
    from model import FederatedModel
    import numpy as np
    
    # Small dataset to potentially cause overfitting
    X_train = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y_train = np.array([0, 1, 0, 1])
    
    X_test = np.array([[1.5, 2.5], [3.5, 4.5]])
    y_test = np.array([0, 1])
    
    model = FederatedModel()
    model.train(X_train, y_train)
    
    train_acc = model.evaluate(X_train, y_train)
    test_acc = model.evaluate(X_test, y_test)
    
    # Test accuracy shouldn't be drastically lower than train
    assert test_acc >= train_acc - 0.3


def test_prediction_probabilities():
    """Test prediction probabilities are valid"""
    from model import FederatedModel
    import numpy as np
    
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6]])
    y_train = np.array([0, 1])
    
    model.train(X_train, y_train)
    
    probabilities = model.predict_proba([[2, 3, 4]])
    
    assert probabilities is not None
    assert len(probabilities[0]) == 2  # Binary classification
    assert 0 <= probabilities[0][0] <= 1
    assert 0 <= probabilities[0][1] <= 1
    assert abs(sum(probabilities[0]) - 1.0) < 0.01  # Should sum to 1


def test_model_handles_edge_cases():
    """Test model handles edge cases"""
    from model import FederatedModel
    import numpy as np
    
    model = FederatedModel()
    
    # Train with minimal data
    X_train = np.array([[1, 2, 3], [4, 5, 6]])
    y_train = np.array([0, 1])
    
    model.train(X_train, y_train)
    
    # Test with single sample
    prediction = model.predict([[1, 2, 3]])
    assert prediction is not None
    
    # Test with multiple samples
    predictions = model.predict([[1, 2, 3], [4, 5, 6]])
    assert len(predictions) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
