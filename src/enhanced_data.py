"""
Enhanced Movie and Web Series Data with Posters and Language Support
Includes movies, web series, posters, and multiple languages (Hindi, English, Hindi Dubbed)
"""

import pandas as pd
import numpy as np

class EnhancedDataProvider:
    def __init__(self):
        self.movies_data = self._create_enhanced_dataset()
    
    def _create_enhanced_dataset(self):
        """Create comprehensive dataset with movies, web series, posters, and languages"""
        
        # Enhanced dataset with movies and web series
        data = [
            # Movies - Action
            {
                'title': 'The Avengers',
                'year': 2012,
                'type': 'movie',
                'genre': 'Action,Adventure,Sci-Fi',
                'language': 'English',
                'director': 'Joss Whedon',
                'actors': 'Robert Downey Jr.,Chris Evans,Scarlett Johansson',
                'imdb_rating': 8.0,
                'description': 'Earth\'s mightiest heroes must come together to stop Loki and his army.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_.jpg',
                'duration': '143 min',
                'country': 'USA'
            },
            {
                'title': 'The Dark Knight',
                'year': 2008,
                'type': 'movie',
                'genre': 'Action,Crime,Drama',
                'language': 'English',
                'director': 'Christopher Nolan',
                'actors': 'Christian Bale,Heath Ledger,Aaron Eckhart',
                'imdb_rating': 9.0,
                'description': 'Batman faces his greatest challenge when the mysterious Joker wreaks havoc on Gotham.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTY5OTU0OTc2NV5BMl5BanBnXkFtZTcwMzU3NTI4NA@@._V1_.jpg',
                'duration': '152 min',
                'country': 'USA'
            },
            {
                'title': 'Inception',
                'year': 2010,
                'type': 'movie',
                'genre': 'Action,Adventure,Sci-Fi',
                'language': 'English',
                'director': 'Christopher Nolan',
                'actors': 'Leonardo DiCaprio,Joseph Gordon-Levitt,Ellen Page',
                'imdb_rating': 8.8,
                'description': 'A thief who steals corporate secrets through dream-sharing technology.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTk3NDE2NzI4NF5BMl5BanBnXkFtZTgwNzE1MzEyMTE@._V1_.jpg',
                'duration': '148 min',
                'country': 'USA'
            },
            
            # Movies - Comedy
            {
                'title': 'The Hangover',
                'year': 2009,
                'type': 'movie',
                'genre': 'Comedy',
                'language': 'English',
                'director': 'Todd Phillips',
                'actors': 'Bradley Cooper,Ed Helms,Zach Galifianakis',
                'imdb_rating': 7.7,
                'description': 'Three friends wake up from a bachelor party with no memory of the previous night.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTg2NDQ3MDc0N15BMl5BanBnXkFtZTcwNTA0NDYyNw@@._V1_.jpg',
                'duration': '100 min',
                'country': 'USA'
            },
            {
                'title': 'Superbad',
                'year': 2007,
                'type': 'movie',
                'genre': 'Comedy',
                'language': 'English',
                'director': 'Greg Mottola',
                'actors': 'Jonah Hill,Michael Cera,Christopher Mintz-Plasse',
                'imdb_rating': 7.6,
                'description': 'Two co-dependent high school seniors are forced to deal with separation anxiety.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTU2NTYyODk0N15BMl5BanBnXkFtZTcwNDk1NDY0Nw@@._V1_.jpg',
                'duration': '113 min',
                'country': 'USA'
            },
            
            # Movies - Drama
            {
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'type': 'movie',
                'genre': 'Drama',
                'language': 'English',
                'director': 'Frank Darabont',
                'actors': 'Tim Robbins,Morgan Freeman,Bob Gunton',
                'imdb_rating': 9.3,
                'description': 'Two imprisoned men bond over a number of years.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNDE3ODhiYjQtNWQ5Mi00ZTRiLWE2NzYtOWU2NDJhN2E5YzYxXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': '142 min',
                'country': 'USA'
            },
            {
                'title': 'Forrest Gump',
                'year': 1994,
                'type': 'movie',
                'genre': 'Drama,Romance',
                'language': 'English',
                'director': 'Robert Zemeckis',
                'actors': 'Tom Hanks,Robin Wright,Gary Sinise',
                'imdb_rating': 8.8,
                'description': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BNWIwODRlZTUtY2U3ZS00Yzg1LWJhNzYtMmZiYmEyNmU1NjMyXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg',
                'duration': '142 min',
                'country': 'USA'
            },
            
            # Web Series - Hindi
            {
                'title': 'Sacred Games',
                'year': 2018,
                'type': 'web_series',
                'genre': 'Crime,Drama,Thriller',
                'language': 'Hindi',
                'director': 'Vikramaditya Motwane,Anurag Kashyap',
                'actors': 'Saif Ali Khan,Nawazuddin Siddiqui,Radhika Apte',
                'imdb_rating': 8.6,
                'description': 'A link in their pasts leads an honest cop to a fugitive gang boss.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjJlMjJlMzYtNWU5Yy00N2MwLTg1MjI5MTZkYzE0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': 'Season 1-2',
                'country': 'India'
            },
            {
                'title': 'Mirzapur',
                'year': 2018,
                'type': 'web_series',
                'genre': 'Action,Crime,Drama',
                'language': 'Hindi',
                'director': 'Karan Anshuman,Mihir Desai',
                'actors': 'Pankaj Tripathi,Ali Fazal,Divyendu Sharma',
                'imdb_rating': 8.4,
                'description': 'A shocking incident at a wedding procession ignites a series of events.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZmQ5YzYzMzQtYjMxYy00YTRiLWI5ZjYtZTRhNWIxZWM2NDM0XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': 'Season 1-3',
                'country': 'India'
            },
            {
                'title': 'Panchayat',
                'year': 2020,
                'type': 'web_series',
                'genre': 'Comedy,Drama',
                'language': 'Hindi',
                'director': 'Deepak Kumar Mishra',
                'actors': 'Jitendra Kumar,Raghubir Yadav,Neena Gupta',
                'imdb_rating': 8.9,
                'description': 'A comedy-drama about an engineering graduate who joins as a Panchayat secretary.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZWRlNDdkNzItMzhlZC00OTMwLTk1ZTgtNmFkMzFhODFkYTRiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': 'Season 1-3',
                'country': 'India'
            },
            
            # Web Series - English
            {
                'title': 'Breaking Bad',
                'year': 2008,
                'type': 'web_series',
                'genre': 'Crime,Drama,Thriller',
                'language': 'English',
                'director': 'Vince Gilligan',
                'actors': 'Bryan Cranston,Aaron Paul,Anna Gunn',
                'imdb_rating': 9.5,
                'description': 'A high school chemistry teacher turned methamphetamine manufacturer.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMjhiMzgxZTctNDc1Ni00OTIxLTlhMTYtZTA3ZWFkODRkNmE2XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
                'duration': 'Season 1-5',
                'country': 'USA'
            },
            {
                'title': 'Game of Thrones',
                'year': 2011,
                'type': 'web_series',
                'genre': 'Action,Adventure,Drama',
                'language': 'English',
                'director': 'David Benioff,D.B. Weiss',
                'actors': 'Emilia Clarke,Peter Dinklage,Kit Harington',
                'imdb_rating': 9.3,
                'description': 'Nine noble families fight for control over the lands of Westeros.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYTRiNDQwYzAtMzVlZS00NTI5LWJjYjUtMzkwNTUzMWMxZTllXkEyXkFqcGdeQXVyNDIzMzcwNjc@._V1_.jpg',
                'duration': 'Season 1-8',
                'country': 'USA'
            },
            {
                'title': 'Stranger Things',
                'year': 2016,
                'type': 'web_series',
                'genre': 'Drama,Fantasy,Horror',
                'language': 'English',
                'director': 'The Duffer Brothers',
                'actors': 'Millie Bobby Brown,Finn Wolfhard,Winona Ryder',
                'imdb_rating': 8.7,
                'description': 'When a young boy disappears, his mother must confront terrifying forces.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMDZkYmVhNjMtNWU4MC00MDQxLWE3MjYtZGMzZWI1ZjhlOWJmXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg',
                'duration': 'Season 1-4',
                'country': 'USA'
            },
            
            # Web Series - Hindi Dubbed
            {
                'title': 'Money Heist (Hindi Dubbed)',
                'year': 2017,
                'type': 'web_series',
                'genre': 'Action,Crime,Drama',
                'language': 'Hindi Dubbed',
                'director': 'Álex Pina',
                'actors': 'Úrsula Corberó,Itziar Ituño,Álvaro Morte',
                'imdb_rating': 8.2,
                'description': 'An unusual group of robbers attempt to carry out the most perfect robbery.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BODJkOGUxNWUtN2U2MS00NDBlLWFkOGEtODUxOTkyMzYxOTRkXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': 'Season 1-5',
                'country': 'Spain'
            },
            {
                'title': 'Dark (Hindi Dubbed)',
                'year': 2017,
                'type': 'web_series',
                'genre': 'Crime,Drama,Mystery',
                'language': 'Hindi Dubbed',
                'director': 'Baran bo Odar,Jantje Friese',
                'actors': 'Louis Hofmann,Karoline Eichhorn,Lisa Vicari',
                'imdb_rating': 8.7,
                'description': 'A missing child sets four families on a frantic hunt for answers.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BOTk2NzUyOTctMTU3OS00NDkzLWFiNzEtZTIyNDM2ODRkMmYzXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': 'Season 1-3',
                'country': 'Germany'
            },
            {
                'title': 'Squid Game (Hindi Dubbed)',
                'year': 2021,
                'type': 'web_series',
                'genre': 'Action,Drama,Thriller',
                'language': 'Hindi Dubbed',
                'director': 'Hwang Dong-hyuk',
                'actors': 'Lee Jung-jae,Park Hae-soo,Wi Ha-joon',
                'imdb_rating': 8.0,
                'description': 'Hundreds of cash-strapped players accept a strange invitation.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BYWE3MDVkN2EtNjQ5MS00ZDQ4LTNiNzItOGYyNGJmNzFjN2FjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': 'Season 1-2',
                'country': 'South Korea'
            },
            
            # Bollywood Movies
            {
                'title': '3 Idiots',
                'year': 2009,
                'type': 'movie',
                'genre': 'Comedy,Drama',
                'language': 'Hindi',
                'director': 'Rajkumar Hirani',
                'actors': 'Aamir Khan,R. Madhavan,Sharman Joshi',
                'imdb_rating': 8.4,
                'description': 'Two friends looking for a lost buddy deal with a forgotten bet.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BZWRlNDdkNzItMzhlZC00OTMwLTk1ZTgtNmFkMzFhODFkYTRiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
                'duration': '170 min',
                'country': 'India'
            },
            {
                'title': 'Lagaan',
                'year': 2001,
                'type': 'movie',
                'genre': 'Adventure,Drama,Sport',
                'language': 'Hindi',
                'director': 'Ashutosh Gowariker',
                'actors': 'Aamir Khan,Gracy Singh,Rachel Shelley',
                'imdb_rating': 8.1,
                'description': 'The people of a small village in Victorian India stake their future on a game of cricket.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTYzODQzMzE3MV5BMl5BanBnXkFtZTcwMTM5MjQ2NQ@@._V1_.jpg',
                'duration': '224 min',
                'country': 'India'
            },
            {
                'title': 'Dangal',
                'year': 2016,
                'type': 'movie',
                'genre': 'Action,Biography,Drama',
                'language': 'Hindi',
                'director': 'Nitesh Tiwari',
                'actors': 'Aamir Khan,Sakshi Tanwar,Fatima Sana Shaikh',
                'imdb_rating': 8.4,
                'description': 'Former wrestler Mahavir Singh Phogat trains his daughters Geeta and Babita.',
                'poster_url': 'https://m.media-amazon.com/images/M/MV5BMTQ4MjQwMzMxN15BMl5BanBnXkFtZTgwOTc1MzQyMzE@._V1_.jpg',
                'duration': '161 min',
                'country': 'India'
            }
        ]
        
        return pd.DataFrame(data)
    
    def get_movies_only(self):
        """Get only movies from the dataset"""
        return self.movies_data[self.movies_data['type'] == 'movie']
    
    def get_web_series_only(self):
        """Get only web series from the dataset"""
        return self.movies_data[self.movies_data['type'] == 'web_series']
    
    def get_by_language(self, language):
        """Get content by specific language"""
        return self.movies_data[self.movies_data['language'] == language]
    
    def get_by_type_and_language(self, content_type, language):
        """Get content by type and language"""
        return self.movies_data[
            (self.movies_data['type'] == content_type) & 
            (self.movies_data['language'] == language)
        ]
    
    def get_all_data(self):
        """Get complete dataset"""
        return self.movies_data
    
    def get_available_languages(self):
        """Get list of available languages"""
        return sorted(self.movies_data['language'].unique().tolist())
    
    def get_available_types(self):
        """Get list of available content types"""
        return sorted(self.movies_data['type'].unique().tolist())
