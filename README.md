# MixLens 🎵

**Audio Production Analysis Platform**

MixLens is a full-stack web application that analyzes uploaded audio tracks and provides actionable production feedback to music producers. Built with Python, Flask, librosa, and Streamlit.

## 🎯 Features

- **Audio Feature Extraction**: Extracts 13+ musical features including tempo, key, loudness, spectral balance, and dynamic range
- **Production Suggestions**: Rule-based engine provides actionable feedback on mix quality
- **Visualizations**: Generates waveform, spectrogram, spectral features, and tempo analysis charts
- **REST API**: Flask backend with 6 endpoints for audio processing
- **Web Dashboard**: Streamlit frontend for easy interaction
- **Metrics Tracking**: Built-in tracking for resume metrics (tracks processed, processing time, etc.)

## 🛠️ Tech Stack

- **Backend**: Flask (REST API)
- **Audio Processing**: librosa, pydub, NumPy, SciPy
- **Frontend**: Streamlit
- **Visualization**: Matplotlib, Plotly
- **Storage**: File system (JSON for results, uploads folder for audio)

## 📋 Prerequisites

- Python 3.8+
- pip

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
cd MixLens
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: librosa requires `soundfile` and may need system audio libraries:
- **macOS**: `brew install libsndfile`
- **Linux**: `sudo apt-get install libsndfile1`
- **Windows**: Usually handled automatically by pip

### 3. Start the Flask Backend

```bash
python app.py
```

The API will start at `http://localhost:5000`

### 4. Start the Streamlit Frontend

In a new terminal:

```bash
streamlit run frontend.py
```

The frontend will open at `http://localhost:8501`

## 📖 Usage

### Via Web Interface (Recommended)

1. Open the Streamlit frontend at `http://localhost:8501`
2. Upload an audio file (WAV, MP3, FLAC, M4A, AAC)
3. Click "Analyze Audio"
4. View extracted features, production suggestions, and visualizations
5. Download results as JSON if needed

### Via API

#### Upload a file:
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@your_audio.mp3"
```

Response:
```json
{
  "file_id": "uuid-here",
  "filename": "your_audio.mp3",
  "status": "uploaded"
}
```

#### Analyze the file:
```bash
curl http://localhost:5000/api/analyze/{file_id}
```

#### Get results:
```bash
curl http://localhost:5000/api/results/{file_id}
```

#### Get visualizations:
```bash
curl http://localhost:5000/api/visualize/{file_id}
```

#### Check metrics:
```bash
curl http://localhost:5000/api/metrics
```

## 📊 Extracted Features

MixLens extracts **13 analysis dimensions**:

1. **Tempo (BPM)** - Beat tracking
2. **Estimated Key** - Chroma-based key detection
3. **RMS (dB)** - Root mean square loudness
4. **LUFS (approx)** - Loudness approximation
5. **Spectral Centroid (Hz)** - Frequency brightness
6. **Spectral Rolloff (%)** - High-frequency content
7. **Zero Crossing Rate** - Noisiness indicator
8. **Spectral Bandwidth (Hz)** - Frequency spread
9. **Dynamic Range (dB)** - Peak to RMS difference
10. **Spectral Contrast** - Harmonic vs noise content
11. **MFCC Mean** - Mel-frequency cepstral coefficient
12. **Harmonic Ratio** - Harmonic content percentage
13. **Percussive Ratio** - Percussive content percentage

## 🎨 Visualizations

- **Waveform**: Time-domain amplitude visualization
- **Spectrogram**: Frequency content over time
- **Spectral Features**: Centroid, rolloff, and bandwidth over time
- **Tempo Analysis**: Beat detection and onset strength

## 📁 Project Structure

```
MixLens/
├── app.py                      # Flask backend (REST API)
├── frontend.py                 # Streamlit frontend
├── audio_processor.py          # Core audio analysis pipeline
├── metrics.py                  # Metrics tracking
├── analyzer/
│   ├── __init__.py
│   ├── feature_extractor.py   # Extract tempo, key, spectral features
│   ├── suggestion_engine.py   # Generate production feedback
│   └── visualizer.py           # Create waveform/spectrogram plots
├── uploads/                    # Temporary audio file storage
├── results/                    # Analysis results (JSON) and visualizations
├── requirements.txt            # Dependencies
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/upload` | POST | Upload audio file |
| `/api/analyze/<file_id>` | GET | Analyze uploaded file |
| `/api/results/<file_id>` | GET | Get saved analysis results |
| `/api/visualize/<file_id>` | GET | Generate visualizations |
| `/api/metrics` | GET | Get platform metrics |

## 📈 Metrics Tracking

MixLens automatically tracks:
- **Tracks Processed**: Total number of analyses
- **Average Processing Time**: Mean analysis time
- **API Endpoints**: Number of endpoints (currently 6)
- **Features Extracted**: Number of analysis dimensions (currently 13)
- **Visualizations**: Number of chart types (currently 4)

View metrics via `/api/metrics` endpoint or in the Streamlit sidebar.

## 🎯 Production Suggestions

The suggestion engine provides feedback on:
- **Loudness**: RMS and LUFS analysis
- **Dynamic Range**: Compression assessment
- **Frequency Balance**: Spectral centroid analysis
- **High-Frequency Content**: Spectral rolloff evaluation
- **Harmonic Content**: Harmonic vs percussive ratio
- **Tempo**: BPM analysis
- **Key Detection**: Estimated musical key

## 🐛 Troubleshooting

### librosa installation issues
- Ensure system audio libraries are installed (see Prerequisites)
- Try: `pip install --upgrade librosa soundfile`

### Port already in use
- Change Flask port in `app.py`: `app.run(port=5001)`
- Change Streamlit port: `streamlit run frontend.py --server.port 8502`

### File upload fails
- Check file size (max 50MB)
- Verify file format (WAV, MP3, FLAC, M4A, AAC)
- Ensure Flask backend is running

### Analysis takes too long
- Large files (>10MB) may take 15-20 seconds
- Consider using shorter audio clips for testing
- Check system resources (CPU, RAM)

## 🚧 Future Enhancements

- Audio processing (normalize, basic EQ)
- Download processed audio
- Batch processing
- More advanced visualizations
- ML-based suggestion improvements
- User accounts and history
- Database integration

## 📝 License

See LICENSE file for details.

## 👤 Author

Built to analyze my fire beats.

---

**Built with ❤️ using Python, Flask, librosa, and Streamlit**
