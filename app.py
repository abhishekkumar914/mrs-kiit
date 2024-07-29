import streamlit as st
import pandas as pd
import numpy as np
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6ccfd9f5d850599e57a90e849a7c4e16&language=en-US')
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster: {e}")
        return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movies_posters.append(poster)
        else:
            recommended_movies_posters.append("")
    return recommended_movies, recommended_movies_posters

def download_data(url):
    response = requests.get(url)
    with open("largefile.csv", "wb") as file:
        file.write(response.content)
    return pd.read_csv("largefile.csv")

data_url = 'https://drive.google.com/file/d/1ZdhsEvaAXjM5SBDLfI5SmSCO37J9gg84/view?usp=drive_link'
similarity_path = download_data(data_url)
movies_dict = r'C:\python\ml\movie-recommender-system\output.csv'
#similarity_path = r'C:\python\ml\movie-recommender-system\similarity.pkl'

movies = pd.read_csv(movies_dict)
similarity = pd.read_pickle(similarity_path)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie!',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.header(names[i])
            if posters[i]:
                st.image(posters[i])
            else:
                st.text("No poster available")
