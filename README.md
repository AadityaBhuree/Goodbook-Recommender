<div align="center">

# 📚 BookRecommender

**Intelligent Book Recommendation System — powered by Machine Learning**

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)


<br>

**Discover your next great read with 3 ML-powered recommendation engines**

</div>

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/AadityaBhuree/Goodbook-Recommender.git
cd Goodbook-Recommender

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
streamlit run app.py
```

The app opens at **(https://aadityabhuree-goodbook-recommender-app-jqagvs.streamlit.app/)**. On first run, it automatically downloads the Goodbooks-10k dataset (~6M ratings). If the download fails, a realistic synthetic dataset is generated instantly.

---

## 🌟 Overview

**BookRecommender** is a production-grade book recommendation system that combines three powerful machine learning approaches into a beautiful interactive dashboard.

### What's Included

| Area | Highlights |
|---|---|
| 🧠 **3 Recommendation Engines** | Popularity-Based (Bayesian score), Content-Based (TF-IDF + cosine), Collaborative Filtering (KNN) |
| 📖 **Explore & Search Catalog** | Filter by year, rating, text search, sort by popularity/rating/title/year, paginated grid |
| 🎨 **Polished Dashboard** | Warm bookish theme, custom CSS, glassmorphism cards, hover animations, Playfair Display typography |
| 🤖 **Smart Data Loading** | Auto-downloads Goodbooks-10k, pickle-cached for instant reload, synthetic fallback |
| ⚙️ **Fully Configurable** | 10+ tunable hyperparameters, color scheme, data filtering thresholds |

---

## 👀 Preview

### 🏠 Home Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│  📚 BookRecommender                                                 │
│  ───────────────────────────────────────────────────────────────     │
│  Discover Your Next Great Read                                      │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐         │
│  │  10,000  │  │  53,424  │  │ 5,976,479  │  │   4.2    │         │
│  │  Books   │  │  Users   │  │  Ratings   │  │  Avg ★   │         │
│  └──────────┘  └──────────┘  └────────────┘  └──────────┘         │
│                                                                     │
│  🔥 Trending Books                                                  │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐    │
│  │       📖         │ │       📖         │ │       📖         │    │
│  │  The Hunger Games│ │  Harry Potter    │ │  The Fault in    │    │
│  │  ★ 4.34 (2.9M)   │ │  ★ 4.55 (4.2M)   │ │  ★ 4.26 (1.8M)   │    │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘    │
│                                                                     │
│  📍 Quick Actions                                                   │
│  [📖 Browse & Search]        [🎯 Get Recommendations]              │
└─────────────────────────────────────────────────────────────────────┘
```

### 📖 Explore Books — Catalog Browser

```
┌─────────────────────────────────────────────────────────────────────┐
│  📖 Explore Books                                                   │
│  ───────────────────────────────────────────────────────────────     │
│  🔍 Search title...    [Year: 1950-2024]    [Rating: Any]          │
│                                                                     │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐    │
│  │       📚         │ │       📚         │ │       📚         │    │
│  │  To Kill a       │ │  1984            │ │  Pride and       │    │
│  │  Mockingbird     │ │  ★ 4.19 (2.6M)   │ │  Prejudice       │    │
│  │  ★ 4.29 (3.1M)   │ │  George Orwell   │ │  ★ 4.28 (2.1M)   │    │
│  │  Harper Lee      │ │  1949            │ │  Jane Austen     │    │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘    │
│                                                                     │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐    │
│  │       📚         │ │       📚         │ │       📚         │    │
│  │  The Great       │ │  Animal Farm     │ │  Lord of the     │    │
│  │  Gatsby          │ │  ★ 3.90 (2.5M)   │ │  Rings           │    │
│  │  ★ 3.93 (3.0M)   │ │  George Orwell   │ │  ★ 4.51 (2.2M)   │    │
│  │  F. Scott Fitz.  │ │  1945            │ │  J.R.R. Tolkien  │    │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘    │
│                                                Page 1 of 834  ▸    │
└─────────────────────────────────────────────────────────────────────┘
```

### 🎯 Get Recommendations — 3 Engines in Action

```
┌─────────────────────────────────────────────────────────────────────┐
│  🎯 Get Recommendations                                             │
│  ───────────────────────────────────────────────────────────────     │
│  [🔥 Popularity]  [📝 Content-Based]  [👥 Collaborative Filtering]  │
│  ───────────────────────────────────────────────────────────────     │
│                                                                     │
│  Selected: "The Hunger Games" by Suzanne Collins  ★ 4.34            │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Find Similar Books                                         │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  #1  Catching Fire           ★ 4.33 · Score: 0.912                 │
│      by Suzanne Collins      ██████████████████░░░░░░░              │
│                                                                     │
│  #2  Mockingjay              ★ 4.12 · Score: 0.874                 │
│      by Suzanne Collins      █████████████████░░░░░░░░              │
│                                                                     │
│  #3  Divergent               ★ 4.24 · Score: 0.756                 │
│      by Veronica Roth        ███████████████░░░░░░░░░               │
│                                                                     │
│  #4  The Maze Runner         ★ 4.08 · Score: 0.721                 │
│      by James Dashner        ██████████████░░░░░░░░░░               │
│                                                                     │
│  #5  The Fault in Our Stars  ★ 4.26 · Score: 0.698                 │
│      by John Green           █████████████░░░░░░░░░░░               │
└─────────────────────────────────────────────────────────────────────┘
```

The app features **4 interconnected pages** — a stats-rich **Home** dashboard, a filterable **Explore Books** catalog, a 3-tab **Get Recommendations** engine, and an **About** page with tech stack details.

---

## 🎯 Key Features

### 📖 Explore Books — Browse the Full Catalog

- **Search** by title or author with live text filtering
- **Filter** by publication year range and minimum rating (★ 3+ through ★ 8+)
- **Sort** by Popularity, Rating (high→low / low→high), Title (A→Z), or Year (new→old)
- **Paginated grid** — 12 books per page with page navigation
- **Detailed book cards** showing title, author, star rating, rating count, year, publisher, and genre

### 🎯 Get Recommendations — Three Methods, One Interface

| Tab | Engine | How it works |
|---|---|---|
| 🔥 **Popularity-Based** | Bayesian weighted score | `(avg_rating × count + C × global_avg) / (count + C)` — prevents rating-count bias |
| 📝 **Content-Based** | TF-IDF + Cosine Similarity | Analyzes author, publisher & genre metadata to find lookalike books |
| 👥 **Collaborative Filtering** | K-Nearest Neighbors | "Readers who liked this also liked..." — item-based & user-based modes |

Each method outputs ranked results with similarity scores, star ratings, and visual score bars.

---

## 🛠️ Tech Stack

| Category | Technology | Role |
|---|---|---|
| **Frontend** | [Streamlit](https://streamlit.io) | Interactive web dashboard, UI components |
| **Backend** | [Python 3.10+](https://python.org) | Core logic, data pipelines |
| **ML / NLP** | [scikit-learn](https://scikit-learn.org) | `TfidfVectorizer`, `cosine_similarity`, `NearestNeighbors` |
| **Data** | [pandas](https://pandas.dev) / [numpy](https://numpy.org) | Data manipulation, matrix operations |
| **Sparse Math** | [scipy](https://scipy.org) `csr_matrix` | Memory-efficient large-matrix operations |
| **Visualization** | [matplotlib](https://matplotlib.org) / [seaborn](https://seaborn.pydata.org) | Charts & plots |
| **Downloads** | [requests](https://requests.readthedocs.io) | Dataset download from GitHub |
| **Caching** | `pickle` | Fast reload of preprocessed data |

---

## 📂 Project Structure

```
book-recommender/
├── app.py                              # Main Streamlit app (dashboard + init)
├── requirements.txt                    # Python dependencies
├── .streamlit/
│   └── config.toml                     # Streamlit theme & server config
├── README.md                           # You are here
│
├── pages/
│   ├── 1_📚_Explore_Books.py           # Catalog browser with filters
│   ├── 2_🎯_Get_Recommendations.py     # 3-tab recommendation interface
│   └── 3_📊_About.py                   # Project info & statistics
│
├── src/
│   ├── config.py                       # 20+ tunable hyperparameters, dataset URLs, theme colors
│   ├── ui.py                           # Custom CSS, cards, stars, hero, footer components
│   ├── preprocessing.py                # Data cleaning pipeline & filtering
│   ├── data/
│   │   ├── loader.py                   # Download, cache, synthetic fallback
│   │   └── models.py                   # Book, User, Rating, RecommendationResult dataclasses
│   └── recommenders/
│       ├── base.py                     # Abstract recommender interface
│       ├── popularity.py               # Bayesian weighted scoring
│       ├── content_based.py            # TF-IDF + cosine similarity
│       └── collaborative.py            # KNN user-based & item-based CF
│
├── scripts/
│   └── download_data.py                # Standalone data downloader
│
└── data/
    ├── books.csv                       # Downloaded Goodbooks-10k (gitignored)
    ├── ratings.csv                     # Downloaded Goodbooks-10k (gitignored)
    └── cache/
        └── processed_data.pkl          # Pickled & ready-to-use (gitignored)
```

---

## 🧠 How It Works

### 🔥 Popularity-Based Recommender

Uses a **Bayesian weighted score** to rank books, preventing obscure books with a single perfect rating from dominating:

```python
# From src/recommenders/popularity.py
C = 50  # damping factor
score = (avg_rating * rating_count + C * avg_rating.mean()) / (rating_count + C)
```

Books with few ratings are pulled toward the global average. Books must have at least `min_ratings` (default: 10) to receive a non-zero score.

### 📝 Content-Based Recommender

1. Builds a text corpus from book metadata (author, publisher, genre)
2. Vectorizes using `TfidfVectorizer` (max 5,000 features, unigrams + bigrams, English stop words)
3. Computes pairwise cosine similarity across the entire catalog
4. Given a seed book, returns the top-N most similar books (excluding the seed)

```python
# From src/recommenders/content_based.py
self._vectorizer = TfidfVectorizer(max_features=5000, stop_words="english", ngram_range=(1, 2))
self._feature_matrix = self._vectorizer.fit_transform(content_features)
self._similarity_matrix = cosine_similarity(self._feature_matrix)
```

### 👥 Collaborative Filtering Recommender

1. Builds a **user-item rating matrix** (pivot table: users × books)
2. Fits two KNN models using **cosine distance** with brute-force algorithm:
   - **Item-based**: Finds books similar to a given book based on rating patterns
   - **User-based**: Finds similar users and recommends books they enjoyed
3. Returns top-N unread books sorted by weighted similarity score

```python
# From src/recommenders/collaborative.py
self._user_knn = NearestNeighbors(n_neighbors=20, metric="cosine", algorithm="brute")
self._user_knn.fit(csr_matrix(self._user_item_matrix.values))
```

---

## 📊 Dataset

### Primary: Goodbooks-10k

| Statistic | Value |
|---|---|
| Books | **10,000** with real titles, authors, cover images |
| Ratings | **5,976,479** (1–5 scale) |
| Users | **53,424** |
| Source | [zygmuntz/goodbooks-10k](https://github.com/zygmuntz/goodbooks-10k) |

### Fallback: Synthetic Data

When the Goodbooks-10k download fails (no internet, network issues), the app generates a realistic synthetic dataset:

| Statistic | Value |
|---|---|
| Books | 500 with realistic titles, 20 genres, 100 authors |
| Users | 1,000 with locations & ages |
| Ratings | 15,000 (distribution biased toward 4–5 stars) |

---

## 🧪 Testing

The project currently supports manual validation via the Streamlit UI. To verify the system works correctly:

```bash
# 1. Start the app
streamlit run app.py

# 2. Click "Load Data & Initialize" on the Home page
# 3. Navigate to "Get Recommendations" and test each of the 3 methods
# 4. Browse books with different filters in "Explore Books"
```

> **Coming soon**: Automated test suite with pytest covering the preprocessing pipeline, recommendation engines, and data loading.

---

## ☁️ Deploy to Streamlit Cloud

Deploy your own instance for free on [Streamlit Cloud](https://share.streamlit.io):

1. **Fork** this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **"New app"**
3. Select your fork → Branch: `main` → Main file: `app.py`
4. Click **"Deploy"**

The app includes proper Streamlit Cloud configuration:
- `.streamlit/config.toml` — Theme colors & server settings
- `requirements.txt` — All dependencies pre-listed

---

## ⚙️ Customization

### Model Parameters (`src/config.py`)

| Parameter | Default | Description |
|---|---|---|
| `min_ratings_per_book` | 2 | Minimum ratings for a book to appear in the dataset |
| `min_ratings_per_user` | 2 | Minimum ratings for a user to be included |
| `content_similarity_top_k` | 20 | Top-K similar books for content-based retrieval |
| `collab_n_neighbors` | 20 | Number of neighbors for KNN collaborative filtering |
| `collab_min_similarity` | 0.0 | Minimum similarity threshold for CF results |
| `default_recommendations` | 12 | Default number of recommendations to display |
| `books_per_page` | 24 | Books per page in Explore view |
| `synthetic_num_books` | 500 | Synthetic dataset fallback size |
| `synthetic_num_users` | 1000 | Synthetic dataset fallback size |
| `synthetic_num_ratings` | 15000 | Synthetic dataset fallback size |

### Theme Colors (`src/config.py`)

```python
COLORS = {
    "primary": "#8B4513",      # SaddleBrown — headings, borders
    "secondary": "#DAA520",    # Goldenrod — accents, borders
    "accent": "#2E8B57",       # SeaGreen — recommendation cards
    "background": "#FAF3E0",   # Cream — page background
    "text": "#2C1810",         # Dark brown
    "rating": "#FFA000",       # Amber — star ratings
}
```

### Streamlit Theme (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#8B4513"
backgroundColor = "#FAF3E0"
textColor = "#2C1810"
```

---

## 🔮 Future Improvements

- [ ] **Automated test suite** — pytest with coverage for all modules
- [ ] **User-based collaborative filtering** in the UI (backend already supports it)
- [ ] **Model export** — save trained similarity matrices for instant startup
- [ ] **Docker support** — `Dockerfile` + `docker-compose.yml`
- [ ] **Streamlit Cloud deployment** badge with live link
- [ ] **CI/CD pipeline** — GitHub Actions for linting + testing

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** your changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to the branch: `git push origin feature/AmazingFeature`
5. Open a **Pull Request**

---

## 📝 License

Distributed under the **MIT License**. The Goodbooks-10k dataset is available for research use per its original license.

---

## 🙏 Acknowledgments

- **[Zygmunt Zając](https://github.com/zygmuntz)** for the Goodbooks-10k dataset
- **[scikit-learn](https://scikit-learn.org)** — the ML framework powering all recommendations
- **[Streamlit](https://streamlit.io)** — the web framework for the interactive dashboard
- **ML-ProjectKart (#31)** — inspiration for the recommendation system architecture

---

<div align="center">
    <br>
    <p>Built with ❤️ for the open-source community</p>
    <a href="https://streamlit.io">
        <img src="https://img.shields.io/badge/Powered%20by-Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Powered by Streamlit">
    </a>
    <a href="https://scikit-learn.org">
        <img src="https://img.shields.io/badge/Powered%20by-scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Powered by scikit-learn">
    </a>
    <br><br>
    <sub>⭐ Star this repo if you find it useful!</sub>
</div>
