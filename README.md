<div align="center">

# 📚 BookRecommender

**Discover your next great read with 3 ML-powered recommendation engines**

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![pandas](https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/AadityaBhuree/Goodbook-Recommender?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree/Goodbook-Recommender/stargazers)
[![Profile](https://img.shields.io/badge/Profile-AadityaBhuree-2D5F6E?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree)

</div>

---

## 🚀 Quickstart

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

Opens at **http://localhost:8501**.

On first run, click **"Load Data & Initialize"** to download the Goodbooks-10k dataset (~6M ratings). If the download fails, a realistic synthetic dataset is generated instantly.

---

## ✨ Features

### 🏠 Home Dashboard

| Stat | Value |
|---|---|
| Books | **10,000** |
| Users | **53,424** |
| Ratings | **5,976,479** |
| Avg Rating | **4.0 ★** |

- **Trending Books** — Top-rated books previewed on the dashboard
- **Quick Actions** — Navigate to Explore or Recommendations pages
- **Sidebar Stats** — Dataset overview at a glance

### 🔍 Explore Books

- **Search** by title or author with live text filtering
- **Filter** by publication year range and minimum rating (★ 3+ to ★ 8+)
- **Sort** by Popularity, Rating, Title, or Year
- **12 books per page** with dropdown pagination
- **Book cards** — cover placeholder, title, author, star rating, rating count

### 🎯 Get Recommendations — 3 Engines

| Tab | Engine | Method |
|---|---|---|
| 🔥 **Popularity** | Bayesian weighted score | `(avg × count + C × global) / (count + C)` |
| 📝 **Content-Based** | TF-IDF + Cosine Similarity | Metadata-based lookalike books |
| 👥 **Collaborative** | K-Nearest Neighbors | "Readers also liked" item-based CF |

Each method returns ranked results with similarity scores, star ratings, and visual score bars.

### 🌙 Dark Mode

Toggle **"🌙 Dark mode"** in the sidebar to switch between light and dark themes. The entire UI adapts — backgrounds, cards, text, borders, scrollbars, tabs, and buttons all re-color consistently. The theme persists per session.

### 📍 Active Nav Indicator

The currently active page in the sidebar is highlighted with a teal left border and subtle background, so you always know which page you're on.

### ✨ Page Transitions

Content fades in with a gentle upward animation each time you navigate between pages.

---

## 🎨 Theme

### Light Mode

| Token | Color | Hex |
|---|---|---|
| Primary | Deep teal | `#2D5F6E` |
| Secondary | Warm copper | `#C4956A` |
| Accent | Sage green | `#7A9E7E` |
| Background | Warm off-white | `#FCF9F5` |
| Surface | White | `#FFFFFF` |
| Text | Warm dark | `#2D2A24` |

### Dark Mode

| Token | Color | Hex |
|---|---|---|
| Primary | Soft teal | `#6BB4D0` |
| Secondary | Warm copper | `#D4A574` |
| Accent | Sage green | `#8DBD8D` |
| Background | Dark | `#1A1A1E` |
| Surface | Warm dark | `#2A2723` |
| Text | Warm light | `#E8E0D8` |

---

## 🛠️ Tech Stack

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

## 📁 Project Structure

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

## ⚙️ Configuration

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

### How the Engines Work

**🔥 Popularity-Based** — Bayesian weighted score prevents books with a single perfect rating from dominating:

```python
C = 50  # damping factor
score = (avg_rating * rating_count + C * global_avg) / (rating_count + C)
```

Books with few ratings are pulled toward the global average.

**📝 Content-Based** — Text corpus from metadata (author, publisher, genre) is vectorized via `TfidfVectorizer` (5K features, unigrams+bigrams), then pairwise cosine similarity finds the closest matches.

**👥 Collaborative Filtering** — A user-item rating matrix is built via pivot table, then KNN with cosine distance finds similar books based on rating patterns.

---

## 📊 Dataset

### Goodbooks-10k (Primary)

| Stat | Value |
|---|---|
| Books | **10,000** — real titles, authors, cover URLs |
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

## 🚢 Deploy

Deploy on [Streamlit Cloud](https://share.streamlit.io) for free:

1. **Fork** this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) → **"New app"**
3. Select fork → `main` branch → `app.py` as main file
4. Click **"Deploy"**

Pre-configured with `.streamlit/config.toml` and `requirements.txt`.

---

## 🗺️ Roadmap

- [x] **v1.0** — Core recommendation engines + dark terminal dashboard
- [x] **v1.1** — On-demand collaborative filtering, cached filters, smooth pagination
- [x] **v1.2** — Warm-modern light theme redesign, dark mode toggle, nav indicator, page transitions
- [ ] **Automated test suite** — pytest with coverage
- [ ] **Docker support** — `Dockerfile` + `docker-compose.yml`
- [ ] **CI/CD** — GitHub Actions for linting + testing

---

## 🤝 Contributing

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit**: `git commit -m 'Add AmazingFeature'`
4. **Push**: `git push origin feature/AmazingFeature`
5. Open a **Pull Request**

---

## 📄 License

Distributed under the **MIT License**. Goodbooks-10k dataset available for research use per its original license.

---

## 🙏 Acknowledgments

- **[Zygmunt Zając](https://github.com/zygmuntz)** — Goodbooks-10k dataset
- **[scikit-learn](https://scikit-learn.org)** — ML framework powering all recommendations
- **[Streamlit](https://streamlit.io)** — Interactive web dashboard
- **ML-ProjectKart (#31)** — Recommendation system architecture inspiration

---

<div align="center">

[![Star](https://img.shields.io/badge/⭐_Star_if_useful-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree/Goodbook-Recommender)
[![Fork](https://img.shields.io/badge/🍴_Fork-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/AadityaBhuree/Goodbook-Recommender/fork)

</div>
