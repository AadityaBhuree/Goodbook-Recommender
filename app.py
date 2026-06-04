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

from src.config import APP_TITLE, COLORS, PAGE_CONFIG
from src.ui import apply_styling, render_hero, render_stat_card, sidebar_footer, stars, format_number
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
    st.session_state._dark_mode = False


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
            <div style="font-size: 1.2rem; font-weight: 600; color: {COLORS['primary']};">{APP_TITLE}</div>
            <div style="font-size: 0.75rem; color: {COLORS['text_secondary']};">Book Recommendation System</div>
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

    # Theme toggle
    st.sidebar.markdown("---")
    dark_mode = st.sidebar.toggle(
        "🌙 Dark mode",
        value=st.session_state.get("_dark_mode", False),
        key="_dark_mode_toggle",
        help="Switch between light and dark theme",
    )
    if dark_mode != st.session_state.get("_dark_mode", False):
        st.session_state._dark_mode = dark_mode
        st.rerun()

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
            background: linear-gradient(135deg, {COLORS['surface']}, {COLORS['background']});
            border-radius: 16px;
            padding: 2.5rem 2rem;
            box-shadow: 0 2px 16px rgba(0,0,0,0.05);
            text-align: center;
            max-width: 520px;
            margin: 0 auto;
            border: 1px solid {COLORS['border']};
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🚀</div>
            <div style="font-size: 1.3rem; font-weight: 600; color: {COLORS['primary']}; margin-bottom: 0.75rem;">
                Ready to discover your next read?
            </div>
            <div style="color: {COLORS['text_secondary']}; margin-bottom: 1.5rem; line-height: 1.6; font-size: 0.95rem;">
                Load the dataset and initialize the recommendation engine to get started.
                Your first run will download the data automatically.
            </div>
            <div>
                <span style="display: inline-block; background: {COLORS['primary']}10; padding: 0.25rem 0.8rem; border-radius: 20px; font-size: 0.75rem; color: {COLORS['text_secondary']}; margin: 0.2rem;">📚 10K books</span>
                <span style="display: inline-block; background: {COLORS['primary']}10; padding: 0.25rem 0.8rem; border-radius: 20px; font-size: 0.75rem; color: {COLORS['text_secondary']}; margin: 0.2rem;">⭐ 6M ratings</span>
                <span style="display: inline-block; background: {COLORS['primary']}10; padding: 0.25rem 0.8rem; border-radius: 20px; font-size: 0.75rem; color: {COLORS['text_secondary']}; margin: 0.2rem;">🤖 3 engines</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀  Load Data & Initialize", use_container_width=True, type="primary"):
            load_data()
            st.rerun()

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 1.5rem; color: {COLORS['text_secondary']}; font-size: 0.82rem;">
            <p>Downloads the Goodbooks-10k dataset (~5MB). If download fails, synthetic data is generated automatically.</p>
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
                st.markdown(
                    f"""
                    <div class="book-card" style="text-align: center; padding: 1.2rem 0.8rem;">
                        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📖</div>
                        <div class="book-card-title" style="font-size: 0.85rem;">{book['title'][:45]}{"…" if len(str(book['title'])) > 45 else ""}</div>
                        <div style="margin-top: 0.3rem;">
                            <span class="book-card-rating">{stars(book['avg_rating'])} {book['avg_rating']:.1f}</span>
                        </div>
                        <div style="font-size: 0.7rem; color: {COLORS['text_secondary']}; margin-top: 0.2rem;">
                            {format_number(int(book['rating_count']))} ratings
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
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
