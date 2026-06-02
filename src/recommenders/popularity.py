"""Popularity-based book recommender.

Recommends books based on their overall popularity (rating count and average rating).
"""

from typing import Optional

import pandas as pd

from src.recommenders.base import BaseRecommender


class PopularityRecommender(BaseRecommender):
    """Recommends books based on popularity metrics.

    Uses a weighted score combining average rating and number of ratings.
    Score = (avg_rating * rating_count) / (rating_count + C)
    where C is a damping factor to avoid books with few ratings dominating.
    """

    def __init__(
        self,
        books: pd.DataFrame,
        ratings: pd.DataFrame,
        damping_factor: float = 50.0,
        min_ratings: int = 10,
    ):
        super().__init__(books, ratings)
        self.damping_factor = damping_factor
        self.min_ratings = min_ratings
        self._scored_books: Optional[pd.DataFrame] = None

    def fit(self) -> None:
        """Compute popularity scores for all books."""
        df = self.books.copy()

        # Weighted rating (Bayesian average-inspired)
        c = self.damping_factor
        df["score"] = (
            (df["avg_rating"] * df["rating_count"] + c * df["avg_rating"].mean())
            / (df["rating_count"] + c)
        )

        # Apply minimum rating threshold
        df.loc[df["rating_count"] < self.min_ratings, "score"] = 0

        df["score"] = df["score"].fillna(0)
        self._scored_books = df
        self._fitted = True

    def recommend(
        self,
        n: int = 10,
        genre: Optional[str] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """Return top-n popular books, optionally filtered by genre."""
        if not self._fitted or self._scored_books is None:
            self.fit()

        df = self._scored_books.copy()

        if genre and genre != "All":
            if "genre" in df.columns:
                df = df[df["genre"].str.lower() == genre.lower()]
            else:
                # Try to infer genre from book features
                pass

        df = df[df["score"] > 0]
        return self._get_top_n(df, n)

