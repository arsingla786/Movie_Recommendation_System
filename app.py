import streamlit as st
import pickle 
import requests
import certifi 
import time 
movies_dict = pickle.load(open('movies.pkl','rb'))

print(movies_dict.keys())
#convert dictionary of titles to list 
movies_list = list(movies_dict['title'].values())
#convert dict of movie_id to list
movie_ids = list(movies_dict['movie_id'].values())

#fetch movie poster

@st.cache_data(ttl=86400, show_spinner=True)
def fetch_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": "b760e48333dec8f0ba13f5a4190beeb0"
    }

    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()
            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:
                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

            return None

        except requests.exceptions.RequestException as e:
            print(
                f"Attempt {attempt + 1} failed "
                f"for movie {movie_id}: {e}"
            )

            if attempt < 2:
                time.sleep(1)

    return None

st.title('Movie Recommender System')

selected_movie_name = option = st.selectbox(
    'Select movie',
    movies_list
)

similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(selected_movie_name):
    movie_index = movies_list.index(selected_movie_name)

    distances = similarity[movie_index]

    # Sort distances and select top 5 similar movies
    my_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movie_ids = []
    recommended_movie_poster = []
    for i in my_list:
        recommended_movies.append(movies_list[i[0]])
        recommended_movie_ids.append(movie_ids[i[0]])
        recommended_movie_poster.append(fetch_movie_poster(movie_ids[i[0]]))
    return recommended_movies, recommended_movie_ids, recommended_movie_poster


if st.button('Recommend'):
    recommended_movies, recommended_movie_ids, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for col, movie_id, movie, poster in zip(cols, recommended_movie_ids, recommended_movies, posters):
        with col:
            
            if poster is not None:
                st.image(poster, use_container_width=True)
            st.write(f"Movie ID: {movie_id}")
            st.write(f"Movie Title: {movie}")

