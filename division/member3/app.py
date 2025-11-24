from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
import os
import tempfile
import threading
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from config import Config
from s3_helper import S3Helper
from server import FederatedServer
from model import FederatedModel
from training_engine import TrainingLogger
from model_stats import ModelStats

app = Flask(__name__)
app.config.from_object(Config)

# Global variables for training state
training_state = {
    'active': False,
    'current_round': 0,
    'total_rounds': 0,
    'logs': [],
    'accuracies': [],
    'completed': False,
    'model_version': None
}

s3_helper = S3Helper()
model_stats = ModelStats()

@app.route('/')
def home():
    # Get system statistics
    datasets = s3_helper.list_files('datasets/')
    models = s3_helper.list_files('models/')
    latest_version = s3_helper.get_latest_model_version()
    
    # Get actual latest model accuracy
    latest_accuracy = model_stats.get_latest_model_accuracy()
    
    stats = {
        'dataset_count': len([f for f in datasets if f.endswith('.csv')]),
        'model_count': len([f for f in models if f.endswith('.pkl')]),
        'latest_accuracy': latest_accuracy
    }
    
    return render_template('home.html', stats=stats)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            
            # Save temporarily
            temp_path = os.path.join(tempfile.gettempdir(), filename)
            file.save(temp_path)
            
            # Upload to S3
            success, s3_key = s3_helper.upload_csv_dataset(temp_path, filename)
            
            # Cleanup
            os.unlink(temp_path)
            
            if success:
                flash(f'File uploaded successfully to S3: {s3_key}', 'success')
            else:
                flash('Failed to upload file to S3', 'error')
        else:
            flash('Please select a CSV file', 'error')
        
        return redirect(url_for('upload'))
    
    # Get current datasets
    dataset_files = s3_helper.list_files('datasets/')
    datasets = []
    for file_key in dataset_files:
        if file_key.endswith('.csv'):
            datasets.append({
                'name': file_key.split('/')[-1],
                'date': 'Recent',  # Could be enhanced with actual metadata
                'size': 'Unknown'
            })
    
    return render_template('upload.html', datasets=datasets)

@app.route('/train')
def train():
    dataset_count = len([f for f in s3_helper.list_files('datasets/') if f.endswith('.csv')])
    return render_template('train.html', dataset_count=dataset_count)

@app.route('/models')
def models():
    model_files = s3_helper.list_files('models/')
    latest_version = s3_helper.get_latest_model_version()
    
    models_list = []
    for file_key in model_files:
        if file_key.endswith('.pkl') and 'model_v' in file_key:
            try:
                version = int(file_key.split('model_v')[1].split('.pkl')[0])
                models_list.append({
                    'version': version,
                    'created_date': 'Recent',
                    'size': 'Unknown',
                    'is_latest': version == latest_version
                })
            except:
                continue
    
    models_list.sort(key=lambda x: x['version'], reverse=True)
    
    latest_model = None
    if models_list:
        latest_accuracy = model_stats.get_latest_model_accuracy()
        latest_model = {
            'version': latest_version,
            'client_count': 'Unknown',
            'rounds': 'Unknown',
            'accuracy': latest_accuracy,
            'created_date': 'Recent'
        }
    
    return render_template('models.html', models=models_list, latest_model=latest_model)

@app.route('/classify')
def classify():
    latest_version = s3_helper.get_latest_model_version()
    model_files = s3_helper.list_files('models/')
    
    available_versions = []
    for file_key in model_files:
        if file_key.endswith('.pkl') and 'model_v' in file_key:
            try:
                version = int(file_key.split('model_v')[1].split('.pkl')[0])
                available_versions.append(version)
            except:
                continue
    
    available_versions.sort(reverse=True)
    
    return render_template('classify.html', 
                         latest_version=latest_version,
                         available_versions=available_versions)

@app.route('/api/train', methods=['POST'])
def api_train():
    global training_state
    
    if training_state['active']:
        return jsonify({'success': False, 'message': 'Training already in progress'})
    
    rounds = int(request.form.get('rounds', 10))
    
    # Reset training state
    training_state = {
        'active': True,
        'current_round': 0,
        'total_rounds': rounds,
        'logs': [],
        'accuracies': [],
        'completed': False,
        'model_version': None
    }
    
    # Start training in background thread
    thread = threading.Thread(target=run_federated_training, args=(rounds,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True})

@app.route('/api/training_status')
def api_training_status():
    return jsonify(training_state)

@app.route('/api/classify', methods=['POST'])
def api_classify():
    email_text = request.form.get('email_text')
    model_version = request.form.get('model_version', 'latest')
    
    if not email_text:
        return jsonify({'success': False, 'message': 'No email text provided'})
    
    try:
        # Determine model version to use
        if model_version == 'latest':
            version = s3_helper.get_latest_model_version()
        else:
            version = int(model_version)
        
        if version == 0:
            return jsonify({'success': False, 'message': 'No trained models available'})
        
        # Download model from S3
        model_key = f'models/model_v{version}.pkl'
        temp_model_path = tempfile.mktemp(suffix='.pkl')
        
        if not s3_helper.download_file(model_key, temp_model_path):
            return jsonify({'success': False, 'message': 'Failed to load model'})
        
        # Load and use model
        model = FederatedModel()
        model.load_model(temp_model_path)
        
        # Make prediction
        prediction = model.predict([email_text])[0]
        probabilities = model.predict_proba([email_text])[0]
        confidence = max(probabilities)
        
        # Cleanup
        os.unlink(temp_model_path)
        
        return jsonify({
            'success': True,
            'prediction': int(prediction),
            'confidence': float(confidence)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/stats')
def api_stats():
    """Get system statistics"""
    datasets = s3_helper.list_files('datasets/')
    models = s3_helper.list_files('models/')
    latest_version = s3_helper.get_latest_model_version()
    
    # Get actual latest model accuracy
    latest_accuracy = model_stats.get_latest_model_accuracy()
    
    return jsonify({
        'dataset_count': len([f for f in datasets if f.endswith('.csv')]),
        'model_count': len([f for f in models if f.endswith('.pkl')]),
        'latest_accuracy': latest_accuracy
    })

@app.route('/api/download_model/<int:version>')
def api_download_model(version):
    """Download model file"""
    try:
        model_key = f'models/model_v{version}.pkl'
        temp_path = tempfile.mktemp(suffix='.pkl')
        
        if s3_helper.download_file(model_key, temp_path):
            return send_file(temp_path, as_attachment=True, 
                           download_name=f'model_v{version}.pkl')
        else:
            return jsonify({'error': 'Model not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/training_plots/<int:version>')
def api_training_plots(version):
    """Get training plot URLs"""
    try:
        plots = {
            'accuracy_plot': f'plots/accuracy_plot_v{version}.png',
            'training_summary': f'plots/training_summary_v{version}.png'
        }
        
        # Check if plots exist in S3
        existing_plots = {}
        for plot_name, s3_key in plots.items():
            if s3_key in s3_helper.list_files('plots/'):
                existing_plots[plot_name] = s3_key
        
        return jsonify(existing_plots)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_federated_training(rounds):
    global training_state
    
    try:
        training_state['logs'].append('Initializing federated server...')
        server = FederatedServer()
        
        training_state['logs'].append('Loading datasets from S3...')
        client_count = server.initialize_clients_from_s3()
        
        if client_count == 0:
            training_state['logs'].append('Error: No valid datasets found in S3')
            training_state['active'] = False
            return
        
        training_state['logs'].append(f'Initialized {client_count} clients')
        
        # Run federated training
        for round_num in range(1, rounds + 1):
            if not training_state['active']:
                break
                
            training_state['current_round'] = round_num
            training_state['logs'].append(f'Starting round {round_num}/{rounds}')
            
            accuracy = server.train_round(round_num)
            training_state['accuracies'].append(accuracy)
            
            # Get recent logs from server
            recent_logs = server.logger.get_recent_logs(5)
            training_state['logs'].extend(recent_logs)
            
            time.sleep(1)  # Small delay for UI updates
        
        if training_state['active']:
            # Save final model
            training_state['logs'].append('Saving model to S3...')
            model_version = server.save_model_to_s3()
            
            if model_version:
                training_state['model_version'] = model_version
                training_state['logs'].append(f'Model saved as version {model_version}')
                training_state['logs'].append('Training artifacts (plots, logs) saved to S3')
            else:
                training_state['logs'].append('Error: Failed to save model to S3')
            
            training_state['completed'] = True
            training_state['logs'].append('Federated training completed successfully!')
        
    except Exception as e:
        training_state['logs'].append(f'Error: {str(e)}')
    finally:
        training_state['active'] = False

if __name__ == '__main__':
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)