import os
import uuid
import time
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import json
import atexit
from metrics import METRICS, initialize_metrics, log_analysis, get_metrics_summary, print_metrics_summary

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'

# Allowed audio extensions
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'aac'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Initialize metrics on startup
initialize_metrics()

# Print metrics summary on shutdown
atexit.register(print_metrics_summary)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'MixLens API is running'})


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Upload audio file endpoint
    Returns: JSON with file_id and status
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    file_extension = filename.rsplit('.', 1)[1].lower()
    
    # Save file with unique ID
    saved_filename = f"{file_id}.{file_extension}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
    file.save(filepath)
    
    return jsonify({
        'file_id': file_id,
        'filename': filename,
        'status': 'uploaded',
        'message': 'File uploaded successfully'
    }), 200


@app.route('/api/analyze/<file_id>', methods=['GET'])
def analyze_file(file_id):
    """
    Analyze uploaded audio file
    Returns: JSON with extracted features and suggestions
    """
    # Find the uploaded file
    upload_path = None
    for ext in ALLOWED_EXTENSIONS:
        potential_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}.{ext}")
        if os.path.exists(potential_path):
            upload_path = potential_path
            break
    
    if not upload_path:
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Start timing
        start_time = time.time()
        
        # Import here to avoid circular imports
        from audio_processor import AudioProcessor
        
        processor = AudioProcessor()
        analysis_result = processor.analyze(upload_path)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Log metrics
        log_analysis(processing_time)
        
        # Add processing time to result
        analysis_result['processing_time'] = round(processing_time, 2)
        
        # Save results
        results_path = os.path.join(app.config['RESULTS_FOLDER'], f"{file_id}.json")
        with open(results_path, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/results/<file_id>', methods=['GET'])
def get_results(file_id):
    """Get saved analysis results"""
    results_path = os.path.join(app.config['RESULTS_FOLDER'], f"{file_id}.json")
    
    if not os.path.exists(results_path):
        return jsonify({'error': 'Results not found'}), 404
    
    with open(results_path, 'r') as f:
        results = json.load(f)
    
    return jsonify(results), 200


@app.route('/api/visualize/<file_id>', methods=['GET'])
def visualize_file(file_id):
    """
    Generate visualizations for analyzed file
    Returns: JSON with visualization paths or data
    """
    results_path = os.path.join(app.config['RESULTS_FOLDER'], f"{file_id}.json")
    
    if not os.path.exists(results_path):
        return jsonify({'error': 'File not analyzed yet'}), 404
    
    try:
        from analyzer.visualizer import Visualizer
        
        visualizer = Visualizer()
        viz_data = visualizer.create_visualizations(file_id)
        
        return jsonify(viz_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get current metrics (useful for monitoring)"""
    return jsonify(get_metrics_summary()), 200


if __name__ == '__main__':
    try:
        print("\n🚀 Starting MixLens API Server...")
        print("   API running at http://localhost:5001")
        print("   Health check: http://localhost:5001/api/health\n")
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print_metrics_summary()

