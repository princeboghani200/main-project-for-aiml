# Movie Recommendation System with IMDB Ratings

A smart movie recommendation system that combines user preferences (genre, actors, directors) with IMDB ratings to suggest the best movies tailored to individual tastes.

## Features

- **Personalized Recommendations**: Based on user's genre preferences, favorite actors, and directors
- **IMDB Rating Integration**: Prioritizes high-rated movies while considering personal taste
- **Smart Filtering**: Combines collaborative and content-based filtering approaches
- **Interactive Web Interface**: Built with Streamlit for easy user interaction
- **Data Analysis**: Comprehensive analysis of movie trends and ratings

## Project Structure

```
PROJECT/
├── data/                   # Movie datasets and processed data
├── models/                 # Trained ML models
├── notebooks/             # Jupyter notebooks for analysis
├── src/                   # Source code
│   ├── data_processing.py # Data cleaning and preprocessing
│   ├── recommendation.py  # Core recommendation algorithms
│   ├── imdb_scraper.py   # IMDB data collection
│   └── web_app.py        # Streamlit web interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the web app**:
   ```bash
   streamlit run src/web_app.py
   ```

2. **Explore data analysis**:
   ```bash
   jupyter notebook
   ```

3. **Train models**:
   ```bash
   python src/recommendation.py
   ```

## How It Works

1. **User Input**: Users select their preferred genres, actors, and directors
2. **Preference Analysis**: System analyzes user's taste patterns
3. **Movie Matching**: Finds movies that match user preferences
4. **Rating Integration**: Combines personal taste with IMDB ratings
5. **Recommendation**: Provides personalized movie suggestions with explanations

## Technologies Used

- **Python**: Core programming language
- **Scikit-learn**: Machine learning algorithms
- **Pandas & NumPy**: Data manipulation and analysis
- **Streamlit**: Web application framework
- **Matplotlib & Seaborn**: Data visualization
- **BeautifulSoup**: Web scraping for IMDB data

## Future Enhancements

- Real-time IMDB data updates
- User rating system integration
- Advanced ML algorithms (deep learning)
- Mobile app version
- Social features (friend recommendations)
