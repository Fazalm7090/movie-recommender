import streamlit as st
import pickle
import requests
import heapq

from dotenv import load_dotenv
load_dotenv()

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import os

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Outfit:wght@300;400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #070810 !important;
    color: #e8e0d4 !important;
    font-family: 'Outfit', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,160,80,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(120,40,140,0.08) 0%, transparent 60%),
        #070810 !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="collapsedControl"] { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Hero Section ── */
.hero {
    position: relative;
    padding: 72px 80px 56px;
    overflow: hidden;
    border-bottom: 1px solid rgba(201,160,80,0.15);
}

.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 80px,
            rgba(255,255,255,0.012) 80px,
            rgba(255,255,255,0.012) 81px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 80px,
            rgba(255,255,255,0.012) 80px,
            rgba(255,255,255,0.012) 81px
        );
    pointer-events: none;
}

.hero-eyebrow {
    font-family: 'Outfit', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a050;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 32px;
    height: 1px;
    background: #c9a050;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(52px, 6vw, 88px);
    font-weight: 900;
    line-height: 0.95;
    letter-spacing: -0.02em;
    color: #f0e8da;
    margin-bottom: 12px;
}

.hero-title em {
    font-style: italic;
    color: #c9a050;
}

.hero-subtitle {
    font-size: 16px;
    font-weight: 300;
    color: rgba(232,224,212,0.5);
    letter-spacing: 0.03em;
    max-width: 460px;
    line-height: 1.7;
    margin-top: 18px;
}

.hero-deco {
    position: absolute;
    right: 80px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Playfair Display', serif;
    font-size: 220px;
    font-weight: 900;
    font-style: italic;
    color: rgba(201,160,80,0.04);
    line-height: 1;
    pointer-events: none;
    user-select: none;
}

/* ── Search Bar Section ── */
.search-section {
    padding: 52px 80px 40px;
    position: relative;
}

.search-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(201,160,80,0.7);
    margin-bottom: 14px;
}

/* ── Streamlit Selectbox Override ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(201,160,80,0.25) !important;
    border-radius: 2px !important;
    color: #f0e8da !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 17px !important;
    font-weight: 400 !important;
    padding: 18px 24px !important;
    transition: border-color 0.3s ease !important;
}

[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: rgba(201,160,80,0.7) !important;
    background: rgba(255,255,255,0.06) !important;
}

[data-testid="stSelectbox"] label { display: none !important; }

/* Dropdown arrow color */
[data-testid="stSelectbox"] svg { color: #c9a050 !important; }

/* ── Button Override ── */
[data-testid="stButton"] {
    display: flex !important;
    align-items: flex-end !important;
    padding-bottom: 1px !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #c9a050 0%, #a07830 100%) !important;
    color: #070810 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    white-space: nowrap !important;
    padding: 0 32px !important;
    height: 58px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 40px rgba(201,160,80,0.2) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #ddb860 0%, #b08840 100%) !important;
    box-shadow: 0 0 60px rgba(201,160,80,0.4) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Selectbox vertical alignment with button ── */
[data-testid="stSelectbox"] {
    margin-bottom: 0 !important;
}

[data-testid="stSelectbox"] > div > div {
    height: 58px !important;
    display: flex !important;
    align-items: center !important;
}

/* ── Divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,160,80,0.4), transparent);
    margin: 0 80px;
}

/* ── Results Section ── */
.results-section {
    padding: 56px 80px 80px;
}

.results-header {
    display: flex;
    align-items: baseline;
    gap: 20px;
    margin-bottom: 48px;
}

.results-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: #f0e8da;
}

.results-count {
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(201,160,80,0.6);
}

/* ── Movie Card ── */
.movie-card {
    position: relative;
    border-radius: 3px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    background: #0f1018;
    border: 1px solid rgba(255,255,255,0.06);
}

.movie-card:hover {
    transform: translateY(-8px);
}

.movie-card:hover .card-overlay {
    opacity: 1;
}

.movie-card:hover .card-poster {
    transform: scale(1.04);
}

.card-poster-wrap {
    position: relative;
    overflow: hidden;
    aspect-ratio: 2/3;
    background: #0f1018;
}

.card-poster {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to top,
        rgba(7,8,16,0.95) 0%,
        rgba(7,8,16,0.5) 40%,
        rgba(7,8,16,0.1) 70%,
        transparent 100%
    );
    opacity: 0.6;
    transition: opacity 0.4s ease;
    display: flex;
    align-items: flex-end;
    padding: 20px 16px;
}

.card-rank {
    position: absolute;
    top: 12px;
    left: 12px;
    width: 28px;
    height: 28px;
    background: rgba(7,8,16,0.8);
    border: 1px solid rgba(201,160,80,0.4);
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 13px;
    font-weight: 700;
    color: #c9a050;
    backdrop-filter: blur(8px);
}

.card-info {
    padding: 14px 14px 16px;
    border-top: 1px solid rgba(255,255,255,0.06);
}

.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 15px;
    font-weight: 700;
    color: #f0e8da;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.card-meta {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.1em;
    color: rgba(201,160,80,0.6);
    margin-top: 6px;
    text-transform: uppercase;
}

/* ── Poster img override ── */
[data-testid="stImage"] {
    border-radius: 3px;
    overflow: hidden;
}

[data-testid="stImage"] img {
    border-radius: 3px;
    transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    border: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stImage"] img:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 24px 60px rgba(0,0,0,0.8), 0 0 0 1px rgba(201,160,80,0.2);
}

/* ── Caption overrides ── */
[data-testid="stImageCaption"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #f0e8da !important;
    text-align: center !important;
    line-height: 1.3 !important;
    margin-top: 10px !important;
}

/* ── Film strip header deco ── */
.filmstrip {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 0;
    height: 6px;
    background: repeating-linear-gradient(
        90deg,
        #c9a050 0px, #c9a050 12px,
        transparent 12px, transparent 18px
    );
    opacity: 0.35;
}

/* ── Loading / Spinner ── */
[data-testid="stSpinner"] {
    color: #c9a050 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #070810; }
::-webkit-scrollbar-thumb { background: rgba(201,160,80,0.3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(201,160,80,0.6); }

/* ── No results ── */
.no-results {
    text-align: center;
    padding: 80px 40px;
    color: rgba(232,224,212,0.3);
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-style: italic;
}

/* ── Stagger animation ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

.stagger-item {
    animation: fadeSlideUp 0.6s ease both;
}

.stagger-1 { animation-delay: 0.05s; }
.stagger-2 { animation-delay: 0.12s; }
.stagger-3 { animation-delay: 0.19s; }
.stagger-4 { animation-delay: 0.26s; }
.stagger-5 { animation-delay: 0.33s; }

/* ── Selected movie chip ── */
.selected-chip {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(201,160,80,0.08);
    border: 1px solid rgba(201,160,80,0.25);
    border-radius: 2px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 500;
    color: #c9a050;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.selected-chip::before {
    content: '▶';
    font-size: 9px;
}

/* column gap fix */
[data-testid="stHorizontalBlock"] {
    gap: 20px !important;
}

/* hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
@st.cache_resource
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    movie_index_map = {title: i for i, title in enumerate(movies['title'])}
    return movies, similarity, movie_index_map

movies, similarity, movie_index_map = load_data()


# ─────────────────────────────────────────────
#  FETCH POSTER
# ─────────────────────────────────────────────
def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    try:
        data = requests.get(url, timeout=5).json()
        if data.get('Poster') and data['Poster'] != "N/A":
            return data['Poster'], data.get('Year', ''), data.get('Genre', '').split(',')[0].strip()
    except Exception:
        pass
    return "https://via.placeholder.com/300x450/0f1018/c9a050?text=No+Image", '', ''


# ─────────────────────────────────────────────
#  RECOMMEND
# ─────────────────────────────────────────────
def recommend(movie_name):
    if movie_name not in movie_index_map:
        return [], [], []
    idx = movie_index_map[movie_name]
    distances = similarity[idx]
    heap = []
    for i, score in enumerate(distances):
        heapq.heappush(heap, (-score, i))
    names, posters, metas = [], [], []
    count = 0
    while count < 6 and heap:
        score, i = heapq.heappop(heap)
        title = movies.iloc[i]['title']
        if title != movie_name:
            poster, year, genre = fetch_poster(title)
            names.append(title)
            posters.append(poster)
            metas.append({'year': year, 'genre': genre})
            count += 1
    return names[:5], posters[:5], metas[:5]


# ─────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────

# Film strip top accent
st.markdown('<div class="filmstrip"></div>', unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Powered by Content Intelligence</div>
    <div class="hero-title">Discover Your<br><em>Next Obsession</em></div>
    <div class="hero-subtitle">
        A curated recommendation engine that maps the invisible threads
        connecting cinema's greatest works.
    </div>
    <div class="hero-deco">C</div>
</div>
""", unsafe_allow_html=True)

# Search section
st.markdown('<div class="search-section"><div class="search-label">Select a Title</div></div>', unsafe_allow_html=True)

col_sel, col_btn, col_space = st.columns([4, 1.6, 1.5])
with col_sel:
    selected_movie = st.selectbox(
        "Select a movie",
        list(movie_index_map.keys()),
        label_visibility="collapsed"
    )
with col_btn:
    recommend_clicked = st.button("Discover  →")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RESULTS
# ─────────────────────────────────────────────
if recommend_clicked:
    st.markdown('<div class="results-section">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="selected-chip">{selected_movie}</div>
    <div class="results-header">
        <div class="results-title">Because You Chose This Film</div>
        <div class="results-count">5 Recommendations</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Curating your selection..."):
        names, posters, metas = recommend(selected_movie)

    if names:
        cols = st.columns(5, gap="large")
        stagger_classes = ['stagger-1','stagger-2','stagger-3','stagger-4','stagger-5']

        for i, col in enumerate(cols):
            with col:
                # Card wrapper with rank badge
                st.markdown(f"""
                <div class="stagger-item {stagger_classes[i]}" style="position:relative;">
                    <div style="
                        position: absolute;
                        top: 10px; left: 10px;
                        z-index: 10;
                        width: 26px; height: 26px;
                        background: rgba(7,8,16,0.85);
                        border: 1px solid rgba(201,160,80,0.45);
                        border-radius: 2px;
                        display: flex; align-items: center; justify-content: center;
                        font-family: 'Playfair Display', serif;
                        font-size: 12px; font-weight: 700;
                        color: #c9a050;
                        backdrop-filter: blur(8px);
                    ">{i+1:02d}</div>
                </div>
                """, unsafe_allow_html=True)

                st.image(posters[i], width='stretch')

                # Title
                st.markdown(f"""
                <div style="margin-top:10px;">
                    <div style="
                        font-family: 'Playfair Display', serif;
                        font-size: 15px;
                        font-weight: 700;
                        color: #f0e8da;
                        line-height: 1.3;
                        text-align: center;
                    ">{names[i]}</div>
                    <div style="
                        font-size: 11px;
                        font-weight: 500;
                        letter-spacing: 0.12em;
                        color: rgba(201,160,80,0.55);
                        text-transform: uppercase;
                        text-align: center;
                        margin-top: 5px;
                    ">{metas[i]['year']}{'  ·  ' + metas[i]['genre'] if metas[i]['genre'] else ''}</div>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.markdown('<div class="no-results">No recommendations found for this title.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty state
    st.markdown("""
    <div style="padding: 80px 80px 60px; text-align: center;">
        <div style="
            font-family: 'Playfair Display', serif;
            font-size: 18px;
            font-style: italic;
            color: rgba(232,224,212,0.18);
            letter-spacing: 0.03em;
            line-height: 1.8;
        ">
            Select a film above and press Discover<br>to reveal what the algorithm sees in it.
        </div>
        <div style="
            margin-top: 32px;
            font-size: 48px;
            opacity: 0.08;
        ">🎞</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    border-top: 1px solid rgba(255,255,255,0.05);
    margin: 40px 80px 0;
    padding: 24px 0 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
">
    <div style="font-size: 11px; letter-spacing: 0.25em; text-transform: uppercase; color: rgba(232,224,212,0.2); font-weight: 500;">
        CineMatch &nbsp;·&nbsp; Content-Based Filtering
    </div>
    <div style="font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; color: rgba(201,160,80,0.25); font-weight: 500;">
        Powered by OMDb API
    </div>
</div>
""", unsafe_allow_html=True)