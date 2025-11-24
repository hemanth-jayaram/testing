"""
Unit Tests - API Endpoints
Member 3: Frontend & Web Developer
"""

import pytest
from flask import Flask


@pytest.fixture
def client():
    """Create test client"""
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200


def test_upload_page(client):
    """Test upload page loads"""
    response = client.get('/upload')
    assert response.status_code == 200


def test_train_page(client):
    """Test train page loads"""
    response = client.get('/train')
    assert response.status_code == 200


def test_models_page(client):
    """Test models page loads"""
    response = client.get('/models')
    assert response.status_code == 200


def test_classify_page(client):
    """Test classify page loads"""
    response = client.get('/classify')
    assert response.status_code == 200


def test_training_status_api(client):
    """Test training status API"""
    response = client.get('/api/training_status')
    assert response.status_code == 200
    assert response.json is not None


def test_stats_api(client):
    """Test stats API"""
    response = client.get('/api/stats')
    assert response.status_code == 200
    assert 'dataset_count' in response.json


def test_classify_api_no_text(client):
    """Test classify API without text"""
    response = client.post('/api/classify', data={})
    assert response.status_code == 200
    assert response.json['success'] == False


def test_train_api_invalid_rounds(client):
    """Test train API with invalid rounds"""
    response = client.post('/api/train', data={'rounds': 0})
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
