"""
Rule-based suggestion engine
Generates production feedback based on extracted features
"""
from typing import List, Dict


class SuggestionEngine:
    """Generate production suggestions based on audio features"""
    
    def __init__(self):
        """Initialize suggestion engine with thresholds"""
        # Define thresholds for suggestions
        self.thresholds = {
            'rms_too_quiet': -20.0,  # dB
            'rms_too_loud': -6.0,    # dB
            'dynamic_range_low': 6.0,  # dB
            'dynamic_range_high': 20.0,  # dB
            'spectral_centroid_low': 2000.0,  # Hz
            'spectral_centroid_high': 4000.0,  # Hz
            'spectral_rolloff_low': 60.0,  # percent
            'spectral_rolloff_high': 90.0,  # percent
            'harmonic_ratio_low': 0.5,
            'percussive_ratio_high': 0.6
        }
    
    def generate(self, features: Dict) -> List[str]:
        """
        Generate suggestions from extracted features
        
        Args:
            features: dict of extracted features
            
        Returns:
            list: List of suggestion strings
        """
        suggestions = []
        extracted = features.get('extracted_features', {})
        
        if not extracted:
            return ["Unable to extract features. Please check audio file."]
        
        # 1. Loudness/RMS analysis
        rms_db = extracted.get('rms_db', 0)
        lufs_approx = extracted.get('lufs_approx', 0)
        
        if rms_db < self.thresholds['rms_too_quiet']:
            suggestions.append(
                f"🔊 **Loudness**: Track is quiet (RMS: {rms_db:.1f} dB). "
                "Consider normalizing or increasing gain to improve perceived loudness."
            )
        elif rms_db > self.thresholds['rms_too_loud']:
            suggestions.append(
                f"🔊 **Loudness**: Track may be too loud (RMS: {rms_db:.1f} dB). "
                "Watch for clipping and consider reducing gain slightly."
            )
        else:
            suggestions.append(
                f"✅ **Loudness**: Good level (RMS: {rms_db:.1f} dB, LUFS approx: {lufs_approx:.1f}). "
                "Track has appropriate loudness for modern production."
            )
        
        # 2. Dynamic Range analysis
        dynamic_range = extracted.get('dynamic_range_db', 0)
        
        if dynamic_range < self.thresholds['dynamic_range_low']:
            suggestions.append(
                f"🎚️ **Dynamic Range**: Very compressed (Range: {dynamic_range:.1f} dB). "
                "Consider easing compression to preserve more natural dynamics and musicality."
            )
        elif dynamic_range > self.thresholds['dynamic_range_high']:
            suggestions.append(
                f"🎚️ **Dynamic Range**: Wide dynamics (Range: {dynamic_range:.1f} dB). "
                "Good for dynamic music, but ensure consistency for streaming platforms."
            )
        else:
            suggestions.append(
                f"✅ **Dynamic Range**: Balanced (Range: {dynamic_range:.1f} dB). "
                "Good balance between dynamics and consistency."
            )
        
        # 3. Spectral Centroid (brightness)
        spectral_centroid = extracted.get('spectral_centroid_hz', 0)
        
        if spectral_centroid < self.thresholds['spectral_centroid_low']:
            suggestions.append(
                f"🎵 **Frequency Balance**: Low-end heavy (Centroid: {spectral_centroid:.0f} Hz). "
                "Mix may lack clarity in the mid/high frequencies. Consider boosting presence or reducing low-end."
            )
        elif spectral_centroid > self.thresholds['spectral_centroid_high']:
            suggestions.append(
                f"🎵 **Frequency Balance**: Bright mix (Centroid: {spectral_centroid:.0f} Hz). "
                "High frequencies are prominent. Watch for harshness or listener fatigue."
            )
        else:
            suggestions.append(
                f"✅ **Frequency Balance**: Well-balanced (Centroid: {spectral_centroid:.0f} Hz). "
                "Good distribution across frequency spectrum."
            )
        
        # 4. Spectral Rolloff (high-frequency content)
        spectral_rolloff = extracted.get('spectral_rolloff_percent', 0)
        
        if spectral_rolloff < self.thresholds['spectral_rolloff_low']:
            suggestions.append(
                f"📊 **High-Frequency Content**: Limited high-end (Rolloff: {spectral_rolloff:.1f}%). "
                "Mix may sound dull. Consider adding air or reducing low-pass filtering."
            )
        elif spectral_rolloff > self.thresholds['spectral_rolloff_high']:
            suggestions.append(
                f"📊 **High-Frequency Content**: Extended high-end (Rolloff: {spectral_rolloff:.1f}%). "
                "Very bright mix. Ensure high frequencies are musical, not harsh."
            )
        else:
            suggestions.append(
                f"✅ **High-Frequency Content**: Appropriate (Rolloff: {spectral_rolloff:.1f}%). "
                "Good high-frequency extension."
            )
        
        # 5. Harmonic vs Percussive content
        harmonic_ratio = extracted.get('harmonic_ratio', 0)
        percussive_ratio = extracted.get('percussive_ratio', 0)
        
        if harmonic_ratio < self.thresholds['harmonic_ratio_low']:
            suggestions.append(
                f"🎸 **Harmonic Content**: Low harmonic content ({harmonic_ratio*100:.1f}%). "
                "Track is more percussive/noisy. If intended, great! If not, check for distortion or noise issues."
            )
        else:
            suggestions.append(
                f"✅ **Harmonic Content**: Good harmonic presence ({harmonic_ratio*100:.1f}%). "
                "Musical elements are well-represented."
            )
        
        # 6. Tempo analysis
        tempo = extracted.get('tempo_bpm', 0)
        
        if tempo < 60:
            suggestions.append(
                f"⏱️ **Tempo**: Slow tempo ({tempo:.1f} BPM). "
                "Great for ambient or ballads. Ensure timing feels intentional."
            )
        elif tempo > 180:
            suggestions.append(
                f"⏱️ **Tempo**: Fast tempo ({tempo:.1f} BPM). "
                "High energy track! Ensure clarity isn't lost at this pace."
            )
        else:
            suggestions.append(
                f"✅ **Tempo**: {tempo:.1f} BPM detected. "
                "Tempo is well-suited for most genres."
            )
        
        # 7. Key detection
        estimated_key = extracted.get('estimated_key', 'Unknown')
        suggestions.append(
            f"🎹 **Key Detection**: Estimated key is {estimated_key}. "
            "Use this as a reference for harmonic mixing or adding complementary elements."
        )
        
        # 8. Overall summary
        suggestion_count = len([s for s in suggestions if s.startswith("✅")])
        total_checks = 7
        
        if suggestion_count >= total_checks * 0.7:
            suggestions.insert(0, 
                "🎉 **Overall**: Your mix shows strong technical qualities! "
                "Most parameters are within optimal ranges."
            )
        else:
            suggestions.insert(0,
                "💡 **Overall**: Your mix has room for improvement in several areas. "
                "Focus on the suggestions below to enhance production quality."
            )
        
        return suggestions

