"""
Visualization module for audio analysis
Creates waveform, spectrogram, and feature plots
"""
# Compatibility shim for scipy.signal.hann (moved to scipy.signal.windows.hann in newer SciPy)
import scipy.signal
if not hasattr(scipy.signal, 'hann'):
    try:
        from scipy.signal.windows import hann
        scipy.signal.hann = hann
    except ImportError:
        pass

import os
import librosa
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from metrics import update_visualizations_count


class Visualizer:
    """Create visualizations for audio analysis"""
    
    def __init__(self):
        """Initialize visualizer"""
        self.viz_folder = 'results'
        os.makedirs(self.viz_folder, exist_ok=True)
        self.viz_types = []
    
    def create_visualizations(self, file_id):
        """
        Create visualizations for analyzed file
        
        Args:
            file_id: Unique file identifier
            
        Returns:
            dict: Visualization data/paths
        """
        # Find the uploaded file
        upload_folder = 'uploads'
        allowed_extensions = ['wav', 'mp3', 'flac', 'm4a', 'aac']
        
        audio_path = None
        for ext in allowed_extensions:
            potential_path = os.path.join(upload_folder, f"{file_id}.{ext}")
            if os.path.exists(potential_path):
                audio_path = potential_path
                break
        
        if not audio_path:
            return {'error': 'Audio file not found'}
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=22050)
        
        # Create visualizations
        viz_paths = {}
        
        # 1. Waveform
        waveform_path = self._create_waveform(y, sr, file_id)
        if waveform_path:
            viz_paths['waveform'] = waveform_path
        
        # 2. Spectrogram
        spectrogram_path = self._create_spectrogram(y, sr, file_id)
        if spectrogram_path:
            viz_paths['spectrogram'] = spectrogram_path
        
        # 3. Spectral features
        spectral_features_path = self._create_spectral_features(y, sr, file_id)
        if spectral_features_path:
            viz_paths['spectral_features'] = spectral_features_path
        
        # 4. Tempo visualization
        tempo_path = self._create_tempo_plot(y, sr, file_id)
        if tempo_path:
            viz_paths['tempo'] = tempo_path
        
        # Update metrics
        self.viz_types = list(viz_paths.keys())
        update_visualizations_count(len(self.viz_types))
        
        return {
            'file_id': file_id,
            'visualizations': viz_paths,
            'visualization_count': len(viz_paths),
            'status': 'visualizations_ready'
        }
    
    def _create_waveform(self, y, sr, file_id):
        """Create waveform visualization"""
        try:
            fig, ax = plt.subplots(figsize=(12, 4))
            
            # Time axis
            time_axis = np.linspace(0, len(y) / sr, len(y))
            
            # Plot waveform
            ax.plot(time_axis, y, color='#1f77b4', linewidth=0.5, alpha=0.8)
            ax.fill_between(time_axis, y, alpha=0.3, color='#1f77b4')
            
            ax.set_xlabel('Time (seconds)', fontsize=11)
            ax.set_ylabel('Amplitude', fontsize=11)
            ax.set_title('Waveform', fontsize=13, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xlim(0, len(y) / sr)
            
            plt.tight_layout()
            
            waveform_path = os.path.join(self.viz_folder, f"{file_id}_waveform.png")
            plt.savefig(waveform_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return waveform_path
        except Exception as e:
            print(f"Error creating waveform: {e}")
            return None
    
    def _create_spectrogram(self, y, sr, file_id):
        """Create spectrogram visualization"""
        try:
            # Compute spectrogram
            D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Display spectrogram
            img = librosa.display.specshow(D, y_axis='hz', x_axis='time', 
                                          sr=sr, ax=ax, cmap='viridis')
            
            ax.set_title('Spectrogram', fontsize=13, fontweight='bold')
            ax.set_xlabel('Time (seconds)', fontsize=11)
            ax.set_ylabel('Frequency (Hz)', fontsize=11)
            
            # Add colorbar
            plt.colorbar(img, ax=ax, format='%+2.0f dB')
            
            plt.tight_layout()
            
            spectrogram_path = os.path.join(self.viz_folder, f"{file_id}_spectrogram.png")
            plt.savefig(spectrogram_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return spectrogram_path
        except Exception as e:
            print(f"Error creating spectrogram: {e}")
            return None
    
    def _create_spectral_features(self, y, sr, file_id):
        """Create spectral features plot"""
        try:
            # Extract features
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
            
            # Time axis
            times = librosa.times_like(spectral_centroid, sr=sr)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Normalize for visualization
            ax.plot(times, spectral_centroid / 1000, label='Spectral Centroid (kHz)', 
                   color='#ff7f0e', linewidth=2)
            ax.plot(times, spectral_rolloff / 1000, label='Spectral Rolloff (kHz)', 
                   color='#2ca02c', linewidth=2)
            ax.plot(times, spectral_bandwidth / 1000, label='Spectral Bandwidth (kHz)', 
                   color='#d62728', linewidth=2, alpha=0.7)
            
            ax.set_xlabel('Time (seconds)', fontsize=11)
            ax.set_ylabel('Frequency (kHz)', fontsize=11)
            ax.set_title('Spectral Features Over Time', fontsize=13, fontweight='bold')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            spectral_path = os.path.join(self.viz_folder, f"{file_id}_spectral_features.png")
            plt.savefig(spectral_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return spectral_path
        except Exception as e:
            print(f"Error creating spectral features: {e}")
            return None
    
    def _create_tempo_plot(self, y, sr, file_id):
        """Create tempo/beat visualization"""
        try:
            # Detect tempo and beats
            tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
            
            # Get beat times
            beat_times = librosa.frames_to_time(beat_frames, sr=sr)
            
            # Create onset strength
            onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
            onset_times = librosa.frames_to_time(onset_frames, sr=sr)
            onset_strength = librosa.onset.onset_strength(y=y, sr=sr)
            onset_times_full = librosa.times_like(onset_strength, sr=sr)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plot onset strength
            ax.plot(onset_times_full, onset_strength, label='Onset Strength', 
                   color='#9467bd', linewidth=1.5, alpha=0.7)
            
            # Mark detected beats
            for bt in beat_times[:50]:  # Show first 50 beats
                ax.axvline(bt, color='#ff7f0e', linestyle='--', alpha=0.6, linewidth=1)
            
            ax.set_xlabel('Time (seconds)', fontsize=11)
            ax.set_ylabel('Onset Strength', fontsize=11)
            ax.set_title(f'Tempo Analysis (Detected: {tempo:.1f} BPM)', 
                        fontsize=13, fontweight='bold')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)
            ax.set_xlim(0, min(30, len(y) / sr))  # Show first 30 seconds
            
            plt.tight_layout()
            
            tempo_path = os.path.join(self.viz_folder, f"{file_id}_tempo.png")
            plt.savefig(tempo_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            return tempo_path
        except Exception as e:
            print(f"Error creating tempo plot: {e}")
            return None

