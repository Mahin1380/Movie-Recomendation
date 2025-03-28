import pickle
import pandas as pd
import streamlit as st
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


# Load the pickled model
def load_pickled_model():
    df = pd.read_csv(os.path.join(base_dir, 'movies.csv'))
    tfidf, cosine_sim = pickle.load(open(os.path.join(base_dir, 'tfidf_model.pkl'), 'rb'))
    return tfidf, cosine_sim, df

# Function to recommend movies
def content_based_recommender_with_pickled_model(movie_title, top_n=5, tfidf=None, cosine_sim=None, df=None):
    # Create a mapping of movie titles to index
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()
    
    # Get the index of the input movie title
    idx = indices.get(movie_title, None)
    if idx is None:
        return f"Movie '{movie_title}' not found in dataset."
    
    # Get similarity scores and sort them
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get indices of top N similar movies (excluding the input movie itself)
    sim_indices = [i[0] for i in sim_scores[1:top_n+1]]
    
    # Return top recommended movies
    return df['title'].iloc[sim_indices].tolist()

# Set up Streamlit app
st.title("Movie Recommender")
st.write("Select the movies you like, and we will recommend similar ones!")

# Load the pickled model
tfidf, cosine_sim, df = load_pickled_model()

# Display movie titles and posters
movie_titles = df['title'].tolist()
movie_posters = df['poster_path'].tolist()

# Let user select movies they like
selected_movies = st.multiselect(
    "Select movies you like:",
    options=movie_titles,
    format_func=lambda x: f"{x}"
)

# If the user selects movies, recommend similar ones
if selected_movies:
    st.subheader("You selected the following movies:")

    # Display the selected movies with their posters and overview
    for i, movie in enumerate(selected_movies):
        movie_data = df[df['title'] == movie].iloc[0]
        
        # Create two columns: one for the poster and one for the title/overview
        col1, col2 = st.columns([2, 3])

        # Display movie poster in the first column
        col1.image(f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}", width=200)

        # Display title, release year, and overview in the second column
        col2.write(f"**Title:** {movie_data['title']}")
        col2.write(f"**Release Year:** {movie_data['release_year']}")
        col2.write(f"**Overview:** {movie_data['overview']}")

        if i < len(selected_movies) - 1:
            st.markdown("---")  # Horizontal line
    # Get recommendations for each selected movie
    recommended_movies = set()  # Use a set to avoid duplicates
    for movie in selected_movies:
        rec_movies = content_based_recommender_with_pickled_model(movie, top_n=5, tfidf=tfidf, cosine_sim=cosine_sim, df=df)
        recommended_movies.update(rec_movies)

    st.markdown("---")
    st.subheader("Here are the recommended movies based on your selection:")

    # Exclude already watched movies from recommendations
    recommended_movies -= set(selected_movies)

    # Display recommended movies with posters and overview
    # Display recommended movies with posters and overview
for i, movie in enumerate(recommended_movies):
    movie_data = df[df['title'] == movie].iloc[0]
    
    # Create two columns for recommended movies
    col1, col2 = st.columns([1, 2])

    # Display movie poster in the first column
    col1.image(f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}", width=200)

    # Display title, release year, and overview in the second column
    col2.write(f"**Title:** {movie_data['title']}")
    col2.write(f"**Release Year:** {movie_data['release_year']}")
    col2.write(f"**Overview:** {movie_data['overview']}")

    # Add a separator between movies (except after the last one)
    if i < len(recommended_movies) - 1:
        st.markdown("---")  # Horizontal line

# Run the Streamlit app
if __name__ == "__main__":
    # To start the app, use the following command:
    # streamlit run app.py
    pass
