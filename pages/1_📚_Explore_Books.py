"""Explore Books — Browse and search the book catalog."""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ui import apply_styling, render_book_card_detailed, sidebar_footer
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
ratings = st.session_state.ratings

# ── Header ───────────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="padding: 1rem 0;">
        <div style="font-family: 'Playfair Display', serif; font-size: 2.2rem; 
             font-weight: 600; color: {COLORS['text']};">📖  Explore Books</div>
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
    # Year range filter
    min_year = int(books[books["year"] > 0]["year"].min()) if not books[books["year"] > 0].empty else 1950
    max_year = int(books["year"].max()) if not books.empty else 2024
    year_range = st.slider(
        "Year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        label_visibility="collapsed",
    )

with col3:
    # Rating filter
    rating_filter = st.selectbox(
        "Min Rating",
        ["Any", "★ 3+", "★ 4+", "★ 5+", "★ 6+", "★ 7+", "★ 8+"],
        label_visibility="collapsed",
    )

with col4:
    # Sort by
    sort_by = st.selectbox(
        "Sort by",
        ["Popularity", "Rating (High→Low)", "Rating (Low→High)", "Title A→Z", "Year (New→Old)"],
        label_visibility="collapsed",
    )

# ── Apply Filters ────────────────────────────────────────────────────────────

filtered = books.copy()

# Text search
if search_query:
    mask = (
        filtered["title"].str.lower().str.contains(search_query.lower(), na=False)
        | filtered["author"].str.lower().str.contains(search_query.lower(), na=False)
    )
    filtered = filtered[mask]

# Year filter
filtered = filtered[
    (filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])
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
min_rating = rating_map[rating_filter]
if min_rating > 0:
    filtered = filtered[filtered["avg_rating"] >= min_rating]

# Sort
if sort_by == "Popularity":
    filtered = filtered.sort_values("rating_count", ascending=False)
elif sort_by == "Rating (High→Low)":
    filtered = filtered.sort_values("avg_rating", ascending=False)
elif sort_by == "Rating (Low→High)":
    filtered = filtered.sort_values("avg_rating", ascending=True)
elif sort_by == "Title A→Z":
    filtered = filtered.sort_values("title")
elif sort_by == "Year (New→Old)":
    filtered = filtered.sort_values("year", ascending=False)

# ── Results Count ────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="margin: 0.5rem 0; font-size: 0.9rem; color: {COLORS['text_secondary']};">
        Showing {min(len(filtered), 24):,} of {len(filtered):,} books
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Grid Display ─────────────────────────────────────────────────────────────

if filtered.empty:
    st.info("No books match your search criteria. Try adjusting the filters.")
else:
    # Pagination
    items_per_page = 12
    total_pages = max(1, (len(filtered) + items_per_page - 1) // items_per_page)
    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1,
        label_visibility="collapsed",
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
                render_book_card_detailed(
                    title=book["title"],
                    author=book.get("author", "Unknown"),
                    rating=book["avg_rating"],
                    rating_count=book["rating_count"],
                    year=book.get("year"),
                    publisher=book.get("publisher"),
                    genre=book.get("genre"),
                )
                st.markdown("<br>", unsafe_allow_html=True)

    # Page navigation
    if total_pages > 1:
        st.markdown(
            f"""
            <div style="text-align: center; color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                Page {page} of {total_pages}
            </div>
            """,
            unsafe_allow_html=True,
        )

sidebar_footer()
