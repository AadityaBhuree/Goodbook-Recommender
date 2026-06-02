"""BookRecommender — Main Streamlit Application.

An intelligent book recommendation system powered by machine learning.
Discover books you'll love through collaborative filtering, content-based
analysis, and popularity insights.
"""

import logging
import sys
from pathlib import Path

import streamlit as st

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.config import APP_TITLE, PAGE_CONFIG
from src.ui import apply_styling, render_hero, render_stat_card, sidebar_footer
from src.data.loader import load_and_cache_data
from src.preprocessing import preprocess_pipeline
from src.recommenders.popularity import PopularityRecommender
from src.recommenders.content_based import ContentBasedRecommender
from src.recommenders.collaborative import CollaborativeRecommender
from src.config import RecommenderConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ── Page Configuration ──────────────────────────────────────────────────────

st.set_page_config(**PAGE_CONFIG)

# ── Session State ────────────────────────────────────────────────────────────

if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.books = None
    st.session_state.ratings = None
    st.session_state.users = None
    st.session_state.config = RecommenderConfig()
    st.session_state.popularity = None
    st.session_state.content = None
    st.session_state.collaborative = None


def load_data() -> None:
    """Load and preprocess all data, then initialize recommenders."""
    config = st.session_state.config

    with st.spinner("📚 Loading book data... This may take a moment on first run."):
        raw_books, raw_users, raw_ratings = load_and_cache_data(config)

    with st.spinner("🧹 Preprocessing data..."):
        books, users, ratings = preprocess_pipeline(
            raw_books, raw_users, raw_ratings, config
        )

    st.session_state.books = books
    st.session_state.ratings = ratings
    st.session_state.users = users

    with st.spinner("🤖 Training recommendation models..."):
        st.session_state.popularity = PopularityRecommender(books, ratings)
        st.session_state.content = ContentBasedRecommender(books, ratings)
        st.session_state.collaborative = CollaborativeRecommender(books, ratings)
        st.session_state.popularity.fit()
        st.session_state.content.fit()
        # Collaborative may take a while for large datasets
        if len(books) < 5000:
            st.session_state.collaborative.fit()
        else:
            logger.info("Skipping collaborative fit for large dataset (build on demand).")

    st.session_state.initialized = True
    logger.info(
        f"App initialized: {len(books)} books, "
        f"{len(ratings)} ratings from {ratings['user_id'].nunique()} users."
    )


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">📚</div>
            <div style="font-family: 'Playfair Display', serif; font-size: 1.4rem; 
                 font-weight: 600; color: #8B4513;">{APP_TITLE}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link("app.py", label="🏠  Home", use_container_width=True)
    st.page_link(
        "pages/1_📚_Explore_Books.py",
        label="📖  Explore Books",
        use_container_width=True,
    )
    st.page_link(
        "pages/2_🎯_Get_Recommendations.py",
        label="🎯  Get Recommendations",
        use_container_width=True,
    )
    st.page_link(
        "pages/3_📊_About.py",
        label="ℹ️  About",
        use_container_width=True,
    )

    st.sidebar.markdown("---")

    if not st.session_state.initialized:
        if st.sidebar.button("🚀 Load Data & Initialize", use_container_width=True):
            load_data()
            st.rerun()
    else:
        st.sidebar.success("✅ System Ready")
        if st.sidebar.button("🔄 Reload Data", use_container_width=True):
            st.session_state.initialized = False
            st.rerun()

    # Show data stats in sidebar if initialized
    if st.session_state.initialized and st.session_state.books is not None:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**📊 Dataset Overview**")
        st.sidebar.markdown(f"- Books: **{len(st.session_state.books):,}**")
        st.sidebar.markdown(f"- Ratings: **{len(st.session_state.ratings):,}**")
        st.sidebar.markdown(
            f"- Users: **{st.session_state.ratings['user_id'].nunique():,}**"
        )

    sidebar_footer()

# ── Main Page ────────────────────────────────────────────────────────────────

apply_styling()

if not st.session_state.initialized:
    # ── Welcome / Landing Page ──────────────────────────────────────────────
    render_hero()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_stat_card("3", "Recommendation Methods")
    with col2:
        render_stat_card("Smart", "Content & Collaborative Filtering")
    with col3:
        render_stat_card("ML-Powered", "scikit-learn Engine")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            text-align: center;
            max-width: 500px;
            margin: 0 auto;
        ">
            <div style="font-size: 1.2rem; font-weight: 600; color: #2C1810; margin-bottom: 0.5rem;">
                Get Started
            </div>
            <div style="color: #6B4F3A; margin-bottom: 1rem;">
                Click the button below to load the dataset and initialize 
                the recommendation engine. Your first run will download data 
                automatically.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀  Load Data & Initialize", use_container_width=True):
            load_data()
            st.rerun()

    st.markdown(
        """
        <div style="text-align: center; margin-top: 2rem; color: #999; font-size: 0.85rem;">
            <p>The app will download the Book-Crossing dataset (~5MB) on first run.<br>
            If download fails, synthetic data will be generated automatically.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # ── Dashboard (when initialized) ──────────────────────────────────────────
    render_hero()

    books = st.session_state.books
    ratings = st.session_state.ratings

    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card(f"{len(books):,}", "Books in Catalog")
    with col2:
        render_stat_card(f"{ratings['user_id'].nunique():,}", "Active Readers")
    with col3:
        render_stat_card(f"{len(ratings):,}", "Total Ratings")
    with col4:
        avg_rating = books["avg_rating"].mean()
        render_stat_card(f"{avg_rating:.1f}", "★ Avg Rating")

    st.markdown("<br>", unsafe_allow_html=True)

    # Show popular books preview
    st.markdown('<div class="section-header">🔥 Trending Books</div>', unsafe_allow_html=True)

    try:
        popular = st.session_state.popularity.recommend(n=6)
        cols = st.columns(3)
        for i, (_, book) in enumerate(popular.iterrows()):
            with cols[i % 3]:
                render_stat_card(
                    f"★ {book['avg_rating']:.1f}",
                    f"{book['title'][:40]}..." if len(str(book['title'])) > 40 else str(book['title']),
                )
    except Exception as e:
        st.warning(f"Could not load trending books: {e}")

    # Quick navigation
    st.markdown('<div class="section-header">📍 Quick Actions</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.page_link(
            "pages/1_📚_Explore_Books.py",
            label="📖  Browse & Search Books",
            use_container_width=True,
        )
    with col2:
        st.page_link(
            "pages/2_🎯_Get_Recommendations.py",
            label="🎯  Get Personalized Recommendations",
            use_container_width=True,
        )
