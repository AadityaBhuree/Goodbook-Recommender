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

LIGHT_COLORS = {
    "primary": "#2D5F6E",      # Deep teal — headings, accents
    "secondary": "#C4956A",    # Warm copper — secondary accents
    "accent": "#7A9E7E",       # Sage green — recommendation cards
    "background": "#FCF9F5",   # Warm off-white paper — page background
    "surface": "#FFFFFF",      # White card surface
    "text": "#2D2A24",         # Warm dark — body text
    "text_secondary": "#8B8174",  # Warm gray — muted text
    "error": "#D14B4B",        # Warm red — errors
    "rating": "#D4952B",       # Warm amber — star ratings
    "border": "#EDE6D9",      # Warm beige border
    "border_hover": "#D4C9B8", # Darker beige hover
}

DARK_COLORS = {
    "primary": "#6BB4D0",      # Soft teal — headings, accents
    "secondary": "#D4A574",    # Warm copper — secondary accents
    "accent": "#8DBD8D",       # Sage green — recommendation cards
    "background": "#1A1A1E",   # Dark page background
    "surface": "#2A2723",      # Warm dark card surface
    "text": "#E8E0D8",         # Warm light — body text
    "text_secondary": "#A09888",  # Warm muted gray
    "error": "#E06060",        # Warm red — errors
    "rating": "#E0A030",       # Warm amber — star ratings
    "border": "#3D3832",       # Dark warm border
    "border_hover": "#5A5448", # Lighter dark hover
}

COLORS = dict(LIGHT_COLORS)  # Mutable copy, swapped at runtime via set_theme()


def set_theme(dark: bool) -> None:
    """Swap COLORS between light and dark mode in-place.
    Called before rendering so all f-string references resolve to the right palette.
    """
    COLORS.clear()
    COLORS.update(DARK_COLORS if dark else LIGHT_COLORS)

# Streamlit page config
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
