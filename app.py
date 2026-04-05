import streamlit as st
import pickle
import pandas as pd
import sklearn
import requests

st.set_page_config(layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }

    .movie-card {
        text-align: center;
    }

    .movie-title {
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
        color: white;
    }

    img {
        border-radius: 12px;
        transition: transform 0.3s ease;
    }

    img:hover {
        transform: scale(1.05);
    }

    .stButton>button {
        background-color: #e50914;
        color: white;
        border-radius: 8px;
        height: 45px;
        width: 200px;
        font-size: 16px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)




def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),
                         reverse=True,
                         key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

##
import requests

OMDB_API_KEY = "81c0a085"


def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_name}"

    data = requests.get(url).json()

    if data['Response'] == 'True':
        return data['Poster']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"





movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

similarity = cosine_similarity(vectors)


# Header
st.markdown("<h1 style='text-align:center;'>🎬 Movie Recommender</h1>", unsafe_allow_html=True)

# Selectbox
selected_movie_name = st.selectbox(
    "SELECT A MOVIE ",
    movies['title'].values
)

# Button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    recommend_clicked = st.button("Recommend")

# Output
if recommend_clicked:
    names, posters = recommend(selected_movie_name)

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" width="180">
                    <div class="movie-title">{names[i]}</div>
                </div>
            """, unsafe_allow_html=True)