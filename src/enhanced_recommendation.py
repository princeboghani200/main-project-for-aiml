"""
Enhanced Movie and Web Series Recommendation System
Supports movies, web series, posters, and multiple languages
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer
import re

class EnhancedMovieRecommender:
    def __init__(self, data_provider):
        self.data_provider = data_provider
        self.df = None
        self.tfidf_matrix = None
        self.genre_matrix = None
        self.similarity_matrix = None
        self.is_fitted = False
    
    def fit(self, df=None):
        """Fit the recommendation system with data"""
        if df is None:
            self.df = self.data_provider.get_all_data()
        else:
            self.df = df
        
        # Process genres
        self.df['genres'] = self.df['genre'].apply(lambda x: [g.strip() for g in str(x).split(',')])
        
        # Create genre matrix
        mlb = MultiLabelBinarizer()
        self.genre_matrix = pd.DataFrame(
            mlb.fit_transform(self.df['genres']),
            columns=mlb.classes_,
            index=self.df.index
        )
        
        # Create text features for TF-IDF
        self.df['text_features'] = self.df.apply(self._create_text_features, axis=1)
        
        # TF-IDF vectorization
        tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.df['text_features'])
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
        
        self.is_fitted = True
        return self
    
    def _create_text_features(self, row):
        """Create text features for TF-IDF"""
        features = []
        features.append(str(row['title']))
        features.append(str(row['director']))
        features.append(str(row['actors']))
        features.append(str(row['description']))
        features.append(str(row['country']))
        features.append(str(row['type']))
        features.append(str(row['language']))
        return ' '.join(features)
    
    def get_recommendations(self, user_preferences, top_n=5, rating_weight=0.7, preference_weight=0.3):
        """Get personalized recommendations based on user preferences"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting recommendations")
        
        # Filter by content type if specified
        content_type = user_preferences.get('content_type', 'all')
        if content_type != 'all':
            filtered_df = self.df[self.df['type'] == content_type]
        else:
            filtered_df = self.df
        
        # Filter by language if specified
        language = user_preferences.get('language', 'all')
        if language != 'all':
            filtered_df = filtered_df[filtered_df['language'] == language]
        
        # Check if we have any data after filtering
        if len(filtered_df) == 0:
            return []
        
        # Calculate preference scores
        preference_scores = self._calculate_preference_scores(filtered_df, user_preferences)
        
        # Get IMDB ratings
        imdb_scores = filtered_df['imdb_rating'].values
        
        # Normalize scores safely
        if len(preference_scores) > 0:
            pref_min, pref_max = preference_scores.min(), preference_scores.max()
            if pref_max > pref_min:
                preference_scores = (preference_scores - pref_min) / (pref_max - pref_min)
            else:
                preference_scores = np.zeros_like(preference_scores)
        
        if len(imdb_scores) > 0:
            imdb_min, imdb_max = imdb_scores.min(), imdb_scores.max()
            if imdb_max > imdb_min:
                imdb_scores = (imdb_scores - imdb_min) / (imdb_max - imdb_min)
            else:
                imdb_scores = np.ones_like(imdb_scores)
        
        # Combine scores
        combined_scores = (rating_weight * imdb_scores + preference_weight * preference_scores)
        
        # Get top recommendations
        top_indices = np.argsort(combined_scores)[::-1][:min(top_n, len(filtered_df))]
        
        recommendations = []
        for idx in top_indices:
            movie = filtered_df.iloc[idx]
            recommendations.append({
                'title': movie['title'],
                'year': movie['year'],
                'type': movie['type'],
                'genres': movie['genres'],
                'director': movie['director'],
                'actors': movie['actors'].split(',') if pd.notna(movie['actors']) else [],
                'imdb_rating': movie['imdb_rating'],
                'description': movie['description'],
                'poster_url': movie['poster_url'],
                'language': movie['language'],
                'duration': movie['duration'],
                'country': movie['country'],
                'explanation': self._explain_recommendation(movie, user_preferences),
                'similarity_score': float(combined_scores[idx])
            })
        
        return recommendations
    
    def _calculate_preference_scores(self, df, user_preferences):
        """Calculate preference match scores"""
        scores = np.zeros(len(df))
        
        # Genre preference
        if 'genres' in user_preferences and user_preferences['genres']:
            for i, movie in df.iterrows():
                movie_genres = set(movie['genres'])
                user_genres = set(user_preferences['genres'])
                genre_overlap = len(movie_genres.intersection(user_genres))
                scores[i] += genre_overlap * 2  # Higher weight for genres
        
        # Actor preference
        if 'actors' in user_preferences and user_preferences['actors']:
            for i, movie in df.iterrows():
                if pd.notna(movie['actors']):
                    movie_actors = set([a.strip().lower() for a in movie['actors'].split(',')])
                    user_actors = set([a.strip().lower() for a in user_preferences['actors']])
                    actor_overlap = len(movie_actors.intersection(user_actors))
                    scores[i] += actor_overlap * 1.5
        
        # Director preference
        if 'directors' in user_preferences and user_preferences['directors']:
            for i, movie in df.iterrows():
                if pd.notna(movie['director']):
                    movie_director = movie['director'].strip().lower()
                    user_directors = [d.strip().lower() for d in user_preferences['directors']]
                    if movie_director in user_directors:
                        scores[i] += 1.5
        
        return scores
    
    def _explain_recommendation(self, movie, user_preferences):
        """Explain why a movie was recommended"""
        reasons = []
        
        # Genre match
        if 'genres' in user_preferences and user_preferences['genres']:
            movie_genres = set(movie['genres'])
            user_genres = set(user_preferences['genres'])
            genre_overlap = movie_genres.intersection(user_genres)
            if genre_overlap:
                reasons.append(f"Matches your preferred genres: {', '.join(genre_overlap)}")
        
        # Actor match
        if 'actors' in user_preferences and user_preferences['actors'] and pd.notna(movie['actors']):
            movie_actors = set([a.strip().lower() for a in movie['actors'].split(',')])
            user_actors = set([a.strip().lower() for a in user_preferences['actors']])
            actor_overlap = movie_actors.intersection(user_actors)
            if actor_overlap:
                reasons.append(f"Features your favorite actors: {', '.join(actor_overlap)}")
        
        # Director match
        if 'directors' in user_preferences and user_preferences['directors'] and pd.notna(movie['director']):
            movie_director = movie['director'].strip().lower()
            user_directors = [d.strip().lower() for d in user_preferences['directors']]
            if movie_director in user_directors:
                reasons.append(f"Directed by your favorite director: {movie['director']}")
        
        # High rating
        if movie['imdb_rating'] >= 8.0:
            reasons.append(f"Highly rated with {movie['imdb_rating']}/10 on IMDB")
        elif movie['imdb_rating'] >= 7.0:
            reasons.append(f"Well-rated with {movie['imdb_rating']}/10 on IMDB")
        
        if not reasons:
            reasons.append("Recommended based on overall popularity and quality")
        
        return " | ".join(reasons)
    
    def get_similar_movies(self, title, top_n=5):
        """Find movies similar to a given title"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting similar movies")
        
        # Find the movie index
        movie_idx = self.df[self.df['title'] == title].index
        if len(movie_idx) == 0:
            return []
        
        movie_idx = movie_idx[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[movie_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top similar movies (excluding itself)
        sim_scores = sim_scores[1:min(top_n+1, len(sim_scores))]
        movie_indices = [i[0] for i in sim_scores]
        
        similar_movies = []
        for idx in movie_indices:
            movie = self.df.iloc[idx]
            similar_movies.append({
                'title': movie['title'],
                'year': movie['year'],
                'type': movie['type'],
                'genres': movie['genres'],
                'director': movie['director'],
                'actors': movie['actors'].split(',') if pd.notna(movie['actors']) else [],
                'imdb_rating': movie['imdb_rating'],
                'poster_url': movie['poster_url'],
                'language': movie['language'],
                'similarity_score': float(sim_scores[movie_indices.index(idx)][1])
            })
        
        return similar_movies
    
    def get_genre_recommendations(self, genre, top_n=5, min_rating=7.0):
        """Get top movies in a specific genre"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting genre recommendations")
        
        # Filter by genre and minimum rating
        genre_movies = self.df[
            (self.df['genres'].apply(lambda x: genre in x)) & 
            (self.df['imdb_rating'] >= min_rating)
        ].sort_values('imdb_rating', ascending=False)
        
        if len(genre_movies) == 0:
            return []
        
        recommendations = []
        for _, movie in genre_movies.head(top_n).iterrows():
            recommendations.append({
                'title': movie['title'],
                'year': movie['year'],
                'type': movie['type'],
                'genres': movie['genres'],
                'director': movie['director'],
                'actors': movie['actors'].split(',') if pd.notna(movie['actors']) else [],
                'imdb_rating': movie['imdb_rating'],
                'poster_url': movie['poster_url'],
                'language': movie['language'],
                'duration': movie['duration']
            })
        
        return recommendations
    
    def get_language_recommendations(self, language, top_n=5):
        """Get top content in a specific language"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting language recommendations")
        
        language_content = self.df[self.df['language'] == language].sort_values('imdb_rating', ascending=False)
        
        if len(language_content) == 0:
            return []
        
        recommendations = []
        for _, content in language_content.head(top_n).iterrows():
            recommendations.append({
                'title': content['title'],
                'year': content['year'],
                'type': content['type'],
                'genres': content['genres'],
                'director': content['director'],
                'actors': content['actors'].split(',') if pd.notna(content['actors']) else [],
                'imdb_rating': content['imdb_rating'],
                'poster_url': content['poster_url'],
                'language': content['language'],
                'duration': content['duration']
            })
        
        return recommendations
    
    def analyze_user_taste(self, user_preferences):
        """Analyze user's taste preferences"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before analyzing user taste")
        
        # Get user's preferred genres
        user_genres = user_preferences.get('genres', [])
        
        # Calculate average ratings for preferred genres
        genre_ratings = {}
        for genre in user_genres:
            genre_movies = self.df[self.df['genres'].apply(lambda x: genre in x)]
            if len(genre_movies) > 0:
                genre_ratings[genre] = genre_movies['imdb_rating'].mean()
        
        # Find underrepresented genres
        all_genres = set()
        for genres in self.df['genres']:
            all_genres.update(genres)
        
        underrepresented = list(all_genres - set(user_genres))
        
        # Get high-rated content recommendations
        high_rated = self.df[self.df['imdb_rating'] >= 8.0].sort_values('imdb_rating', ascending=False)
        high_rated_genres = []
        for _, content in high_rated.head(10).iterrows():
            for genre in content['genres']:
                if genre not in user_genres:
                    high_rated_genres.append((genre, content['imdb_rating']))
                    break
        
        return {
            'genre_ratings': genre_ratings,
            'underrepresented_genres': underrepresented,
            'recommendations': {
                'high_rated_genres': high_rated_genres[:5]
            }
        }
