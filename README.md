# CineMatch — Movie Recommendation System 🎬

A content-based Movie Recommendation System built using Python, Scikit-learn, Pandas, and Streamlit.

The app recommends movies similar to the one selected by the user using TF-IDF Vectorization and Cosine Similarity on movie metadata and processed tags.

---

## 🚀 Live Demo

https://movie-recommender-7a7ajpntcjceavdnvzkw5e.streamlit.app

---

## 📸 Screenshots

<img width="1470" height="956" alt="Screenshot 2026-05-07 at 5 24 31 AM" src="https://github.com/user-attachments/assets/f7d8f537-7a25-41db-8de4-ac84b6048188" />

<img width="1470" height="956" alt="Screenshot 2026-05-07 at 5 24 49 AM" src="https://github.com/user-attachments/assets/357beca3-5aa3-4588-a3fa-98be75322da4" />

<img width="1470" height="956" alt="Screenshot 2026-05-07 at 5 25 47 AM" src="https://github.com/user-attachments/assets/63c305ac-85e1-4fda-a163-685c73793e7b" />

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
