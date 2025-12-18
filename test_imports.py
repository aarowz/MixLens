"""
Quick import test to verify all dependencies are installed correctly
Run: python test_imports.py
"""
import sys

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    
    try:
        import flask
        print("✅ Flask")
    except ImportError as e:
        print(f"❌ Flask: {e}")
        return False
    
    try:
        import librosa
        print("✅ librosa")
    except ImportError as e:
        print(f"❌ librosa: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    try:
        import scipy
        print("✅ SciPy")
    except ImportError as e:
        print(f"❌ SciPy: {e}")
        return False
    
    try:
        import matplotlib
        print("✅ Matplotlib")
    except ImportError as e:
        print(f"❌ Matplotlib: {e}")
        return False
    
    try:
        import streamlit
        print("✅ Streamlit")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False
    
    try:
        import pandas
        print("✅ Pandas")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        return False
    
    # Test local imports
    try:
        from metrics import METRICS
        print("✅ metrics.py")
    except ImportError as e:
        print(f"❌ metrics.py: {e}")
        return False
    
    try:
        from analyzer.feature_extractor import FeatureExtractor
        print("✅ analyzer.feature_extractor")
    except ImportError as e:
        print(f"❌ analyzer.feature_extractor: {e}")
        return False
    
    try:
        from analyzer.suggestion_engine import SuggestionEngine
        print("✅ analyzer.suggestion_engine")
    except ImportError as e:
        print(f"❌ analyzer.suggestion_engine: {e}")
        return False
    
    try:
        from analyzer.visualizer import Visualizer
        print("✅ analyzer.visualizer")
    except ImportError as e:
        print(f"❌ analyzer.visualizer: {e}")
        return False
    
    try:
        from audio_processor import AudioProcessor
        print("✅ audio_processor")
    except ImportError as e:
        print(f"❌ audio_processor: {e}")
        return False
    
    print("\n🎉 All imports successful! Ready to run MixLens.")
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

