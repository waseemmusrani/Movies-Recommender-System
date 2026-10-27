# Import Required Libraries
import io

import pandas as pd
import pickle
import requests
import streamlit as st
from PIL import Image, ImageDraw

# Import API Key from config.py
from config import API_KEY

# Stop early with a clear message if the API key is not configured
if not API_KEY:
    st.error("TMDB_API_KEY is missing. Create a .env file (see .env.example).")
    st.stop()

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# ---------- Helper: local placeholder (no internet needed) ----------
def make_placeholder():
    """Create a grey 'No Poster' image locally.
    (via.placeholder.com is no longer reliable, so we don't depend on it.)"""
    img = Image.new("RGB", (500, 750), color=(200, 200, 200))
    ImageDraw.Draw(img).text((200, 365), "No Poster", fill=(120, 120, 120))
    return img


PLACEHOLDER = make_placeholder()


# ---------- Fetch from TMDB ----------
@st.cache_data(show_spinner=False)
def _fetch_from_tmdb(movie_id):
    """Call TMDB. Raises an exception on ANY failure.
    st.cache_data does NOT cache exceptions, so a temporary failure
    won't be remembered as 'N/A' forever."""
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": API_KEY},
        timeout=10,
    )
    data = response.json()

    # TMDB sends errors as JSON too (e.g. invalid key) -> check the status!
    if response.status_code != 200:
        raise RuntimeError(
            f"TMDB error {response.status_code}: {data.get('status_message')}"
        )

    poster = IMAGE_BASE_URL + data["poster_path"] if data.get("poster_path") else None
    rating = round(data["vote_average"], 1) if data.get("vote_average") else "N/A"
    return poster, rating


def fetch_movie_details(movie_id):
    """Returns (poster, rating, error_message)."""
    try:
        poster, rating = _fetch_from_tmdb(int(movie_id))
        return (poster or PLACEHOLDER), rating, None
    except Exception as e:  # network error, bad key, bad JSON...
        return PLACEHOLDER, "N/A", str(e)


# ---------- Load model files ----------
movies = pd.DataFrame(pickle.load(open("movies_dict.pkl", "rb")))
similarity = pickle.load(open("similarity.pkl", "rb"))


# ---------- Recommendation logic ----------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    # Top 5 most similar movies (index 0 is the movie itself, so skip it)
    movies_list = sorted(
        enumerate(distances), key=lambda x: x[1], reverse=True
    )[1:6]

    results = []
    for index, _score in movies_list:
        row = movies.iloc[index]
        poster, rating, error = fetch_movie_details(row.movie_id)
        results.append(
            {"title": row["title"], "poster": poster, "rating": rating, "error": error}
        )
    return results


# ---------- UI ----------
st.title("Movie Recommender System")

selected_movie = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    with st.spinner("🔍 Finding similar movies... Please wait"):
        results = recommend(selected_movie)

    # Show the real reason if something failed (only once, not 5 times)
    errors = {r["error"] for r in results if r["error"]}
    if errors:
        st.error("Could not load poster/rating from TMDB: " + " | ".join(errors))

    # One loop instead of copy-pasting 5 near-identical blocks
    for col, r in zip(st.columns(5), results):
        with col:
            st.image(r["poster"])
            st.markdown(f"**{r['title']}**")
            st.write(f"⭐ TMDB Rating: {r['rating']}/10")
