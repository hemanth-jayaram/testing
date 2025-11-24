"""
Integration Tests - Federated Learning Workflow
Member 1 & Member 2: ML + Cloud Integration
"""

import pytest
import tempfile
import os


def test_server_client_integration():
    """Test server and client integration"""
    from server import FederatedServer
    from client import FederatedClient
    
    # Create temporary dataset
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("phishing email,1\n")
    temp_file.write("legitimate email,0\n")
    temp_file.close()
    
    try:
        # Initialize server
        server = FederatedServer()
        
        # Initialize client
        client = FederatedClient(client_id=1)
        client.load_data(temp_file.name)
        
        # Get initial weights from server
        initial_weights = server.get_global_weights()
        
        # Client trains
        updated_weights = client.train(initial_weights, epochs=1)
        
        assert updated_weights is not None
    finally:
        os.unlink(temp_file.name)


def test_federated_averaging():
    """Test federated averaging with multiple clients"""
    from server import FederatedServer
    import numpy as np
    
    server = FederatedServer()
    
    # Simulate client weights
    client_weights_1 = [np.array([1.0, 2.0, 3.0])]
    client_weights_2 = [np.array([2.0, 3.0, 4.0])]
    
    all_weights = [client_weights_1, client_weights_2]
    data_sizes = [100, 100]
    
    # Perform averaging
    server.federated_averaging(all_weights, data_sizes)
    
    averaged = server.get_global_weights()
    assert averaged is not None


def test_model_save_load():
    """Test model saving and loading"""
    from model import FederatedModel
    import numpy as np
    import pickle
    
    # Train model
    model = FederatedModel()
    X_train = np.array([[1, 2, 3], [4, 5, 6]])
    y_train = np.array([0, 1])
    model.train(X_train, y_train)
    
    # Save model
    temp_file = tempfile.mktemp(suffix='.pkl')
    model.save_model(temp_file)
    
    try:
        # Load model
        loaded_model = FederatedModel()
        loaded_model.load_model(temp_file)
        
        # Test prediction
        prediction = loaded_model.predict([[2, 3, 4]])
        assert prediction is not None
    finally:
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_training_engine_logging():
    """Test training engine logging"""
    from training_engine import TrainingLogger
    
    logger = TrainingLogger()
    
    # Log some events
    logger.log("Test log message")
    logger.log_round(1, 0.75)
    
    # Get logs
    logs = logger.get_recent_logs(5)
    assert len(logs) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
