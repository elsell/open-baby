"""Common SQL persistence dependencies for Open Baby.

This module provides both a regular and a read-only connection to the database for FastAPI applications.
The `get_db` and `get_db_read_only` functions are dependencies that can be used in FastAPI routes.

Example:
    ```python
    from fastapi import Depends
    from persistence.dependencies import get_db, get_db_read_only

    @app.get("/items/")
    async def read_items(db: Session = Depends(get_db_read_only)):
        items = db.query(Item).all()
        return items

    @app.post("/items/")
    async def create_item(item: Item, db: Session = Depends(get_db)):
        db.add(item)
        db.commit()
        return item
    ```
"""

import logging
from typing import Generator


from sqlalchemy.orm import Session

from persistence.database import SessionLocal, SessionLocalReadonly

log = logging.getLogger(__name__)


def get_db() -> Generator[Session, None, None]:
    """Get database session.

    Closes session on error and when request finished.

    Yields:
        db: sqlalchemy orm database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        log.debug("Closing database session")
        db.close()


def get_db_read_only() -> Generator[Session, None, None]:
    """Get a readonly database session.

    Closes session on error and when request finished.

    Yields:
        db: sqlalchemy orm database session
    """
    db = SessionLocalReadonly()
    try:
        yield db
    finally:
        log.debug("Closing readonly database session")
        db.close()
