"""Content-based book recommender.

Recommends books similar to a given book based on metadata features
(genre, author, etc.). Uses TF-IDF and cosine similarity.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.recommenders.base import BaseRecommender

logger = logging.getLogger(__name__)


class ContentBasedRecommender(BaseRecommender):
    """Recommends books similar to a given book using content features."""

    def __init__(
        self,
        books: pd.DataFrame,
        ratings: pd.DataFrame,
        top_k: int = 20,
    ):
        super().__init__(books, ratings)
        self.top_k = top_k
        self._similarity_matrix: Optional[np.ndarray] = None
        self._feature_matrix: Optional[np.ndarray] = None
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._isbn_to_idx: Optional[dict] = None
        self._idx_to_isbn: Optional[dict] = None

    def _build_content_features(self) -> pd.Series:
        """Build text features from book metadata for similarity computation."""
        df = self.books.copy()

        # Fill missing values
        features = pd.DataFrame()
        features["author"] = df["author"].fillna("").str.lower().str.replace(r"\s+", " ", regex=True)
        features["publisher"] = df["publisher"].fillna("").str.lower().str.replace(r"\s+", " ", regex=True)
        features["genre"] = df.get("genre", pd.Series(["general"] * len(df))).fillna("general").str.lower()

        # Combine features into a single text field
        combined = (
            features["author"] + " " +
            features["publisher"] + " " +
            features["genre"]
        )

        return combined

    def fit(self) -> None:
        """Build the TF-IDF matrix and compute pairwise similarities."""
        content_features = self._build_content_features()

        # Create TF-IDF features
        self._vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self._feature_matrix = self._vectorizer.fit_transform(content_features)

        # Compute cosine similarity matrix
        logger.info("Computing similarity matrix...")
        self._similarity_matrix = cosine_similarity(self._feature_matrix)

        # Build index mappings
        self._isbn_to_idx = {
            isbn: i for i, isbn in enumerate(self.books["isbn"])
        }
        self._idx_to_isbn = {
            i: isbn for i, isbn in enumerate(self.books["isbn"])
        }

        self._fitted = True
        logger.info(f"Content-based model fitted on {len(self.books)} books.")

    def recommend(
        self,
        n: int = 10,
        book_isbn: Optional[str] = None,
        book_title: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """Recommend books similar to the given book.

        Args:
            n: Number of recommendations.
            book_isbn: ISBN of the seed book.
            book_title: Title of the seed book (used if book_isbn not provided).

        Returns:
            DataFrame of recommended books with similarity scores.
        """
        if not self._fitted:
            self.fit()

        # Find the seed book
        if book_isbn is None and book_title is not None:
            book = self._get_book_by_title(book_title)
            if book is None:
                return pd.DataFrame()
            book_isbn = book["isbn"]

        if book_isbn is None or book_isbn not in self._isbn_to_idx:
            logger.warning(f"Book ISBN '{book_isbn}' not found in index.")
            return pd.DataFrame()

        idx = self._isbn_to_idx[book_isbn]
        sim_scores = list(enumerate(self._similarity_matrix[idx]))

        # Sort by similarity (excluding self)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1 : n + 1]

        book_indices = [i[0] for i in sim_scores]
        scores = [i[1] for i in sim_scores]

        result = self.books.iloc[book_indices].copy()
        result["score"] = scores

        return result

