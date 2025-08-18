"""This module configures the database connection.

Example Usage:

```python
    from growlinkcommon.persistence.sql.database import SessionLocal, SessionLocalReadonly

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_db_readonly():
        db = SessionLocalReadonly()
        try:
            yield db
        finally:
            db.close()
```
"""

import logging
from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import config

log = logging.getLogger(__name__)

Base = declarative_base()


class DatabaseConfig:
    """Handles the configuration of the database connection.

    This class initializes the database connection using an environment variable
    and provides methods to get a SQLAlchemy engine and sessionmaker.
    """

    def __init__(self):
        """Initializes DatabaseConfig with the database URL from an environment variable.

        Raises:
            DatabaseCreationException: If the required environment variable for the database URL is not set.
        """
        database_url = config.database_url

        log.info(f"Creating database connection: {database_url}")

        self.database_url = database_url

    def get_engine(self):
        """Creates and returns a SQLAlchemy engine.

        Returns:
            A SQLAlchemy engine.

        Raises:
            DatabaseCreationException: If the engine cannot be created.
        """
        try:
            engine = create_engine(self.database_url)
            return engine
        except Exception as e:
            log.error(f"Failed to create engine: {e}")
            raise RuntimeError("Failed to create database engine.") from e

    def get_session(self) -> Tuple[sessionmaker, sessionmaker]:
        """Creates and returns both a regular and read-only SQLAlchemy sessionmaker.

        Returns:
            Tuple[sessionmaker, sessionmaker]: (sessionmaker, readonly-sessionmaker)
        """
        engine = self.get_engine()

        # Create a "Sub-engine" that is a shallow-copy of the original engine but with a
        # different isolation level.
        #   Note: `READ COMMITTED` may be too low a level of isolation. `REPEATABLE READ` might be considered,
        #   but it should be noted that performance could be degraded due to increased locking.
        readonly_engine = engine.execution_options(isolation_level="READ COMMITTED")

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        SessionLocalReadonly = sessionmaker(
            autocommit=False, autoflush=False, bind=readonly_engine
        )

        return SessionLocal, SessionLocalReadonly


# Usage
db_config = DatabaseConfig()
SessionLocal, SessionLocalReadonly = db_config.get_session()
