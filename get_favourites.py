import requests
from dotenv import load_dotenv
from data_cleaning import clean_df, extract_and_store
import os

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

request_token_url = "https://api.themoviedb.org/3/authentication/token/new"
params = {"api_key": api_key}

response = requests.get(request_token_url, params=params)

if response.status_code == 200:
    request_token = response.json()["request_token"]
    print("Request token:", request_token)
else:
    print("Error fetching request token.")
    exit()


# %%
# The user needs to visit this URL to authenticate
auth_url = f"https://www.themoviedb.org/authenticate/{request_token}"
print(f"Please visit this URL to authenticate: {auth_url}")


# %%
verification = input("Press 'Enter' After Approval: ")

# Step 2: Exchange the request token for a session ID
session_url = "https://api.themoviedb.org/3/authentication/session/new"
params = {"api_key": api_key, "request_token": request_token}
response = requests.post(session_url, params=params)

if response.status_code == 200:
    session_id = response.json()["session_id"]
    print("Session ID:", session_id)
else:
    print("Error fetching session ID.")

account_url = "https://api.themoviedb.org/3/account"
params = {"api_key": api_key, "session_id": session_id}
response = requests.get(account_url, params=params)

if response.status_code == 200:
    account_info = response.json()
    account_id = account_info["id"]
    print(f"Account ID: {account_id}")
else:
    print("Error fetching account info.")


def fetch_favorites(session_id):
    favorites_url = f"https://api.themoviedb.org/3/account/{account_id}/favorite/movies"
    params = {
        "api_key": api_key,
        "session_id": session_id,
        "language": "en-US",
        "sort_by": "created_at.asc",
        "page": 1,  # Start from page 1
    }

    all_favorites = []

    while True:
        response = requests.get(favorites_url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_favorites.extend(data["results"])  # Append movies from the current page

            if data["page"] < data["total_pages"]:  # Check if more pages exist
                params["page"] += 1  # Go to the next page
            else:
                break  # Stop when all pages are retrieved
        else:
            print("Failed to fetch favorite movies.")
            break

    return all_favorites


favorite_movies = fetch_favorites(session_id)


favorite_movies_data = extract_and_store(favorite_movies)
favorite_movies_data.to_csv(
    r"C:\Users\Mahin\Personal-Projects\Movie-Recommendation-System\favourite_movies(1).csv",
    index=False,
)
favorite_movies_data = clean_df(
    r"C:\Users\Mahin\Personal-Projects\Movie-Recommendation-System\favourite_movies(1).csv"
)
favorite_movies_data.to_csv(
    r"C:\Users\Mahin\Personal-Projects\Movie-Recommendation-System\favourite_movies.csv"
)
os.remove(
    r"C:\Users\Mahin\Personal-Projects\Movie-Recommendation-System\favourite_movies(1).csv"
)
