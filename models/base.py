"""SQLAlchemy Declarative Base – wird von allen Modellen importiert."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Basisklasse für alle ORM-Modelle."""
    pass