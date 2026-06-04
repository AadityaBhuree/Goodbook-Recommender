"""Explore Books — Browse and search the book catalog."""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ui import apply_styling, sidebar_footer, stars, format_number
from src.config import COLORS

st.set_page_config(page_title="Explore Books", page_icon="📖", layout="wide")

apply_styling()

# Check if initialized
if not st.session_state.get("initialized", False):
    st.warning("⚠️ Please initialize the system first on the Home page.")
    st.page_link("app.py", label="🏠  Go to Home", use_container_width=True)
    sidebar_footer()
    st.stop()

books = st.session_state.books

# ── Cache computed values once ───────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def get_year_range(_books: pd.DataFrame):
    """Get the min and max year from the books dataset."""
    books_with_year = _books[_books["year"] > 0]
    if books_with_year.empty:
        return 1950, 2024
    return int(books_with_year["year"].min()), int(_books["year"].max())

min_year, max_year = get_year_range(books)

# ── Header ───────────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="padding: 1rem 0;">
        <div style="font-size: 1.8rem; font-weight: 600; color: {COLORS['primary']};">📖 Explore Books</div>
        <div style="color: {COLORS['text_secondary']}; font-size: 1rem;">
            Browse our catalog of {len(books):,} books. Search, filter, and discover your next read.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Filters ──────────────────────────────────────────────────────────────────

st.markdown("### 🔍 Search & Filter")

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

with col1:
    search_query = st.text_input(
        "Search by title",
        placeholder="e.g., Harry Potter, The Great Gatsby...",
        label_visibility="collapsed",
    )

with col2:
    year_range = st.slider(
        "Year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        label_visibility="collapsed",
    )

with col3:
    rating_filter = st.selectbox(
        "Min Rating",
        ["Any", "★ 3+", "★ 4+", "★ 5+", "★ 6+", "★ 7+", "★ 8+"],
        label_visibility="collapsed",
    )

with col4:
    sort_by = st.selectbox(
        "Sort by",
        ["Popularity", "Rating (High→Low)", "Rating (Low→High)", "Title A→Z", "Year (New→Old)"],
        label_visibility="collapsed",
    )

# ── Apply Filters (cached) ──────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def apply_filters(_books: pd.DataFrame, query: str, y_range: tuple, rating: str, sort: str):
    """Apply all filters and sorting to the books dataframe."""
    df = _books.copy()

    # Text search
    if query:
        mask = (
            df["title"].str.lower().str.contains(query.lower(), na=False)
            | df["author"].str.lower().str.contains(query.lower(), na=False)
        )
        df = df[mask]

    # Year filter
    df = df[
        (df["year"] >= y_range[0]) & (df["year"] <= y_range[1])
    ]

    # Rating filter
    rating_map = {
        "Any": 0,
        "★ 3+": 3,
        "★ 4+": 4,
        "★ 5+": 5,
        "★ 6+": 6,
        "★ 7+": 7,
        "★ 8+": 8,
    }
    min_rating = rating_map[rating]
    if min_rating > 0:
        df = df[df["avg_rating"] >= min_rating]

    # Sort
    if sort == "Popularity":
        df = df.sort_values("rating_count", ascending=False)
    elif sort == "Rating (High→Low)":
        df = df.sort_values("avg_rating", ascending=False)
    elif sort == "Rating (Low→High)":
        df = df.sort_values("avg_rating", ascending=True)
    elif sort == "Title A→Z":
        df = df.sort_values("title")
    elif sort == "Year (New→Old)":
        df = df.sort_values("year", ascending=False)

    return df

filtered = apply_filters(books, search_query, year_range, rating_filter, sort_by)

# Reset pagination when filters change (detect via a filter fingerprint)
filter_fingerprint = (search_query, year_range, rating_filter, sort_by)
if st.session_state.get("_explore_filter_fp") != filter_fingerprint:
    st.session_state._explore_page = 0
    st.session_state._explore_filter_fp = filter_fingerprint

# ── Results Count ────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="margin: 0.5rem 0; font-size: 0.9rem; color: {COLORS['text_secondary']};">
        Showing {min(len(filtered), 12):,} of {len(filtered):,} books
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Grid Display ─────────────────────────────────────────────────────────────

if filtered.empty:
    st.info("No books match your search criteria. Try adjusting the filters.")
else:
    items_per_page = 12
    total_pages = max(1, (len(filtered) + items_per_page - 1) // items_per_page)

    # Use selectbox for smoother page navigation instead of number_input
    page_options = [f"Page {i+1}" for i in range(total_pages)]
    if "_explore_page" not in st.session_state:
        st.session_state._explore_page = 0

    col_pager, col_info = st.columns([1, 2])
    with col_pager:
        selected_page = st.selectbox(
            "Page",
            options=page_options,
            index=min(st.session_state._explore_page, total_pages - 1),
            label_visibility="collapsed",
            key="_explore_page_select",
        )
        page = page_options.index(selected_page) + 1
        st.session_state._explore_page = page - 1
    with col_info:
        if total_pages > 1:
            st.markdown(
                f"""
                <div style="padding-top: 0.5rem; color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                    Page {page} of {total_pages}
                </div>
                """,
                unsafe_allow_html=True,
            )

    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_books = filtered.iloc[start_idx:end_idx]

    # Display in rows of 3
    rows = [page_books.iloc[i : i + 3] for i in range(0, len(page_books), 3)]
    for row in rows:
        cols = st.columns(3)
        for col_idx, (_, book) in enumerate(row.iterrows()):
            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div class="book-card" style="text-align: center; padding-bottom: 0.8rem;">
                        <div class="book-cover-placeholder" style="height: 120px; font-size: 2.5rem;">📖</div>
                        <div class="book-card-title" style="font-size: 0.9rem;">{book['title'][:50]}{"…" if len(str(book['title'])) > 50 else ""}</div>
                        <div class="book-card-author">by {book.get('author', 'Unknown')[:35]}{"…" if len(str(book.get('author', ''))) > 35 else ""}</div>
                        <div>
                            <span class="book-card-rating">{stars(book['avg_rating'])} {book['avg_rating']:.1f}</span>
                        </div>
                        <div class="book-card-meta">{format_number(int(book['rating_count']))} ratings{f" · {int(book['year'])}" if book.get('year') and book['year'] > 0 else ""}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

sidebar_footer()
