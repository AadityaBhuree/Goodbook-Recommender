"""Application configuration and settings."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"

# Dataset URLs (Goodbooks-10k — stable GitHub host)
GOODBOOKS_BOOKS_URL = "https://github.com/zygmuntz/goodbooks-10k/raw/master/books.csv"
GOODBOOKS_RATINGS_URL = "https://github.com/zygmuntz/goodbooks-10k/raw/master/ratings.csv"

# Local file paths
BOOKS_FILE = DATA_DIR / "books.csv"
RATINGS_FILE = DATA_DIR / "ratings.csv"
USERS_FILE = None  # Goodbooks-10k has no user metadata
PROCESSED_DATA_FILE = CACHE_DIR / "processed_data.pkl"


@dataclass
class RecommenderConfig:
    """Configuration for the recommendation system."""

    # Data filtering
    min_ratings_per_book: int = 2
    min_ratings_per_user: int = 2
    max_rating: int = 10

    # Content-based recommender
    content_similarity_top_k: int = 20

    # Collaborative filtering
    collab_n_neighbors: int = 20
    collab_min_similarity: float = 0.0
    collab_max_genres: int = 5

    # Display
    default_recommendations: int = 12
    books_per_page: int = 24

    # Synthetic fallback
    synthetic_num_books: int = 500
    synthetic_num_users: int = 1000
    synthetic_num_ratings: int = 15000
    synthetic_seed: int = 42


# App theme
APP_TITLE = "BookRecommender"
APP_SUBTITLE = "Discover Your Next Great Read"
APP_DESCRIPTION = (
    "An intelligent book recommendation system powered by machine learning. "
    "Discover books you'll love through collaborative filtering, content-based "
    "analysis, and popularity insights."
)

COLORS = {
    "primary": "#00FFFF",  # Cyan — headings, accents
    "secondary": "#8B5CF6",  # Purple — secondary accents, borders
    "accent": "#10B981",  # Emerald — recommendation cards, success
    "background": "#0D1117",  # Near-black — page background
    "surface": "#161B22",  # Dark card surface
    "text": "#E5E7EB",  # Light gray — body text
    "text_secondary": "#9CA3AF",  # Muted text
    "error": "#EF4444",  # Red — errors
    "rating": "#F59E0B",  # Amber — star ratings
}

# Streamlit page config
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
