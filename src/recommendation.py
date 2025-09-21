"""
Movie Recommendation Engine
Combines user preferences with IMDB ratings for personalized recommendations
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class MovieRecommender:
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.df_processed = None
        self.genre_features = None
        self.text_features = None
        self.similarity_matrix = None
        
    def fit(self, df):
        """Process data and build similarity matrix"""
        self.df_processed, self.genre_features, self.text_features = \
            self.data_processor.process_movie_data(df)
        
        # Build similarity matrix based on genre features
        self.similarity_matrix = cosine_similarity(self.genre_features)
        
        return self
    
    def get_recommendations(self, user_preferences, top_n=5, rating_weight=0.7, preference_weight=0.3):
        """
        Get movie recommendations based on user preferences and IMDB ratings
        
        Args:
            user_preferences: dict with 'genres', 'actors', 'directors'
            top_n: number of recommendations to return
            rating_weight: weight for IMDB rating (0-1)
            preference_weight: weight for user preference matching (0-1)
        """
        if self.df_processed is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Create user preference vector
        user_vector = self.data_processor.create_user_preference_vector(
            user_preferences.get('genres', []),
            user_preferences.get('actors', []),
            user_preferences.get('directors', [])
        )
        
        # Calculate preference scores
        preference_scores = []
        for idx in range(len(self.df_processed)):
            movie_features = self.data_processor.get_movie_features(self.df_processed, idx)
            preference_score = self.data_processor.calculate_similarity(user_vector, movie_features)
            preference_scores.append(preference_score)
        
        # Normalize preference scores
        preference_scores = np.array(preference_scores)
        preference_scores = (preference_scores - preference_scores.min()) / (preference_scores.max() - preference_scores.min() + 1e-8)
        
        # Normalize IMDB ratings (0-10 scale to 0-1)
        imdb_scores = self.df_processed['imdb_rating'].values / 10.0
        
        # Combine scores with weights
        combined_scores = (rating_weight * imdb_scores + 
                          preference_weight * preference_scores)
        
        # Get top recommendations
        top_indices = np.argsort(combined_scores)[::-1][:top_n]
        
        recommendations = []
        for idx in top_indices:
            movie = self.df_processed.iloc[idx]
            recommendation = {
                'title': movie['title'],
                'year': movie['year'],
                'genres': movie['genres_clean'],
                'director': movie['director'],
                'actors': movie['actors_clean'],
                'imdb_rating': movie['imdb_rating'],
                'description': movie['description'],
                'preference_score': preference_scores[idx],
                'combined_score': combined_scores[idx],
                'explanation': self._generate_explanation(movie, preference_scores[idx], imdb_scores[idx])
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _generate_explanation(self, movie, preference_score, imdb_score):
        """Generate explanation for why a movie was recommended"""
        explanations = []
        
        if preference_score > 0.7:
            explanations.append("High match with your preferences")
        elif preference_score > 0.4:
            explanations.append("Good match with your preferences")
        else:
            explanations.append("Based on high IMDB rating")
        
        if movie['imdb_rating'] >= 8.5:
            explanations.append("Critically acclaimed")
        elif movie['imdb_rating'] >= 7.5:
            explanations.append("Well-rated by audiences")
        
        if movie['year'] >= 2010:
            explanations.append("Recent release")
        elif movie['year'] >= 1990:
            explanations.append("Classic from the 90s/2000s")
        else:
            explanations.append("Classic film")
        
        return " | ".join(explanations)
    
    def get_similar_movies(self, movie_title, top_n=5):
        """Get movies similar to a specific movie"""
        if self.df_processed is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Find movie index
        movie_idx = self.df_processed[self.df_processed['title'] == movie_title].index
        if len(movie_idx) == 0:
            raise ValueError(f"Movie '{movie_title}' not found in dataset")
        
        movie_idx = movie_idx[0]
        
        # Get similarity scores for this movie
        movie_similarities = self.similarity_matrix[movie_idx]
        
        # Get top similar movies (excluding the movie itself)
        similar_indices = np.argsort(movie_similarities)[::-1][1:top_n+1]
        
        similar_movies = []
        for idx in similar_indices:
            movie = self.df_processed.iloc[idx]
            similar_movies.append({
                'title': movie['title'],
                'year': movie['year'],
                'genres': movie['genres_clean'],
                'imdb_rating': movie['imdb_rating'],
                'similarity_score': movie_similarities[idx]
            })
        
        return similar_movies
    
    def get_genre_recommendations(self, genre, top_n=5, min_rating=7.0):
        """Get top movies in a specific genre above a minimum rating"""
        if self.df_processed is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Filter movies by genre and minimum rating
        genre_mask = self.df_processed[genre] == 1
        rating_mask = self.df_processed['imdb_rating'] >= min_rating
        
        filtered_movies = self.df_processed[genre_mask & rating_mask]
        
        if len(filtered_movies) == 0:
            return []
        
        # Sort by IMDB rating
        top_movies = filtered_movies.nlargest(top_n, 'imdb_rating')
        
        recommendations = []
        for _, movie in top_movies.iterrows():
            recommendations.append({
                'title': movie['title'],
                'year': movie['year'],
                'genres': movie['genres_clean'],
                'director': movie['director'],
                'actors': movie['actors_clean'],
                'imdb_rating': movie['imdb_rating'],
                'description': movie['description']
            })
        
        return recommendations
    
    def analyze_user_taste(self, user_preferences):
        """Analyze user's taste patterns and provide insights"""
        if self.df_processed is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Get user's preferred genres
        preferred_genres = user_preferences.get('genres', [])
        
        # Analyze genre distribution in dataset
        genre_counts = self.genre_features.sum().sort_values(ascending=False)
        
        # Find underrepresented genres
        available_genres = set(self.genre_features.columns)
        user_genres = set(preferred_genres)
        underrepresented = available_genres - user_genres
        
        # Get average ratings for preferred genres
        genre_ratings = {}
        for genre in preferred_genres:
            if genre in self.genre_features.columns:
                genre_movies = self.df_processed[self.genre_features[genre] == 1]
                if len(genre_movies) > 0:
                    genre_ratings[genre] = genre_movies['imdb_rating'].mean()
        
        analysis = {
            'preferred_genres': preferred_genres,
            'total_movies_in_dataset': len(self.df_processed),
            'available_genres': list(available_genres),
            'underrepresented_genres': list(underrepresented),
            'genre_ratings': genre_ratings,
            'recommendations': {
                'explore_genres': list(underrepresented)[:3],
                'high_rated_genres': sorted(genre_ratings.items(), key=lambda x: x[1], reverse=True)[:3]
            }
        }
        
        return analysis
