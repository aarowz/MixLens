"""
Metrics tracking for MixLens
Tracks usage statistics for resume metrics
"""
import time
from datetime import datetime

METRICS = {
    'tracks_processed': 0,
    'total_processing_time': 0.0,
    'api_endpoints': 0,  # Will be updated as endpoints are added
    'features_extracted': 0,  # Will be updated as features are added
    'visualizations': 0,  # Will be updated as visualizations are added
    'start_date': datetime.now().strftime('%b %d, %Y')
}

# Track which endpoints exist (update this as you add endpoints)
ENDPOINTS = [
    '/api/health',
    '/api/upload',
    '/api/analyze/<file_id>',
    '/api/results/<file_id>',
    '/api/visualize/<file_id>',
    '/api/metrics'
]

def initialize_metrics():
    """Initialize metrics on startup"""
    METRICS['api_endpoints'] = len(ENDPOINTS)
    print(f"📊 MixLens Metrics Initialized")
    print(f"   Start Date: {METRICS['start_date']}")
    print(f"   API Endpoints: {METRICS['api_endpoints']}")


def log_analysis(processing_time):
    """
    Log a completed analysis
    
    Args:
        processing_time: Time taken in seconds
    """
    METRICS['tracks_processed'] += 1
    METRICS['total_processing_time'] += processing_time
    
    avg_time = METRICS['total_processing_time'] / METRICS['tracks_processed']
    
    print(f"✅ Analysis #{METRICS['tracks_processed']} completed")
    print(f"   Processing Time: {processing_time:.2f}s")
    print(f"   Average Time: {avg_time:.2f}s")
    print(f"   Total Tracks: {METRICS['tracks_processed']}")


def update_features_count(count):
    """
    Update the number of features extracted
    
    Args:
        count: Number of features being extracted
    """
    if count > METRICS['features_extracted']:
        METRICS['features_extracted'] = count
        print(f"📈 Features Updated: {METRICS['features_extracted']} analysis dimensions")


def update_visualizations_count(count):
    """
    Update the number of visualization types
    
    Args:
        count: Number of visualization types
    """
    if count > METRICS['visualizations']:
        METRICS['visualizations'] = count
        print(f"📊 Visualizations Updated: {METRICS['visualizations']} chart types")


def get_metrics_summary():
    """
    Get current metrics summary
    
    Returns:
        dict: Current metrics
    """
    avg_time = 0.0
    if METRICS['tracks_processed'] > 0:
        avg_time = METRICS['total_processing_time'] / METRICS['tracks_processed']
    
    return {
        **METRICS,
        'average_processing_time': round(avg_time, 2),
        'total_processing_time_rounded': round(METRICS['total_processing_time'], 2)
    }


def print_metrics_summary():
    """Print a formatted metrics summary"""
    summary = get_metrics_summary()
    
    print("\n" + "="*50)
    print("📊 MIXLENS METRICS SUMMARY")
    print("="*50)
    print(f"Start Date: {summary['start_date']}")
    print(f"Tracks Processed: {summary['tracks_processed']}")
    print(f"API Endpoints: {summary['api_endpoints']}")
    print(f"Features Extracted: {summary['features_extracted']}")
    print(f"Visualizations: {summary['visualizations']}")
    print(f"Average Processing Time: {summary['average_processing_time']:.2f}s")
    print(f"Total Processing Time: {summary['total_processing_time_rounded']:.2f}s")
    print("="*50 + "\n")

