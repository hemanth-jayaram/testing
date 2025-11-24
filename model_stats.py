"""
Model Statistics Helper
Provides utilities for tracking and retrieving model training statistics
"""

import os
import json
from s3_helper import S3Helper


class ModelStats:
    """Helper class for managing model statistics"""
    
    def __init__(self):
        self.s3_helper = S3Helper()
    
    def get_latest_model_accuracy(self):
        """
        Get the accuracy of the latest trained model
        
        Returns:
            float: Latest model accuracy, or 0.0 if no models exist
        """
        try:
            # Get latest model version
            latest_version = self.s3_helper.get_latest_model_version()
            
            if latest_version == 0:
                return 0.0
            
            # Try to get accuracy from logs
            log_key = f'logs/training_log_v{latest_version}.txt'
            logs = self.s3_helper.list_files('logs/')
            
            if log_key in logs:
                # Download and parse log file
                import tempfile
                temp_log = tempfile.mktemp(suffix='.txt')
                
                if self.s3_helper.download_file(log_key, temp_log):
                    with open(temp_log, 'r') as f:
                        lines = f.readlines()
                        # Look for accuracy in last few lines
                        for line in reversed(lines):
                            if 'accuracy' in line.lower():
                                # Extract accuracy value
                                parts = line.split(':')
                                if len(parts) > 1:
                                    try:
                                        accuracy = float(parts[-1].strip())
                                        os.unlink(temp_log)
                                        return accuracy
                                    except ValueError:
                                        continue
                    os.unlink(temp_log)
            
            # Default to 0.0 if no accuracy found
            return 0.0
            
        except Exception as e:
            print(f"Error getting latest model accuracy: {e}")
            return 0.0
    
    def get_model_stats(self, version):
        """
        Get statistics for a specific model version
        
        Args:
            version (int): Model version number
            
        Returns:
            dict: Model statistics including accuracy, rounds, etc.
        """
        try:
            stats = {
                'version': version,
                'accuracy': 0.0,
                'rounds': 0,
                'clients': 0
            }
            
            # Try to get stats from log file
            log_key = f'logs/training_log_v{version}.txt'
            logs = self.s3_helper.list_files('logs/')
            
            if log_key in logs:
                import tempfile
                temp_log = tempfile.mktemp(suffix='.txt')
                
                if self.s3_helper.download_file(log_key, temp_log):
                    with open(temp_log, 'r') as f:
                        content = f.read()
                        
                        # Parse log content
                        if 'accuracy' in content.lower():
                            lines = content.split('\n')
                            for line in reversed(lines):
                                if 'accuracy' in line.lower():
                                    try:
                                        parts = line.split(':')
                                        if len(parts) > 1:
                                            stats['accuracy'] = float(parts[-1].strip())
                                            break
                                    except ValueError:
                                        continue
                        
                        # Count rounds
                        stats['rounds'] = content.lower().count('round')
                        
                        # Count clients
                        if 'clients' in content.lower():
                            for line in content.split('\n'):
                                if 'client' in line.lower():
                                    try:
                                        # Extract number of clients
                                        words = line.split()
                                        for i, word in enumerate(words):
                                            if word.isdigit() and 'client' in line.lower():
                                                stats['clients'] = int(word)
                                                break
                                    except:
                                        continue
                    
                    os.unlink(temp_log)
            
            return stats
            
        except Exception as e:
            print(f"Error getting model stats: {e}")
            return {
                'version': version,
                'accuracy': 0.0,
                'rounds': 0,
                'clients': 0
            }
