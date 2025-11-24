"""
Unit Tests - Client Functions
Member 1: Backend & ML Engineer
"""

import pytest
import numpy as np


def test_client_initialization():
    """Test client can be initialized"""
    from client import FederatedClient
    client = FederatedClient(client_id=1)
    assert client.client_id == 1


def test_client_load_data():
    """Test client can load data"""
    from client import FederatedClient
    import pandas as pd
    import tempfile
    import os
    
    # Create temporary CSV
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("test email 1,0\n")
    temp_file.write("test email 2,1\n")
    temp_file.close()
    
    try:
        client = FederatedClient(client_id=1)
        client.load_data(temp_file.name)
        
        assert client.X_train is not None
        assert client.y_train is not None
    finally:
        os.unlink(temp_file.name)


def test_client_train():
    """Test client local training"""
    from client import FederatedClient
    import pandas as pd
    import tempfile
    import os
    
    # Create temporary CSV
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("phishing email,1\n")
    temp_file.write("legitimate email,0\n")
    temp_file.write("spam message,1\n")
    temp_file.close()
    
    try:
        client = FederatedClient(client_id=1)
        client.load_data(temp_file.name)
        
        # Train with initial weights
        initial_weights = None
        updated_weights = client.train(initial_weights, epochs=1)
        
        assert updated_weights is not None
    finally:
        os.unlink(temp_file.name)


def test_client_get_data_size():
    """Test getting client data size"""
    from client import FederatedClient
    import tempfile
    import os
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("email 1,0\n")
    temp_file.write("email 2,1\n")
    temp_file.close()
    
    try:
        client = FederatedClient(client_id=1)
        client.load_data(temp_file.name)
        
        size = client.get_data_size()
        assert size > 0
    finally:
        os.unlink(temp_file.name)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
