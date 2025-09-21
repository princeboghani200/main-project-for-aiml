#!/usr/bin/env python3
"""
Simple Test Script for Movie Recommendation System
Tests basic functionality to ensure no import errors
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported successfully"""
    print("🧪 Testing imports...")
    
    # Add src directory to path
    src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    sys.path.insert(0, src_path)
    
    try:
        from data_processing import MovieDataProcessor
        print("✅ data_processing imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import data_processing: {e}")
        return False
    
    try:
        from recommendation import MovieRecommender
        print("✅ recommendation imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import recommendation: {e}")
        return False
    
    try:
        from imdb_scraper import IMDBScraper
        print("✅ imdb_scraper imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import imdb_scraper: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of the system"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test data processor
        from data_processing import MovieDataProcessor
        data_processor = MovieDataProcessor()
        df = data_processor.load_sample_data()
        print(f"✅ Loaded {len(df)} movies from sample data")
        
        # Test data processing
        df_processed, genre_features, text_features = data_processor.process_movie_data(df)
        print(f"✅ Processed data successfully - {genre_features.shape[1]} genre features")
        
        # Test recommender
        from recommendation import MovieRecommender
        recommender = MovieRecommender(data_processor)
        recommender.fit(df)
        print("✅ Recommender system initialized successfully")
        
        # Test basic recommendation
        user_preferences = {'genres': ['Action'], 'actors': [], 'directors': []}
        recommendations = recommender.get_recommendations(user_preferences, top_n=2)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    print("🎬 Movie Recommendation System - System Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return False
    
    # Test functionality
    if not test_basic_functionality():
        print("\n❌ Functionality tests failed. Please check your installation.")
        return False
    
    print("\n🎉 All tests passed! The system is working correctly.")
    print("\nYou can now:")
    print("  • Run the demo: python demo.py")
    print("  • Start the web app: streamlit run src/web_app.py")
    print("  • Open Jupyter: jupyter notebook notebooks/movie_analysis.ipynb")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
