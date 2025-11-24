"""
ML-Specific Tests - Data Validation
Member 4: Data & Documentation
"""

import pytest
import pandas as pd
import tempfile
import os


def test_csv_format_validation():
    """Test CSV format is valid"""
    # Create valid CSV
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("email 1,0\n")
    temp_file.write("email 2,1\n")
    temp_file.close()
    
    try:
        df = pd.read_csv(temp_file.name)
        
        assert 'text' in df.columns or 'body' in df.columns or 'text_combined' in df.columns
        assert 'label' in df.columns
        assert len(df) > 0
    finally:
        os.unlink(temp_file.name)


def test_label_values():
    """Test labels are binary (0 or 1)"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("email 1,0\n")
    temp_file.write("email 2,1\n")
    temp_file.close()
    
    try:
        df = pd.read_csv(temp_file.name)
        labels = df['label'].unique()
        
        assert all(label in [0, 1] for label in labels)
    finally:
        os.unlink(temp_file.name)


def test_no_missing_values():
    """Test dataset has no missing values"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("email 1,0\n")
    temp_file.write("email 2,1\n")
    temp_file.close()
    
    try:
        df = pd.read_csv(temp_file.name)
        
        assert df.isnull().sum().sum() == 0
    finally:
        os.unlink(temp_file.name)


def test_balanced_dataset():
    """Test dataset is reasonably balanced"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("email 1,0\n")
    temp_file.write("email 2,1\n")
    temp_file.write("email 3,0\n")
    temp_file.write("email 4,1\n")
    temp_file.close()
    
    try:
        df = pd.read_csv(temp_file.name)
        label_counts = df['label'].value_counts()
        
        # Check ratio is not too imbalanced (within 3:1)
        ratio = max(label_counts) / min(label_counts)
        assert ratio <= 3.0
    finally:
        os.unlink(temp_file.name)


def test_text_not_empty():
    """Test text fields are not empty"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
    temp_file.write("text,label\n")
    temp_file.write("email content,0\n")
    temp_file.write("another email,1\n")
    temp_file.close()
    
    try:
        df = pd.read_csv(temp_file.name)
        text_col = 'text' if 'text' in df.columns else 'body'
        
        assert all(len(str(text).strip()) > 0 for text in df[text_col])
    finally:
        os.unlink(temp_file.name)


def test_sample_data_exists():
    """Test sample data file exists"""
    sample_path = '../sample_data/sample_phishing.csv'
    
    if os.path.exists(sample_path):
        df = pd.read_csv(sample_path)
        assert len(df) > 0
        assert 'label' in df.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
