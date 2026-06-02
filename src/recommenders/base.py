"""Base recommender class defining the interface."""

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class BaseRecommender(ABC):
    """Abstract base class for all recommendation models."""

    def __init__(self, books: pd.DataFrame, ratings: pd.DataFrame):
        self.books = books
        self.ratings = ratings
        self._fitted = False

    @abstractmethod
    def fit(self) -> None:
        """Fit the recommendation model."""
        ...

    @abstractmethod
    def recommend(
        self,
        n: int = 10,
        **kwargs,
    ) -> pd.DataFrame:
        """Return top-n book recommendations.

        Returns:
            DataFrame with columns from books plus an additional 'score' column.
        """
        ...

    def _get_book_by_title(self, title: str) -> Optional[pd.Series]:
        """Find a book by its title (case-insensitive partial match)."""
        mask = self.books["title"].str.lower().str.contains(title.lower(), na=False)
        matches = self.books[mask]
        if matches.empty:
            return None
        return matches.iloc[0]

    def _ensure_score_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ensure the result has a 'score' column."""
        if "score" not in df.columns:
            if "avg_rating" in df.columns:
                df = df.copy()
                df["score"] = df["avg_rating"]
            else:
                df = df.copy()
                df["score"] = 1.0
        return df

    def _get_top_n(self, df: pd.DataFrame, n: int) -> pd.DataFrame:
        """Sort by score descending and return top-n."""
        result = df.sort_values("score", ascending=False).head(n)
        result["score"] = result["score"].round(3)
        return result
