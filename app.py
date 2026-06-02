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
from src.app_init import ensure_collab_fitted

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
    st.session_state.collab_ready = False
    st.session_state._stats = None


def load_data() -> None:
    """Load and preprocess all data, then initialize recommenders."""
    config = st.session_state.config
    status = st.status("📚 Initializing BookRecommender...", expanded=True)

    with status:
        st.write("📚 Loading book data...")
        raw_books, raw_users, raw_ratings = load_and_cache_data(config)
        st.write("✅ Data loaded")

        st.write("🧹 Preprocessing data...")
        books, users, ratings = preprocess_pipeline(
            raw_books, raw_users, raw_ratings, config
        )
        st.write("✅ Preprocessing complete")

    st.session_state.books = books
    st.session_state.ratings = ratings
    st.session_state.users = users

    # Show a progress bar for model training
    progress_bar = st.progress(0.0, text="🤖 Training popularity model...")
    st.session_state.popularity = PopularityRecommender(books, ratings)
    st.session_state.popularity.fit()
    progress_bar.progress(0.35, text="🤖 Training content-based model...")
    st.session_state.content = ContentBasedRecommender(books, ratings)
    st.session_state.content.fit()
    progress_bar.progress(0.65, text="⏭️ Collaborative model will load on demand when you visit the Recommendations tab.")

    # Always initialize (but don't fit) collaborative — it'll fit on first use
    st.session_state.collaborative = CollaborativeRecommender(books, ratings)
    st.session_state.collab_ready = False

    progress_bar.progress(1.0, text="✅ Initialization complete!")
    progress_bar.empty()

    # Pre-compute stats once to avoid re-hashing large DataFrames on every re-render
    st.session_state._stats = {
        "n_books": len(books),
        "n_users": ratings["user_id"].nunique(),
        "n_ratings": len(ratings),
        "avg_rating": books["avg_rating"].mean(),
    }

    st.session_state.initialized = True
    logger.info(
        f"App initialized: {len(books)} books, "
        f"{len(ratings)} ratings from {ratings['user_id'].nunique()} users."
    )


# Stats are computed once during load_data() and stored in session state
# to avoid re-hashing large DataFrames on every re-render.
# See st.session_state._stats (set in load_data()).


# ── Sidebar ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">📚</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; 
                 font-weight: 600; color: #00FFFF;">{APP_TITLE}</div>
            <div style="font-size: 0.75rem; color: #9CA3AF;">~/.recommender</div>
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

    # Show data stats in sidebar if initialized (using pre-computed stats)
    if st.session_state.initialized and st.session_state._stats is not None:
        s = st.session_state._stats
        st.sidebar.markdown("---")
        st.sidebar.markdown("**📊 Dataset Overview**")
        st.sidebar.markdown(f"- Books: **{s['n_books']:,}**")
        st.sidebar.markdown(f"- Ratings: **{s['n_ratings']:,}**")
        st.sidebar.markdown(f"- Users: **{s['n_users']:,}**")

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
        f"""
        <div style="
            background: #161B22;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            margin: 0 auto;
            border: 1px solid rgba(255,255,255,0.06);
        ">
            <div style="font-size: 1.2rem; font-weight: 600; color: #00FFFF; margin-bottom: 0.5rem;">
                ~/get_started
            </div>
            <div style="color: #9CA3AF; margin-bottom: 1rem;">
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
        f"""
        <div style="text-align: center; margin-top: 2rem; color: #9CA3AF; font-size: 0.85rem;">
            <p>The app will download the Book-Crossing dataset (~5MB) on first run.<br>
            If download fails, synthetic data will be generated automatically.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # ── Dashboard (when initialized) ──────────────────────────────────────────
    # Note: hero renders only on the landing page, not here (avoids redundancy)

    books = st.session_state.books
    ratings = st.session_state.ratings

    # Stats row (pre-computed during load_data — no DataFrame hashing on re-render)
    stats = st.session_state._stats

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_stat_card(f"{stats['n_books']:,}", "Books in Catalog")
    with col2:
        render_stat_card(f"{stats['n_users']:,}", "Active Readers")
    with col3:
        render_stat_card(f"{stats['n_ratings']:,}", "Total Ratings")
    with col4:
        render_stat_card(f"{stats['avg_rating']:.1f}", "★ Avg Rating")

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
