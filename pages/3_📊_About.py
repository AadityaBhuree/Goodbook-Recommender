"""About — Project information and documentation."""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Remove unused Path import - it's used via sys.path manipulation above

from src.ui import apply_styling, sidebar_footer
from src.config import COLORS, APP_TITLE

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

apply_styling()

# ── Header ───────────────────────────────────────────────────────────────────

st.markdown(
    f"""
    <div style="padding: 1rem 0;">
        <div style="font-family: 'Playfair Display', serif; font-size: 2.2rem; 
             font-weight: 600; color: {COLORS['text']};">ℹ️  About {APP_TITLE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── About Section ────────────────────────────────────────────────────────────

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📚 What is BookRecommender?")

    st.markdown(
        f"""
        **{APP_TITLE}** is an intelligent book recommendation system that uses 
        machine learning algorithms to help you discover your next great read.
        
        Built with **Streamlit** and **scikit-learn**, the application combines 
        three powerful recommendation approaches to provide diverse, 
        personalized suggestions.
        """
    )

    st.markdown("### 🎯 Recommendation Methods")

    st.markdown(
        f"""
        **🔥 Popularity-Based**
        - Recommends books with the highest weighted score combining average rating and rating count
        - Uses a Bayesian average to prevent books with few ratings from dominating
        - Great for discovering trending and widely-loved books
        
        **📝 Content-Based Filtering**
        - Finds books similar to one you already enjoy
        - Uses TF-IDF vectorization and cosine similarity on book metadata (author, publisher, genre)
        - Perfect for finding more of what you like
        
        **👥 Collaborative Filtering**
        - Discovers books by finding patterns in user rating behavior
        - Uses K-Nearest Neighbors on the user-item rating matrix
        - "People who liked this also liked..."
        """
    )

    st.markdown("### 🗄️ Dataset")

    st.markdown(
        """
        The system uses the **Goodbooks-10k Dataset**, a collection of 
        10,000 books with 6 million ratings from 53,000+ users, curated 
        by Zygmunt Zając.
        
        If the dataset is unavailable, the system automatically generates a 
        synthetic dataset to demonstrate all features.
        """
    )

    st.markdown("### 🛠️ Tech Stack")

    tech_cols = st.columns(3)
    with tech_cols[0]:
        st.markdown(
            """
            **Frontend**
            - Streamlit
            - Custom CSS
            """
        )
    with tech_cols[1]:
        st.markdown(
            """
            **ML & Data**
            - scikit-learn
            - pandas / numpy
            - scipy
            """
        )
    with tech_cols[2]:
        st.markdown(
            """
            **Visualization**
            - matplotlib
            - seaborn
            """
        )

with col2:
    # Project info card
    st.markdown(
        f"""
        <div style="
            background: {COLORS['surface']};
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        ">
            <div style="font-family: 'Playfair Display', serif; font-size: 1.3rem; 
                 font-weight: 600; color: {COLORS['text']}; margin-bottom: 1rem;">
                Quick Info
            </div>
            <table style="width: 100%; font-size: 0.9rem;">
                <tr>
                    <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Version</td>
                    <td style="padding: 0.4rem 0; font-weight: 500;">1.0.0</td>
                </tr>
                <tr>
                    <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Framework</td>
                    <td style="padding: 0.4rem 0; font-weight: 500;">Streamlit</td>
                </tr>
                <tr>
                    <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">ML Engine</td>
                    <td style="padding: 0.4rem 0; font-weight: 500;">scikit-learn</td>
                </tr>
                <tr>
                    <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Methods</td>
                    <td style="padding: 0.4rem 0; font-weight: 500;">3 (Pop, Content, Collab)</td>
                </tr>
                <tr>
                    <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Data Source</td>
                    <td style="padding: 0.4rem 0; font-weight: 500;">Goodbooks-10k Dataset</td>
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Data statistics if initialized
    if st.session_state.get("initialized", False):
        books = st.session_state.books
        ratings = st.session_state.ratings

        st.markdown(
            f"""
            <div style="
                background: {COLORS['surface']};
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            ">
                <div style="font-family: 'Playfair Display', serif; font-size: 1.3rem; 
                     font-weight: 600; color: {COLORS['text']}; margin-bottom: 1rem;">
                    Current Data Stats
                </div>
                <table style="width: 100%; font-size: 0.9rem;">
                    <tr>
                        <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Books</td>
                        <td style="padding: 0.4rem 0; font-weight: 500;">{len(books):,}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Ratings</td>
                        <td style="padding: 0.4rem 0; font-weight: 500;">{len(ratings):,}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Users</td>
                        <td style="padding: 0.4rem 0; font-weight: 500;">{ratings['user_id'].nunique():,}</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.4rem 0; color: {COLORS['text_secondary']};">Avg Rating</td>
                        <td style="padding: 0.4rem 0; font-weight: 500;">{books['avg_rating'].mean():.2f}</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer ──────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #999; font-size: 0.85rem; padding: 1rem;">
        <p>
            Built as a reference implementation of recommendation system algorithms.
            <br>
            Inspired by ML-ProjectKart (#31: Book Recommendation Systems).
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_footer()
