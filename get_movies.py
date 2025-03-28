import requests
from dotenv import load_dotenv
import os
from data_cleaning import clean_df, extract_and_store
import time
from tqdm import tqdm  # Import tqdm for the progress bar

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

base_url = "https://api.themoviedb.org/3"


def fetch_movies(endpoint, total_pages):
    all_movies = []
    for page in tqdm(
        range(1, total_pages + 1), desc="Fetching pages", unit="page"
    ):  # Using tqdm for progress bar
        params = {"api_key": api_key, "page": page}
        try:
            response = requests.get(
                f"{base_url}{endpoint}", params=params, timeout=10
            )  # 10 seconds timeout
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
            data = response.json()
            movies = data.get("results", [])
            all_movies.extend(movies)
            time.sleep(0.3)  # Avoid rate limiting
        except requests.exceptions.Timeout:
            print(f"Timeout occurred on page {page}. Retrying...")
            time.sleep(2)  # Wait before retrying
            continue
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            print(
                f"Response content: {response.text}"
            )  # Log the response content for debugging
            break
    return all_movies


popular_movies = fetch_movies(
    "/movie/popular", total_pages=300
)  # Adjust the total pages as needed

popular_movie_data = extract_and_store(popular_movies)

# Save the raw data to a temporary file
raw_file_path = r"C:\Users\Mahin\Personal-Projects\Movie-Recommendation-System\popular_movies_raw.csv"
popular_movie_data.to_csv(raw_file_path)

# Clean the raw data and save the cleaned data
cleaned_data = clean_df(raw_file_path)
cleaned_data.to_csv(
    r"C:\Users\Mahin\Personal-Projects\Movie-Recommendation-System\popular_movies.csv"
)

# Attempt to remove the raw file after processing
try:
    os.remove(raw_file_path)
except OSError as e:
    print(f"Error removing the raw file: {e}")
