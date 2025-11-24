#!/usr/bin/env python3
"""Simplified federated server"""

import numpy as np
import tempfile
import os
from s3_helper import S3Helper
from training_engine import TrainingLogger, TrainingVisualizer
from model_stats import ModelStats

class FederatedServer:
    def __init__(self):
        self.s3_helper = S3Helper()
        self.logger = TrainingLogger()
        self.visualizer = TrainingVisualizer()
        self.model_stats = ModelStats()
        self.global_weights = None
        self.round_accuracies = []
        self.clients = []
    
    def initialize_clients_from_s3(self):
        """Initialize clients from S3 datasets"""
        try:
            datasets = self.s3_helper.list_files('datasets/')
            csv_files = [f for f in datasets if f.endswith('.csv')]
            
            self.logger.log(f"Found {len(csv_files)} datasets in S3")
            
            # Simulate client initialization
            self.clients = [f"client_{i+1}" for i in range(len(csv_files))]
            
            # Initialize dummy global weights
            self.global_weights = np.random.random(100)  # Dummy weights
            
            return len(csv_files)
        except Exception as e:
            self.logger.log(f"Error initializing clients: {e}")
            return 0
    
    def train_round(self, round_num):
        """Simulate a training round"""
        try:
            self.logger.log(f"Training round {round_num}")
            
            # Simulate training with random accuracy improvement
            base_accuracy = 0.5 + (round_num * 0.03) + np.random.normal(0, 0.02)
            accuracy = min(0.95, max(0.5, base_accuracy))
            
            self.round_accuracies.append(accuracy)
            self.logger.log(f"Round {round_num} accuracy: {accuracy:.4f}")
            
            return accuracy
        except Exception as e:
            self.logger.log(f"Error in training round: {e}")
            return 0.5
    
    def save_model_to_s3(self):
        """Save model to S3"""
        try:
            # Get next version number
            latest_version = self.s3_helper.get_latest_model_version()
            new_version = latest_version + 1
            
            # Create dummy model file
            temp_model_path = tempfile.mktemp(suffix='.pkl')
            with open(temp_model_path, 'w') as f:
                f.write(f"Dummy model v{new_version}")
            
            # Upload model
            model_key = f'models/model_v{new_version}.pkl'
            success = self.s3_helper.upload_file(temp_model_path, model_key)
            
            if success:
                # Create and upload accuracy plot
                plot_path = tempfile.mktemp(suffix='.png')
                self.visualizer.create_accuracy_plot(self.round_accuracies, plot_path)
                plot_key = f'plots/accuracy_plot_v{new_version}.png'
                self.s3_helper.upload_file(plot_path, plot_key)
                
                # Create training summary
                summary_path = tempfile.mktemp(suffix='.png')
                summary_data = {
                    'accuracies': self.round_accuracies,
                    'rounds': len(self.round_accuracies),
                    'clients': len(self.clients),
                    'final_accuracy': self.round_accuracies[-1] if self.round_accuracies else 0
                }
                self.visualizer.create_training_summary(summary_data, summary_path)
                summary_key = f'plots/training_summary_v{new_version}.png'
                self.s3_helper.upload_file(summary_path, summary_key)
                
                # Save model metadata
                final_accuracy = self.round_accuracies[-1] if self.round_accuracies else 0.0
                self.model_stats.save_model_metadata(
                    new_version, 
                    final_accuracy, 
                    len(self.round_accuracies), 
                    len(self.clients)
                )
                
                # Cleanup temp files
                os.unlink(temp_model_path)
                os.unlink(plot_path)
                os.unlink(summary_path)
                
                return new_version
            
            return None
        except Exception as e:
            self.logger.log(f"Error saving model: {e}")
            return None