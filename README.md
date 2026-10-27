# 🎬 Movie Recommender System

A content-based movie recommendation web app built with **Python, scikit-learn and Streamlit**.
Pick a movie you like and the app suggests the 5 most similar movies, showing each poster and its
TMDB rating.

## ✨ Features

- Content-based recommendations for ~4,800 movies
- Similarity based on plot overview, genres, keywords, top 3 cast members and the director
- Posters and ratings fetched live from the [TMDB API](https://www.themoviedb.org/documentation/api)
- Clear error messages if the API key is missing/invalid or the network fails
- Simple, interactive Streamlit interface

## 🧠 How it works

This is a **content-based filtering** system: it recommends movies whose *content* is similar to the
selected movie.

1. **Data preparation** – The TMDB 5000 *movies* and *credits* datasets are merged and cleaned.
2. **Feature extraction** – From each movie, the overview, genres, keywords, top 3 cast and director
   are extracted from JSON-like text.
3. **Tag creation** – All features are combined into one `tags` text per movie. Spaces inside names are
   removed (`Sam Worthington` → `SamWorthington`) so that each person/genre stays a single token.
4. **Stemming** – Words are reduced to their root with NLTK's `PorterStemmer` (`loved`, `loving` → `love`).
5. **Vectorization** – `CountVectorizer` (top 5,000 words, English stop-words removed) turns every
   movie's tags into a numeric vector (Bag of Words).
6. **Similarity** – **Cosine similarity** compares every pair of movie vectors. Two movies pointing in a
   similar direction have a score close to 1.
7. **Recommendation** – For the selected movie, the 5 movies with the highest similarity scores are
   returned, and `app.py` fetches their posters and ratings from TMDB using the movie id.

## 🛠️ Tech Stack

| Area | Tools |
|------|-------|
| Language | Python 3.10+ |
| Data handling | pandas, NumPy |
| NLP / ML | NLTK, scikit-learn |
| Web app | Streamlit |
| External API | TMDB API (`requests`) |

## 📁 Project Structure

```
Movies-Recommender-System/
├── app.py             # Streamlit web app (UI + recommendation + TMDB calls)
├── model.py           # Builds the model: cleaning, tags, vectors, similarity matrix
├── config.py          # Reads the TMDB API key from the environment
├── requirements.txt   # Python dependencies
├── .env.example       # Template for your local secrets
├── .gitignore
├── LICENSE
└── README.md
```

Generated locally (not stored in Git because of their size): `movies_dict.pkl`, `similarity.pkl` (~185 MB).

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/waseemmusrani/Movies-Recommender-System.git
cd Movies-Recommender-System
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Download the dataset

Download **TMDB 5000 Movie Dataset** from Kaggle:
<https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata>

Place these two files in the project root:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 4. Get a TMDB API key

1. Create a free account at <https://www.themoviedb.org/>.
2. Go to **Settings → API** and request a key (choose *Developer*).
3. Copy `.env.example` to `.env` and paste your key:

```
TMDB_API_KEY=your_real_key_here
```

> ⚠️ Never commit `.env`. It is already listed in `.gitignore`.

### 5. Build the model

```bash
python model.py
```

This creates `movies_dict.pkl` and `similarity.pkl`. NLTK's stemmer needs no extra download.
The first run may take a minute.

### 6. Run the app

```bash
streamlit run app.py
```

Open the URL shown in the terminal (usually <http://localhost:8501>).

## 🧪 Usage

1. Choose a movie from the dropdown.
2. Click **Recommend**.
3. See 5 similar movies with their posters and TMDB ratings.

## 🩺 Troubleshooting

| Problem | Likely cause / fix |
|---------|--------------------|
| Red message: `TMDB error 401 ... Invalid API key` | The key in `.env` is wrong or revoked. Generate a new one on TMDB. |
| `TMDB_API_KEY is missing` | You have not created `.env` (see step 4). |
| Network error / timeout | TMDB may be blocked by your ISP or network. Try another network or a VPN. |
| `FileNotFoundError: movies_dict.pkl` | Run `python model.py` first (step 5). |
| `FileNotFoundError: tmdb_5000_movies.csv` | Download the dataset and place it in the project root (step 3). |

## ⚠️ Known Limitations

- Some titles appear more than once (e.g. *Batman*) because the datasets are merged on `title`;
  merging on the movie id would avoid duplicates.
- Content-based filtering only uses movie metadata, not user behaviour, so it cannot learn personal taste.
- Bag-of-Words ignores word meaning and order.

## 🔮 Future Improvements

- Remove duplicate titles by merging on the movie id
- Use TF-IDF or sentence embeddings instead of Bag of Words
- Add a hybrid approach with collaborative filtering
- Add filters (genre, year, minimum rating) and movie details/trailer
- Deploy the app online (Streamlit Community Cloud)
- Add unit tests for the recommendation function

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie data and API. *This product uses the TMDB API but is
  not endorsed or certified by TMDB.*
- [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle.

## 👤 Author

**Waseem Abbas** – Computer Science student, aspiring AI/ML Engineer

## 📄 License

Released under the [MIT License](LICENSE).
