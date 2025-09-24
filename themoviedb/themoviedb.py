import os
import requests
from datetime import datetime, timedelta
import logging
from dotenv import find_dotenv, load_dotenv


class TheMovieDB:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.logger = logging.getLogger(__name__)
        self.themoviedb_api_token = os.environ.get("THEMOVIEDB_API_TOKEN")
        self.themoviedb_api_url = 'https://api.themoviedb.org/3'
        self.discover_movie_url = f"{self.themoviedb_api_url}/discover/movie"
        self.discover_show_url = f"{self.themoviedb_api_url}/discover/tv"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.themoviedb_api_token}"
        }
        self.date_7_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.todays_date = datetime.now().strftime('%Y-%m-%d')
        self.params = self.get_params('en-US', 'US', 'en')
        self.params_hindi = self.get_params('en-US', 'IN', 'hi')

    def get_common_params(self):
        return {
            'language': 'en-US',
            'region': 'US',
            'page': '1',
            "video": 'true',
            'adult': 'true',
        }

    def get_params(self, language, region, original_language):
        return {
            'language': language,
            'region': region,
            'with_original_language': original_language,
            'sort_by': 'release_date.desc',
            'primary_release_date.gte': self.date_7_days_ago,
            'primary_release_date.lte': self.todays_date,
            'page': '1',
            'include_adult': 'false',
            'include_video': 'false',
        }

    def get_themoviedb(self, url, params):
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting data from theMovieDB: {e}")
            return None

    def get_this_weeks_movies(self, language):
        params = self.params_hindi if language == 'hindi' else self.params
        movies = self.get_themoviedb(self.discover_movie_url, params)
        if movies is not None:
            for movie in movies.get('results', []):
                movie['media_type'] = 'movie'
        return movies

    def get_this_weeks_shows(self, language):
        params = self.params_hindi if language == 'hindi' else self.params
        shows = self.get_themoviedb(self.discover_show_url, params)
        if shows is not None:
            for show in shows.get('results', []):
                show['media_type'] = 'tv'
        return shows

    def get_now_playing(self, media_type):
        url = f"{self.themoviedb_api_url}/{media_type}/now_playing"
        now_playing = self.get_themoviedb(url, self.get_common_params())
        if now_playing is not None:
            for item in now_playing.get('results', []):
                item['media_type'] = media_type
        return now_playing

    def get_trending(self, time_window):
        url = f"{self.themoviedb_api_url}/trending/all/{time_window}"
        return self.get_themoviedb(url, self.get_common_params())

    def get_upcoming(self, media_type):
        url = f"{self.themoviedb_api_url}/{media_type}/upcoming"
        upcoming = self.get_themoviedb(url, self.get_common_params())
        if upcoming is not None:
            for item in upcoming.get('results', []):
                item['media_type'] = media_type
        return upcoming

    def find(self, media_type, query, year):
        url = f"{self.themoviedb_api_url}/search/{media_type}"
        params = {
            'query': query,
        }
        if media_type == 'tv':
            params['first_air_date_year'] = year
        else:
            params['primary_release_year'] = year
        return self.get_themoviedb(url, params)
