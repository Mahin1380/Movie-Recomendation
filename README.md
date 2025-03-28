
# Movie Recommendation System with Streamlit

## Features
- **Movie Recommendations**: Get movie recommendations based on your selected movies.
- **User Interaction**: Select movies you like, and the app will recommend similar movies.
- **Movie Overview**: View the synopsis, genres, and poster of the recommended movies.

## Getting Started

Ensure that the following Python libraries are installed to set up and run the system.

### Prerequisites

- tqdm
- pandas
- streamlit
- python-dotenv
- pickle
- requests
- scikit-learn
- numpy

### Scripts

1. **data_cleaning.py**  
   This script handles the cleaning and preparation of the movie data, such as dealing with missing values and creating the features required for analysis.

2. **get_movies.py**  
   This script fetches movie information from TMDb using their API, including movie titles, overviews, genres, etc.

3. **get_favourites.py**  
   This script retrieves your favorite movies from your TMDb account, which will be used for personalized recommendations.

4. **app.py**  
   The main Streamlit application that displays the recommendations and allows interaction with the system.

## How to Use

1. Clone the repository to your local machine.
   
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Install the dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   
   ```bash
   streamlit run app.py
   ```

4. Open your browser to the provided localhost URL and interact with the system.

## Dataset

The dataset is sourced from **TMDb (The Movie Database)** and includes the following features:

- `title`: Movie title
- `overview`: Movie synopsis
- `genres`: Movie genres
- `poster_path`: URL path to the movie poster
- `release_year`: Year of release

## Installation

### 1️⃣ Clone the repository:
```bash
git clone https://github.com/Mahin1380/movie-recommender.git
cd movie-recommender
```

### 2️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. **Launch the Streamlit app.**
2. **Select movies you like** from the provided list.
3. **Get personalized movie recommendations** based on your selection.
4. If you have already watched a recommended movie, the system will suggest another one.

## How It Works

1. **Data Preprocessing**:
   - The `genres` and `overview` fields are combined into a new feature called `tags`.
   - **TF-IDF Vectorization** is applied to the `tags` to convert text data into numerical representations.
   - **Cosine similarity** is calculated between all movies based on the vectorized tags.

2. **Pickling the Model**:
   - The trained **TF-IDF vectorizer** and **cosine similarity matrix** are saved using **pickle** to enable fast model loading.

3. **Making Recommendations**:
   - When a user selects a movie, the system retrieves the most similar movies based on cosine similarity.
   - **Already watched movies** are removed from the list of recommendations.

## File Structure

```
📂 movie-recommender
│-- 📜 app.py              # Streamlit web app
│-- 📜 tfidf_model.pkl      # Pickled TF-IDF model & similarity matrix
│-- 📜 movies.csv           # Dataset from TMDb
│-- 📜 data_cleaning.py     # Script for cleaning movie data
│-- 📜 get_movies.py        # Script for fetching movie data from TMDb
│-- 📜 get_favourites.py    # Script for fetching user favorite movies from TMDb
│-- 📜 recommender.py       # Recommendation logic
│-- 📜 requirements.txt     # Dependencies
│-- 📜 README.md            # Project documentation
```

## Future Improvements
- Add **collaborative filtering** to enhance the recommendation system.
- Implement **deep learning models** like **BERT** for improved text understanding.
- Add **user authentication** to save movie preferences and watch history.

## Credits
- Dataset: [TMDb API](https://www.themoviedb.org/documentation/api)
- Frameworks: **Scikit-learn, Pandas, NumPy, Streamlit**

## License
This project is licensed under the **MIT License**.
