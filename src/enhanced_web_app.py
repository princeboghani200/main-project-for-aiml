"""
Enhanced Streamlit Web Application for Movie and Web Series Recommendation System
Features: Movie posters, web series, multiple languages (Hindi, English, Hindi Dubbed)
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

from enhanced_data import EnhancedDataProvider
from enhanced_recommendation import EnhancedMovieRecommender

# Page configuration
st.set_page_config(
    page_title="Enhanced Movie & Web Series Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with posters
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .movie-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
    }
    .movie-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .rating-badge {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .genre-tag {
        background: linear-gradient(45deg, #6c757d, #495057);
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .poster-container {
        text-align: center;
        margin: 1rem 0;
    }
    .poster-image {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        max-width: 200px;
        height: auto;
    }
    .content-type-badge {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    .language-badge {
        background: linear-gradient(45deg, #4ecdc4, #44a08d);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    .sidebar-section {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .stat-item {
        text-align: center;
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def load_recommendation_system():
    """Load and initialize the enhanced recommendation system"""
    try:
        data_provider = EnhancedDataProvider()
        df = data_provider.get_all_data()
        recommender = EnhancedMovieRecommender(data_provider)
        recommender.fit(df)
        return recommender, df, data_provider
    except Exception as e:
        st.error(f"Error loading recommendation system: {str(e)}")
        return None, None, None

def get_available_genres(df):
    """Get list of available genres from the dataset"""
    if df is None:
        return []
    all_genres = []
    for genres in df['genre'].dropna():
        all_genres.extend([g.strip() for g in genres.split(',')])
    return sorted(list(set(all_genres)))

def display_movie_card(movie, index=None):
    """Display a movie card with poster and enhanced styling"""
    index_text = f"#{index} " if index else ""
    
    st.markdown(f"""
    <div class="movie-card">
        <div class="poster-container">
            <img src="{movie['poster_url']}" alt="{movie['title']}" class="poster-image" 
                 onerror="this.src='https://via.placeholder.com/200x300/cccccc/666666?text=Poster+Not+Found'">
        </div>
        
        <h3>{index_text}{movie['title']} ({movie['year']})</h3>
        
        <div class="stats-container">
            <span class="rating-badge">⭐ {movie['imdb_rating']}/10</span>
            <span class="content-type-badge">{movie['type'].replace('_', ' ').title()}</span>
            <span class="language-badge">{movie['language']}</span>
        </div>
        
        <br>
        <strong>Genres:</strong> {', '.join([f'<span class="genre-tag">{g}</span>' for g in movie['genres']])}
        <br>
        <strong>Director:</strong> {movie['director']}
        <br>
        <strong>Cast:</strong> {', '.join(movie['actors'])}
        <br>
        <strong>Duration:</strong> {movie['duration']}
        <br>
        <strong>Country:</strong> {movie['country']}
        <br><br>
        <strong>Why recommended:</strong> {movie['explanation']}
        <br><br>
        <em>{movie['description']}</em>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 Enhanced Movie & Web Series Recommendation System</h1>', unsafe_allow_html=True)
    st.markdown("### Get personalized recommendations for movies and web series with posters, multiple languages, and smart AI!")
    
    # Load recommendation system
    recommender, df, data_provider = load_recommendation_system()
    
    if recommender is None or df is None or data_provider is None:
        st.error("Failed to load the recommendation system. Please check the console for errors.")
        return
    
    available_genres = get_available_genres(df)
    available_languages = data_provider.get_available_languages()
    available_types = data_provider.get_available_types()
    
    # Sidebar for user preferences
    st.sidebar.header("🎯 Your Preferences")
    
    # Content type selection
    st.sidebar.subheader("Content Type")
    content_type = st.sidebar.selectbox(
        "Choose content type:",
        options=['all'] + available_types,
        format_func=lambda x: 'All Content' if x == 'all' else x.replace('_', ' ').title()
    )
    
    # Language selection
    st.sidebar.subheader("Language Preference")
    language = st.sidebar.selectbox(
        "Choose language:",
        options=['all'] + available_languages,
        format_func=lambda x: 'All Languages' if x == 'all' else x
    )
    
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
        placeholder="e.g., Leonardo DiCaprio, Tom Hanks, Aamir Khan"
    )
    preferred_actors = [actor.strip() for actor in actor_input.split(',')] if actor_input else []
    
    # Director preferences
    st.sidebar.subheader("Favorite Directors")
    director_input = st.sidebar.text_input(
        "Enter your favorite directors (comma-separated):",
        placeholder="e.g., Christopher Nolan, Quentin Tarantino, Rajkumar Hirani"
    )
    preferred_directors = [director.strip() for director in director_input.split(',')] if director_input else []
    
    # Recommendation parameters
    st.sidebar.subheader("Recommendation Settings")
    num_recommendations = st.sidebar.slider("Number of recommendations:", 3, 15, 6)
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
        
        if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
            if not selected_genres:
                st.error("Please select at least one genre preference!")
            else:
                with st.spinner("Analyzing your preferences and finding the best content..."):
                    try:
                        # Prepare user preferences
                        user_preferences = {
                            'content_type': content_type,
                            'language': language,
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
                        
                        if not recommendations:
                            st.warning("No recommendations found for your current preferences. Try adjusting your filters.")
                        else:
                            # Display recommendations
                            for i, rec in enumerate(recommendations, 1):
                                display_movie_card(rec, i)
                            
                            # Show user taste analysis
                            st.header("📊 Your Taste Analysis")
                            try:
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
                                            labels={'x': 'Genre', 'y': 'Average Rating'},
                                            color=list(genre_ratings.values()),
                                            color_continuous_scale='viridis'
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
                            except Exception as e:
                                st.error(f"Error analyzing user taste: {str(e)}")
                    except Exception as e:
                        st.error(f"Error getting recommendations: {str(e)}")
    
    with col2:
        st.header("📚 Quick Actions")
        
        # Content type filter
        st.subheader("🎬 Browse by Type")
        browse_type = st.selectbox(
            "Select content type to browse:",
            options=available_types,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if st.button(f"Browse {browse_type.replace('_', ' ').title()}"):
            try:
                type_content = data_provider.get_by_type_and_language(browse_type, 'all')
                st.subheader(f"Top {browse_type.replace('_', ' ').title()}")
                for _, content in type_content.head(5).iterrows():
                    st.markdown(f"**{content['title']}** ({content['year']}) - ⭐ {content['imdb_rating']}/10")
                    st.markdown(f"*{content['language']} • {content['duration']}*")
                    st.markdown("---")
            except Exception as e:
                st.error(f"Error browsing by type: {str(e)}")
        
        # Language filter
        st.subheader("🌍 Browse by Language")
        browse_language = st.selectbox(
            "Select language to browse:",
            options=available_languages
        )
        
        if st.button(f"Browse {browse_language}"):
            try:
                language_content = recommender.get_language_recommendations(browse_language, top_n=5)
                if language_content:
                    st.subheader(f"Top {browse_language} Content")
                    for content in language_content:
                        st.markdown(f"**{content['title']}** ({content['year']}) - ⭐ {content['imdb_rating']}/10")
                        st.markdown(f"*{content['type'].replace('_', ' ').title()} • {content['duration']}*")
                        st.markdown("---")
                else:
                    st.info(f"No {browse_language} content found.")
            except Exception as e:
                st.error(f"Error browsing by language: {str(e)}")
        
        # Similar content finder
        st.subheader("🔍 Find Similar Content")
        content_search = st.selectbox(
            "Select content to find similar ones:",
            options=df['title'].tolist()
        )
        
        if st.button("Find Similar"):
            with st.spinner("Finding similar content..."):
                try:
                    similar_content = recommender.get_similar_movies(content_search, top_n=3)
                    if similar_content:
                        st.subheader("Similar Content:")
                        for content in similar_content:
                            st.markdown(f"**{content['title']}** ({content['year']}) - ⭐ {content['imdb_rating']}/10")
                            st.markdown(f"*Similarity: {content['similarity_score']:.2f}*")
                            st.markdown("---")
                    else:
                        st.info("No similar content found.")
                except Exception as e:
                    st.error(f"Error finding similar content: {str(e)}")
        
        # Genre recommendations
        st.subheader("🎭 Top Content by Genre")
        genre_choice = st.selectbox(
            "Select a genre:",
            options=available_genres
        )
        
        if st.button("Get Top Content"):
            with st.spinner("Finding top content in this genre..."):
                try:
                    genre_content = recommender.get_genre_recommendations(genre_choice, top_n=3, min_rating=7.0)
                    if genre_content:
                        st.subheader(f"Top {genre_choice} Content:")
                        for content in genre_content:
                            st.markdown(f"**{content['title']}** ({content['year']}) - ⭐ {content['imdb_rating']}/10")
                            st.markdown(f"*{content['type'].replace('_', ' ').title()} • {content['language']}*")
                            st.markdown("---")
                    else:
                        st.info(f"No {genre_choice} content found with rating 7.0+.")
                except Exception as e:
                    st.error(f"Error getting genre recommendations: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🎬 Enhanced Movie & Web Series Recommendation System | Powered by AI & IMDB Ratings</p>
        <p>Get personalized recommendations for movies and web series in Hindi, English, and Hindi Dubbed!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
