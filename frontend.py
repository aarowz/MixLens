"""
Streamlit frontend for MixLens
Provides UI for uploading audio and viewing analysis results
"""
import streamlit as st
import requests
import json
import os
import time
from pathlib import Path

# Page config
st.set_page_config(
    page_title="MixLens - Audio Production Analysis",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:5001/api"

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .suggestion-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def upload_file(uploaded_file):
    """Upload file to API"""
    try:
        files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(f"{API_BASE_URL}/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.json().get('error', 'Upload failed')}
    except Exception as e:
        return {'error': str(e)}


def analyze_file(file_id):
    """Analyze uploaded file"""
    try:
        response = requests.get(f"{API_BASE_URL}/analyze/{file_id}", timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': response.json().get('error', 'Analysis failed')}
    except Exception as e:
        return {'error': str(e)}


def get_results(file_id):
    """Get saved analysis results"""
    try:
        response = requests.get(f"{API_BASE_URL}/results/{file_id}", timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None


def get_visualizations(file_id):
    """Get visualizations for file"""
    try:
        response = requests.get(f"{API_BASE_URL}/visualize/{file_id}", timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None


def display_features(features):
    """Display extracted features"""
    if 'extracted_features' not in features:
        return
    
    extracted = features['extracted_features']
    
    st.subheader("📊 Extracted Features")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tempo", f"{extracted.get('tempo_bpm', 0):.1f} BPM")
        st.metric("Key", extracted.get('estimated_key', 'N/A'))
        st.metric("RMS", f"{extracted.get('rms_db', 0):.1f} dB")
    
    with col2:
        st.metric("LUFS (approx)", f"{extracted.get('lufs_approx', 0):.1f}")
        st.metric("Dynamic Range", f"{extracted.get('dynamic_range_db', 0):.1f} dB")
        st.metric("Spectral Centroid", f"{extracted.get('spectral_centroid_hz', 0):.0f} Hz")
    
    with col3:
        st.metric("Spectral Rolloff", f"{extracted.get('spectral_rolloff_percent', 0):.1f}%")
        st.metric("Spectral Bandwidth", f"{extracted.get('spectral_bandwidth_hz', 0):.0f} Hz")
        st.metric("Zero Crossing Rate", f"{extracted.get('zero_crossing_rate', 0):.4f}")
    
    with col4:
        st.metric("Harmonic Ratio", f"{extracted.get('harmonic_ratio', 0)*100:.1f}%")
        st.metric("Percussive Ratio", f"{extracted.get('percussive_ratio', 0)*100:.1f}%")
        st.metric("MFCC Mean", f"{extracted.get('mfcc_mean', 0):.2f}")


def display_suggestions(suggestions):
    """Display production suggestions"""
    if not suggestions:
        return
    
    st.subheader("💡 Production Suggestions")
    
    for suggestion in suggestions:
        st.markdown(f'<div class="suggestion-box">{suggestion}</div>', 
                   unsafe_allow_html=True)


def display_visualizations(viz_data):
    """Display visualization images"""
    if not viz_data or 'visualizations' not in viz_data:
        return
    
    viz_paths = viz_data['visualizations']
    
    if not viz_paths:
        return
    
    st.subheader("📈 Visualizations")
    
    # Display each visualization
    for viz_name, viz_path in viz_paths.items():
        if os.path.exists(viz_path):
            st.image(viz_path, caption=viz_name.replace('_', ' ').title(), 
                    use_column_width=True)


def main():
    """Main Streamlit app"""
    # Header
    st.markdown('<div class="main-header">🎵 MixLens</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Audio Production Analysis Platform</div>', 
                unsafe_allow_html=True)
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ API server is not running. Please start the Flask backend:")
        st.code("python app.py", language="bash")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        st.markdown("---")
        
        # Metrics display
        try:
            metrics_response = requests.get(f"{API_BASE_URL}/metrics", timeout=2)
            if metrics_response.status_code == 200:
                metrics = metrics_response.json()
                st.subheader("📊 Platform Metrics")
                st.metric("Tracks Processed", metrics.get('tracks_processed', 0))
                st.metric("API Endpoints", metrics.get('api_endpoints', 0))
                st.metric("Features Extracted", metrics.get('features_extracted', 0))
                st.metric("Visualizations", metrics.get('visualizations', 0))
                if metrics.get('tracks_processed', 0) > 0:
                    st.metric("Avg Processing Time", 
                             f"{metrics.get('average_processing_time', 0):.2f}s")
        except:
            pass
        
        st.markdown("---")
        st.markdown("### 🎯 Quick Start")
        st.markdown("""
        1. Upload an audio file (WAV, MP3)
        2. Click "Analyze Audio"
        3. View features and suggestions
        4. Explore visualizations
        """)
    
    # Main content
    tab1, tab2 = st.tabs(["🎤 Upload & Analyze", "📊 View Results"])
    
    with tab1:
        st.header("Upload Audio File")
        
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'flac', 'm4a', 'aac'],
            help="Supported formats: WAV, MP3, FLAC, M4A, AAC"
        )
        
        if uploaded_file is not None:
            st.audio(uploaded_file, format=uploaded_file.type)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 Analyze Audio", type="primary", use_container_width=True):
                    with st.spinner("Uploading file..."):
                        upload_result = upload_file(uploaded_file)
                    
                    if 'error' in upload_result:
                        st.error(f"Upload failed: {upload_result['error']}")
                    else:
                        file_id = upload_result['file_id']
                        st.success(f"✅ File uploaded! ID: {file_id[:8]}...")
                        
                        # Store file_id in session state
                        st.session_state['current_file_id'] = file_id
                        
                        with st.spinner("Analyzing audio (this may take 10-15 seconds)..."):
                            analysis_result = analyze_file(file_id)
                        
                        if 'error' in analysis_result:
                            st.error(f"Analysis failed: {analysis_result['error']}")
                        else:
                            st.session_state['analysis_result'] = analysis_result
                            st.success("✅ Analysis complete!")
                            
                            # Display results
                            if 'features' in analysis_result:
                                display_features(analysis_result['features'])
                            
                            if 'suggestions' in analysis_result:
                                display_suggestions(analysis_result['suggestions'])
                            
                            # Get and display visualizations
                            with st.spinner("Generating visualizations..."):
                                viz_data = get_visualizations(file_id)
                                if viz_data:
                                    st.session_state['viz_data'] = viz_data
                                    display_visualizations(viz_data)
            
            with col2:
                if st.button("📥 Download Results", use_container_width=True):
                    if 'analysis_result' in st.session_state:
                        analysis_json = json.dumps(st.session_state['analysis_result'], indent=2)
                        st.download_button(
                            label="Download JSON",
                            data=analysis_json,
                            file_name=f"mixlens_analysis_{st.session_state.get('current_file_id', 'unknown')[:8]}.json",
                            mime="application/json"
                        )
    
    with tab2:
        st.header("View Analysis Results")
        
        file_id_input = st.text_input(
            "Enter File ID",
            value=st.session_state.get('current_file_id', ''),
            help="Enter the file ID from a previous analysis"
        )
        
        if st.button("Load Results", type="primary"):
            if file_id_input:
                with st.spinner("Loading results..."):
                    results = get_results(file_id_input)
                    
                    if results:
                        st.session_state['analysis_result'] = results
                        st.session_state['current_file_id'] = file_id_input
                        st.success("✅ Results loaded!")
                        
                        # Display results
                        if 'features' in results:
                            display_features(results['features'])
                        
                        if 'suggestions' in results:
                            display_suggestions(results['suggestions'])
                        
                        # Get visualizations
                        viz_data = get_visualizations(file_id_input)
                        if viz_data:
                            display_visualizations(viz_data)
                    else:
                        st.error("Results not found. Please check the file ID.")
        
        # Display cached results if available
        if 'analysis_result' in st.session_state:
            st.info("Showing cached results. Use 'Load Results' to fetch from server.")
            if 'features' in st.session_state['analysis_result']:
                display_features(st.session_state['analysis_result']['features'])
            if 'suggestions' in st.session_state['analysis_result']:
                display_suggestions(st.session_state['analysis_result']['suggestions'])
            if 'viz_data' in st.session_state:
                display_visualizations(st.session_state['viz_data'])


if __name__ == "__main__":
    main()

