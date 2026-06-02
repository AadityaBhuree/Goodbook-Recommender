#!/usr/bin/env python3
"""Standalone script to download the Goodbooks-10k dataset.

Usage:
    python scripts/download_data.py

Downloads 10k books and 6M ratings from GitHub.
Falls back to generating synthetic data if download fails.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.loader import (
    download_goodbooks_dataset,
    generate_synthetic_data,
    load_goodbooks_books,
    load_goodbooks_ratings,
    resolve_book_ids,
    generate_users_from_ratings,
)
from src.config import RecommenderConfig
from src.data.loader import cache_processed_data
from src.preprocessing import preprocess_pipeline


def main() -> None:
    """Download or generate the dataset."""
    config = RecommenderConfig()

    print("=" * 60)
    print("  BookRecommender - Data Download Script")
    print("=" * 60)

    print("\n[Download] Downloading Goodbooks-10k dataset...")
    success = download_goodbooks_dataset()

    if success:
        print("\n[OK] Dataset downloaded!")
        print(f"   Files saved to: {Path('data').resolve()}")

        print("\n[Process] Loading and preprocessing data...")
        books = load_goodbooks_books()
        ratings = load_goodbooks_ratings()

        if books is not None and ratings is not None:
            ratings = resolve_book_ids(ratings, books)
            users = generate_users_from_ratings(ratings)
            books, users, ratings = preprocess_pipeline(books, users, ratings, config)
            cache_processed_data(books, users, ratings)
            print(
                f"[OK] Preprocessed and cached: {len(books)} books, "
                f"{len(ratings):,} ratings, {len(users):,} users"
            )
        else:
            print("\n[Warning] Failed to parse downloaded files. Using synthetic...")
            books, users, ratings = generate_synthetic_data(config)
            books, users, ratings = preprocess_pipeline(books, users, ratings, config)
            cache_processed_data(books, users, ratings)
            print(f"[OK] Synthetic dataset cached: {len(books)} books, {len(ratings):,} ratings")
    else:
        print("\n[Warning] Download failed. Generating synthetic dataset...")
        books, users, ratings = generate_synthetic_data(config)
        books, users, ratings = preprocess_pipeline(books, users, ratings, config)
        cache_processed_data(books, users, ratings)
        print(f"[OK] Synthetic dataset cached: {len(books)} books, {len(ratings):,} ratings")

    print("\n" + "=" * 60)
    print("  Ready! Run the app with:  streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
