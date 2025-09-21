"""
Streamlit Web Application for Movie Recommendation System
Provides interactive interface for users to get personalized movie recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add current directory to path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from data_processing import MovieDataProcessor
from recommendation import MovieRecommender
from imdb_scraper import IMDBScraper

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .movie-card {
        background-color: #000000;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .rating-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .genre-tag {
        background-color: #6c757d;
        color: white;
        padding: 0.2rem 0.4rem;
        border-radius: 12px;
        font-size: 0.7rem;
        margin: 0.1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommendation_system():
    """Load and initialize the recommendation system"""
    data_processor = MovieDataProcessor()
    df = data_processor.load_sample_data()
    recommender = MovieRecommender(data_processor)
    recommender.fit(df)
    return recommender, df

@st.cache_data
def get_available_genres(df):
    """Get list of available genres from the dataset"""
    all_genres = []
    for genres in df['genre'].dropna():
        all_genres.extend([g.strip() for g in genres.split(',')])
    return sorted(list(set(all_genres)))

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 Movie Recommendation System</h1>', unsafe_allow_html=True)
    st.markdown("### Get personalized movie recommendations based on your taste and IMDB ratings!")
    
    # Load recommendation system
    recommender, df = load_recommendation_system()
    available_genres = get_available_genres(df)
    
    # Sidebar for user preferences
    st.sidebar.header("🎯 Your Preferences")
    
    # Genre selection
    st.sidebar.subheader("Favorite Genres")
    selected_genres = st.sidebar.multiselect(
        "Select your favorite genres:",
        options=available_genres,
        default=available_genres[:3] if len(available_genres) >= 3 else available_genres
    )
    
    # Actor preferences
    st.sidebar.subheader("Favorite Actors")
    actor_input = st.sidebar.text_input(
        "Enter your favorite actors (comma-separated):",
        placeholder="e.g., Leonardo DiCaprio, Tom Hanks"
    )
    preferred_actors = [actor.strip() for actor in actor_input.split(',')] if actor_input else []
    
    # Director preferences
    st.sidebar.subheader("Favorite Directors")
    director_input = st.sidebar.text_input(
        "Enter your favorite directors (comma-separated):",
        placeholder="e.g., Christopher Nolan, Quentin Tarantino"
    )
    preferred_directors = [director.strip() for director in director_input.split(',')] if director_input else []
    
    # Recommendation parameters
    st.sidebar.subheader("Recommendation Settings")
    num_recommendations = st.sidebar.slider("Number of recommendations:", 3, 10, 5)
    rating_weight = st.sidebar.slider("IMDB Rating Weight:", 0.0, 1.0, 0.7, 0.1)
    preference_weight = st.sidebar.slider("Preference Match Weight:", 0.0, 1.0, 0.3, 0.1)
    
    # Ensure weights sum to 1
    if rating_weight + preference_weight != 1.0:
        st.sidebar.warning("Weights should sum to 1.0")
        preference_weight = 1.0 - rating_weight
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎬 Your Personalized Recommendations")
        
        if st.button("🚀 Get Recommendations", type="primary"):
            if not selected_genres:
                st.error("Please select at least one genre preference!")
            else:
                with st.spinner("Analyzing your preferences and finding the best movies..."):
                    # Prepare user preferences
                    user_preferences = {
                        'genres': selected_genres,
                        'actors': preferred_actors,
                        'directors': preferred_directors
                    }
                    
                    # Get recommendations
                    recommendations = recommender.get_recommendations(
                        user_preferences,
                        top_n=num_recommendations,
                        rating_weight=rating_weight,
                        preference_weight=preference_weight
                    )
                    
                    # Display recommendations
                    for i, rec in enumerate(recommendations, 1):
                        with st.container():
                            st.markdown(f"""
                            <div class="movie-card">
                                <h3>#{i} {rec['title']} ({rec['year']})</h3>
                                <span class="rating-badge">⭐ {rec['imdb_rating']}/10</span>
                                <br><br>
                                <strong>Genres:</strong> {', '.join([f'<span class="genre-tag">{g}</span>' for g in rec['genres']])}
                                <br>
                                <strong>Director:</strong> {rec['director']}
                                <br>
                                <strong>Cast:</strong> {', '.join(rec['actors'])}
                                <br><br>
                                <strong>Why recommended:</strong> {rec['explanation']}
                                <br><br>
                                <em>{rec['description']}</em>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Show user taste analysis
                    st.header("📊 Your Taste Analysis")
                    analysis = recommender.analyze_user_taste(user_preferences)
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.subheader("🎭 Genre Preferences")
                        genre_ratings = analysis['genre_ratings']
                        if genre_ratings:
                            fig = px.bar(
                                x=list(genre_ratings.keys()),
                                y=list(genre_ratings.values()),
                                title="Average IMDB Ratings for Your Preferred Genres",
                                labels={'x': 'Genre', 'y': 'Average Rating'}
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col_b:
                        st.subheader("🔍 Explore New Genres")
                        underrepresented = analysis['underrepresented_genres']
                        if underrepresented:
                            st.info(f"Consider exploring these genres: {', '.join(underrepresented[:5])}")
                        
                        st.subheader("📈 High-Rated Genres")
                        high_rated = analysis['recommendations']['high_rated_genres']
                        if high_rated:
                            for genre, rating in high_rated:
                                st.metric(genre, f"{rating:.1f}/10")
    
    with col2:
        st.header("📚 Quick Actions")
        
        # Similar movies finder
        st.subheader("🔍 Find Similar Movies")
        movie_search = st.selectbox(
            "Select a movie to find similar ones:",
            options=df['title'].tolist()
        )
        
        if st.button("Find Similar"):
            with st.spinner("Finding similar movies..."):
                similar_movies = recommender.get_similar_movies(movie_search, top_n=5)
                
                st.subheader("Similar Movies:")
                for movie in similar_movies:
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>{movie['title']} ({movie['year']})</h4>
                        <span class="rating-badge">⭐ {movie['imdb_rating']}/10</span>
                        <br>
                        <strong>Genres:</strong> {', '.join([f'<span class="genre-tag">{g}</span>' for g in movie['genres']])}
                        <br>
                        <strong>Similarity:</strong> {movie['similarity_score']:.2f}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Genre recommendations
        st.subheader("🎭 Top Movies by Genre")
        genre_choice = st.selectbox(
            "Select a genre:",
            options=available_genres
        )
        
        if st.button("Get Top Movies"):
            with st.spinner("Finding top movies in this genre..."):
                genre_movies = recommender.get_genre_recommendations(genre_choice, top_n=5, min_rating=7.0)
                
                st.subheader(f"Top {genre_choice} Movies:")
                for movie in genre_movies:
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>{movie['title']} ({movie['year']})</h4>
                        <span class="rating-badge">⭐ {movie['imdb_rating']}/10</span>
                        <br>
                        <strong>Director:</strong> {movie['director']}
                        <br>
                        <strong>Cast:</strong> {', '.join(movie['actors'])}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎬 Movie Recommendation System | Powered by Machine Learning & IMDB Ratings</p>
        <p>Get personalized movie suggestions based on your taste and critical acclaim!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
