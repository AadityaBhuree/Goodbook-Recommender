"""Collaborative filtering book recommender.

Uses K-Nearest Neighbors on the user-item rating matrix to find similar
users and recommend books they liked.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from src.recommenders.base import BaseRecommender

logger = logging.getLogger(__name__)


class CollaborativeRecommender(BaseRecommender):
    """Recommends books using collaborative filtering with KNN.

    Two modes:
    - User-based: Find users similar to the query user, recommend books they liked.
    - Item-based: Find books similar to books the user liked.
    """

    def __init__(
        self,
        books: pd.DataFrame,
        ratings: pd.DataFrame,
        n_neighbors: int = 20,
        min_similarity: float = 0.0,
        use_item_based: bool = False,
    ):
        super().__init__(books, ratings)
        self.n_neighbors = n_neighbors
        self.min_similarity = min_similarity
        self.use_item_based = use_item_based

        # State
        self._user_item_matrix: Optional[pd.DataFrame] = None
        self._item_user_matrix: Optional[pd.DataFrame] = None
        self._user_knn: Optional[NearestNeighbors] = None
        self._item_knn: Optional[NearestNeighbors] = None
        self._user_map: Optional[dict] = None
        self._reverse_user_map: Optional[dict] = None
        self._item_map: Optional[dict] = None
        self._reverse_item_map: Optional[dict] = None

    def _build_matrices(self) -> None:
        """Build the user-item rating matrix."""
        logger.info("Building user-item rating matrix...")

        # Create user-item matrix
        self._user_item_matrix = self.ratings.pivot(
            index="user_id",
            columns="isbn",
            values="rating",
        ).fillna(0)

        # Build mappings
        self._user_map = {
            uid: i for i, uid in enumerate(self._user_item_matrix.index)
        }
        self._reverse_user_map = {
            i: uid for uid, i in self._user_map.items()
        }
        self._item_map = {
            isbn: j for j, isbn in enumerate(self._user_item_matrix.columns)
        }
        self._reverse_item_map = {
            j: isbn for isbn, j in self._item_map.items()
        }

        # Item-user matrix (transpose)
        self._item_user_matrix = self._user_item_matrix.T

        logger.info(
            f"Matrix shape: {self._user_item_matrix.shape} "
            f"({len(self._user_map)} users, {len(self._item_map)} books)"
        )

    def _fit_knn(self) -> None:
        """Fit the KNN models."""
        logger.info("Fitting KNN models...")

        # User-based KNN
        user_sparse = csr_matrix(self._user_item_matrix.values)
        self._user_knn = NearestNeighbors(
            n_neighbors=min(self.n_neighbors, user_sparse.shape[0] - 1),
            metric="cosine",
            algorithm="brute",
        )
        self._user_knn.fit(user_sparse)

        # Item-based KNN
        item_sparse = csr_matrix(self._item_user_matrix.values)
        self._item_knn = NearestNeighbors(
            n_neighbors=min(self.n_neighbors, item_sparse.shape[0] - 1),
            metric="cosine",
            algorithm="brute",
        )
        self._item_knn.fit(item_sparse)

    def fit(self) -> None:
        """Build matrices and fit KNN models."""
        self._build_matrices()
        self._fit_knn()
        self._fitted = True
        logger.info("Collaborative filtering model fitted.")

    def recommend(
        self,
        n: int = 10,
        user_id: Optional[int] = None,
        book_isbn: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """Get recommendations for a user or based on a book.

        Args:
            n: Number of recommendations.
            user_id: Get recommendations for this user (user-based CF).
            book_isbn: Get recommendations similar to this book (item-based CF).

        Returns:
            DataFrame of recommended books with scores.
        """
        if not self._fitted:
            self.fit()

        if user_id is not None and not self.use_item_based:
            return self._recommend_for_user(user_id, n)
        elif book_isbn is not None or self.use_item_based:
            isbn = book_isbn or self.books["isbn"].iloc[0]
            return self._recommend_similar_books(isbn, n)
        else:
            # Default: recommend popular books the user might like
            df = self.books.copy()
            df["score"] = df["avg_rating"] * np.sqrt(df["rating_count"])
            return self._get_top_n(df, n)

    def _recommend_for_user(self, user_id: int, n: int) -> pd.DataFrame:
        """Recommend books for a specific user using user-based CF.

        Note: Currently unused by the UI (both tabs use item-based mode).
        Available for future user-based collaborative filtering features.
        """
        if user_id not in self._user_map:
            logger.warning(f"User {user_id} not found in training data.")
            # Fallback to popular books
            df = self.books.copy()
            df["score"] = df["avg_rating"] * np.sqrt(df["rating_count"])
            return self._get_top_n(df, n)

        user_idx = self._user_map[user_id]
        user_vector = self._user_item_matrix.iloc[user_idx].values.reshape(1, -1)

        # Find similar users
        distances, indices = self._user_knn.kneighbors(user_vector, n_neighbors=self.n_neighbors)

        # Get books the user hasn't rated but similar users liked
        user_rated = set(
            self.ratings[self.ratings["user_id"] == user_id]["isbn"].values
        )

        # Score books by weighted rating from similar users
        # Weights are (1 - cosine_distance) so closer users contribute more
        book_scores = {}
        for neighbor_idx, dist in zip(indices[0], distances[0]):
            neighbor_id = self._reverse_user_map[neighbor_idx]
            if neighbor_id == user_id:
                continue
            weight = 1.0 - dist  # Cosine similarity (1 - cosine distance)
            if weight <= self.min_similarity:
                continue
            neighbor_ratings = self.ratings[
                self.ratings["user_id"] == neighbor_id
            ]
            for _, row in neighbor_ratings.iterrows():
                isbn = row["isbn"]
                if isbn not in user_rated:
                    book_scores[isbn] = book_scores.get(isbn, 0) + row["rating"] * weight

        if not book_scores:
            # Fallback
            df = self.books.copy()
            df["score"] = df["avg_rating"] * np.sqrt(df["rating_count"])
            return self._get_top_n(df, n)

        # Get top-n books
        sorted_books = sorted(book_scores.items(), key=lambda x: x[1], reverse=True)[:n]
        top_isbns = [isbn for isbn, _ in sorted_books]
        top_scores = [score for _, score in sorted_books]

        result = self.books[self.books["isbn"].isin(top_isbns)].copy()
        # Preserve order
        result["_order"] = result["isbn"].map({isbn: i for i, isbn in enumerate(top_isbns)})
        result = result.sort_values("_order")
        result["score"] = result["isbn"].map({isbn: score for isbn, score in zip(top_isbns, top_scores)})
        result = result.drop(columns=["_order"])

        return result.head(n)

    def _recommend_similar_books(self, book_isbn: str, n: int) -> pd.DataFrame:
        """Find books similar to a given book using item-based CF."""
        if book_isbn not in self._item_map:
            logger.warning(f"Book {book_isbn} not found in item index.")
            return pd.DataFrame()

        item_idx = self._item_map[book_isbn]
        item_vector = self._item_user_matrix.iloc[item_idx].values.reshape(1, -1)

        distances, indices = self._item_knn.kneighbors(item_vector, n_neighbors=n + 1)

        similar_items = []
        for i, idx in enumerate(indices[0]):
            if self._reverse_item_map[idx] == book_isbn:
                continue
            similarity = 1 - distances[0][i]
            if similarity < self.min_similarity:
                continue
            similar_items.append((self._reverse_item_map[idx], similarity))

            if len(similar_items) >= n:
                break

        if not similar_items:
            return pd.DataFrame()

        top_isbns = [isbn for isbn, _ in similar_items]
        top_scores = [score for _, score in similar_items]

        result = self.books[self.books["isbn"].isin(top_isbns)].copy()
        result["_order"] = result["isbn"].map({isbn: i for i, isbn in enumerate(top_isbns)})
        result = result.sort_values("_order")
        result["score"] = result["isbn"].map(
            {isbn: score for isbn, score in zip(top_isbns, top_scores)}
        )
        result = result.drop(columns=["_order"])

        return result

