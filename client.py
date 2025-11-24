import pandas as pd
import numpy as np
from model import FederatedModel
from sklearn.metrics import accuracy_score

class FederatedClient:
    def __init__(self, client_id, data_path):
        self.client_id = client_id
        self.data_path = data_path
        self.model = FederatedModel()
        self.X_train = None
        self.y_train = None
        self.load_data()

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            
            # Auto-detect CSV format
            if 'text' in df.columns and 'label' in df.columns:
                self.X_train = df['text'].astype(str).tolist()
                self.y_train = df['label'].tolist()
            elif 'body' in df.columns and 'label' in df.columns:
                self.X_train = df['body'].astype(str).tolist()
                self.y_train = df['label'].tolist()
            elif 'text_combined' in df.columns and 'label' in df.columns:
                self.X_train = df['text_combined'].astype(str).tolist()
                self.y_train = df['label'].tolist()
            else:
                # Fallback: use first text column and last column as label
                text_cols = df.select_dtypes(include=['object']).columns
                if len(text_cols) > 0:
                    self.X_train = df[text_cols[0]].astype(str).tolist()
                    self.y_train = df.iloc[:, -1].tolist()
                else:
                    raise ValueError("No suitable text column found")

            # Handle single class datasets
            unique_labels = set(self.y_train)
            if len(unique_labels) == 1:
                # Add synthetic opposite class samples
                label = list(unique_labels)[0]
                opposite_label = 1 - label if label in [0, 1] else 0
                synthetic_texts = ["Normal email content", "Regular message", "Standard communication"]
                self.X_train.extend(synthetic_texts)
                self.y_train.extend([opposite_label] * len(synthetic_texts))

            print(f"Client {self.client_id}: Loaded {len(self.X_train)} samples")
            
        except Exception as e:
            print(f"Client {self.client_id}: Error loading data - {e}")
            self.X_train = []
            self.y_train = []

    def train_local_model(self, global_weights=None):
        if len(self.X_train) < 2:
            return None
            
        if global_weights:
            self.model.set_weights(global_weights)
        
        self.model.fit(self.X_train, self.y_train)
        return self.model.get_weights()

    def evaluate_model(self, X_test, y_test):
        if not self.model.is_fitted:
            return 0.0
        predictions = self.model.predict(X_test)
        return accuracy_score(y_test, predictions)