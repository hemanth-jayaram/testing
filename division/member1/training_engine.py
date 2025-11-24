#!/usr/bin/env python3
"""Simplified training engine without pandas dependency"""

import matplotlib.pyplot as plt
import os
from datetime import datetime

class TrainingLogger:
    def __init__(self):
        self.logs = []
    
    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_recent_logs(self, count=5):
        return self.logs[-count:] if self.logs else []

class TrainingVisualizer:
    def __init__(self):
        pass
    
    def create_accuracy_plot(self, accuracies, save_path=None):
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(accuracies) + 1), accuracies, 'b-o')
        plt.title('Federated Learning Accuracy')
        plt.xlabel('Round')
        plt.ylabel('Accuracy')
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()
    
    def create_training_summary(self, data, save_path=None):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Accuracy plot
        if 'accuracies' in data:
            ax1.plot(data['accuracies'], 'b-o')
            ax1.set_title('Training Accuracy')
            ax1.set_xlabel('Round')
            ax1.set_ylabel('Accuracy')
            ax1.grid(True)
        
        # Summary stats
        ax2.text(0.1, 0.8, f"Total Rounds: {data.get('rounds', 'N/A')}", transform=ax2.transAxes)
        ax2.text(0.1, 0.6, f"Clients: {data.get('clients', 'N/A')}", transform=ax2.transAxes)
        ax2.text(0.1, 0.4, f"Final Accuracy: {data.get('final_accuracy', 'N/A'):.4f}", transform=ax2.transAxes)
        ax2.set_title('Training Summary')
        ax2.axis('off')
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
        plt.close()