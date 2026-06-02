"""Data preprocessing pipeline for the book recommendation system."""

import logging
from typing import Tuple

import numpy as np
import pandas as pd

from src.config import RecommenderConfig

logger = logging.getLogger(__name__)


def clean_books(books: pd.DataFrame, config: RecommenderConfig) -> pd.DataFrame:
    """Clean and normalize the books dataframe."""
    if books is None or books.empty:
        return books

    df = books.copy()

    # Drop duplicate ISBNs
    df = df.drop_duplicates(subset=["isbn"])

    # Clean title
    if "title" in df.columns:
        df["title"] = df["title"].str.strip().str.replace(r"\s+", " ", regex=True)
        df = df[df["title"].notna() & (df["title"] != "")]

    # Clean author
    if "author" in df.columns:
        df["author"] = df["author"].fillna("Unknown Author").str.strip()
        df["author"] = df["author"].replace("", "Unknown Author")

    # Clean year
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        # Filter reasonable years
        df.loc[df["year"] < 1800, "year"] = np.nan
        df.loc[df["year"] > 2025, "year"] = np.nan
        df["year"] = df["year"].fillna(0).astype(int)

    # Clean publisher
    if "publisher" in df.columns:
        df["publisher"] = df["publisher"].fillna("Unknown Publisher").str.strip()
        df["publisher"] = df["publisher"].replace("", "Unknown Publisher")

    # Ensure ISBN is string
    df["isbn"] = df["isbn"].astype(str).str.strip()

    # Genre column is only present in synthetic data (with actual genre labels)
    # Real datasets like Goodbooks-10k don't have it — UI handles this gracefully

    return df


def clean_users(users: pd.DataFrame, config: RecommenderConfig) -> pd.DataFrame:
    """Clean and normalize the users dataframe."""
    if users is None or users.empty:
        return users

    df = users.copy()

    # Clean age - filter unrealistic values
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df.loc[(df["age"] < 5) | (df["age"] > 120), "age"] = np.nan
        df["age"] = df["age"].fillna(df["age"].median())

    # Clean location
    if "location" in df.columns:
        df["location"] = df["location"].fillna("Unknown").str.strip()

    return df


def clean_ratings(ratings: pd.DataFrame, config: RecommenderConfig) -> pd.DataFrame:
    """Clean and normalize the ratings dataframe."""
    if ratings is None or ratings.empty:
        return ratings

    df = ratings.copy()

    # Ensure correct types
    df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce").astype("Int64")
    df["isbn"] = df["isbn"].astype(str).str.strip()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # Drop invalid ratings
    df = df.dropna(subset=["user_id", "isbn", "rating"])
    df = df[df["rating"] > 0]  # Remove implicit ratings (0 = implicit in Book-Crossing)

    # Normalize ratings to 1-10 scale if they're 1-10
    if df["rating"].max() <= 10:
        pass  # Already in correct range

    return df


def filter_by_frequency(
    ratings: pd.DataFrame,
    books: pd.DataFrame,
    users: pd.DataFrame | None,
    config: RecommenderConfig,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame | None]:
    """Filter out books and users with too few ratings."""
    df = ratings.copy()

    # Filter books with minimum ratings
    book_rating_counts = df.groupby("isbn").size()
    valid_books = book_rating_counts[book_rating_counts >= config.min_ratings_per_book].index
    df = df[df["isbn"].isin(valid_books)]

    # Filter users with minimum ratings
    user_rating_counts = df.groupby("user_id").size()
    valid_users = user_rating_counts[user_rating_counts >= config.min_ratings_per_user].index
    df = df[df["user_id"].isin(valid_users)]

    # Filter books to only those with ratings
    books_filtered = books[books["isbn"].isin(df["isbn"].unique())].copy()

    # Filter users if provided
    users_filtered = users
    if users is not None and not users.empty:
        users_filtered = users[users["user_id"].isin(df["user_id"].unique())].copy()

    logger.info(
        f"After filtering: {len(books_filtered)} books, "
        f"{len(df)} ratings from {df['user_id'].nunique()} users."
    )
    return df, books_filtered, users_filtered


def compute_book_stats(
    ratings: pd.DataFrame,
    books: pd.DataFrame,
) -> pd.DataFrame:
    """Compute average rating and rating count for each book.

    If books already has avg_rating / rating_count (e.g. Goodbooks-10k),
    use those; otherwise compute from the ratings dataframe.
    """
    # Check if we already have the stats (Goodbooks-10k provides them)
    has_precomputed = "avg_rating" in books.columns and "rating_count" in books.columns

    if has_precomputed and books["avg_rating"].notna().sum() > 0:
        # Already have good data — just ensure clean values
        books = books.copy()
        books["avg_rating"] = pd.to_numeric(books["avg_rating"], errors="coerce").fillna(0).round(2)
        books["rating_count"] = pd.to_numeric(books["rating_count"], errors="coerce").fillna(0).astype(int)
        return books

    # Compute from ratings dataframe
    stats = (
        ratings.groupby("isbn")
        .agg(avg_rating=("rating", "mean"), rating_count=("rating", "count"))
        .reset_index()
    )
    stats["avg_rating"] = stats["avg_rating"].round(2)

    books = books.merge(stats, on="isbn", how="left")
    books["avg_rating"] = books["avg_rating"].fillna(0)
    books["rating_count"] = books["rating_count"].fillna(0).astype(int)

    return books


def preprocess_pipeline(
    books: pd.DataFrame,
    users: pd.DataFrame | None,
    ratings: pd.DataFrame,
    config: RecommenderConfig,
) -> Tuple[pd.DataFrame, pd.DataFrame | None, pd.DataFrame]:
    """Run the full preprocessing pipeline.

    Returns:
        Tuple of (cleaned_books, cleaned_users, cleaned_ratings)
    """
    logger.info("Starting preprocessing pipeline...")

    books = clean_books(books, config)
    if users is not None and not users.empty:
        users = clean_users(users, config)
    ratings = clean_ratings(ratings, config)

    ratings, books, users = filter_by_frequency(ratings, books, users, config)

    books = compute_book_stats(ratings, books)

    logger.info(
        f"Preprocessing complete: {len(books)} books, "
        f"{len(ratings)} ratings, "
        f"{ratings['user_id'].nunique() if not ratings.empty else 0} users."
    )
    return books, users, ratings
