"""
Pytest Configuration
Shared fixtures and setup for all tests
"""

import pytest
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../member1'))
sys.path.insert(0, os.path.abspath('../../member2'))
sys.path.insert(0, os.path.abspath('../../member3'))


@pytest.fixture
def sample_data():
    """Provide sample training data"""
    import numpy as np
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    y = np.array([0, 1, 0])
    return X, y


@pytest.fixture
def temp_csv():
    """Create temporary CSV file"""
    import tempfile
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("phishing email,1\n")
    temp_file.write("legitimate email,0\n")
    temp_file.close()
    
    yield temp_file.name
    
    # Cleanup
    os.unlink(temp_file.name)
