import pickle
import pandas as pd
import streamlit as st
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the pickled model
def load_pickled_model():
    # Load the dataframe from CSV
    df = pd.read_csv(os.path.join(base_dir, "movies.csv"))
    
    # Unpack only the two objects (tfidf_matrix and cosine_sim) from the pickle file
    tfidf_matrix, cosine_sim = pickle.load(
        open(os.path.join(base_dir, "tfidf_model3.pkl"), "rb")
    )
    
    return tfidf_matrix, cosine_sim, df


# Function to recommend movies
def content_based_recommender_with_pickled_model(
    movie_title, top_n=5, tfidf=None, cosine_sim=None, df=None
):
    # Create a mapping of movie titles to index
    indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

    # Get the index of the input movie title
    idx = indices.get(movie_title, None)
    if idx is None:
        return f"Movie '{movie_title}' not found in dataset."

    # Get similarity scores and sort them
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get all similar movies (excluding the input movie itself)
    sim_indices = [i[0] for i in sim_scores[1:21]]  # Get top 20 for replacement pool
    
    # Ensure we return only the top_n recommendations
    sim_indices = sim_indices[:top_n]  # Slice to return only top_n recommendations
    
    # Return recommended movies
    return df["title"].iloc[sim_indices].tolist()

# Set up Streamlit app
st.title("Movie Recommender")
st.write("Select the movies you like, and we will recommend similar ones!")

# Load the pickled model
tfidf, cosine_sim, df = load_pickled_model()

# Display movie titles
movie_titles = df["title"].tolist()

# Initialize session state
if 'seen_movies' not in st.session_state:
    st.session_state.seen_movies = set()

if 'replacement_pool' not in st.session_state:
    st.session_state.replacement_pool = []

if 'displayed_recommendations' not in st.session_state:
    st.session_state.displayed_recommendations = []

# Let user select movies they like
selected_movies = st.multiselect(
    "Select movies you like:", options=movie_titles, format_func=lambda x: f"{x}"
)

# If the user selects movies, recommend similar ones
if selected_movies:
    st.markdown("---")
    st.subheader("Here are the recommended movies based on your selection:")

    # Check if selections changed - if so, rebuild recommendations
    rebuild_recommendations = False
    if 'previous_selections' not in st.session_state or st.session_state.previous_selections != selected_movies:
        st.session_state.previous_selections = selected_movies.copy()
        rebuild_recommendations = True
    
    # Build initial recommendation set and replacement pool
    if rebuild_recommendations or not st.session_state.displayed_recommendations:
        # Get recommendations for each selected movie
        all_recommendations = set()
        st.session_state.replacement_pool = []
        
        for movie in selected_movies:
            rec_movies = content_based_recommender_with_pickled_model(
                movie, top_n=20, tfidf=tfidf, cosine_sim=cosine_sim, df=df
            )
            
            if isinstance(rec_movies, list):
                # Add first 5 to recommendations, rest to replacement pool
                all_recommendations.update(rec_movies[:5])
                st.session_state.replacement_pool.extend(rec_movies[5:])
        
        # Remove selected and seen movies
        all_recommendations -= set(selected_movies)
        all_recommendations -= st.session_state.seen_movies
        
        # Update displayed recommendations
        st.session_state.displayed_recommendations = list(all_recommendations)[:10]  # Display up to 10
    
    # Clean replacement pool (remove duplicates, seen movies, and selected movies)
    unique_replacements = []
    for movie in st.session_state.replacement_pool:
        if (movie not in st.session_state.seen_movies and 
            movie not in selected_movies and 
            movie not in st.session_state.displayed_recommendations and
            movie not in unique_replacements):
            unique_replacements.append(movie)
    
    st.session_state.replacement_pool = unique_replacements
    
    # Display recommended movies with posters and overview
    for i, movie in enumerate(st.session_state.displayed_recommendations):
        try:
            movie_data = df[df["title"] == movie].iloc[0]
            
            # Create three columns for each recommended movie
            col1, col2, col3 = st.columns([1, 2, 1])
            
            # Display movie poster in the first column
            poster_path = movie_data['poster_path']
            if pd.notna(poster_path):
                col1.image(f"https://image.tmdb.org/t/p/w500{poster_path}", width=200)
            else:
                col1.write("No poster available")
            
            # Display title, rating, release year, and overview in the second column
            col2.write(f"**Title:** {movie_data['title']}")
            col2.write(f"**Rating:** {movie_data['vote_average']}")
            col2.write(f"**Release Year:** {movie_data['release_year']}")
            col2.write(f"**Overview:** {movie_data['overview']}")
            
            # Add a unique key for each button
            button_key = f"seen_{i}_{movie.replace(' ', '_')}"
            if col3.button("Seen it", key=button_key):
                # Add to seen movies
                st.session_state.seen_movies.add(movie)
                
                # Remove from displayed recommendations
                st.session_state.displayed_recommendations.remove(movie)
                
                # Add a replacement if available
                if st.session_state.replacement_pool:
                    new_recommendation = st.session_state.replacement_pool.pop(0)
                    st.session_state.displayed_recommendations.append(new_recommendation)
                
                # If replacement pool is getting low, generate more recommendations
                if len(st.session_state.replacement_pool) < 5:
                    for base_movie in selected_movies:
                        additional_recs = content_based_recommender_with_pickled_model(
                            base_movie, top_n=10, tfidf=tfidf, cosine_sim=cosine_sim, df=df
                        )
                        if isinstance(additional_recs, list):
                            for rec in additional_recs:
                                if (rec not in st.session_state.seen_movies and 
                                    rec not in selected_movies and 
                                    rec not in st.session_state.displayed_recommendations and
                                    rec not in st.session_state.replacement_pool):
                                    st.session_state.replacement_pool.append(rec)
                
                st.rerun()
            
            # Add a separator between movies
            if i < len(st.session_state.displayed_recommendations) - 1:
                st.markdown("---")
        except Exception as e:
            st.error(f"Error displaying movie '{movie}': {e}")
            continue