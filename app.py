import streamlit as st
import pickle 

movies_dict = pickle.load(open('movies.pkl','rb'))

print(movies_dict.keys())
#convert dictionary of titles to list 
movies_list = list(movies_dict['title'].values())
#convert dict of movie_id to list
movie_ids = list(movies_dict['movie_id'].values())

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

    for i in my_list:
        recommended_movies.append(movies_list[i[0]])
        recommended_movie_ids.append(movie_ids[i[0]])

    return recommended_movies, recommended_movie_ids


if st.button('Recommend'):
    recommended_movies, recommended_movie_ids = recommend(selected_movie_name)

    for movie_id, movie in zip(recommended_movie_ids, recommended_movies):
        st.write(f"Movie ID: {movie_id}")
        st.write(f"Movie Title: {movie}")

            


