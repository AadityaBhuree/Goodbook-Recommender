"""UI components, styling, and helper functions for the Streamlit app."""

from typing import Optional

import pandas as pd
import streamlit as st

from src.config import APP_DESCRIPTION, APP_SUBTITLE, APP_TITLE, COLORS

# ── CSS Styling ──────────────────────────────────────────────────────────────


def get_custom_css() -> str:
    """Return the custom CSS for the app."""
    return f"""
    <style>
        /* Main app styling */
        .stApp {{
            background: linear-gradient(135deg, {COLORS["background"]} 0%, #FFF8E7 100%);
        }}

        /* Typography */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

        h1, h2, h3, h4 {{
            font-family: 'Playfair Display', serif !important;
            color: {COLORS["text"]} !important;
        }}

        /* Hero section */
        .hero-title {{
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 700;
            color: {COLORS["primary"]};
            margin-bottom: 0.5rem;
            line-height: 1.2;
        }}
        .hero-subtitle {{
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            color: {COLORS["text_secondary"]};
            font-weight: 400;
            margin-bottom: 1rem;
        }}
        .hero-description {{
            font-size: 1.1rem;
            color: {COLORS["text_secondary"]};
            max-width: 600px;
            line-height: 1.6;
        }}

        /* Book card */
        .book-card {{
            background: {COLORS["surface"]};
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            height: 100%;
            border: 1px solid rgba(139, 69, 19, 0.08);
        }}
        .book-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(139, 69, 19, 0.15);
        }}
        .book-card-title {{
            font-family: 'Playfair Display', serif;
            font-weight: 600;
            font-size: 1rem;
            color: {COLORS["text"]};
            margin-bottom: 0.3rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        .book-card-author {{
            font-size: 0.85rem;
            color: {COLORS["text_secondary"]};
            margin-bottom: 0.4rem;
        }}
        .book-card-meta {{
            font-size: 0.75rem;
            color: #999;
        }}
        .book-card-rating {{
            color: {COLORS["rating"]};
            font-weight: 600;
            font-size: 0.9rem;
        }}
        .book-card-year {{
            font-size: 0.75rem;
            color: #999;
        }}
        .book-cover-placeholder {{
            width: 100%;
            height: 160px;
            background: linear-gradient(135deg, #f5e6d3 0%, #e8d5c4 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            margin-bottom: 0.8rem;
            border: 1px solid #e0d0c0;
        }}

        /* Stats cards */
        .stat-card {{
            background: {COLORS["surface"]};
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-left: 4px solid {COLORS["primary"]};
        }}
        .stat-number {{
            font-size: 2.2rem;
            font-weight: 700;
            color: {COLORS["primary"]};
            font-family: 'Playfair Display', serif;
        }}
        .stat-label {{
            font-size: 0.85rem;
            color: {COLORS["text_secondary"]};
            margin-top: 0.3rem;
        }}

        /* Section header */
        .section-header {{
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 600;
            color: {COLORS["text"]};
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {COLORS["secondary"]};
        }}

        /* Rating stars */
        .rating-stars {{
            color: {COLORS["rating"]};
            letter-spacing: 2px;
        }}

        /* Recommendation card variant */
        .rec-card {{
            background: linear-gradient(135deg, {COLORS["surface"]}, #FFF8E7);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.5rem;
            border-left: 4px solid {COLORS["accent"]};
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
        }}
        .rec-rank {{
            font-family: 'Playfair Display', serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: {COLORS["secondary"]};
            min-width: 36px;
        }}
        .rec-title {{
            font-weight: 600;
            color: {COLORS["text"]};
        }}
        .rec-score {{
            font-size: 0.8rem;
            color: {COLORS["text_secondary"]};
        }}

        /* Button styling */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(139, 69, 19, 0.2);
        }}

        /* Sidebar styling */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #FAF3E0 0%, #F5E6D3 100%);
        }}
        section[data-testid="stSidebar"] .stButton > button {{
            width: 100%;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {COLORS["surface"]} !important;
            border-top: 2px solid {COLORS["primary"]} !important;
        }}

        /* Progress/Score bar */
        .score-bar {{
            height: 4px;
            background: linear-gradient(90deg, {COLORS["secondary"]}, {COLORS["primary"]});
            border-radius: 2px;
            margin-top: 4px;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            color: #999;
            font-size: 0.8rem;
            padding: 2rem 0;
            border-top: 1px solid #eee;
            margin-top: 3rem;
        }}

        /* Spinner */
        .stSpinner > div > div {{
            border-color: {COLORS["primary"]} transparent transparent transparent !important;
        }}
    </style>
    """


# ── Utility Functions ────────────────────────────────────────────────────────


def stars(rating: float, max_stars: int = 5) -> str:
    """Return a star rating string.

    Handles both 1-5 and 1-10 rating scales automatically.
    """
    if rating > 5:
        rating = rating / 2.0  # Normalize 1-10 scale to 0-5
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = max_stars - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def format_number(num: int) -> str:
    """Format a number with K/M suffix."""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


# ── Render Functions ─────────────────────────────────────────────────────────


def render_hero() -> None:
    """Render the hero section on the home page."""
    st.markdown(
        f"""
        <div style="padding: 2rem 0;">
            <div class="hero-title">{APP_TITLE}</div>
            <div class="hero-subtitle">{APP_SUBTITLE}</div>
            <div class="hero-description">{APP_DESCRIPTION}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(number: str, label: str) -> None:
    """Render a single stat card."""
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{number}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_book_card(
    title: str,
    author: str,
    rating: float,
    rating_count: int,
    year: Optional[int] = None,
    score: Optional[float] = None,
    rank: Optional[int] = None,
    genre: Optional[str] = None,
) -> None:
    """Render a single book card."""
    year_str = f" · {int(year)}" if year and year > 0 else ""
    score_str = f" — Score: {score:.3f}" if score is not None else ""
    rank_str = f"#{rank} " if rank is not None else ""

    st.markdown(
        f"""
        <div class="book-card">
            <div class="book-cover-placeholder">📖</div>
            <div class="book-card-title">{rank_str}{title}</div>
            <div class="book-card-author">by {author}</div>
            <div>
                <span class="book-card-rating">{stars(rating)} {rating:.1f}</span>
                <span class="book-card-meta">({format_number(rating_count)} ratings{year_str})</span>
            </div>
            <div class="rec-score">{score_str}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_book_card_detailed(
    title: str,
    author: str,
    rating: float,
    rating_count: int,
    year: Optional[int] = None,
    publisher: Optional[str] = None,
    genre: Optional[str] = None,
    description: Optional[str] = None,
) -> None:
    """Render a detailed book card for the explore page."""
    year_str = f" · {int(year)}" if year and year > 0 else ""
    pub_str = f" · {publisher}" if publisher and publisher != "Unknown Publisher" else ""
    genre_str = f"<span style='background: {COLORS['secondary']}20; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; color: {COLORS['text_secondary']};'>{genre}</span>" if genre else ""

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(
            """
            <div style="
                width: 100%;
                aspect-ratio: 2/3;
                background: linear-gradient(135deg, #f5e6d3 0%, #e8d5c4 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
                border: 1px solid #e0d0c0;
            ">📚</div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div>
                <div style="font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 600; color: {COLORS['text']};">{title}</div>
                <div style="font-size: 0.95rem; color: {COLORS['text_secondary']}; margin: 0.3rem 0;">by <strong>{author}</strong></div>
                <div style="margin: 0.3rem 0;">
                    <span class="book-card-rating">{stars(rating)} {rating:.1f}</span>
                    <span style="font-size: 0.8rem; color: #999;">({format_number(rating_count)} ratings{year_str}{pub_str})</span>
                </div>
                <div style="margin: 0.3rem 0;">{genre_str}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_recommendation_row(rank: int, title: str, author: str, score: float, rating: float) -> None:
    """Render a single recommendation row."""
    # Normalize score to a 0-100 percentage for the score bar.
    # Scores typically fall in 0-1 range for similarity measures.
    # We use a soft scale: clamp to 0-1 then multiply by 100.
    score_pct = max(0.0, min(score, 1.0)) * 100.0
    st.markdown(
        f"""
        <div class="rec-card" style="display: flex; align-items: center; gap: 1rem;">
            <div class="rec-rank">#{rank}</div>
            <div style="flex: 1;">
                <div class="rec-title">{title}</div>
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">by {author}</div>
                <div>
                    <span style="color: {COLORS['rating']};">{stars(rating)} {rating:.1f}</span>
                    <span class="rec-score"> · Score: {score:.3f}</span>
                </div>
                <div class="score-bar" style="width: {score_pct:.0f}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_styling() -> None:
    """Apply custom CSS to the Streamlit app."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def sidebar_footer() -> None:
    """Render the sidebar footer."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; font-size: 0.75rem; color: #999;">
            <p>Built with ❤️ using Streamlit & scikit-learn</p>
            <p>{APP_TITLE} v1.0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
