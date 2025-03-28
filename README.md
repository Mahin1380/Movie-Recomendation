# Movie Recommendation System

## Overview
This project is a **content-based movie recommendation system** using **TF-IDF and cosine similarity**. It allows users to **select movies they like**, and based on their selections, it recommends similar movies. The project includes a **pickled model for fast inference** and a **Streamlit web app** for easy user interaction.

## Features
- **Content-based filtering** using movie overviews and genres.
- **Pre-trained TF-IDF model** stored as a pickle file for fast recommendations.
- **Streamlit web app** to select favorite movies and get recommendations.
- **Displays movie posters, titles, and overviews** for a better user experience.
- **Avoids recommending already watched movies.**

## Dataset
The dataset is sourced from **TMDb (The Movie Database)** and contains:
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
2. **Select movies you like** from the list.
3. **Get recommendations** based on your selection.
4. If you have already watched a recommended movie, **it suggests another one.**

## How It Works
1. **Data Preprocessing**
   - Combines `genres` and `overview` into a new feature called `tags`.
   - Uses **TF-IDF Vectorization** to convert `tags` into numerical representations.
   - Computes **cosine similarity** between all movies.

2. **Pickling the Model**
   - The trained **TF-IDF vectorizer** and **cosine similarity matrix** are saved using pickle for faster loading.
   
3. **Making Recommendations**
   - When a user selects a movie, the system retrieves the most similar movies using cosine similarity.
   - **Removes already watched movies** from the recommendations.
   
## File Structure
```
📂 movie-recommender
│-- 📜 app.py              # Streamlit web app
│-- 📜 tfidf_model.pkl           # Pickled TF-IDF model & similarity matrix
│-- 📜 movies.csv          # Dataset from TMDb
│-- 📜 recommender.py      # Recommendation logic
│-- 📜 requirements.txt    # Dependencies
│-- 📜 README.md           # Project documentation
```

## Future Improvements
- Add **collaborative filtering** for hybrid recommendations.
- Use **deep learning models** like **BERT** for better text understanding.
- Implement **user authentication** to save preferences.

## Credits
- Dataset: [TMDb API](https://www.themoviedb.org/documentation/api)
- Frameworks: **Scikit-learn, Pandas, NumPy, Streamlit**

## License
This project is licensed under the **MIT License**.

