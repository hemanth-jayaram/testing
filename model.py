#!/usr/bin/env python3
"""Simplified federated model"""

import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class FederatedModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = LogisticRegression()
        self.is_trained = False
    
    def train(self, texts, labels):
        """Train the model"""
        try:
            # Vectorize texts
            X = self.vectorizer.fit_transform(texts)
            
            # Train classifier
            self.classifier.fit(X, labels)
            self.is_trained = True
            
            return True
        except Exception as e:
            print(f"Training error: {e}")
            return False
    
    def predict(self, texts):
        """Make predictions"""
        if not self.is_trained:
            # Return dummy predictions
            return np.random.randint(0, 2, len(texts))
        
        try:
            X = self.vectorizer.transform(texts)
            return self.classifier.predict(X)
        except Exception as e:
            print(f"Prediction error: {e}")
            return np.random.randint(0, 2, len(texts))
    
    def predict_proba(self, texts):
        """Get prediction probabilities"""
        if not self.is_trained:
            # Return dummy probabilities
            return np.random.random((len(texts), 2))
        
        try:
            X = self.vectorizer.transform(texts)
            return self.classifier.predict_proba(X)
        except Exception as e:
            print(f"Probability prediction error: {e}")
            return np.random.random((len(texts), 2))
    
    def save_model(self, filepath):
        """Save model to file"""
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'is_trained': self.is_trained
            }
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False
    
    def load_model(self, filepath):
        """Load model from file"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data.get('vectorizer', self.vectorizer)
            self.classifier = model_data.get('classifier', self.classifier)
            self.is_trained = model_data.get('is_trained', False)
            
            return True
        except Exception as e:
            print(f"Load error: {e}")
            return False