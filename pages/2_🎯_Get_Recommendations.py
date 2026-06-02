"""Get Recommendations — Personalized book recommendations."""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.ui import apply_styling, render_recommendation_row, sidebar_footer
from src.config import COLORS

st.set_page_config(page_title="Get Recommendations", page_icon="🎯", layout="wide")

apply_styling()

# Check if initialized
if not st.session_state.get("initialized", False):
    st.warning("⚠️ Please initialize the system first on the Home page.")
    st.page_link("app.py", label="🏠  Go to Home", use_container_width=True)
    sidebar_footer()
    st.stop()

books = st.session_state.books
ratings = st.session_state.ratings
popularity = st.session_state.popularity
content = st.session_state.content
collaborative = st.session_state.collaborative

# ── Header ───────────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="padding: 1rem 0;">
        <div style="font-family: 'Playfair Display', serif; font-size: 2.2rem; 
             font-weight: 600; color: {COLORS['text']};">🎯  Get Recommendations</div>
        <div style="color: {COLORS['text_secondary']}; font-size: 1rem;">
            Three powerful recommendation methods — each offers a unique way to discover books you'll love.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Method Description ──────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="display: flex; gap: 0.5rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
        <span style="background: {COLORS['primary']}15; padding: 0.3rem 0.8rem; border-radius: 20px; 
              font-size: 0.85rem; color: {COLORS['primary']}; border: 1px solid {COLORS['primary']}30;">
            🔥 Popularity-Based
        </span>
        <span style="background: {COLORS['accent']}15; padding: 0.3rem 0.8rem; border-radius: 20px; 
              font-size: 0.85rem; color: {COLORS['accent']}; border: 1px solid {COLORS['accent']}30;">
            📝 Content-Based
        </span>
        <span style="background: {COLORS['secondary']}15; padding: 0.3rem 0.8rem; border-radius: 20px; 
              font-size: 0.85rem; color: {COLORS['secondary']}; border: 1px solid {COLORS['secondary']}30;">
            👥 Collaborative Filtering
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tabs ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(["🔥 Popularity-Based", "📝 Content-Based", "👥 Collaborative Filtering"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: Popularity-Based
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text']};">🔥 Popular Books</div>
            <div style="font-size: 0.9rem; color: {COLORS['text_secondary']};">
                Discover the most popular books across all readers. These are the books everyone's talking about — 
                ranked by a weighted score of average rating and number of ratings.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        pop_n = st.slider(
            "Number of recommendations",
            min_value=5,
            max_value=30,
            value=10,
            key="pop_n",
        )
    with col2:
        # Check if genre column exists
        if "genre" in books.columns:
            genres = ["All"] + sorted(books["genre"].dropna().unique().tolist())
            pop_genre = st.selectbox("Genre filter", genres, key="pop_genre")
        else:
            pop_genre = "All"
            st.info("Genre filtering not available (dataset has no genre data).")

    if st.button("🎯 Get Popular Recommendations", key="pop_btn", use_container_width=True):
        with st.spinner("Finding popular books..."):
            genre = None if pop_genre == "All" else pop_genre
            try:
                results = popularity.recommend(n=pop_n, genre=genre)
                if results.empty:
                    st.warning("No results found for the selected genre.")
                else:
                    for i, (_, book) in enumerate(results.iterrows()):
                        render_recommendation_row(
                            rank=i + 1,
                            title=book["title"],
                            author=book.get("author", "Unknown"),
                            score=book["score"],
                            rating=book["avg_rating"],
                        )
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: Content-Based
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text']};">📝 Similar Books</div>
            <div style="font-size: 0.9rem; color: {COLORS['text_secondary']};">
                Find books similar to one you already love. Our algorithm analyzes book metadata 
                (author, publisher, genre) using TF-IDF and cosine similarity to find matches 
                with the same style and character.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Book selector
    book_titles = ["Select a book..."] + sorted(
        books["title"].dropna().unique().tolist()
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_title = st.selectbox(
            "Choose a book you like",
            options=book_titles,
            key="cb_book",
        )
    with col2:
        cb_n = st.slider(
            "Number of recommendations",
            min_value=5,
            max_value=20,
            value=8,
            key="cb_n",
        )

    if selected_title and selected_title != "Select a book...":
        # Show the selected book info
        seed_book = books[books["title"] == selected_title].iloc[0]

        st.markdown(
            f"""
            <div style="
                background: {COLORS['surface']};
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0 1rem 0;
                border-left: 4px solid {COLORS['accent']};
            ">
                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']};">You selected:</div>
                <div style="font-weight: 600; font-size: 1.1rem;">{seed_book['title']}</div>
                <div style="font-size: 0.9rem; color: {COLORS['text_secondary']};">
                    by {seed_book.get('author', 'Unknown')} 
                    ★ {seed_book['avg_rating']:.1f}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🎯 Find Similar Books", key="cb_btn", use_container_width=True):
            with st.spinner("Computing content similarity..."):
                try:
                    results = content.recommend(
                        n=cb_n,
                        book_isbn=seed_book["isbn"],
                    )
                    if results.empty:
                        st.info("No similar books found. Try a different selection.")
                    else:
                        for i, (_, book) in enumerate(results.iterrows()):
                            render_recommendation_row(
                                rank=i + 1,
                                title=book["title"],
                                author=book.get("author", "Unknown"),
                                score=book["score"],
                                rating=book["avg_rating"],
                            )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.info("👆 Select a book above to get content-based recommendations.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: Collaborative Filtering
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <div style="font-size: 1.1rem; font-weight: 600; color: {COLORS['text']};">👥 People Also Liked</div>
            <div style="font-size: 0.9rem; color: {COLORS['text_secondary']};">
                Collaborative filtering finds users with similar reading tastes and recommends 
                books they enjoyed. The more ratings you provide, the better the recommendations get.
                Uses K-Nearest Neighbors on the user-item rating matrix.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mode selection
    cf_mode = st.radio(
        "Recommendation mode",
        options=["Find similar books (Item-based)", "Readers also liked (Item-based)"],
        horizontal=True,
        key="cf_mode",
    )

    if cf_mode == "Find similar books (Item-based)":
        # Item-based: pick a book
        cf_book = st.selectbox(
            "Choose a book to find similar ones",
            options=book_titles,
            key="cf_book_select",
        )
        cf_n = st.slider(
            "Number of recommendations",
            min_value=5,
            max_value=20,
            value=8,
            key="cf_n_item",
        )

        if cf_book and cf_book != "Select a book..." and st.button("🎯 Get Recommendations", key="cf_item_btn", use_container_width=True):
            with st.spinner("Finding similar books via collaborative filtering..."):
                try:
                    book_isbn = books[books["title"] == cf_book].iloc[0]["isbn"]
                    results = collaborative.recommend(
                        n=cf_n,
                        book_isbn=book_isbn,
                    )
                    if results.empty:
                        st.info("No similar books found via collaborative filtering.")
                    else:
                        for i, (_, book) in enumerate(results.iterrows()):
                            render_recommendation_row(
                                rank=i + 1,
                                title=book["title"],
                                author=book.get("author", "Unknown"),
                                score=book["score"],
                                rating=book["avg_rating"],
                            )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    else:
        # Item-based: pick a book (simplified — same as item-based mode)
        st.markdown(
            f"""
            <div style="font-size: 0.9rem; color: {COLORS['text_secondary']}; margin-bottom: 0.5rem;">
                Pick a book you enjoy, and our collaborative filtering algorithm will find 
                other books that readers with similar tastes also loved.
            </div>
            """,
            unsafe_allow_html=True,
        )

        cf_user_book = st.selectbox(
            "Choose a book you like",
            options=book_titles,
            key="cf_user_book",
        )
        cf_n_user = st.slider(
            "Number of recommendations",
            min_value=5,
            max_value=20,
            value=8,
            key="cf_n_user",
        )

        if cf_user_book and cf_user_book != "Select a book...":
            if st.button("🎯 Get Recommendations", key="cf_user_btn", use_container_width=True):
                with st.spinner("Finding users with similar tastes..."):
                    try:
                        book_isbn = books[books["title"] == cf_user_book].iloc[0]["isbn"]
                        results = collaborative.recommend(
                            n=cf_n_user,
                            book_isbn=book_isbn,
                        )
                        if results.empty:
                            st.info("No recommendations found. Try a different book.")
                        else:
                            st.markdown(
                                f"""
                                <div style="font-size: 0.85rem; color: {COLORS['text_secondary']}; margin-bottom: 0.5rem;">
                                    Readers who liked <strong>{cf_user_book}</strong> also enjoyed:
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            for i, (_, book) in enumerate(results.iterrows()):
                                render_recommendation_row(
                                    rank=i + 1,
                                    title=book["title"],
                                    author=book.get("author", "Unknown"),
                                    score=book["score"],
                                    rating=book["avg_rating"],
                                )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        else:
            st.info("👆 Select a book above to get recommendations.")

sidebar_footer()
