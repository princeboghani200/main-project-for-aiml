"""
IMDB Data Scraper Module
Collects movie data from IMDB for real-time recommendations
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import re
from typing import List, Dict, Optional

class IMDBScraper:
    def __init__(self):
        self.base_url = "https://www.imdb.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_movies(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for movies on IMDB
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of movie dictionaries with basic info
        """
        try:
            # IMDB search URL
            search_url = f"{self.base_url}/find?q={query.replace(' ', '+')}&s=tt&ttype=ft"
            
            response = self.session.get(search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find movie results
            movie_results = []
            result_items = soup.find_all('li', class_='find-result-item')
            
            for item in result_items[:max_results]:
                try:
                    # Extract movie title and link
                    title_element = item.find('a')
                    if title_element:
                        title = title_element.get_text(strip=True)
                        movie_url = self.base_url + title_element['href']
                        
                        # Extract year if available
                        year_text = item.find('span', class_='result-item-year')
                        year = year_text.get_text(strip=True).strip('()') if year_text else None
                        
                        movie_results.append({
                            'title': title,
                            'year': year,
                            'url': movie_url
                        })
                except Exception as e:
                    print(f"Error parsing movie result: {e}")
                    continue
            
            return movie_results
            
        except Exception as e:
            print(f"Error searching movies: {e}")
            return []
    
    def get_movie_details(self, movie_url: str) -> Optional[Dict]:
        """
        Get detailed information about a specific movie
        
        Args:
            movie_url: URL of the movie page
            
        Returns:
            Dictionary with movie details or None if error
        """
        try:
            response = self.session.get(movie_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract movie title
            title = soup.find('h1', {'data-testid': 'hero-title-block__title'})
            title = title.get_text(strip=True) if title else "Unknown"
            
            # Extract year
            year_element = soup.find('span', {'data-testid': 'hero-title-block__metadata'})
            year = None
            if year_element:
                year_text = year_element.get_text()
                year_match = re.search(r'(\d{4})', year_text)
                year = year_match.group(1) if year_match else None
            
            # Extract rating
            rating_element = soup.find('span', {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
            rating = None
            if rating_element:
                rating_text = rating_element.get_text()
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                rating = float(rating_match.group(1)) if rating_match else None
            
            # Extract genres
            genres = []
            genre_elements = soup.find_all('a', {'data-testid': 'genres'})
            for genre_elem in genre_elements:
                genre_text = genre_elem.get_text(strip=True)
                if genre_text:
                    genres.append(genre_text)
            
            # Extract director
            director = "Unknown"
            director_section = soup.find('section', {'data-testid': 'title-details-section'})
            if director_section:
                director_elem = director_section.find('a', href=re.compile(r'/name/nm\d+'))
                if director_elem:
                    director = director_elem.get_text(strip=True)
            
            # Extract cast
            cast = []
            cast_section = soup.find('section', {'data-testid': 'title-cast'})
            if cast_section:
                cast_elements = cast_section.find_all('a', href=re.compile(r'/name/nm\d+'))
                for cast_elem in cast_elements[:5]:  # Top 5 cast members
                    cast_name = cast_elem.get_text(strip=True)
                    if cast_name and cast_name not in cast:
                        cast.append(cast_name)
            
            # Extract plot summary
            plot = "No plot available"
            plot_element = soup.find('span', {'data-testid': 'plot-summary'})
            if plot_element:
                plot = plot_element.get_text(strip=True)
            
            movie_details = {
                'title': title,
                'year': year,
                'imdb_rating': rating,
                'genres': genres,
                'director': director,
                'cast': cast,
                'plot': plot,
                'url': movie_url
            }
            
            return movie_details
            
        except Exception as e:
            print(f"Error getting movie details: {e}")
            return None
    
    def get_top_movies(self, category: str = "top", min_rating: float = 7.0) -> List[Dict]:
        """
        Get top-rated movies from IMDB
        
        Args:
            category: Category to search (top, popular, etc.)
            min_rating: Minimum IMDB rating
            
        Returns:
            List of top movies
        """
        try:
            if category == "top":
                url = f"{self.base_url}/chart/top/"
            elif category == "popular":
                url = f"{self.base_url}/chart/moviemeter/"
            else:
                url = f"{self.base_url}/chart/top/"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            movies = []
            movie_elements = soup.find_all('h3', class_='ipc-title__text')
            
            for i, elem in enumerate(movie_elements[:50]):  # Top 50 movies
                try:
                    title_text = elem.get_text(strip=True)
                    # Remove ranking number
                    title = re.sub(r'^\d+\.\s*', '', title_text)
                    
                    # Get movie URL
                    movie_link = elem.find_parent('a')
                    movie_url = self.base_url + movie_link['href'] if movie_link else None
                    
                    if movie_url:
                        # Get detailed info
                        movie_details = self.get_movie_details(movie_url)
                        if movie_details and movie_details.get('imdb_rating', 0) >= min_rating:
                            movies.append(movie_details)
                        
                        # Be respectful with requests
                        time.sleep(1)
                        
                except Exception as e:
                    print(f"Error processing movie {i}: {e}")
                    continue
            
            return movies
            
        except Exception as e:
            print(f"Error getting top movies: {e}")
            return []
    
    def get_movies_by_genre(self, genre: str, max_results: int = 20) -> List[Dict]:
        """
        Get movies by specific genre
        
        Args:
            genre: Genre to search for
            max_results: Maximum number of results
            
        Returns:
            List of movies in the specified genre
        """
        try:
            # Search for genre-specific movies
            search_query = f"{genre} movies"
            search_results = self.search_movies(search_query, max_results)
            
            movies = []
            for result in search_results:
                if result['url']:
                    movie_details = self.get_movie_details(result['url'])
                    if movie_details and genre.lower() in [g.lower() for g in movie_details.get('genres', [])]:
                        movies.append(movie_details)
                    
                    # Be respectful with requests
                    time.sleep(1)
                    
                    if len(movies) >= max_results:
                        break
            
            return movies
            
        except Exception as e:
            print(f"Error getting movies by genre: {e}")
            return []
    
    def save_to_csv(self, movies: List[Dict], filename: str):
        """Save movie data to CSV file"""
        try:
            df = pd.DataFrame(movies)
            df.to_csv(filename, index=False)
            print(f"Saved {len(movies)} movies to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
    
    def save_to_json(self, movies: List[Dict], filename: str):
        """Save movie data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(movies, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(movies)} movies to {filename}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")

# Example usage and testing
if __name__ == "__main__":
    scraper = IMDBScraper()
    
    # Test search functionality
    print("Searching for 'Inception'...")
    search_results = scraper.search_movies("Inception", max_results=5)
    print(f"Found {len(search_results)} results")
    
    # Test getting movie details
    if search_results:
        print("\nGetting details for first result...")
        movie_details = scraper.get_movie_details(search_results[0]['url'])
        if movie_details:
            print(f"Title: {movie_details['title']}")
            print(f"Year: {movie_details['year']}")
            print(f"Rating: {movie_details['imdb_rating']}")
            print(f"Genres: {', '.join(movie_details['genres'])}")
            print(f"Director: {movie_details['director']}")
            print(f"Cast: {', '.join(movie_details['cast'])}")
            print(f"Plot: {movie_details['plot'][:100]}...")
