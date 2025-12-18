"""
Feature extraction using librosa
Extracts musical and technical features from audio files
"""
# Compatibility shim for scipy.signal.hann (moved to scipy.signal.windows.hann in newer SciPy)
import scipy.signal
if not hasattr(scipy.signal, 'hann'):
    try:
        from scipy.signal.windows import hann
        scipy.signal.hann = hann
    except ImportError:
        pass

import librosa
import numpy as np
from scipy import stats


class FeatureExtractor:
    """Extract musical features from audio"""
    
    def __init__(self, target_sr=22050):
        """
        Initialize feature extractor
        
        Args:
            target_sr: Target sample rate for analysis (default: 22050)
        """
        self.target_sr = target_sr
    
    def extract(self, filepath):
        """
        Extract comprehensive features from audio file
        
        Args:
            filepath: Path to audio file
            
        Returns:
            dict: Extracted features
        """
        # Load audio file
        y, sr = librosa.load(filepath, sr=self.target_sr, duration=None)
        
        # Basic audio properties
        duration = len(y) / sr
        
        # 1. Tempo (BPM)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(tempo)
        
        # 2. Key detection (simplified - using chroma features)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        key_idx = np.argmax(chroma_mean)
        keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        estimated_key = keys[key_idx]
        
        # 3. Loudness (RMS)
        rms = librosa.feature.rms(y=y)
        rms_mean = float(np.mean(rms))
        rms_db = float(20 * np.log10(rms_mean + 1e-10))  # Convert to dB
        
        # 4. LUFS approximation (using RMS as proxy)
        # Note: True LUFS requires ITU-R BS.1770, but RMS gives good approximation
        lufs_approx = rms_db - 23.0  # Rough calibration
        
        # 5. Spectral Centroid (brightness)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = float(np.mean(spectral_centroid))
        
        # 6. Spectral Rolloff (high-frequency content)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        spectral_rolloff_mean = float(np.mean(spectral_rolloff))
        spectral_rolloff_percent = float((spectral_rolloff_mean / (sr / 2)) * 100)
        
        # 7. Zero Crossing Rate (noisiness/brightness)
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = float(np.mean(zcr))
        
        # 8. Spectral Bandwidth (frequency spread)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        spectral_bandwidth_mean = float(np.mean(spectral_bandwidth))
        
        # 9. Dynamic Range (peak - RMS)
        peak = float(np.max(np.abs(y)))
        peak_db = float(20 * np.log10(peak + 1e-10))
        dynamic_range = peak_db - rms_db
        
        # 10. Spectral Contrast (harmonic vs noise)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_contrast_mean = float(np.mean(spectral_contrast))
        
        # 11. MFCC (Mel-frequency cepstral coefficients) - first coefficient
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_mean = float(np.mean(mfccs[0]))  # First MFCC coefficient
        
        # 12. Harmonic/Percussive separation
        y_harmonic, y_percussive = librosa.effects.hpss(y)
        harmonic_ratio = float(np.sum(np.abs(y_harmonic)) / (np.sum(np.abs(y)) + 1e-10))
        percussive_ratio = float(np.sum(np.abs(y_percussive)) / (np.sum(np.abs(y)) + 1e-10))
        
        # Compile all features
        extracted_features = {
            'tempo_bpm': round(tempo, 2),
            'estimated_key': estimated_key,
            'rms_db': round(rms_db, 2),
            'lufs_approx': round(lufs_approx, 2),
            'spectral_centroid_hz': round(spectral_centroid_mean, 2),
            'spectral_rolloff_percent': round(spectral_rolloff_percent, 2),
            'zero_crossing_rate': round(zcr_mean, 4),
            'spectral_bandwidth_hz': round(spectral_bandwidth_mean, 2),
            'dynamic_range_db': round(dynamic_range, 2),
            'spectral_contrast': round(spectral_contrast_mean, 2),
            'mfcc_mean': round(mfcc_mean, 2),
            'harmonic_ratio': round(harmonic_ratio, 3),
            'percussive_ratio': round(percussive_ratio, 3)
        }
        
        return {
            'duration_seconds': round(duration, 2),
            'sample_rate': sr,
            'extracted_features': extracted_features,
            'audio_data': {
                'length_samples': len(y),
                'peak_amplitude': round(peak, 4),
                'peak_db': round(peak_db, 2)
            }
        }

