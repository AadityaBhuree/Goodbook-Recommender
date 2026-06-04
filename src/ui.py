"""UI components, styling, and helper functions for the Streamlit app."""

from typing import Optional

import pandas as pd
import streamlit as st

from src.config import APP_DESCRIPTION, APP_SUBTITLE, APP_TITLE, COLORS, set_theme

# ── CSS Styling ──────────────────────────────────────────────────────────────


def get_custom_css() -> str:
    """Return the custom CSS for the app."""
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Page transition ─────────────────────────────────────── */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .main > div {{
            animation: fadeIn 0.35s ease-out;
        }}

        /* ── Base typography ─────────────────────────────────────── */
        html {{ scroll-behavior: smooth; }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: {COLORS["text"]} !important;
            letter-spacing: -0.01em;
        }}

        p, li, div, span {{ color: {COLORS["text"]}; }}

        /* ── Active nav indicator ────────────────────────────────── */
        section[data-testid="stSidebar"] a[aria-current="page"] {{
            background: {COLORS["primary"]}10 !important;
            border-left: 3px solid {COLORS["primary"]} !important;
            border-radius: 0 8px 8px 0 !important;
            font-weight: 600 !important;
        }}

        /* ── Sidebar styling ─────────────────────────────────────── */
        section[data-testid="stSidebar"] {{
            background: {COLORS["surface"]};
            border-right: 1px solid #EDE6D9;
        }}
        section[data-testid="stSidebar"] .stPageLink {{ 
            margin: 0.15rem 0;
            transition: opacity 0.15s;
        }}
        section[data-testid="stSidebar"] .stPageLink:hover {{
            opacity: 0.8;
        }}
        section[data-testid="stSidebar"] .stPageLink a {{
            border-radius: 8px !important;
            transition: all 0.15s ease;
        }}
        section[data-testid="stSidebar"] .stButton > button {{
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.15s ease;
        }}

        /* ── Hero section ────────────────────────────────────────── */
        .hero-title {{
            font-size: 2.8rem;
            font-weight: 700;
            color: {COLORS["text"]};
            margin-bottom: 0.5rem;
            line-height: 1.15;
            letter-spacing: -0.02em;
        }}
        .hero-subtitle {{
            font-size: 1.2rem;
            color: {COLORS["secondary"]};
            font-weight: 500;
            margin-bottom: 0.8rem;
        }}
        .hero-description {{
            font-size: 1rem;
            color: {COLORS["text_secondary"]};
            max-width: 600px;
            line-height: 1.7;
            margin: 0 auto;
        }}

        /* ── Book card ───────────────────────────────────────────── */
        .book-card {{
            background: {COLORS["surface"]};
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            border: 1px solid #EDE6D9;
            position: relative;
            overflow: hidden;
        }}
        .book-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["secondary"]});
            opacity: 0;
            transition: opacity 0.25s ease;
        }}
        .book-card:hover::after {{ opacity: 1; }}
        .book-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(45,95,110,0.1);
            border-color: #D4C9B8;
        }}
        .book-card-title {{
            font-weight: 600;
            font-size: 0.95rem;
            color: {COLORS["text"]};
            margin-bottom: 0.25rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            line-height: 1.4;
        }}
        .book-card-author {{
            font-size: 0.8rem;
            color: {COLORS["text_secondary"]};
            margin-bottom: 0.3rem;
        }}
        .book-card-meta {{
            font-size: 0.7rem;
            color: {COLORS["text_secondary"]};
        }}
        .book-card-rating {{
            color: {COLORS["rating"]};
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 0.5px;
        }}
        .book-cover-placeholder {{
            width: 100%;
            height: 140px;
            background: linear-gradient(135deg, #F5F0E8 0%, #F0F4EC 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            margin-bottom: 0.7rem;
            border: 1px solid #EDE6D9;
            transition: transform 0.3s ease;
        }}
        .book-card:hover .book-cover-placeholder {{
            transform: scale(1.02);
        }}

        /* ── Stats cards ─────────────────────────────────────────── */
        .stat-card {{
            background: {COLORS["surface"]};
            border-radius: 12px;
            padding: 1.4rem 1rem;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            border: 1px solid #EDE6D9;
            border-left: 3px solid {COLORS["primary"]};
            transition: all 0.2s ease;
        }}
        .stat-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            border-color: #D4C9B8;
        }}
        .stat-number {{
            font-size: 2rem;
            font-weight: 700;
            color: {COLORS["primary"]};
            letter-spacing: -0.02em;
        }}
        .stat-label {{
            font-size: 0.8rem;
            color: {COLORS["text_secondary"]};
            margin-top: 0.2rem;
            font-weight: 500;
        }}

        /* ── Section header ──────────────────────────────────────── */
        .section-header {{
            font-size: 1.3rem;
            font-weight: 600;
            color: {COLORS["text"]};
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 0.6rem;
            border-bottom: 2px solid #EDE6D9;
            position: relative;
        }}
        .section-header::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 60px;
            height: 2px;
            background: {COLORS["primary"]};
        }}

        /* ── Rating stars ────────────────────────────────────────── */
        .rating-stars {{
            color: {COLORS["rating"]};
            letter-spacing: 2px;
        }}

        /* ── Recommendation card ─────────────────────────────────── */
        .rec-card {{
            background: {COLORS["surface"]};
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.6rem;
            border-left: 3px solid {COLORS["accent"]};
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.2s ease;
            border: 1px solid #EDE6D9;
            border-left-width: 3px;
        }}
        .rec-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            border-color: #D4C9B8;
            border-left-color: {COLORS["accent"]};
        }}
        .rec-rank {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {COLORS["secondary"]};
            min-width: 36px;
        }}
        .rec-title {{
            font-weight: 600;
            color: {COLORS["text"]};
        }}
        .rec-score {{
            font-size: 0.78rem;
            color: {COLORS["text_secondary"]};
        }}

        /* ── Score bar ───────────────────────────────────────────── */
        .score-bar {{
            height: 4px;
            background: linear-gradient(90deg, {COLORS["secondary"]}, {COLORS["primary"]});
            border-radius: 2px;
            margin-top: 4px;
            transition: width 0.5s ease;
        }}

        /* ── Tabs ────────────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 1px solid #EDE6D9;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px 8px 0 0;
            padding: 0.5rem 1.2rem;
            font-weight: 500;
            color: {COLORS["text_secondary"]} !important;
            transition: all 0.15s ease;
        }}
        .stTabs [aria-selected="true"] {{
            background: {COLORS["surface"]} !important;
            color: {COLORS["primary"]} !important;
            border-top: 2px solid {COLORS["primary"]} !important;
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: {COLORS["text"]} !important;
        }}

        /* ── Buttons ─────────────────────────────────────────────── */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.15s ease;
            border: 1px solid #EDE6D9;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(45,95,110,0.12);
            border-color: {COLORS["primary"]};
        }}
        .stButton > button:active {{
            transform: translateY(0);
        }}

        /* ── Form elements ───────────────────────────────────────── */
        .stSelectbox, .stTextInput, .stSlider {{ 
            color: {COLORS["text"]} !important;
        }}
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{
            border-radius: 8px !important;
            border-color: #EDE6D9 !important;
            transition: border-color 0.15s ease;
        }}
        .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {{
            border-color: {COLORS["primary"]} !important;
            box-shadow: 0 0 0 2px {COLORS["primary"]}15 !important;
        }}

        /* ── Spinner ─────────────────────────────────────────────── */
        .stSpinner > div > div {{
            border-color: {COLORS["primary"]} transparent transparent transparent !important;
        }}

        /* ── Progress bar ────────────────────────────────────────── */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, {COLORS["secondary"]}, {COLORS["primary"]}) !important;
        }}

        /* ── Expander ────────────────────────────────────────────── */
        .stExpander {{
            border: 1px solid #EDE6D9 !important;
            border-radius: 8px !important;
        }}

        /* ── Info / Success / Warning boxes ──────────────────────── */
        .stAlert {{
            border-radius: 8px !important;
            border: 1px solid #EDE6D9 !important;
        }}

        /* ── Custom scrollbar ────────────────────────────────────── */
        ::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #D4C9B8;
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #C4B9A8;
        }}

        /* ── Footer ──────────────────────────────────────────────── */
        .footer {{
            text-align: center;
            color: {COLORS["text_secondary"]};
            font-size: 0.78rem;
            padding: 2rem 0;
            border-top: 1px solid #EDE6D9;
            margin-top: 3rem;
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
        <div style="padding: 2rem 0; text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 0.5rem;">📚</div>
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





def render_recommendation_row(rank: int, title: str, author: str, score: float, rating: float) -> None:
    """Render a single recommendation row."""
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


def get_dark_css() -> str:
    """Return dark mode CSS overrides."""
    return f"""
    <style id="dark-theme">
        .stApp {{
            background: {COLORS['background']} !important;
        }}
        section[data-testid="stSidebar"] {{
            background: {COLORS['surface']} !important;
            border-right-color: {COLORS['border']} !important;
        }}
        section[data-testid="stSidebar"] a[aria-current="page"] {{
            background: {COLORS['primary']}15 !important;
        }}
        .book-card, .stat-card, .rec-card, .stAlert, .stExpander {{
            border-color: {COLORS['border']} !important;
        }}
        .book-card:hover, .stat-card:hover, .rec-card:hover {{
            border-color: {COLORS['border_hover']} !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25) !important;
        }}
        .stat-card:hover, .rec-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }}
        .book-cover-placeholder {{
            border-color: {COLORS['border']} !important;
            background: linear-gradient(135deg, #2A2723 0%, #2D3028 100%) !important;
        }}
        .section-header {{
            border-bottom-color: {COLORS['border']} !important;
        }}
        .section-header::after {{
            background: {COLORS['primary']} !important;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            border-bottom-color: {COLORS['border']} !important;
        }}
        .stTabs [aria-selected="true"] {{
            background: {COLORS['surface']} !important;
        }}
        .footer {{
            border-top-color: {COLORS['border']} !important;
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['border']} !important;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['border_hover']} !important;
        }}
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {{
            border-color: {COLORS['border']} !important;
        }}
        .stButton > button {{
            border-color: {COLORS['border']} !important;
        }}
        .stAlert {{
            background: {COLORS['surface']} !important;
            color: {COLORS['text']} !important;
        }}
    </style>
    """


def apply_styling() -> None:
    """Apply custom CSS to the Streamlit app and sync theme from session state."""
    is_dark = st.session_state.get("_dark_mode", False)
    set_theme(is_dark)
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    if is_dark:
        st.markdown(get_dark_css(), unsafe_allow_html=True)


def sidebar_footer() -> None:
    """Render the sidebar footer."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"""
        <div style="text-align: center; font-size: 0.72rem; color: {COLORS['text_secondary']};">
            <p>Built with ❤️ using Streamlit &amp; scikit-learn</p>
            <p>{APP_TITLE} v1.0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
