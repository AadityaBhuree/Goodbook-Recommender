<div align="center">
<img width="100%" src="https://raw.githubusercontent.com/AadityaBhuree/Goodbook-Recommender/main/banner.svg" alt="~/.bookrecommender" />

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/AadityaBhuree/Goodbook-Recommender?style=flat-square&logo=github&logoColor=white&color=00FFFF)](https://github.com/AadityaBhuree/Goodbook-Recommender/stargazers)
[![Profile](https://img.shields.io/badge/Profile-AadityaBhuree-8B5CF6?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree)

**Discover your next great read with 3 ML-powered recommendation engines**

</div>

---

## `~/.quickstart`

```bash
# 1. Clone & enter
git clone https://github.com/AadityaBhuree/Goodbook-Recommender.git
cd Goodbook-Recommender

# 2. Virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install & launch
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501** — or try the live demo at **[streamlit.app](https://aadityabhuree-goodbook-recommender-app-jqagvs.streamlit.app/)**.

On first run, it automatically downloads the Goodbooks-10k dataset (~6M ratings). If the download fails, a realistic synthetic dataset is generated instantly.

---

## `~/.overview`

**BookRecommender** combines three recommendation approaches into a dark-themed interactive dashboard. 10K books, 6M ratings, 53K users — all at your fingertips.

| Area | Highlights |
|---|---|
| 🧠 **3 Engines** | Popularity (Bayesian), Content (TF-IDF + cosine), Collaborative (KNN) |
| 📖 **Catalog** | Filter by year/rating, search title/author, sort 5 ways, paginated grid |
| 🎨 **Dashboard** | Dark terminal theme, glassmorphism cards, hover animations |
| 🤖 **Smart Load** | Auto-downloads Goodbooks-10k, pickle-cached, synthetic fallback |
| ⚙️ **Configurable** | 10+ hyperparameters, theme colors, filtering thresholds |

---

## `~/.features`

### 🏠 Home Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  ~/.bookrecommender                                                 │
│  ───────────────────────────────────────────────────────────────     │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐         │
│  │  10,000  │  │  53,424  │  │ 5,976,479  │  │   4.2    │         │
│  │  Books   │  │  Users   │  │  Ratings   │  │  Avg ★   │         │
│  └──────────┘  └──────────┘  └────────────┘  └──────────┘         │
│                                                                     │
│  🔥 Trending Books  📍 Quick Actions                               │
│  [Browse & Search]    [Get Personalized Recs]                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 📖 Explore Books

- **Search** by title or author with live text filtering
- **Filter** by publication year range and minimum rating (★ 3+ to ★ 8+)
- **Sort** by Popularity, Rating, Title, or Year
- **12 books per page** with dropdown pagination
- **Detailed cards** — title, author, star rating, rating count, year, publisher, genre

### 🎯 Get Recommendations — 3 Engines

| Tab | Engine | Method |
|---|---|---|
| 🔥 **Popularity** | Bayesian weighted score | `(avg × count + C × global) / (count + C)` |
| 📝 **Content-Based** | TF-IDF + Cosine Similarity | Metadata-based lookalike books |
| 👥 **Collaborative** | K-Nearest Neighbors | "Readers also liked" item-based CF |

Each method returns ranked results with similarity scores, star ratings, and visual score bars.

---

## `~/.stack`

| Category | Technology |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io) — interactive dashboard |
| **Backend** | [Python 3.10+](https://python.org) — core logic & pipelines |
| **ML / NLP** | [scikit-learn](https://scikit-learn.org) — `TfidfVectorizer`, `cosine_similarity`, `NearestNeighbors` |
| **Data** | [pandas](https://pandas.dev) / [numpy](https://numpy.org) — manipulation & matrix ops |
| **Sparse Math** | [scipy](https://scipy.org) `csr_matrix` — memory-efficient operations |
| **Visualization** | [matplotlib](https://matplotlib.org) / [seaborn](https://seaborn.pydata.org) — charts |
| **Downloads** | [requests](https://requests.readthedocs.io) — dataset fetching |
| **Caching** | `pickle` — fast reload of preprocessed data |

---

## `~/.structure`

```
book-recommender/
├── app.py                    # Main app — init, sidebar, dashboard
├── requirements.txt          # Dependencies
├── .streamlit/config.toml    # Theme & server config
├── README.md                 # You are here
│
├── pages/
│   ├── 1_📚_Explore_Books.py         # Catalog browser + filters
│   ├── 2_🎯_Get_Recommendations.py   # 3-tab recommendation engine
│   └── 3_📊_About.py                # Project info
│
├── src/
│   ├── config.py              # Hyperparameters, URLs, theme colors
│   ├── ui.py                  # Custom CSS, cards, stars, components
│   ├── app_init.py            # Shared init utilities (on-demand collab)
│   ├── preprocessing.py       # Data cleaning & filtering pipeline
│   ├── data/
│   │   ├── loader.py          # Download, cache, synthetic fallback
│   │   └── models.py          # Book/User/Rating dataclasses
│   └── recommenders/
│       ├── base.py            # Abstract recommender interface
│       ├── popularity.py      # Bayesian weighted scoring
│       ├── content_based.py   # TF-IDF + cosine similarity
│       └── collaborative.py   # KNN item-based & user-based CF
│
├── scripts/
│   └── download_data.py       # Standalone data downloader
│
└── data/
    ├── books.csv              # Goodbooks-10k (gitignored)
    ├── ratings.csv            # Goodbooks-10k (gitignored)
    └── cache/processed_data.pkl  # Pickled cache (gitignored)
```

---

## `~/.engines`

### 🔥 Popularity-Based

Bayesian weighted score — prevents books with a single perfect rating from dominating:

```python
C = 50  # damping factor
score = (avg_rating * rating_count + C * global_avg) / (rating_count + C)
```

Books with few ratings are pulled toward the global average. Minimum `min_ratings` (default: 10) threshold.

### 📝 Content-Based

1. Text corpus from metadata (author, publisher, genre)
2. Vectorized via `TfidfVectorizer` (5K features, unigrams+bigrams, English stop words)
3. Pairwise cosine similarity across the entire catalog
4. Top-N most similar books returned (seed excluded)

```python
self._vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))
self._similarity_matrix = cosine_similarity(self._vectorizer.fit_transform(content_features))
```

### 👥 Collaborative Filtering

1. User-item rating matrix built via pivot table
2. Two KNN models with cosine distance (brute-force):
   - **Item-based**: books similar to a given book by rating patterns
   - **User-based**: similar users' enjoyed books
3. Top-N unread books sorted by weighted similarity

```python
self._user_knn = NearestNeighbors(n_neighbors=20, metric="cosine", algorithm="brute")
self._user_knn.fit(csr_matrix(self._user_item_matrix.values))
```

---

## `~/.dataset`

### Goodbooks-10k (Primary)

| Stat | Value |
|---|---|
| Books | **10,000** — real titles, authors, cover images |
| Ratings | **5,976,479** (1–5 scale) |
| Users | **53,424** |
| Source | [zygmuntz/goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) |

### Synthetic (Fallback)

| Stat | Value |
|---|---|
| Books | 500 — 20 genres, 100 authors |
| Users | 1,000 — locations & ages |
| Ratings | 15,000 — biased toward 4–5 stars |

---

## `~/.config`

### Model Parameters (`src/config.py`)

| Parameter | Default | Description |
|---|---|---|
| `min_ratings_per_book` | 2 | Min ratings for a book in dataset |
| `min_ratings_per_user` | 2 | Min ratings for a user included |
| `content_similarity_top_k` | 20 | Top-K similar for content retrieval |
| `collab_n_neighbors` | 20 | KNN neighbors for collaborative filtering |
| `default_recommendations` | 12 | Default recommendations to display |
| `synthetic_num_books` | 500 | Synthetic fallback book count |
| `synthetic_num_ratings` | 15000 | Synthetic fallback rating count |

### Theme Colors (terminal dark)

```python
COLORS = {
    "primary": "#00FFFF",      # Cyan — headings, accents
    "secondary": "#8B5CF6",    # Purple — secondary accents
    "accent": "#10B981",       # Emerald — recommendation cards
    "background": "#0D1117",   # Near-black — page background
    "surface": "#161B22",      # Dark card surface
    "text": "#E5E7EB",         # Light gray — body text
    "text_secondary": "#9CA3AF", # Muted text
    "error": "#EF4444",        # Red — errors
    "rating": "#F59E0B",       # Amber — star ratings
}
```

---

## `~/.deploy`

Deploy on [Streamlit Cloud](https://share.streamlit.io) for free:

1. **Fork** this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) → **"New app"**
3. Select fork → `main` branch → `app.py` as main file
4. Click **"Deploy"**

Pre-configured with `.streamlit/config.toml` and `requirements.txt`.

---

## `~/.roadmap`

- [x] **v1.0** — Core recommendation engines + dashboard
- [x] **v1.1** — On-demand collaborative filtering, cached filters, smooth pagination
- [ ] **Automated test suite** — pytest with coverage
- [ ] **User-based CF** in the UI (backend exists)
- [ ] **Docker support** — `Dockerfile` + `docker-compose.yml`
- [ ] **CI/CD** — GitHub Actions for linting + testing

---

## `~/.contributing`

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit**: `git commit -m 'Add AmazingFeature'`
4. **Push**: `git push origin feature/AmazingFeature`
5. Open a **Pull Request**

---

## `~/.license`

Distributed under the **MIT License**. Goodbooks-10k dataset available for research use per its original license.

---

## `~/.acknowledgments`

- **[Zygmunt Zając](https://github.com/zygmuntz)** — Goodbooks-10k dataset
- **[scikit-learn](https://scikit-learn.org)** — ML framework powering all recommendations
- **[Streamlit](https://streamlit.io)** — Interactive web dashboard
- **ML-ProjectKart (#31)** — Recommendation system architecture inspiration

---

<div align="center">

```
⚡ print("Hello, World!")  —  Let's build something awesome.
```

[![Star](https://img.shields.io/badge/⭐_Star_if_useful-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree/Goodbook-Recommender)
[![Fork](https://img.shields.io/badge/🍴_Fork-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree/Goodbook-Recommender/fork)

</div>
