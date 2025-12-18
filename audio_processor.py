import librosa
import numpy as np
from analyzer.feature_extractor import FeatureExtractor
from analyzer.suggestion_engine import SuggestionEngine
from metrics import update_features_count


class AudioProcessor:
    """Main audio processing pipeline"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.suggestion_engine = SuggestionEngine()
    
    def analyze(self, filepath):
        """
        Analyze audio file and return features + suggestions
        
        Args:
            filepath: Path to audio file
            
        Returns:
            dict: Analysis results with features and suggestions
        """
        # Extract features
        features = self.feature_extractor.extract(filepath)
        
        # Update metrics with feature count
        extracted_features = features.get('extracted_features', {})
        feature_count = len(extracted_features)
        if feature_count > 0:
            update_features_count(feature_count)
        
        # Generate suggestions
        suggestions = self.suggestion_engine.generate(features)
        
        return {
            'file_id': filepath.split('/')[-1].split('.')[0],
            'features': features,
            'suggestions': suggestions,
            'status': 'completed'
        }

