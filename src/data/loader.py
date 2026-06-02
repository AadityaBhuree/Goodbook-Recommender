"""Data loading module with automatic download and synthetic fallback.

Primary dataset: Goodbooks-10k (10k books, 6M ratings)
GitHub: https://github.com/zygmuntz/goodbooks-10k
"""

import logging
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import requests

from src.config import (
    BOOKS_FILE,
    CACHE_DIR,
    DATA_DIR,
    PROCESSED_DATA_FILE,
    RATINGS_FILE,
    GOODBOOKS_BOOKS_URL,
    GOODBOOKS_RATINGS_URL,
    RecommenderConfig,
)

logger = logging.getLogger(__name__)


def ensure_directories() -> None:
    """Create necessary directories if they don't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, timeout: int = 60) -> bool:
    """Download a file from URL to destination path.

    Returns True if successful, False otherwise.
    """
    try:
        logger.info(f"Downloading {url}...")
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        logger.info(f"Saved to {dest} ({len(resp.content):,} bytes)")
        return True
    except Exception as e:
        logger.warning(f"Failed to download {url}: {e}")
        return False


def download_goodbooks_dataset() -> bool:
    """Download the Goodbooks-10k dataset.

    Returns True if all files were downloaded successfully.
    """
    ensure_directories()

    files = [
        (GOODBOOKS_BOOKS_URL, BOOKS_FILE),
        (GOODBOOKS_RATINGS_URL, RATINGS_FILE),
    ]

    all_ok = True
    for url, dest in files:
        if not dest.exists():
            if not download_file(url, dest):
                all_ok = False
                break
        else:
            logger.info(f"{dest.name} already exists ({dest.stat().st_size:,} bytes), skipping.")

    return all_ok


def load_goodbooks_books() -> Optional[pd.DataFrame]:
    """Load and normalize the Goodbooks-10k books CSV."""
    if not BOOKS_FILE.exists():
        logger.warning("Books file not found.")
        return None

    try:
        df = pd.read_csv(BOOKS_FILE, encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to read books CSV: {e}")
        return None

    # Map Goodbooks columns to our schema
    # Goodbooks schema: book_id, goodreads_book_id, best_book_id, work_id,
    #   books_count, isbn, isbn13, authors, original_publication_year,
    #   original_title, title, language_code, average_rating, ratings_count,
    #   work_ratings_count, work_text_reviews_count, ratings_1-5,
    #   image_url, small_image_url

    # Ensure ISBN is a string; generate one from book_id if missing
    df["isbn"] = df["isbn"].fillna("").astype(str)
    mask_no_isbn = df["isbn"].str.strip() == ""
    df.loc[mask_no_isbn, "isbn"] = df.loc[mask_no_isbn, "book_id"].apply(
        lambda x: f"GB{x:06d}X"
    )

    # Normalize column names
    # Note: Goodbooks-10k has no genre column; UI handles missing genres gracefully
    result = pd.DataFrame({
        "isbn": df["isbn"],
        "book_id": df["book_id"],
        "title": df["title"].fillna(df["original_title"].fillna("Unknown Title")),
        "author": df["authors"].fillna("Unknown Author"),
        "year": pd.to_numeric(df["original_publication_year"], errors="coerce"),
        "publisher": None,  # Goodbooks doesn't include publisher
        "avg_rating": pd.to_numeric(df["average_rating"], errors="coerce"),
        "rating_count": pd.to_numeric(df["ratings_count"], errors="coerce").fillna(0).astype(int),
        "image_url_small": df["small_image_url"].fillna(""),
        "image_url_medium": df["image_url"].fillna(""),
        "image_url_large": df["image_url"].fillna(""),
    })

    # Clean year
    result["year"] = result["year"].fillna(0).astype(int)
    result.loc[(result["year"] < 1800) | (result["year"] > 2025), "year"] = 0

    logger.info(f"Loaded {len(result)} books from Goodbooks-10k.")
    return result


def load_goodbooks_ratings() -> Optional[pd.DataFrame]:
    """Load and normalize the Goodbooks-10k ratings CSV."""
    if not RATINGS_FILE.exists():
        logger.warning("Ratings file not found.")
        return None

    try:
        # ratings.csv: user_id, book_id, rating (1-5 scale)
        df = pd.read_csv(RATINGS_FILE, encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to read ratings CSV: {e}")
        return None

    # Map to our schema — we'll convert to ISBN later when merging
    result = pd.DataFrame({
        "user_id": df["user_id"],
        "book_id": df["book_id"],
        "rating": df["rating"],  # Keep Goodbooks' native 1-5 scale
    })

    logger.info(f"Loaded {len(result):,} ratings from Goodbooks-10k.")
    return result


def resolve_book_ids(
    ratings: pd.DataFrame,
    books: pd.DataFrame,
) -> pd.DataFrame:
    """Map book_id in ratings to isbn from books dataframe."""
    id_map = books[["book_id", "isbn"]].drop_duplicates("book_id")
    ratings = ratings.merge(id_map, on="book_id", how="inner")
    ratings = ratings.drop(columns=["book_id"])
    return ratings


def generate_users_from_ratings(ratings: pd.DataFrame) -> pd.DataFrame:
    """Generate a synthetic user table from rating user_ids."""
    users = pd.DataFrame({
        "user_id": sorted(ratings["user_id"].unique()),
        "location": "Unknown",
        "age": np.nan,
    })
    return users


def generate_synthetic_data(config: RecommenderConfig) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate synthetic book, user, and rating data for demo purposes.

    Returns:
        Tuple of (books_df, users_df, ratings_df)
    """
    logger.info("Generating synthetic dataset for demo...")
    rng = np.random.default_rng(config.synthetic_seed)

    genres = [
        "Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery",
        "Romance", "Thriller", "Horror", "Biography", "History",
        "Self-Help", "Science", "Technology", "Philosophy", "Poetry",
        "Drama", "Comedy", "Adventure", "Children", "Young Adult",
    ]
    authors = [f"Author {i}" for i in range(1, 101)]
    publishers = [f"Publisher {i}" for i in range(1, 31)]

    years = rng.integers(1950, 2024, size=config.synthetic_num_books)
    prefixes = ["The", "A", "Dark", "Lost", "Last", "First", "Secret",
                 "Hidden", "Forgotten", "Eternal", "Silent", "Broken",
                 "Golden", "Crimson", "Sapphire"]
    suffixes = ["Kingdom", "World", "Dream", "Shadow", "Light",
                 "Heart", "Soul", "Crown", "Storm", "Fate", "River",
                 "Mountain", "Forest", "Ocean", "Star"]
    titles = [
        "Book {}: {} {}".format(
            i,
            " ".join(rng.choice(prefixes, size=2)),
            " ".join(rng.choice(suffixes, size=2)),
        )
        for i in range(1, config.synthetic_num_books + 1)
    ]

    books_df = pd.DataFrame({
        "isbn": [f"{i:010d}X" for i in range(1, config.synthetic_num_books + 1)],
        "book_id": list(range(1, config.synthetic_num_books + 1)),
        "title": titles,
        "author": rng.choice(authors, size=config.synthetic_num_books),
        "year": years,
        "publisher": rng.choice(publishers, size=config.synthetic_num_books),
        "genre": rng.choice(genres, size=config.synthetic_num_books),
        "avg_rating": rng.uniform(2.5, 5.0, size=config.synthetic_num_books),
        "rating_count": rng.integers(1, 200, size=config.synthetic_num_books),
        "image_url_small": [""] * config.synthetic_num_books,
        "image_url_medium": [""] * config.synthetic_num_books,
        "image_url_large": [""] * config.synthetic_num_books,
    })

    ages = rng.integers(18, 80, size=config.synthetic_num_users)
    locations = [
        "New York, USA", "London, UK", "Tokyo, Japan", "Paris, France",
        "Berlin, Germany", "Sydney, Australia", "Toronto, Canada",
        "Mumbai, India", "Sao Paulo, Brazil", "Seoul, South Korea",
    ]
    users_df = pd.DataFrame({
        "user_id": range(1, config.synthetic_num_users + 1),
        "location": rng.choice(locations, size=config.synthetic_num_users),
        "age": ages,
    })

    ratings_data = []
    for _ in range(config.synthetic_num_ratings):
        uid = rng.integers(1, config.synthetic_num_users + 1)
        bid = rng.integers(1, config.synthetic_num_books + 1)
        rating = rng.choice([1, 2, 3, 4, 5], p=[
            0.05, 0.10, 0.20, 0.40, 0.25,
        ])
        ratings_data.append({
            "user_id": uid,
            "isbn": f"{bid:010d}X",
            "rating": rating,
        })

    ratings_df = pd.DataFrame(ratings_data)
    ratings_df = ratings_df.drop_duplicates(subset=["user_id", "isbn"], keep="last")

    logger.info(
        f"Generated {len(books_df)} books, {len(users_df)} users, "
        f"{len(ratings_df)} ratings."
    )
    return books_df, users_df, ratings_df


def load_and_cache_data(config: RecommenderConfig) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load data from cache, download Goodbooks-10k, or generate synthetic.

    Returns:
        Tuple of (books_df, users_df, ratings_df)
    """
    ensure_directories()

    # 1) Try loading from processed cache
    if PROCESSED_DATA_FILE.exists():
        try:
            import pickle
            with open(PROCESSED_DATA_FILE, "rb") as f:
                data = pickle.load(f)
            logger.info("Loaded cached processed data.")
            return data["books"], data["users"], data["ratings"]
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")

    # 2) Try downloading real Goodbooks-10k dataset
    if download_goodbooks_dataset():
        books = load_goodbooks_books()
        ratings = load_goodbooks_ratings()

        if books is not None and ratings is not None:
            # Map book_id in ratings to isbn from books
            ratings = resolve_book_ids(ratings, books)
            users = generate_users_from_ratings(ratings)

            logger.info(
                f"Loaded Goodbooks-10k dataset: {len(books)} books, "
                f"{len(ratings):,} ratings, {len(users):,} users."
            )
            return books, users, ratings

    # 3) Fallback to synthetic data
    logger.info("Using synthetic data as fallback.")
    return generate_synthetic_data(config)


def cache_processed_data(
    books: pd.DataFrame,
    users: pd.DataFrame,
    ratings: pd.DataFrame,
) -> None:
    """Cache processed data to disk for faster loading."""
    import pickle
    ensure_directories()
    try:
        with open(PROCESSED_DATA_FILE, "wb") as f:
            pickle.dump({"books": books, "users": users, "ratings": ratings}, f)
        logger.info("Cached processed data to disk.")
    except Exception as e:
        logger.warning(f"Failed to cache data: {e}")
