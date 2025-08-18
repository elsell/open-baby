"""Common service module for backend operations."""

from abc import ABC
from sqlalchemy.orm import Session


class CommonService(ABC):
    """Abstract base class for common service operations."""

    def __init__(self, db: Session):
        """
        Initialize the service with a database session.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self._db = db
