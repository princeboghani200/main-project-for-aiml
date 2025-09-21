#!/usr/bin/env python3
"""
Demo Script for Movie Recommendation System
Demonstrates the core functionality of the recommendation engine
"""

import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

try:
    from data_processing import MovieDataProcessor
    from recommendation import MovieRecommender
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def main():
    print("🎬 Movie Recommendation System Demo")
    print("=" * 50)
    
    # Initialize the system
    print("\n1. Initializing the system...")
    try:
        data_processor = MovieDataProcessor()
        df = data_processor.load_sample_data()
        
        print(f"   Loaded {len(df)} movies")
        print(f"   Available genres: {', '.join(set([g.strip() for genres in df['genre'].dropna() for g in genres.split(',')]))}")
        
        # Process data
        print("\n2. Processing movie data...")
        df_processed, genre_features, text_features = data_processor.process_movie_data(df)
        print(f"   Created {genre_features.shape[1]} genre features")
        
        # Initialize recommender
        print("\n3. Training recommendation model...")
        recommender = MovieRecommender(data_processor)
        recommender.fit(df)
        print("   Model trained successfully!")
        
        # Test different user profiles
        test_users = [
            {
                'name': 'Action Movie Fan',
                'preferences': {
                    'genres': ['Action'],
                    'actors': [],
                    'directors': []
                }
            },
            {
                'name': 'Drama Lover',
                'preferences': {
                    'genres': ['Drama'],
                    'actors': [],
                    'directors': []
                }
            },
            {
                'name': 'Christopher Nolan Fan',
                'preferences': {
                    'genres': [],
                    'actors': [],
                    'directors': ['Christopher Nolan']
                }
            },
            {
                'name': 'Balanced Viewer',
                'preferences': {
                    'genres': ['Action', 'Drama', 'Crime'],
                    'actors': ['Leonardo DiCaprio'],
                    'directors': ['Christopher Nolan']
                }
            }
        ]
        
        print("\n4. Testing recommendations for different user profiles...")
        print("=" * 60)
        
        for user in test_users:
            print(f"\n👤 User: {user['name']}")
            print(f"   Preferences: {user['preferences']}")
            
            try:
                # Get recommendations
                recommendations = recommender.get_recommendations(
                    user['preferences'], 
                    top_n=3,
                    rating_weight=0.7,
                    preference_weight=0.3
                )
                
                print("   🎯 Top 3 Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"      {i}. {rec['title']} ({rec['year']}) - ⭐ {rec['imdb_rating']}/10")
                    print(f"         Genres: {', '.join(rec['genres'])}")
                    print(f"         Director: {rec['director']}")
                    print(f"         Why: {rec['explanation']}")
                    print()
            
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Test similar movies
        print("\n5. Testing similar movie finder...")
        print("=" * 40)
        
        test_movie = "The Dark Knight"
        try:
            similar_movies = recommender.get_similar_movies(test_movie, top_n=3)
            
            print(f"\n🎭 Movies similar to '{test_movie}':")
            for i, movie in enumerate(similar_movies, 1):
                print(f"   {i}. {movie['title']} ({movie['year']}) - ⭐ {movie['imdb_rating']}/10")
                print(f"      Similarity Score: {movie['similarity_score']:.2f}")
        except Exception as e:
            print(f"   ❌ Error finding similar movies: {e}")
        
        # Test genre recommendations
        print("\n6. Testing genre-based recommendations...")
        print("=" * 45)
        
        test_genre = "Action"
        try:
            genre_movies = recommender.get_genre_recommendations(test_genre, top_n=3, min_rating=7.5)
            
            print(f"\n🎬 Top {test_genre} movies (rating >= 7.5):")
            for i, movie in enumerate(genre_movies, 1):
                print(f"   {i}. {movie['title']} ({movie['year']}) - ⭐ {movie['imdb_rating']}/10")
                print(f"      Director: {movie['director']}")
        except Exception as e:
            print(f"   ❌ Error getting genre recommendations: {e}")
        
        # User taste analysis
        print("\n7. Testing user taste analysis...")
        print("=" * 40)
        
        user_preferences = {'genres': ['Action', 'Drama'], 'actors': ['Leonardo DiCaprio'], 'directors': []}
        try:
            analysis = recommender.analyze_user_taste(user_preferences)
            
            print(f"\n📊 Taste Analysis for user with preferences: {user_preferences}")
            print(f"   Preferred Genres: {analysis['preferred_genres']}")
            print(f"   Total Movies in Dataset: {analysis['total_movies_in_dataset']}")
            print(f"   Available Genres: {analysis['available_genres']}")
            print(f"   Underrepresented Genres: {analysis['underrepresented_genres']}")
            print(f"   Genre Ratings: {analysis['genre_ratings']}")
            print(f"   Recommendations to Explore: {analysis['recommendations']['explore_genres']}")
            print(f"   High-Rated Genres: {analysis['recommendations']['high_rated_genres']}")
        except Exception as e:
            print(f"   ❌ Error analyzing user taste: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\nTo run the web application:")
        print("   streamlit run src/web_app.py")
        print("\nTo explore data analysis:")
        print("   jupyter notebook notebooks/movie_analysis.ipynb")
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check that all dependencies are installed:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
