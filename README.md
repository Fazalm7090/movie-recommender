# CineMatch — Movie Recommendation System 🎬

A content-based Movie Recommendation System built using Python, Scikit-learn, Pandas, and Streamlit.

The app recommends movies similar to the one selected by the user using TF-IDF Vectorization and Cosine Similarity on movie metadata and processed tags.

---

## 🚀 Live Demo

Add your deployed Streamlit link here:

https://your-streamlit-app-link.streamlit.app

---

## 📸 Screenshots

Add screenshots of:
- Home page
- Recommendation results
- Movie cards UI

---

## ✨ Features

- 🎥 Movie recommendation engine
- 🧠 Content-based filtering
- ⚡ Fast similarity computation
- 🌐 OMDb API integration for posters and metadata
- 🎨 Modern cinematic UI using Streamlit
- ☁️ Fully deployed on Streamlit Cloud

---

## 🛠️ Technologies Used

### Programming Language
- Python

### Libraries & Frameworks
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Requests

### Machine Learning Concepts
- NLP preprocessing
- TF-IDF Vectorization
- Cosine Similarity
- Feature Engineering

### APIs
- OMDb API

---

# 📂 Project Structure

```text
movie-recommender/
│
├── app.py
├── movies.csv
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧠 How the Recommendation System Works

This project uses a Content-Based Recommendation System.

## Step 1 — Data Preprocessing

The TMDB movie dataset was cleaned and processed using:
- movie overview
- genres
- keywords
- cast
- crew

These features were combined into a single `tags` column.

---

## Step 2 — Text Vectorization

The tags were converted into numerical vectors using:

```python
TfidfVectorizer(stop_words='english')
```

TF-IDF helps convert movie descriptions into machine-understandable numerical representations.

---

## Step 3 — Similarity Computation

Cosine Similarity was used to measure how similar two movies are.

```python
cosine_similarity(vectors)
```

Movies with the highest similarity scores are recommended.

---

# ⚡ Deployment Optimization

Initially, the project used large `.pkl` similarity matrix files.

To make deployment lightweight and GitHub-friendly:
- large `.pkl` files were removed
- similarity is computed dynamically from `movies.csv`
- project size was significantly reduced

This improved:
- deployment reliability
- scalability
- repository cleanliness

---

# ▶️ Run Locally

## Clone Repository

```bash
git clone git@github.com:Fazalm7090/movie-recommender.git
```

## Move Into Project Folder

```bash
cd movie-recommender
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Streamlit App

```bash
streamlit run app.py
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
OMDB_API_KEY=your_api_key_here
```

Never upload `.env` files to GitHub.

---

# 📊 Dataset

Dataset used:
- TMDB 5000 Movie Dataset

The dataset was cleaned and transformed before use.

---

# 📌 Future Improvements

- 🔍 Fuzzy search
- 🎭 Genre filtering
- ⭐ IMDb ratings integration
- 🎬 Trailer integration
- 👤 User authentication
- 🤖 Hybrid recommendation system

---

# 🙌 Acknowledgements

- TMDB Dataset
- OMDb API
- Streamlit
- Scikit-learn

---

# 👨‍💻 Author

**Fazal Mehdi**

GitHub:
https://github.com/Fazalm7090
