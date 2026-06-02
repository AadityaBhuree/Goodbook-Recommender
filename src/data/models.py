"""Data models for the book recommendation system."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Book:
    """Represents a book with its metadata."""

    isbn: str
    title: str
    author: str
    year: Optional[int] = None
    publisher: Optional[str] = None
    image_url_small: Optional[str] = None
    image_url_medium: Optional[str] = None
    image_url_large: Optional[str] = None
    avg_rating: float = 0.0
    rating_count: int = 0


@dataclass
class User:
    """Represents a user in the system."""

    user_id: int
    location: Optional[str] = None
    age: Optional[float] = None


@dataclass
class Rating:
    """Represents a rating given by a user to a book."""

    user_id: int
    isbn: str
    rating: int


@dataclass
class RecommendationResult:
    """Result of a recommendation query."""

    books: list = field(default_factory=list)
    method: str = ""
    explanation: str = ""
