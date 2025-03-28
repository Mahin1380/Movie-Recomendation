# %%
from dotenv import load_dotenv
import requests
import pandas as pd
import os
import ast

load_dotenv()
api_key = os.getenv('TMDB_API_KEY')


# Extract and store in DataFrame
def extract_and_store(movies):
    movie_list = []
    for movie in movies:
        movie_list.append({
            'id': movie['id'],
            'title': movie['title'],
            'release_date': movie.get('release_date'),
            'vote_average': movie.get('vote_average'),
            'overview': movie.get('overview'),
            'genre_ids': movie.get('genre_ids'),
            'popularity': movie.get('popularity'),
            'poster_path': movie.get('poster_path')
        })
    return pd.DataFrame(movie_list)




# %%
genre_url = 'https://api.themoviedb.org/3/genre/movie/list'
params = {'api_key': api_key}

response = requests.get(genre_url, params=params)
genres = response.json()['genres']

genre_dict = {genre['id']: genre['name'] for genre in genres}

# %%
def map_genres(genre_ids):
    return [genre_dict.get(genre_id, '') for genre_id in genre_ids]

def clean_df(csv_path):
    df = pd.read_csv(csv_path)
    
    # Drop duplicates based on 'title'
    df.drop_duplicates(subset='title', keep='first', inplace=True)
    
    # Drop missing values
    df.dropna(inplace=True)

    # Convert 'genre_ids' column from string to list
    df['genre_ids'] = df['genre_ids'].apply(ast.literal_eval)
    
    # Map genres
    df['genres'] = df['genre_ids'].apply(map_genres)
    
    # Convert 'release_date' to datetime format
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    
    # Extract release year
    df['release_year'] = df['release_date'].dt.year

    # Drop unnecessary columns if they exist
    columns_to_drop = ['Unnamed: 0.1', 'Unnamed: 0']
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

    # Convert 'genres' list to a comma-separated string
    df['genres'] = df['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')

    return df

