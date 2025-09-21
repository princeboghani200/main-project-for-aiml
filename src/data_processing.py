"""
Data Processing Module for Movie Recommendation System
Handles data cleaning, preprocessing, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import re
import json

class MovieDataProcessor:
    def __init__(self):
        self.genre_encoder = MultiLabelBinarizer()
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
    def load_sample_data(self):
        """Load sample movie data (in real scenario, this would be from IMDB API or database)"""
        sample_data = {
            'title': [
                'The Shawshank Redemption', 'The Godfather', 'The Dark Knight',
                'Pulp Fiction', 'Fight Club', 'Forrest Gump', 'Inception',
                'The Matrix', 'Goodfellas', 'The Silence of the Lambs'
            ],
            'genre': [
                'Drama', 'Crime, Drama', 'Action, Crime, Drama',
                'Crime, Drama', 'Drama', 'Drama, Romance', 'Action, Adventure, Sci-Fi',
                'Action, Sci-Fi', 'Biography, Crime, Drama', 'Crime, Drama, Thriller'
            ],
            'director': [
                'Frank Darabont', 'Francis Ford Coppola', 'Christopher Nolan',
                'Quentin Tarantino', 'David Fincher', 'Robert Zemeckis', 'Christopher Nolan',
                'Lana Wachowski, Lilly Wachowski', 'Martin Scorsese', 'Jonathan Demme'
            ],
            'actors': [
                'Tim Robbins, Morgan Freeman', 'Marlon Brando, Al Pacino',
                'Christian Bale, Heath Ledger', 'John Travolta, Samuel L. Jackson',
                'Brad Pitt, Edward Norton', 'Tom Hanks, Robin Wright',
                'Leonardo DiCaprio, Joseph Gordon-Levitt', 'Keanu Reeves, Laurence Fishburne',
                'Robert De Niro, Ray Liotta', 'Jodie Foster, Anthony Hopkins'
            ],
            'imdb_rating': [9.3, 9.2, 9.0, 8.9, 8.8, 8.8, 8.8, 8.7, 8.7, 8.6],
            'year': [1994, 1972, 2008, 1994, 1999, 1994, 2010, 1999, 1990, 1991],
            'description': [
                'Two imprisoned men bond over a number of years...',
                'The aging patriarch of an organized crime dynasty...',
                'When the menace known as the Joker wreaks havoc...',
                'The lives of two mob hitmen, a boxer, a gangster...',
                'An insomniac office worker and a devil-may-care...',
                'The presidencies of Kennedy and Johnson...',
                'A thief who steals corporate secrets through...',
                'A computer programmer discovers that reality...',
                'The story of Henry Hill and his life in the mob...',
                'A young F.B.I. cadet must receive the help of...'
            ]
        }
        return pd.DataFrame(sample_data)
    
    def clean_genres(self, genre_string):
        """Clean and standardize genre strings"""
        if pd.isna(genre_string):
            return []
        # Split by comma and clean each genre
        genres = [genre.strip() for genre in str(genre_string).split(',')]
        # Remove empty strings and standardize
        genres = [genre for genre in genres if genre and genre != 'nan']
        return genres
    
    def clean_actors(self, actors_string):
        """Clean and standardize actor strings"""
        if pd.isna(actors_string):
            return []
        # Split by comma and clean each actor name
        actors = [actor.strip() for actor in str(actors_string).split(',')]
        # Remove empty strings and standardize
        actors = [actor for actor in actors if actor and actor != 'nan']
        return actors
    
    def clean_directors(self, director_string):
        """Clean and standardize director strings"""
        if pd.isna(director_string):
            return []
        # Split by comma and clean each director name
        directors = [director.strip() for director in str(director_string).split(',')]
        # Remove empty strings and standardize
        directors = [director for director in directors if director and director != 'nan']
        return directors
    
    def process_movie_data(self, df):
        """Process and clean the movie dataset"""
        # Clean genres, actors, and directors
        df['genres_clean'] = df['genre'].apply(self.clean_genres)
        df['actors_clean'] = df['actors'].apply(self.clean_actors)
        df['directors_clean'] = df['director'].apply(self.clean_directors)
        
        # Create genre features
        genre_matrix = self.genre_encoder.fit_transform(df['genres_clean'])
        genre_features = pd.DataFrame(
            genre_matrix, 
            columns=self.genre_encoder.classes_,
            index=df.index
        )
        
        # Create text features from description
        text_features = self.tfidf_vectorizer.fit_transform(df['description'].fillna(''))
        
        # Combine all features
        df_processed = df.copy()
        df_processed = pd.concat([df_processed, genre_features], axis=1)
        
        return df_processed, genre_features, text_features
    
    def create_user_preference_vector(self, preferred_genres, preferred_actors, preferred_directors):
        """Create a user preference vector for recommendation"""
        # Initialize preference vector
        preference_vector = np.zeros(len(self.genre_encoder.classes_))
        
        # Set preferred genres to 1
        for genre in preferred_genres:
            if genre in self.genre_encoder.classes_:
                genre_idx = list(self.genre_encoder.classes_).index(genre)
                preference_vector[genre_idx] = 1
        
        return preference_vector
    
    def calculate_similarity(self, user_preferences, movie_features):
        """Calculate similarity between user preferences and movie features"""
        # Cosine similarity between user preferences and movie genre features
        similarity = np.dot(user_preferences, movie_features) / (
            np.linalg.norm(user_preferences) * np.linalg.norm(movie_features) + 1e-8
        )
        return similarity
    
    def get_movie_features(self, df_processed, movie_id):
        """Get feature vector for a specific movie"""
        movie_row = df_processed.iloc[movie_id]
        genre_features = movie_row[self.genre_encoder.classes_].values
        return genre_features
